from tools import add_anime, remove_anime, get_anime_list, search_anime, format_anime_list, display_anime_cards, hianime_watchlink, anime_suggestion
from smolagents import CodeAgent, OpenAIServerModel
from smolagents import DuckDuckGoSearchTool
from dotenv import load_dotenv
import os

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

def initialize_agent():
    """
    Initialize the agent with necessary tools and configurations.
    """
    tools = [
        add_anime,
        remove_anime,
        get_anime_list,
        search_anime,
        format_anime_list,
        display_anime_cards,
        hianime_watchlink,
        anime_suggestion,
        DuckDuckGoSearchTool()
    ]
    
    # Configure models
    gemini_llm = OpenAIServerModel(
        model_id="gemini-2.0-flash",
        api_base="https://generativelanguage.googleapis.com/v1beta/openai/",
        api_key=GEMINI_API_KEY,
        max_tokens=1096,
        temperature=0.5,
    )
    
    deepseek_llm = OpenAIServerModel(
        model_id="deepseek-chat",
        api_base="https://api.deepseek.com",
        api_key=DEEPSEEK_API_KEY,
    )

    
    
    return CodeAgent(
        model=gemini_llm,  # Changed parameter to 'llm'
        tools=tools,
        # max_tokens=4096,
        # temperature=0.5
    )
