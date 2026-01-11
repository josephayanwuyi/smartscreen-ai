import streamlit as st
import streamlit.components.v1 as components
import os



def render_contact():
    st.header("📬 Connect & Review")
    st.write("I'd love to hear from you!")

    my_email = os.getenv("CONTACT_EMAIL")

    if "show_finalize" not in st.session_state:
        st.session_state.show_finalize = False

    with st.form("contact_form", clear_on_submit=False):
        name = st.text_input("Name")
        email = st.text_input("Email")
        message = st.text_area("Message")
        submit_button = st.form_submit_button("🚀 Submit Details")

    if submit_button:
        if name and email and message:
            st.session_state.show_finalize = True
            st.session_state.form_data = {"name": name, "email": email, "message": message}
            st.balloons()
        else:
            st.error("Please fill in all fields.")

    if st.session_state.show_finalize:
        data = st.session_state.form_data
        st.success("✅ All set! Click the button below to send your message.")
        
        # We use a component to ensure the HTML renders as a real button
        html_button = f"""
            <div style="display: flex; justify-content: center; font-family: sans-serif;">
                <form action="https://formsubmit.co/{my_email}" method="POST" target="_blank">
                    <input type="hidden" name="name" value="{data['name']}">
                    <input type="hidden" name="email" value="{data['email']}">
                    <input type="hidden" name="message" value="{data['message']}">
                    <input type="hidden" name="_captcha" value="false">
                    <button type="submit" style="
                        background-color: #28a745; 
                        color: white; 
                        border: none; 
                        padding: 10px 20px; 
                        border-radius: 5px; 
                        font-size: 14px; 
                        cursor: pointer;
                        font-weight: bold;
                    ">
                        Confirm & Send Email 📧
                    </button>
                </form>
            </div>
        """
        # Height 60 ensures the button has room to show up without scrollbars
        components.html(html_button, height=60)
        
        if st.button("Cancel / Send Another"):
            st.session_state.show_finalize = False
            st.rerun()