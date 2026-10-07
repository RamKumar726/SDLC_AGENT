from app.models.graph_state import graph_state
from app.models.architecture import ArchitectureDesign
from langchain_core.prompts import ChatPromptTemplate
from app.llm.llm_model import LLMModel

class ArchitectureDesignerNode:
    def __init__(self):
        pass

    def architecture_designer(self, state: graph_state):
        requirements = state['requirements']
        app_classification = state['app_classification']

        llm_prompt = ChatPromptTemplate.from_messages(
            [
                ('system',
                 '''
                 You are a senior software architect.
                 Design the architecture based on the requirements and application classification.
                 Provide a high-level architecture design, including components, modules, and their interactions.
                 '''),
                ('human', 
                 '''
                 Requirements:
                 {requirements}
                 
                 Application Classification:
                 {app_classification}
                 ''')
            ]
        )

        llm = LLMModel().create_llm()

        chain = llm_prompt | llm.with_structured_output(ArchitectureDesign, method='json_schema', strict = True)

        architecture_design_result = chain.invoke({
            'requirements': requirements,
            'app_classification': app_classification
        })
        state['architecture_design'] = architecture_design_result
        return {"architecture_design": architecture_design_result}