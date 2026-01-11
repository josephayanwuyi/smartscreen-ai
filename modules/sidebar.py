import streamlit as st


def render_sidebar(hide_nav=False): # Add this parameter
    with st.sidebar:
        st.title("✨ SmartSelect")
        st.caption("AI-Powered Actions")
        st.divider()

        if not hide_nav:
            # 1. Define the pages
            pages = ["New Scan", "History", "Settings"]
            
            # 2. Sync with Session State
            current_page = st.session_state.get("page", "New Scan")
            
            try:
                default_idx = pages.index(current_page)
            except ValueError:
                default_idx = 0

            # 3. Create radio menu with a UNIQUE KEY to fix the error
            selected_page = st.radio(
                label="Navigation",
                options=pages,
                index=default_idx,
                key="main_nav_radio"
            )
            
            st.session_state.page = selected_page
        else:
            # If hiding nav, we just return the current state
            selected_page = st.session_state.get("page", "New Scan")

        # The "Get in Touch" button always stays
        st.markdown("""
            <div style="margin-top: 20px;">
                <p style="color: gray; font-size: 14px; margin-bottom: 5px;">GET IN TOUCH</p>
                <a href="/?page=contact" target="_self" style="
                    text-decoration: none; 
                    color: #FF4B4B; 
                    font-weight: bold; 
                    font-size: 16px;
                    display: block;
                    padding: 10px;
                    border: 2px solid #FF4B4B;
                    border-radius: 5px;
                    text-align: center;
                ">📬 Contact & Reviews</a>
            </div>
        """, unsafe_allow_html=True)
        
        return selected_page