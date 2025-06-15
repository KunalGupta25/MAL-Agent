---
title: MAL Agent
emoji: 🚀
colorFrom: red
colorTo: red
sdk: docker
app_port: 8501
tags:
- streamlit
pinned: false
short_description: MyAnimeList Based Agent
license: mit
---

# Welcome to Streamlit!

Edit `/src/streamlit_app.py` to customize this app to your heart's desire. :heart:

If you have any questions, checkout our [documentation](https://docs.streamlit.io) and [community
forums](https://discuss.streamlit.io).

# MAL Agent 🚀

A Streamlit-powered assistant for managing your [MyAnimeList](https://myanimelist.net/) anime list, discovering new anime, and getting recommendations—all in a friendly chat interface.

---

## Features

- **MyAnimeList Management:**  
  - View, add, and remove anime from your personal MAL list.
  - Filter your list by status (Watching, Completed, etc.).
- **Anime Recommendations:**  
  - Get personalized anime suggestions.
  - Display recommendations as visually appealing cards.
- **Web Search:**  
  - Search for additional anime info using DuckDuckGo.
- **Watch Links:**  
  - Get streaming links exclusively from HiAnime.
- **Secure Authentication:**  
  - OAuth2 login with your MAL account.

---

## Getting Started

### 1. Clone the Repository

```sh
# Using PowerShell
git clone https://github.com/yourusername/MAL-Agent.git
cd MAL_Agent
```

### 2. Set Up Environment Variables

Copy `example.env` to `.env` and fill in your API keys and MAL credentials:

```sh
Copy-Item example.env .env
```

Edit `.env` and provide your keys:
```
GEMINI_API_KEY=your_gemini_api_key
DEEPSEEK_API_KEY=your_deepseek_api_key
MAL_CLIENT_ID=your_mal_client_id
MAL_CLIENT_SECRET=your_mal_client_secret
MAL_REDIRECT_URI=http://localhost:8080/callback
MAL_PORT=8080
```

### 3. Install Dependencies

```sh
pip install -r requirements.txt
```

### 4. Run the App

```sh
streamlit run src/streamlit_app.py
```

The app will be available at [http://localhost:8501](http://localhost:8501).

---

## Project Structure

```
MAL_Agent/
├── .env
├── Dockerfile
├── README.md
├── requirements.txt
├── src/
│   ├── agent.py
│   ├── auth.py
│   ├── streamlit_app.py
│   └── tools.py
```

---

## Docker

You can also run the app in Docker:

```sh
docker build -t mal-agent .
docker run -p 8501:8501 --env-file .env mal-agent
```

---

## License

MIT

---

## Credits

- [Streamlit](https://streamlit.io/)
- [MyAnimeList API](https://myanimelist.net/apiconfig/references/api/v2)
- [smolagents](https://github.com/smol-ai/smol-agents)

---

## Support Me

If you like this project, consider supporting me on Ko-fi!

<a href="https://ko-fi.com/yourusername" target="_blank">
  <img src="https://cdn.ko-fi.com/cdn/kofi_button.png?v=3" alt="Buy Me a Coffee at ko-fi.com" height="36" style="border:0px;height:36px;" />
</a>
