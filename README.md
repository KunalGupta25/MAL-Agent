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

## Screenshots
![Login](https://github.com/user-attachments/assets/924b90c4-2443-4da9-a0f1-db264ea6a646)

![Homepage](https://github.com/user-attachments/assets/5dffd346-0d27-411e-925d-b9aa346907a1)

![My Anime List Query](https://github.com/user-attachments/assets/2f7a1199-467e-48a4-8d50-1e53d93049fe)

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

### Important Note
> **This app can only be run locally.**

> Due to the way MyAnimeList OAuth and PKCE authentication works, you must run this app on your own machine (localhost). Hosting on Streamlit Community Cloud or other remote servers is not supported for full authentication functionality.



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

[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/Y8Y6IPAOF)
