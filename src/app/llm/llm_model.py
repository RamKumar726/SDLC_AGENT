from langchain_groq import ChatGroq
from app.configuration.config import Config

class LLMModel:
    def create_llm(self):
        llm = ChatGroq(model = "openai/gpt-oss-120b",max_retries = 5)
        return llm
