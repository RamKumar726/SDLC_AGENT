from langchain_core.prompts import ChatPromptTemplate
from app.models.graph_state import graph_state
from app.models.api_design import APIDesigner
from app.llm.llm_model import LLMModel

class APIDesignerNode:
    def api_designer(self, state: graph_state):
        requirements = state['requirements']
        architecture_design = state['architecture_design']
        llm_prompt  = ChatPromptTemplate.from_messages(
            [
                ('system',
                 '''
                You are a senior backend/API architect.
    
                Design the REST API for the application.
    
                Based on the requirements and architecture,
                define:
    
                - API style
                - Base path
                - Endpoints
                - HTTP methods
                - Request data
                - Response data
                - Authentication requirements
    
                Ensure the API covers all important
                functional requirements.
    
                Follow RESTful API design principles.
                Return data matching the APIDesigner schema only. Do not include markdown,
                comments (such as // or /* */), or text outside the structured result.
                Return a valid JSON object matching the APIDesigner schema.
                Do not design database tables.
                Do not design frontend components.
                
                 '''),
                 ('human',
                  '''
                  Requirements:
                  {requirements}
                  
                  Architecture Design:
                  {architecture_design}
                
                  ''')
            ]
        )

        llm = LLMModel().create_llm()

        chain = llm_prompt | llm.with_structured_output(APIDesigner, method='json_schema', strict=True)
        api_design_result = chain.invoke({
            'requirements': requirements,
            'architecture_design': architecture_design
            })
        state['api_design'] = api_design_result
        return {
            "api_design": api_design_result
        }