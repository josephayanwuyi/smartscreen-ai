import streamlit as st
from modules.services.db_service import get_scans, delete_scan

def render_history():
    st.header("📜 Scan History")

    current_identity = st.session_state.user if st.session_state.user else st.session_state.guest_id
    scans = get_scans(current_identity)

    if not scans:
        st.info("No scans found yet.")
        return

    # 'scans' now contains (id, type, content)
    for scan_id, scan_type, content in scans:
        with st.expander(f"📅 {scan_type}"):
            st.markdown(content)
            
            # Action buttons
            col1, col2, col3 = st.columns([1, 1, 1])
            with col1:
                # Unique key is required for buttons in a loop
                if st.button("🗑️ Delete", key=f"del_{scan_id}"):
                    delete_scan(scan_id)
                    st.toast("Scan deleted!")
                    st.rerun() # Refresh the history view
            with col2:
                wa_url = f"https://wa.me/?text={content[:100]}..."
                st.link_button("💬 WhatsApp", wa_url)