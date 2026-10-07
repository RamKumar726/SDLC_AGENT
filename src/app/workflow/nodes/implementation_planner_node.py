from langchain_core.prompts import ChatPromptTemplate
from app.models.graph_state import graph_state
from app.models.implementation_plan import ImplementationPlan
from app.llm.llm_model import LLMModel

class ImplementationPlannerNode:
    def implementation_planner(self, state: graph_state):
        requirements = state['requirements']
        architecture_design = state['architecture_design']
        database_schema = state['database_schema']
        api_design = state['api_design']
        llm_prompt  = ChatPromptTemplate.from_messages(
            [
                ('system',
                 '''
                You are a senior software project manager.

                Create a detailed implementation plan for the application.

                Based on the requirements, architecture, database schema,
                and API design, define:

                - Implementation phases
                - Objectives for each phase
                - Specific tasks for each phase
                - Dependencies between tasks
                - Estimated timeline
                - Resource requirements
                - Risk assessment

                Ensure the plan is practical and achievable.
                Return data matching the ImplementationPlan schema only. Do not include markdown,
                comments (such as // or /* */), or text outside the structured result.
                Return a valid JSON object matching the ImplementationPlan schema.
                 '''),
                 ('human',
                  '''
                  Requirements:
                  {requirements}
                  
                  Architecture Design:
                  {architecture_design}
                  
                  Database Schema:
                  {database_schema}
                  
                  API Design:
                  {api_design}
                
                  ''')
            ]
        )

        llm = LLMModel().create_llm()

        chain = llm_prompt | llm.with_structured_output(ImplementationPlan, method='json_schema', strict=True)
        implementation_plan_result = chain.invoke({
            'requirements': requirements,
            'architecture_design': architecture_design,
            'database_schema': database_schema,
            'api_design': api_design
            })
        state['implementation_plan'] = implementation_plan_result
        return {
            'implementation_plan': implementation_plan_result
        }