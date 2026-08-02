"""LLM configuration - provider is AUTO-DETECTED from which credentials
exist in .env. Keep exactly ONE credential block (Groq or Azure)."""
import os
from dotenv import load_dotenv

load_dotenv()


def require(var: str) -> str:
    value = os.getenv(var)
    if not value:
        raise EnvironmentError(f"Missing '{var}' in .env - add it and rerun.")
    return value


has_azure = bool(os.getenv("AZURE_OPENAI_API_KEY"))
has_groq = bool(os.getenv("GROQ_API_KEY"))

if has_azure and has_groq:
    raise EnvironmentError(
        "Both Azure and Groq credentials found in .env - keep only one block "
        "so the provider is unambiguous."
    )

if has_azure:
    PROVIDER = "azure"
    endpoint = require("AZURE_OPENAI_ENDPOINT").rstrip("/")
    config = {
        "model": require("AZURE_OPENAI_MODEL"),
        "api_key": require("AZURE_OPENAI_API_KEY"),
        "base_url": f"{endpoint}/openai/v1/",
    }
elif has_groq:
    PROVIDER = "groq"
    config = {
        "model": require("GROQ_MODEL"),
        "api_key": require("GROQ_API_KEY"),
        "base_url": require("GROQ_BASE_URL"),
        "price": [0.0, 0.0],
    }
else:
    raise EnvironmentError(
        "No LLM credentials in .env - add either the AZURE_OPENAI_* block "
        "or the GROQ_* block."
    )

llm_config = {"config_list": [config], "temperature": 0}