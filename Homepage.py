import streamlit as st

st.set_page_config(
    page_title="MappIT", 
    layout="wide",
    page_icon="🗺️",
    initial_sidebar_state="expanded"
)

# Custom CSS with Google Maps inspired colors
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
    
    .nav-button {
        background: linear-gradient(135deg, #1a73e8, #4285f4);
        color: white;
        border: none;
        padding: 0.75rem 1.5rem;
        border-radius: 8px;
        cursor: pointer;
        font-weight: 500;
        transition: all 0.2s ease;
        box-shadow: 0 2px 4px rgba(26, 115, 232, 0.3);
    }
    
    .nav-button:hover {
        background: linear-gradient(135deg, #1557b0, #3367d6);
        transform: translateY(-1px);
        box-shadow: 0 4px 8px rgba(26, 115, 232, 0.4);
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
    
    .stats-container {
        display: flex;
        justify-content: space-around;
        margin: 2rem 0;
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid #e8eaed;
    }
    
    .stat-item {
        text-align: center;
        padding: 1rem;
    }
    
    .stat-number {
        font-size: 2rem;
        font-weight: 600;
        color: #1a73e8;
    }
    
    .stat-label {
        color: #5f6368;
        font-size: 0.9rem;
        font-weight: 500;
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

# Main header
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
        <div class="team-member">
            <div class="member-name">🚀 Amar Kumar</div>
        </div>
        <div class="team-member">
            <div class="member-name">💻 Ajinkya Raut</div>
        </div>
        <div class="team-member">
            <div class="member-name">🎯 Samhita</div>
        </div>
        <div class="team-member">
            <div class="member-name">⭐ Aashritha</div>
        </div>
        <div class="team-member">
            <div class="member-name">🌟 Sarvesh</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# Features section with navigation buttons
st.markdown("### 🚀 Explore Our Features")

# Create columns for better layout
col1, col2 = st.columns(2)

with col1:
    # GPS Tracking Feature
    st.markdown("""
    <div class="feature-card">
        <div class="feature-title">📍 GPS Tracking</div>
        <div class="feature-description">
            Discover your current location with precision using advanced IP-based geolocation technology. 
            View your position on an interactive map with detailed coordinates and address information.
            Perfect for location verification and geographic awareness.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🎯 Launch GPS Tracking", key="gps", help="View your current location"):
        st.switch_page("pages/01_GPS_Tracking.py")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Nearby Places Feature
    st.markdown("""
    <div class="feature-card">
        <div class="feature-title">🏙️ Nearby Places Search</div>
        <div class="feature-description">
            Discover what's around you with our comprehensive nearby places finder. Search for restaurants, 
            hospitals, ATMs, gas stations, and more using OpenStreetMap data. Get directions, 
            contact information, and ratings for local businesses and services.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🔍 Find Nearby Places", key="nearby", help="Search for places around you"):
        st.switch_page("pages/03_Nearby_Places.py")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # GeoGuessr Feature
    st.markdown("""
    <div class="feature-card">
        <div class="feature-title">🚩 Flag Guesser</div>
        <div class="feature-description">
           Test your flag knowledge with our fun and educational flag guessing game! 
        Identify flags from around the world and improve your global awareness in an interactive way.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🎮 Play FlagGuessr", key="flagguessr", help="Start the game"):
        st.switch_page("pages/05_Flag_Guesser.py")

with col2:
    # Current Location Feature
    st.markdown("""
    <div class="feature-card">
        <div class="feature-title">📌 Current Location Finder</div>
        <div class="feature-description">
            Transform coordinates into meaningful addresses with our reverse geocoding service. 
            Input latitude and longitude values to get detailed location information including 
            street addresses, city, state, and country data.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("📍 Get Address Details", key="location", help="Convert coordinates to address"):
        st.switch_page("pages/02_Current_Location.py")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Group Location Feature
    st.markdown("""
    <div class="feature-card">
        <div class="feature-title">👨‍👩‍👧‍👦 Group Location Sharing</div>
        <div class="feature-description">
            Stay connected with your team, family, or friends through real-time location sharing. 
            View all group members' locations on a single interactive map. Great for events, 
            travel coordination, and keeping everyone in sync. (Requires Firebase setup)
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("👥 Join Group Tracking", key="group", help="Share location with group"):
        st.switch_page("pages/04_Group_Location.py")

# Quick navigation section
st.markdown("---")
st.markdown("""
<div class="quick-nav">
    <h3 style="text-align: center; color: #1a73e8; margin-bottom: 1rem;">⚡ Quick Navigation</h3>
</div>
""", unsafe_allow_html=True)

nav_col1, nav_col2, nav_col3, nav_col4, nav_col5 = st.columns(5)

with nav_col1:
    if st.button("📍 GPS", key="nav_gps", use_container_width=True):
        st.switch_page("pages/01_GPS_Tracking.py")

with nav_col2:
    if st.button("📌 Location", key="nav_location", use_container_width=True):
        st.switch_page("pages/02_Current_Location.py")

with nav_col3:
    if st.button("🏙️ Places", key="nav_places", use_container_width=True):
        st.switch_page("pages/03_Nearby_Places.py")

with nav_col4:
    if st.button("👥 Group", key="nav_group", use_container_width=True):
        st.switch_page("pages/04_Group_Location.py")

with nav_col5:
    if st.button("🎮 Game", key="nav_game", use_container_width=True):
        st.switch_page("pages/05_GeoGuesser.py")

# Information section
st.markdown("---")
col1, col2, col3 = st.columns(3)

with col1:
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

with col2:
    st.markdown("""
    <div class="info-section">
        <h4>🌐 Technology Stack</h4>
        <ul>
            <li>Streamlit framework</li>
            <li>OpenStreetMap data</li>
            <li>IP geolocation services</li>
            <li>Real-time mapping</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="info-section">
        <h4>📱 Features</h4>
        <ul>
            <li>Mobile responsive design</li>
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