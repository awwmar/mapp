import streamlit as st
from supabase import create_client, Client

class FlagGameDatabase:
    def __init__(self):
        self.setup_supabase_connection()
    
    def setup_supabase_connection(self):
        try:
            url = st.secrets["supabase"]["url"]
            key = st.secrets["supabase"]["key"]
            self.supabase: Client = create_client(url, key)
        except Exception as e:
            st.error(f"Failed to connect to database: {e}")
            self.supabase = None 