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

    def start_oauth_flow(self):
        auth_url = (
            "https://myanimelist.net/v1/oauth2/authorize?"
            f"response_type=code&"
            f"client_id={CLIENT_ID}&"
            f"code_challenge={self.code_challenge}&"
            f"redirect_uri={REDIRECT_URI}"
        )
        st.markdown(f"[Click here to authenticate with MyAnimeList]({auth_url})", unsafe_allow_html=True)

        # Streamlit Community Cloud: handle redirect via query params
        query_params = st.query_params
        if "code" in query_params:
            self.auth_code = query_params["code"][0] if isinstance(query_params["code"], list) else query_params["code"]
            return self.auth_code, None
        elif "error" in query_params:
            self.error = query_params["error"][0] if isinstance(query_params["error"], list) else query_params["error"]
            return None, self.error

        # Local: try to run a local HTTP server if running on localhost
        if "localhost" in REDIRECT_URI or "127.0.0.1" in REDIRECT_URI:
            try:
                from http.server import HTTPServer, BaseHTTPRequestHandler
                import threading
                import time
                class OAuthHandler(BaseHTTPRequestHandler):
                    auth_code = None
                    error = None
                    def do_GET(self):
                        from urllib.parse import urlparse, parse_qs
                        parsed = urlparse(self.path)
                        params = parse_qs(parsed.query)
                        if "code" in params:
                            OAuthHandler.auth_code = params["code"][0]
                            self.send_response(200)
                            self.end_headers()
                            self.wfile.write(b"Authorization successful! Return to the app.")
                        elif "error" in params:
                            OAuthHandler.error = params["error"][0]
                            self.send_response(400)
                            self.end_headers()
                            self.wfile.write(b"Authorization failed. Check your settings.")
                        else:
                            self.send_response(400)
                            self.end_headers()
                            self.wfile.write(b"Invalid request")
                server = HTTPServer(('localhost', PORT), OAuthHandler)
                server.timeout = 120
                server_thread = threading.Thread(target=server.handle_request)
                server_thread.daemon = True
                server_thread.start()
                import webbrowser
                webbrowser.open(auth_url)
                start_time = time.time()
                while not OAuthHandler.auth_code and not OAuthHandler.error:
                    if time.time() - start_time > 120:
                        return None, "Authorization timed out"
                    time.sleep(0.5)
                return OAuthHandler.auth_code, OAuthHandler.error
            except Exception as e:
                return None, f"Local OAuth server failed: {e}"
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
