import os
import streamlit as st
import base64
from groq import Groq
import httpx
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

api_key_from_env = os.getenv("GROQ_API_KEY")


# Update your client initialization
client = Groq(
    api_key=api_key_from_env,
    timeout=60.0,
    http_client=httpx.Client(verify=False) # This skips the SSL handshake check
)
# client = Groq(api_key="")

def encode_image(image_file):
    # Works with both file paths or file-like objects
    return base64.b64encode(image_file.read()).decode('utf-8')

def analyze_image_with_groq(image_file):
    base64_image = encode_image(image_file)
    
    # Get the user's region from session state (defaults to 'Global' if not logged in)
    user_region = st.session_state.get("region", "Global")
    
    response = client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text", 
                        "text": f"Identify the ingredients in this fridge. "
                                f"Since I am located in {user_region}, suggest 3 recipes "
                                f"that are popular in this region or use local cooking styles. "
                                f"Format the output in clean Markdown."
                    },
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
                    },
                ],
            }
        ],
    )
    return response.choices[0].message.content