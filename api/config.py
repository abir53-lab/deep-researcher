import os
from dotenv import load_dotenv

# This loads your .env file so Python can read your API keys
load_dotenv()

# OpenRouter settings
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"

# The LLM model we'll use via OpenRouter (cheap + fast for hackathon)
MODEL_NAME = "deepseek/deepseek-chat"

# Tavily search API key
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

# Sanity check — this runs when you test this file directly
if __name__ == "__main__":
    print("OpenRouter Key loaded:", "✅" if OPENROUTER_API_KEY else "❌ MISSING")
    print("Tavily Key loaded:", "✅" if TAVILY_API_KEY else "❌ MISSING")
    print("Model:", MODEL_NAME)