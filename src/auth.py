# auth.py
import streamlit as st
import requests
import webbrowser
import secrets
import threading
import time
from http.server import HTTPServer, BaseHTTPRequestHandler
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

    class OAuthHandler(BaseHTTPRequestHandler):
        auth_code = None
        error = None

        def do_GET(self):
            parsed = urlparse(self.path)
            params = parse_qs(parsed.query)
            if "code" in params:
                MALAuth.OAuthHandler.auth_code = params["code"][0]
                self.send_response(200)
                self.end_headers()
                self.wfile.write(b"Authorization successful! Return to the app.")
            elif "error" in params:
                MALAuth.OAuthHandler.error = params["error"][0]
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b"Authorization failed. Check your settings.")
            else:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b"Invalid request")

    def run_server(self):
        server = HTTPServer(('localhost', PORT), self.OAuthHandler)
        server.timeout = 120
        server.handle_request()

    def start_oauth_flow(self):
        server_thread = threading.Thread(target=self.run_server)
        server_thread.daemon = True
        server_thread.start()

        auth_url = (
            "https://myanimelist.net/v1/oauth2/authorize?"
            f"response_type=code&"
            f"client_id={CLIENT_ID}&"
            f"code_challenge={self.code_challenge}&"
            f"redirect_uri={REDIRECT_URI}"
        )
        webbrowser.open(auth_url)

        start_time = time.time()
        while not self.OAuthHandler.auth_code and not self.OAuthHandler.error:
            if time.time() - start_time > 120:
                return None, "Authorization timed out"
            time.sleep(0.5)

        return self.OAuthHandler.auth_code, self.OAuthHandler.error

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
