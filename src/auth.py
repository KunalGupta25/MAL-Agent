# auth.py
import streamlit as st
import requests
import webbrowser
import secrets
import time
from urllib.parse import urlparse, parse_qs
from dotenv import load_dotenv
import os

load_dotenv()

# Configuration (move these to secrets.toml in production)
CLIENT_ID = os.getenv("MAL_CLIENT_ID")
CLIENT_SECRET = os.getenv("MAL_CLIENT_SECRET")
REDIRECT_URI = os.getenv("MAL_REDIRECT_URI", "http://localhost:8000/callback")
PORT = int(os.getenv("MAL_PORT", 8000))

class MALAuth:
    def __init__(self):
        self.code_verifier = secrets.token_urlsafe(64)
        self.code_challenge = self.code_verifier  # Using 'plain' method
        self.auth_code = None
        self.error = None

    def start_oauth_flow(self):
        auth_url = (
            "https://myanimelist.net/v1/oauth2/authorize?"
            f"response_type=code&"
            f"client_id={CLIENT_ID}&"
            f"code_challenge={self.code_challenge}&"
            f"redirect_uri={REDIRECT_URI}"
        )
        st.markdown(f"[Click here to authenticate with MyAnimeList]({auth_url})", unsafe_allow_html=True)

        # Check for code in query params (Streamlit Cloud compatible)
        query_params = st.experimental_get_query_params()
        if "code" in query_params:
            self.auth_code = query_params["code"][0]
            return self.auth_code, None
        elif "error" in query_params:
            self.error = query_params["error"][0]
            return None, self.error
        else:
            return None, None

    def get_access_token(self, auth_code):
        token_url = "https://myanimelist.net/v1/oauth2/token"
        data = {
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "code": auth_code,
            "code_verifier": self.code_verifier,
            "grant_type": "authorization_code",
            "redirect_uri": REDIRECT_URI
        }
        try:
            response = requests.post(token_url, data=data)
            response.raise_for_status()
            return response.json()["access_token"], None
        except requests.exceptions.HTTPError as e:
            return None, f"Token exchange failed: {e.response.status_code} {e.response.text}"

def login_button():
    """Streamlit component for handling MAL login"""
    if st.button("Login with MyAnimeList"):
        with st.spinner("Authenticating..."):
            auth = MALAuth()
            auth_code, error = auth.start_oauth_flow()
            
            if error:
                st.error(error)
                return False
                
            access_token, error = auth.get_access_token(auth_code)
            if error:
                st.error(error)
                return False
                
            st.session_state.access_token = access_token
            st.rerun()
    return True
