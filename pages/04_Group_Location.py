import streamlit as st
import time
from datetime import datetime
from utils.map_utils import (
    create_base_map,
    add_location_marker,
    display_map
)
from utils.location_utils import (
    create_group,
    add_group_member,
    get_group_members
)
from utils.api_utils import get_current_location

# Page configuration
st.set_page_config(
    page_title="Group Location",
    page_icon="👥",
    layout="wide"
)

# Initialize session state
if 'current_location' not in st.session_state:
    st.session_state.current_location = None
if 'groups' not in st.session_state:
    st.session_state.groups = []
if 'active_group' not in st.session_state:
    st.session_state.active_group = None
if 'group_members' not in st.session_state:
    st.session_state.group_members = []

# Page title
st.title("Group Location Sharing")
st.markdown("Share your location with friends and family in real-time")

# Sidebar controls
with st.sidebar:
    st.header("Group Management")
    
    # Create new group
    st.subheader("Create New Group")
    new_group_name = st.text_input("Group Name")
    
    if st.button("Create Group", type="primary"):
        if new_group_name:
            group_id = create_group(new_group_name, 1)  # Using user_id 1 for demo
            st.session_state.groups.append({
                'id': group_id,
                'name': new_group_name,
                'created_at': datetime.now().isoformat()
            })
            st.success(f"Group '{new_group_name}' created!")
        else:
            st.error("Please enter a group name")
    
    # Join existing group
    st.subheader("Join Group")
    group_code = st.text_input("Group Code")
    
    if st.button("Join Group"):
        if group_code:
            # In a real application, you would validate the group code
            st.success("Joined group successfully!")
        else:
            st.error("Please enter a group code")
    
    # Group settings
    if st.session_state.active_group:
        st.subheader("Group Settings")
        
        # Member permissions
        st.write("Member Permissions")
        for member in st.session_state.group_members:
            st.write(f"{member['username']}: {member['permissions']}")
        
        # Emergency alerts
        st.checkbox("Enable Emergency Alerts", value=True)
        
        # Location update interval
        update_interval = st.slider(
            "Location Update Interval (seconds)",
            min_value=5,
            max_value=60,
            value=10,
            step=5
        )

# Main content area
col1, col2 = st.columns([2, 1])

with col1:
    # Map display
    if st.session_state.active_group:
        # Create and display map
        m = create_base_map(
            center_lat=st.session_state.current_location['latitude'],
            center_lon=st.session_state.current_location['longitude'],
            zoom_start=15
        )
        
        # Add member locations
        for member in st.session_state.group_members:
            if 'location' in member:
                m = add_location_marker(
                    m,
                    member['location']['latitude'],
                    member['location']['longitude'],
                    popup=f"{member['username']}'s Location",
                    color="blue",
                    icon="user"
                )
        
        # Display map
        display_map(m)
    else:
        # Display empty map
        m = create_base_map()
        display_map(m)

with col2:
    # Group list
    st.subheader("Your Groups")
    
    if st.session_state.groups:
        for group in st.session_state.groups:
            with st.expander(f"{group['name']}"):
                st.write(f"Created: {group['created_at']}")
                
                if st.button(f"Activate {group['name']}"):
                    st.session_state.active_group = group
                    st.session_state.group_members = get_group_members(group['id'])
                    st.experimental_rerun()
    else:
        st.info("Create or join a group to start sharing locations")
    
    # Active group information
    if st.session_state.active_group:
        st.subheader("Active Group")
        st.write(f"Group: {st.session_state.active_group['name']}")
        
        # Member list
        st.write("Members:")
        for member in st.session_state.group_members:
            st.write(f"- {member['username']}")
        
        # Location sharing controls
        st.subheader("Location Sharing")
        
        if st.button("Share My Location", type="primary"):
            location = get_current_location()
            if location:
                st.session_state.current_location = location
                st.success("Location shared!")
            else:
                st.error("Could not get your location")
        
        # Emergency alert button
        if st.button("Send Emergency Alert", type="secondary"):
            st.warning("Emergency alert sent to all group members!")
    
    # Group chat (placeholder)
    if st.session_state.active_group:
        st.subheader("Group Chat")
        st.text_area("Message", key="chat_message")
        
        if st.button("Send Message"):
            st.info("Message sent to group!")

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center'>
        <p>Group location sharing is end-to-end encrypted. Your privacy is our priority.</p>
    </div>
""", unsafe_allow_html=True) 