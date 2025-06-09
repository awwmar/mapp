import streamlit as st
from datetime import datetime
import pandas as pd
import geocoder  # ✅ added for IP geolocation
from streamlit_javascript import st_javascript
from utils.map_utils import (
    create_base_map,
    add_location_marker,
    add_location_circle,
    display_map
)
from utils.api_utils import (
    get_location_details,
    get_timezone_info
)

st.set_page_config(page_title="Current Location", page_icon="🎯", layout="wide")

if 'current_location' not in st.session_state:
    st.session_state.current_location = None
if 'location_details' not in st.session_state:
    st.session_state.location_details = None
if 'favorite_locations' not in st.session_state:
    st.session_state.favorite_locations = []

st.title("Current Location Finder")
st.markdown("Find your precise location with detailed address information")

col1, col2 = st.columns([2, 1])

with col1:
    if st.session_state.current_location:
        m = create_base_map(
            center_lat=st.session_state.current_location['latitude'],
            center_lon=st.session_state.current_location['longitude'],
            zoom_start=15
        )
        m = add_location_marker(
            m,
            st.session_state.current_location['latitude'],
            st.session_state.current_location['longitude'],
            popup="Your Current Location"
        )
        if 'accuracy' in st.session_state.current_location:
            m = add_location_circle(
                m,
                st.session_state.current_location['latitude'],
                st.session_state.current_location['longitude'],
                radius=st.session_state.current_location['accuracy'],
                color="blue",
                fill=True,
                popup="Location Accuracy"
            )
        display_map(m)

        st.subheader("Alternative Map View")
        map_data = pd.DataFrame({
            'lat': [st.session_state.current_location['latitude']],
            'lon': [st.session_state.current_location['longitude']]
        })
        st.map(map_data)
    else:
        m = create_base_map()
        display_map(m)

with col2:
    st.subheader("Location Controls")

    if st.button("Get Current Location", type="primary"):
        with st.spinner("Trying browser location first..."):
            location = st_javascript(
                """
                new Promise((resolve, reject) => {
                    if (!navigator.geolocation) {
                        reject("Geolocation not supported by your browser.");
                    } else {
                        navigator.geolocation.getCurrentPosition(
                            (pos) => {
                                resolve({
                                    latitude: pos.coords.latitude,
                                    longitude: pos.coords.longitude,
                                    accuracy: pos.coords.accuracy
                                });
                            },
                            (err) => {
                                reject("Error getting location: " + err.message);
                            },
                            {
                                enableHighAccuracy: true,
                                timeout: 10000,
                                maximumAge: 0
                            }
                        );
                    }
                });
                """
            )

        if location and isinstance(location, dict):
            st.session_state.current_location = location
            st.session_state.location_details = get_location_details(
                location['latitude'],
                location['longitude']
            )
            st.success("Precise browser location found!")
        else:
            st.warning("Browser location failed. Using IP-based location instead...")
            g = geocoder.ip('me')
            if g.ok:
                ip_location = {
                    'latitude': g.latlng[0],
                    'longitude': g.latlng[1],
                    'accuracy': 20000  # Approximate accuracy for IP
                }
                st.session_state.current_location = ip_location
                st.session_state.location_details = get_location_details(
                    ip_location['latitude'],
                    ip_location['longitude']
                )
                st.success("IP-based location found.")
            else:
                st.error("Unable to get location via browser or IP. Please try manual input.")

    st.subheader("Manual Location Input")
    manual_lat = st.number_input("Latitude", value=0.0, format="%.6f")
    manual_lon = st.number_input("Longitude", value=0.0, format="%.6f")

    if st.button("Set Manual Location"):
        st.session_state.current_location = {
            'latitude': manual_lat,
            'longitude': manual_lon
        }
        st.session_state.location_details = get_location_details(
            manual_lat,
            manual_lon
        )
        st.success("Manual location set!")

    if st.session_state.current_location:
        st.subheader("Location Information")
        st.write(f"Latitude: {st.session_state.current_location['latitude']:.6f}")
        st.write(f"Longitude: {st.session_state.current_location['longitude']:.6f}")
        if 'accuracy' in st.session_state.current_location:
            st.write(f"Accuracy: ±{st.session_state.current_location['accuracy']:.0f} meters")

        if st.session_state.location_details:
            st.subheader("Address Details")
            st.write(f"Address: {st.session_state.location_details.get('address', 'N/A')}")
            st.write(f"City: {st.session_state.location_details.get('city', 'N/A')}")
            st.write(f"State: {st.session_state.location_details.get('state', 'N/A')}")
            st.write(f"Country: {st.session_state.location_details.get('country', 'N/A')}")
            st.write(f"Postal Code: {st.session_state.location_details.get('postcode', 'N/A')}")

            timezone_info = get_timezone_info(
                st.session_state.current_location['latitude'],
                st.session_state.current_location['longitude']
            )
            if timezone_info:
                st.subheader("Timezone Information")
                st.write(f"Timezone: {timezone_info['timezone']}")
                st.write(f"UTC Offset: {timezone_info['offset']} seconds")
                st.write(f"DST: {'Yes' if timezone_info['dst'] else 'No'}")

        if st.button("Save to Favorites"):
            favorite = {
                'name': st.session_state.location_details.get('address', 'Unnamed Location'),
                'latitude': st.session_state.current_location['latitude'],
                'longitude': st.session_state.current_location['longitude'],
                'timestamp': datetime.now().isoformat()
            }
            st.session_state.favorite_locations.append(favorite)
            st.success("Location saved to favorites!")

    if st.session_state.favorite_locations:
        st.subheader("Favorite Locations")
        for i, fav in enumerate(st.session_state.favorite_locations):
            with st.expander(f"{fav['name']}"):
                st.write(f"Latitude: {fav['latitude']:.6f}")
                st.write(f"Longitude: {fav['longitude']:.6f}")
                st.write(f"Saved: {fav['timestamp']}")

                if st.button(f"Load Location {i+1}"):
                    st.session_state.current_location = {
                        'latitude': fav['latitude'],
                        'longitude': fav['longitude']
                    }
                    st.session_state.location_details = get_location_details(
                        fav['latitude'],
                        fav['longitude']
                    )
                    st.experimental_rerun()

st.markdown("---")
st.markdown("""
<div style='text-align: center'>
    <p>Your location data is only stored locally and is not shared with any third parties.</p>
</div>
""", unsafe_allow_html=True)
