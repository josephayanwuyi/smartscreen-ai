import streamlit as st
import uuid

def init_state():
    # 1. Permanent User (if logged in)
    if "user" not in st.session_state:
        st.session_state.user = None

    # 2. Guest ID (to track history for people not logged in)
    if "guest_id" not in st.session_state:
        st.session_state.guest_id = str(uuid.uuid4())

    # 3. Scan Counter (for the 5-scan limit logic)
    if "scan_count" not in st.session_state:
        st.session_state.scan_count = 0

    # 4. AI Model Selection
    if "ai_model" not in st.session_state:
        st.session_state.ai_model = "meta-llama/llama-4-scout-17b-16e-instruct"