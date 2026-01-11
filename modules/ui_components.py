import streamlit as st

def inject_custom_css():
    st.markdown("""
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.2/css/all.min.css">
        
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Delius&display=swap');        
        
        /* 1. Target ONLY the big titles and the result text */
        /* This is the safest way to keep your icons working */
        .stApp h1, .stApp h2, .stApp h3, [data-testid="stMarkdownContainer"] p {
            font-family: 'Delius', cursive !important;
        }

        /* 5. UI Elements (Footer & Layout) */
        .sticky-footer {
            position: fixed;
            left: 0;
            bottom: 0;
            width: 100%;
            background-color: white;
            border-top: 1px solid #eee;
            padding: 10px 0;
            text-align: center;
            z-index: 999;
        }

        .main .block-container {
            padding-bottom: 120px; 
        }

        .footer-link {
            text-decoration: none !important;
            color: #555;
            margin: 0 5px;
            font-weight: 600;
            font-size: 16px;
            transition: color 0.3s;
            display: inline-flex;
            align-items: center;
        }
                
        .footer-link i {
            font-size: 20px;
            vertical-align: middle;
        }

        .footer-link:hover {
            color: #FF4B4B;
        }
        </style>
    """, unsafe_allow_html=True)

def render_footer():
    # Replace these with your actual URLs
    github_url = "https://github.com/yourusername"
    linkedin_url = "https://linkedin.com/in/yourusername"
    x_url = "https://x.com/yourusername"
    
    footer_html = f"""
    <div class="sticky-footer">
        <div style="font-size: 14px; color: #444;">
            AI Engineering Project | © 2026 SmartSelect AI | Connect with me:
            <a href="{github_url}" target="_blank" class="footer-link">
                <i class="fa-brands fa-github"></i>
            </a>
            <a href="{linkedin_url}" target="_blank" class="footer-link">
                <i class="fa-brands fa-linkedin"></i>
            </a>
            <a href="{x_url}" target="_blank" class="footer-link">
                <i class="fa-brands fa-x-twitter"></i>
            </a>
        </div>
    </div>
    """
    st.markdown(footer_html, unsafe_allow_html=True)