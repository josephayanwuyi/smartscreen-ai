import streamlit as st

from modules.state import init_state
from modules.sidebar import render_sidebar
from modules.services.db_service import backup_database, init_db
from modules.pages.new_scan import render_new_scan
from modules.pages.history import render_history
from modules.pages.settings import render_settings
from modules.pages.contact import render_contact
from modules.ui_components import inject_custom_css, render_footer

# 1. Config and CSS MUST come first
st.set_page_config(page_title="SmartSelect AI", page_icon="✨")
inject_custom_css()

# 2. INITIALIZE APP STATE AND DATABASE
init_state()
init_db()
backup_database()

# 3. CHECK URL PARAMS BEFORE RENDERING SIDEBAR
query_params = st.query_params
url_page = query_params.get("page")
is_contact = (url_page == "contact")

# 4. RENDER SIDEBAR AND GET SELECTED PAGE
page = render_sidebar(hide_nav=is_contact)

# 5. PAGE ROUTING
if is_contact:
    render_contact()
    if st.button("⬅️ Back to Home"):
        st.query_params.clear()
        st.rerun()
else:
    if page == "New Scan":
        render_new_scan()
    elif page == "History":
        render_history()
    elif page == "Settings":
        render_settings()

# 6. Global Footer
render_footer()