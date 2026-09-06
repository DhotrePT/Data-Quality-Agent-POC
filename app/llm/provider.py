import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI


load_dotenv()


def get_llm():

    model = os.getenv(
        "LLM_MODEL",
        "gpt-oss:20b"
    )

    base_url = os.getenv(
        "LLM_BASE_URL",
        "http://localhost:11434/v1"
    )

    api_key = os.getenv(
        "LLM_API_KEY",
        "ollama"
    )

    return ChatOpenAI(
        model=model,
        base_url=base_url,
        api_key=api_key,
        temperature=0,
    )