import io
import streamlit as st

from modules.services.scan_service import analyze_image
from modules.services.db_service import save_scan
from modules.services.background_service import run_in_background


def process_scan(image_bytes, user, model):
    image_file = io.BytesIO(image_bytes)
    result = analyze_image(image_file, model)

    save_scan(
        user=user,
        scan_type=result["type"],
        content=", ".join(result["items"])
    )


def render_new_scan():
    st.header("📸 New Scan")

    # 1. HYBRID IDENTITY: Check if we use a real username or the temporary Guest ID
    current_user = st.session_state.user if st.session_state.user else st.session_state.guest_id
    is_guest = st.session_state.user is None

    # 2. THE WALL: Check the 5-scan limit only if they are a guest
    if is_guest and st.session_state.scan_count >= 5:
        st.warning("🚀 Free Limit Reached!")
        st.info("You've used your 5 free guest scans. Create an account to see your history and get unlimited scans.")
        if st.button("✨ Go to Settings to Register"):
            # This triggers a page change in your app.py logic
            st.session_state.page = "Settings" 
            st.rerun()
        return # STOP HERE: Don't show the camera or upload button

    # 3. SCAN INTERFACE: Only visible if logged in or under the limit
    source = st.segmented_control(
    "Source", 
    ["Camera", "Upload"], 
    default="Camera", 
    key="scan_source_selector" # Add this unique key
    )

    img = st.camera_input("Take a photo") if source == "Camera" else st.file_uploader("Upload", type=["jpg", "jpeg", "png"])

    if img:
        image_bytes = img.read()
        
        with st.spinner("Analyzing your fridge..."):
            image_file = io.BytesIO(image_bytes)
            # Use the Llama 4 vision model we set up earlier
            result = analyze_image(image_file, st.session_state.ai_model)
            
        st.subheader("Results")
        st.markdown(result["analysis"])
        
        st.warning("⚠️ **AI Disclaimer**: SmartSelect AI can make mistakes. Always verify ingredient safety and expiration dates, especially for allergies. Recommendations are for informational purposes only.")
        
        # 4. DATA PERSISTENCE: Save to DB immediately so it counts
        save_scan(current_user, "Fridge Scan", result["analysis"])
        
        # 5. COUNTER: Update the count in the session
        st.session_state.scan_count += 1 
        st.toast(f"Scan {st.session_state.scan_count}/5 saved!")
        st.balloons()