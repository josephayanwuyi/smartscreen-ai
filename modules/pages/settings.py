import streamlit as st
import os
from dotenv import load_dotenv
from modules.auth import login # Import the new tabbed form
from modules.services.db_service import get_connection, DB_NAME

load_dotenv()
def render_settings():
    st.header("⚙️ Account & System")
    
    # Create tabs to keep the UI organized
    tab1, tab2, tab3 = st.tabs(["👤 My Account", "🛠️ System Status", "📋 Debug Logs"])

    with tab1:
        # 1. If user is logged in, show their profile info
        if st.session_state.user:
            st.success(f"Logged in as: **{st.session_state.user}**")
            # Pull region from session state
            region = st.session_state.get("region", "Global")
            st.info(f"📍 Region: {region}")
            
            if st.button("Logout"):
                st.session_state.user = None
                st.session_state.region = None
                st.rerun()
        
        # 2. If not logged in, call the combined Login/Register form from auth.py
        else:
            login()

    with tab2:
        st.subheader("🔑 Connection Status")
        # Check for Groq API key
        api_key = os.getenv("GROQ_API_KEY") 
        
        if api_key:
            st.success("API Connection: Active ✅")
        else:
            st.error("API Connection: Offline ❌")
            
        st.divider()
        # Display current AI model
        current_model = st.session_state.get("ai_model", "meta-llama/llama-4-scout-17b-16e-instruct")
        st.caption(f"Running on Model: {current_model}")
    
    with tab3:
        admin_username = os.getenv("ADMIN_USERNAME", "admin_default")
        if st.session_state.user == admin_username:
            st.subheader("🖥️ Server Health")
            
            # 1. Calculate Database Size
            if os.path.exists(DB_NAME):
                file_size = os.path.getsize(DB_NAME) / 1024  # Convert to KB
                st.metric("Database Size", f"{file_size:.2f} KB")
            
            # 2. Get Quick Database Stats
            try:
                conn = get_connection()
                c = conn.cursor()
                
                c.execute("SELECT COUNT(*) FROM users")
                total_users = c.fetchone()[0]
                
                c.execute("SELECT COUNT(*) FROM scans")
                total_scans = c.fetchone()[0]
                
                col1, col2 = st.columns(2)
                col1.metric("Total Registered Users", total_users)
                col2.metric("Total Scans Performed", total_scans)
                
                conn.close()
            except Exception as e:
                st.error("Could not fetch DB stats")

            st.divider()

            # --- Existing Log Viewer Code ---
            st.subheader("📋 Backend Logs")
            log_file = "logs/backend.log"
            if os.path.exists(log_file):
                with open(log_file, "r") as f:
                    logs = f.readlines()
                    st.text_area("Live Log Feed", "".join(logs[-20:]), height=300)
            # ... rest of log code ...
        else:
            st.warning("Access Restricted: Administrator login required.")