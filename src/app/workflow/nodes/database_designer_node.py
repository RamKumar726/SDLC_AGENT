from langchain_core.prompts import ChatPromptTemplate
from app.models import database
from app.models.graph_state import graph_state
from app.models.database import DatabaseSchema
from app.llm.llm_model import LLMModel

class DatabaseDesignerNode:
    def database_designer(self, state: graph_state):
        architecture_design = state['architecture_design']
        requirements = state['requirements']
        llm_prompt  = ChatPromptTemplate.from_messages(
            [
                ('system',
                 '''
                 You are a senior database architect.
                
                            Design the database for the application.
                
                            Based on the requirements and architecture, determine:
                
                            - Database type
                            - Appropriate database technology
                            - Required entities/tables
                            - Important fields
                            - Relationships
                            - Indexes
                            - Constraints
                
                            Avoid unnecessary tables.
                
                            Follow normalization principles where appropriate.
                            Return a valid json object matching the DatabaseSchema fields.
                            
                            Do not design APIs or frontend components.
                            Focus only on database design.
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

        chain = llm_prompt | llm.with_structured_output(DatabaseSchema, method='json_schema', strict=True)
        database_schema_result = chain.invoke({
            'requirements': requirements,
            'architecture_design': architecture_design
            })
        state['database_schema'] = database_schema_result
        return {
            "database_schema": database_schema_result
        }