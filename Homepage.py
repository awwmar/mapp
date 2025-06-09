import streamlit as st

st.set_page_config(
    page_title="MappIT", 
    layout="wide",
    page_icon="🗺️",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(135deg, #1a73e8 0%, #34a853 50%, #ea4335 100%);
        color: white;
        border-radius: 12px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 12px rgba(26, 115, 232, 0.3);
    }
    .feature-card {
        background: #ffffff;
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid #e8eaed;
        margin: 1rem 0;
        box-shadow: 0 2px 8px rgba(60, 64, 67, 0.15);
        transition: all 0.3s ease;
    }
    .feature-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 24px rgba(60, 64, 67, 0.25);
        border-color: #1a73e8;
    }
    .feature-title {
        color: #202124;
        font-size: 1.2rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    .feature-description {
        color: #5f6368;
        line-height: 1.6;
        margin-bottom: 1rem;
    }
    .team-section {
        background: linear-gradient(135deg, #f8f9fa 0%, #e8f0fe 100%);
        padding: 2rem;
        border-radius: 12px;
        margin: 2rem 0;
        border: 1px solid #dadce0;
    }
    .team-header {
        text-align: center;
        color: #1a73e8;
        font-size: 1.8rem;
        font-weight: 600;
        margin-bottom: 1.5rem;
    }
    .team-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1rem;
        margin-top: 1rem;
    }
    .team-member {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        text-align: center;
        border: 1px solid #e8eaed;
        box-shadow: 0 1px 4px rgba(60, 64, 67, 0.1);
        transition: all 0.2s ease;
    }
    .team-member:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(60, 64, 67, 0.15);
    }
    .member-name {
        color: #202124;
        font-weight: 500;
        font-size: 1rem;
    }
    .info-section {
        background: #ffffff;
        border: 1px solid #e8eaed;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
    }
    .info-section h4 {
        color: #1a73e8;
        margin-bottom: 1rem;
    }
    .info-section ul {
        color: #5f6368;
        line-height: 1.6;
    }
    .quick-nav {
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid #e8eaed;
        margin: 2rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1>🗺️ Welcome to MappIT</h1>
    <p>Your comprehensive toolkit for location-based services and geographic exploration</p>
</div>
""", unsafe_allow_html=True)

# Team Section
st.markdown("""
<div class="team-section">
    <div class="team-header">👥 Meet Team Jai Ballaya</div>
    <div class="team-grid">
        <div class="team-member"><div class="member-name">🚀 Amar Kumar</div></div>
        <div class="team-member"><div class="member-name">💻 Ajinkya Raut</div></div>
        <div class="team-member"><div class="member-name">🎯 Samhita</div></div>
        <div class="team-member"><div class="member-name">⭐ Aashritha</div></div>
        <div class="team-member"><div class="member-name">🌟 Sarvesh</div></div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("---")
st.markdown("### 🚀 Explore Our Features")

# Layout Columns
col1, col2 = st.columns(2)

with col1:
    # GPS Tracking
    st.markdown("""
    <div class="feature-card">
        <div class="feature-title">📍 GPS Tracking</div>
        <div class="feature-description">
            Find your current location using IP-based geolocation and view it on an interactive map with coordinates and address details.
        </div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("🎯 Launch GPS Tracking", key="gps"):
        st.switch_page("pages/01_GPS_Tracking.py")

    # Nearby Places
    st.markdown("""
    <div class="feature-card">
        <div class="feature-title">🏙️ Nearby Places Search</div>
        <div class="feature-description">
            Search for nearby restaurants, hospitals, ATMs, gas stations and more using OpenStreetMap data and smart filters.
        </div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("🔍 Find Nearby Places", key="places"):
        st.switch_page("pages/03_Nearby_Places.py")

    # Flag Guessing
    st.markdown("""
    <div class="feature-card">
        <div class="feature-title">🚩 Flag Guesser</div>
        <div class="feature-description">
            Test your knowledge of world flags in this interactive and fun learning game!
        </div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("🎮 Play FlagGuessr", key="flag"):
        st.switch_page("pages/05_Flag_Guesser.py")

with col2:
    # Reverse Geocoding
    st.markdown("""
    <div class="feature-card">
        <div class="feature-title">📌 Current Location Finder</div>
        <div class="feature-description">
            Enter coordinates and instantly convert them to readable street addresses, city, and country.
        </div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("📍 Get Address Details", key="address"):
        st.switch_page("pages/02_Current_Location.py")

    # Weather Dashboard
    st.markdown("""
    <div class="feature-card">
        <div class="feature-title">🌦️ Weather Dashboard</div>
        <div class="feature-description">
            Get real-time weather updates for your location or any city with forecasts and temperature charts.
        </div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("☀️ Check Weather", key="weather"):
        st.switch_page("pages/04_Weather_Dashboard.py")

    # Route Planner
    st.markdown("""
    <div class="feature-card">
        <div class="feature-title">🧭 Route Planner</div>
        <div class="feature-description">
            Plan your travel route between two locations with distance, duration, and turn-by-turn directions.
        </div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("🗺️ Plan Route", key="route"):
        st.switch_page("pages/06_Route_Planning.py")

# Quick Navigation
st.markdown("---")
st.markdown("""
<div class="quick-nav">
    <h3 style="text-align: center; color: #1a73e8; margin-bottom: 1rem;">⚡ Quick Navigation</h3>
</div>
""", unsafe_allow_html=True)

nav1, nav2, nav3, nav4, nav5 = st.columns(5)
with nav1:
    if st.button("📍 GPS", key="nav_gps"): st.switch_page("pages/01_GPS_Tracking.py")
with nav2:
    if st.button("📌 Location", key="nav_location"): st.switch_page("pages/02_Current_Location.py")
with nav3:
    if st.button("🏙️ Places", key="nav_places"): st.switch_page("pages/03_Nearby_Places.py")
with nav4:
    if st.button("☀️ Weather", key="nav_weather"): st.switch_page("pages/06_Weather_Dashboard.py")
with nav5:
    if st.button("🧭 Route", key="nav_route"): st.switch_page("pages/07_Route_Planner.py")

# Info Section
st.markdown("---")
i1, i2, i3 = st.columns(3)

with i1:
    st.markdown("""
    <div class="info-section">
        <h4>🛡️ Privacy & Security</h4>
        <ul>
            <li>No personal data stored</li>
            <li>Secure API connections</li>
            <li>Location data processed locally</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with i2:
    st.markdown("""
    <div class="info-section">
        <h4>🌐 Technology Stack</h4>
        <ul>
            <li>Streamlit framework</li>
            <li>OpenStreetMap</li>
            <li>Weather APIs</li>
            <li>Geolocation Services</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with i3:
    st.markdown("""
    <div class="info-section">
        <h4>📱 Features</h4>
        <ul>
            <li>Mobile responsive</li>
            <li>Interactive maps</li>
            <li>Real-time updates</li>
            <li>Cross-platform support</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #5f6368; padding: 1rem;">
    <p>Built with ❤️ by Team Jai Ballaya | Powered by Streamlit & OpenStreetMap</p>
</div>
""", unsafe_allow_html=True)
