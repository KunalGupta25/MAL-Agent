# app.py
import streamlit as st
from auth import login_button
from agent import initialize_agent

st.set_page_config(page_title="MyAnimeList Chat Assistant", page_icon="🎮")

system_prompt = """
You are a Helpful and Friendly Anime Assistant with comprehensive capabilities for managing and discovering anime content.

## Core Responsibilities:
- **MyAnimeList Management**: View, add, and remove anime from user's personal list
- **Anime Recommendations**: Provide personalized suggestions based on user preferences
- **Web Search**: Search for additional anime information when needed
- **Watch Links**: Provide streaming links exclusively from HiAnime

## Tool Usage Guidelines:
- **format_anime_list**: ALWAYS use this tool to display anime lists in a user-friendly format
- **anime_suggestion**: Use for generating personalized anime recommendations
- **display_anime_cards**: Format anime suggestions into visually appealing cards
- **hianime_watchlink**: ONLY use this tool for providing watch links - no other sources
- **DuckDuckGoSearchTool**: Use for additional web searches when more information is needed

## Key Rules:
1. Always format anime lists using the format_anime_list tool
2. Present recommendations as cards using display_anime_cards
3. Only provide HiAnime links for watching anime online
4. Be helpful, friendly, and engaging in all interactions
5. Search the web when you need additional context or information
"""

# Initialize session state variables
if "access_token" not in st.session_state:
    st.session_state.access_token = None
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hi! I'm your MyAnimeList assistant. How can I help you today?"}
    ]
if "agent" not in st.session_state:
    st.session_state.agent = None
if "user_stats" not in st.session_state:
    st.session_state.user_stats = None

# --- Authentication Flow ---
if not st.session_state.access_token:
    st.title("MyAnimeList Assistant")
    st.write("Please log in with your MyAnimeList account to continue.")
    login_button()
else:
    # Initialize the agent after login if not already done
    if st.session_state.agent is None:
        with st.spinner("Setting up your personalized assistant..."):
            # Option 1: Simple initialization with custom system prompt
            st.session_state.agent = initialize_agent()
            
            # Option 2: Personalized initialization (if you have user stats)
            # if st.session_state.user_stats:
            #     st.session_state.agent = initialize_personalized_agent(st.session_state.user_stats)
            # else:
            #     st.session_state.agent = initialize_agent()

    st.title("MyAnimeList Chat Assistant")
    
    # Add a sidebar with agent info (optional)
    with st.sidebar:
        st.header("Assistant Info")
        st.write("🤖 **Specialized MAL Assistant**")
        st.write("I can help you with:")
        st.write("- View your anime list")
        st.write("- Filter by status")
        st.write("- Get recommendations")
        st.write("- Analyze your viewing habits")
        
        # Reset conversation button
        if st.button("🔄 Reset Conversation"):
            st.session_state.messages = [
                {"role": "assistant", "content": "Hi! I'm your MyAnimeList assistant. How can I help you today?"}
            ]
            st.rerun()

    # Display chat history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])  # Use markdown for better table rendering

    # Chat input
    if prompt := st.chat_input("Ask me anything about your anime list..."):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message immediately
        with st.chat_message("user"):
            st.markdown(prompt)

        # Get agent response
        with st.chat_message("assistant"):
            with st.spinner("Analyzing your request..."):
                main_prompt = f"""
                System: {system_prompt}
                
                User: {prompt}
                """
                try:
                    response = st.session_state.agent.run(prompt, reset=False)  # Keep context
                    st.markdown(response)
                    st.session_state.messages.append({"role": "assistant", "content": response})
                except Exception as e:
                    error_msg = f"Sorry, I encountered an error: {str(e)}"
                    st.error(error_msg)
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})

        st.rerun()  # Refresh to display the new message