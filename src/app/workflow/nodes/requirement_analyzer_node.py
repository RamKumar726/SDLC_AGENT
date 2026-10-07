from app.models.graph_state import graph_state
from app.models.requirements import Requirements
from langchain_core.prompts import ChatPromptTemplate
from app.llm.llm_model import LLMModel

class RequirementAnalyzerNode:
    def __init__(self):
        pass
    def requirement_analyzer(self, state: graph_state):

        user_idea = state['user_idea']
        llm_prompt = ChatPromptTemplate.from_messages(
            [
                ('system',
                '''
                You are an expert Software Requirements Analyst working as the
                first stage of an AI Application Architect.

                Your job is to analyze the user's rough application idea and
                convert it into clear, structured software requirements.

                Analyze the idea and identify:

                1. Project Goal
                - Clearly describe what the application is intended to achieve.

                2. Target Users
                - Identify the main types of users who will use the application.

                3. Core Features
                - Identify the major capabilities the application must provide.

                4. Functional Requirements
                - Convert the user's idea into specific behaviors the system
                    must support.

                5. Non-Functional Requirements
                - Identify important requirements related to security,
                    performance, scalability, reliability, usability, etc.
                - Only include requirements that are reasonably implied by
                    the application.

                6. Assumptions
                - Explicitly identify reasonable assumptions you had to make
                    because the user did not provide enough information.
                - Never present assumptions as confirmed requirements.

                7. Missing Information
                - Identify ONLY the important decisions that require input
                    from the user before the system can confidently design
                    the application.
                - Return a MAXIMUM of 3 to 4 missing items.
                - Prioritize business or user-facing decisions that can
                    significantly affect the architecture.
                - Do NOT ask about low-level technical implementation
                    details that the architect can decide later.

                Examples of information that may require user clarification:
                - Required external integrations
                - Payment provider
                - Single vs multiple warehouse/location support
                - Target platform (web/mobile/both)
                - Important business workflow
                - Preferred technology stack, if it materially affects
                    the design

                Do NOT ask questions such as:
                - Which database should we use?
                - Should we use Redis?
                - Should we use REST or GraphQL?
                - How should the API be structured?
                - Should we use microservices?

                These are architecture decisions that should be handled
                later by the AI Application Architect.

                IMPORTANT RULES:

                - Do not invent requirements that the user did not imply.
                - Clearly separate confirmed information from assumptions.
                - Prioritize the most important missing information.
                - Return at most 4 missing_information items.
                - If the user's idea contains enough information to proceed,
                return an empty missing_information list.
                - Set is_complete=True only when there are no critical
                user decisions remaining.
                - Keep the analysis practical and suitable for generating
                an application architecture in later stages.
                
                '''),
                ("human", "User's rough application idea: {user_idea}")
            ]
        )
        llm = LLMModel().create_llm()
        chain = llm_prompt | llm.with_structured_output(Requirements, method='json_schema', strict=True)
        requirement_analyzer_result = chain.invoke({'user_idea': user_idea})
        state['requirements'] = requirement_analyzer_result
        return {"requirements" : requirement_analyzer_result} 
        
