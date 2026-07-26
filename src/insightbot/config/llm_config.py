# -----------------------------------------------------------------------
"""LLM configuration - works with any OpenAI-compatible provider.
Switch providers by editing .env only (Groq / Gemini / Ollama / Azure...)."""
import os
from dotenv import load_dotenv

load_dotenv()

llm_config = {
    "config_list": [
        {
            "model": os.getenv("LLM_MODEL", "llama-3.3-70b-versatile"),
            "api_key": os.getenv("LLM_API_KEY"),
            "base_url": os.getenv("LLM_BASE_URL", "https://api.groq.com/openai/v1"),
            "price": [0.0, 0.0],   # free tier -> silences unknown-model cost warnings
        }
    ],
    "temperature": 0,
}