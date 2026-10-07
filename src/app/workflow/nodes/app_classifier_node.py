from app.models.graph_state import graph_state
from langchain_core.prompts import ChatPromptTemplate
from app.models.app_classification import AppClassification
from app.llm.llm_model import LLMModel

class AppClassifierNode:
    def __init__(self):
        pass

    def app_classifier(self, state: graph_state):
        requirements = state['requirements']

        llm_prompt = ChatPromptTemplate.from_messages(
            [
                ('system',
                '''
                You are a senior software architect.

                Classify the application based on its requirements.

                Determine:
                - Application type
                - Business domain
                - Suitable architecture pattern
                - Overall complexity

                Do not design the detailed architecture yet.
                Only classify the application.
                '''),
                ('human', 
                 '''
                Requirements:

                {requirements}

                 ''')
            ]
        )

        chain = llm_prompt | LLMModel().create_llm().with_structured_output(AppClassification)

        classification_result = chain.invoke({'requirements': requirements})
        state['app_classification'] = classification_result
        return {"app_classification": classification_result}