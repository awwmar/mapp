import streamlit as st
import requests
import folium
from streamlit_folium import st_folium
import geocoder

# Streamlit Page Configuration
st.set_page_config(page_title="Nearby Places", page_icon="🔍", layout="wide")
st.title("Nearby Places")
st.markdown("Discover points of interest around your location")

# Session state initialization
if 'current_location' not in st.session_state:
    st.session_state.current_location = None
if 'nearby_places' not in st.session_state:
    st.session_state.nearby_places = []
if 'selected_category' not in st.session_state:
    st.session_state.selected_category = None

# Sidebar
with st.sidebar:
    st.header("Search Settings")

    radius = st.slider("Search Radius (meters)", 100, 5000, 1000, 100)

    categories = [
        "All", "restaurant", "cafe", "bar", "hotel", "shop",
        "pharmacy", "hospital", "school", "park", "museum", "bank"
    ]
    selected_category = st.selectbox("Category", categories)
    st.session_state.selected_category = None if selected_category == "All" else selected_category

    if st.button("Search Nearby Places", type="primary"):
        if st.session_state.current_location:
            lat = st.session_state.current_location["lat"]
            lon = st.session_state.current_location["lon"]
            query = st.session_state.selected_category or ""
            url = f"https://photon.komoot.io/api/?q={query}&lat={lat}&lon={lon}&limit=15"
            try:
                with st.spinner("Searching..."):
                    res = requests.get(url)
                    features = res.json().get("features", [])
                    places = []
                    for f in features:
                        coords = f["geometry"]["coordinates"]
                        props = f["properties"]
                        places.append({
                            "name": props.get("name", "Unnamed"),
                            "type": props.get("osm_value", "unknown"),
                            "lat": coords[1],
                            "lon": coords[0]
                        })
                    st.session_state.nearby_places = places
                    st.success(f"Found {len(places)} places.")
            except Exception as e:
                st.error(f"Error fetching places: {e}")
        else:
            st.error("Set or detect your location first!")

# Layout
col1, col2 = st.columns([2, 1])

# Map Display
with col1:
    if st.session_state.current_location:
        m = folium.Map(location=[
            st.session_state.current_location["lat"],
            st.session_state.current_location["lon"]
        ], zoom_start=15)

        folium.Marker(
            [st.session_state.current_location["lat"], st.session_state.current_location["lon"]],
            tooltip="You are here"
        ).add_to(m)

        for place in st.session_state.nearby_places:
            folium.Marker(
                [place["lat"], place["lon"]],
                popup=f"{place['name']} ({place['type']})"
            ).add_to(m)

        st_folium(m, height=500)
    else:
        m = folium.Map(location=[0, 0], zoom_start=2)
        st_folium(m, height=500)

# Controls
with col2:
    st.subheader("Location Controls")

    if st.button("Detect My Location"):
        try:
            g = geocoder.ip('me')
            if g.ok:
                st.session_state.current_location = {"lat": g.latlng[0], "lon": g.latlng[1]}
                st.success(f"Location: {g.latlng}")
            else:
                st.error("Could not detect location.")
        except Exception as e:
            st.error(f"Error: {e}")

    st.subheader("Manual Location Input")
    lat = st.number_input("Latitude", format="%.6f")
    lon = st.number_input("Longitude", format="%.6f")

    if st.button("Set Manual Location"):
        st.session_state.current_location = {"lat": lat, "lon": lon}
        st.success("Manual location set.")

    if st.session_state.nearby_places:
        st.subheader("Nearby Places")
        for place in st.session_state.nearby_places:
            with st.expander(f"{place['name']} ({place['type']})"):
                st.write(f"Location: {place['lat']}, {place['lon']}")
                if st.button(f"Center map on {place['name']}", key=place["name"]):
                    st.session_state.current_location = {
                        "lat": place["lat"],
                        "lon": place["lon"]
                    }
                    st.rerun()

# Footer
st.markdown("---")
st.markdown("<center><small>Powered by Photon API + OpenStreetMap</small></center>", unsafe_allow_html=True)
