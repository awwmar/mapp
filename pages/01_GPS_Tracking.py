import streamlit as st
import geocoder
import folium
from streamlit_folium import st_folium

st.title("📍 GPS Tracking (via IP Geolocation)")

try:
    g = geocoder.ip('me')
    if g.ok:
        lat, lon = g.latlng
        st.success(f"Your approximate location: {lat}, {lon}")
        
        m = folium.Map(location=[lat, lon], zoom_start=13)
        folium.Marker([lat, lon], popup="You are here!").add_to(m)
        st_folium(m, height=500)
    else:
        st.error("Unable to retrieve location. Please check your connection.")
except Exception as e:
    st.error(f"Error: {e}")
