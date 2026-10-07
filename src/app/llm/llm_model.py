from langchain_openai import AzureChatOpenAI
from app.configuration.config import Config

class LLMModel:
    def create_llm(self):
        llm = AzureChatOpenAI(
            azure_deployment="gpt-4.1-mini",
        )
        return llm
