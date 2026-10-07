from app.models import requirements
from app.models.graph_state import graph_state
from app.models.update_requirements import UpdateRequirements
from langchain_core.prompts import ChatPromptTemplate
from app.llm.llm_model import LLMModel


class RequirementUpdaterNode:
    def __init__(self):
        pass

    def requirement_updater(self, state: graph_state):
        requirements = state['requirements']
        human_responses = state['human_responses']

        if not human_responses:
            return {"requirements": requirements}
        prompt = ChatPromptTemplate.from_messages(
            [
                ('system',
                 '''
                 You are a software requirements analyst.
                Update the existing requirements using all supplied user
                clarifications. Apply each answer to the appropriate requirement.
                Remove a missing-information item only when its answer is non-empty.
                Keep unanswered items in missing_information. Do not invent details.
                Set is_complete=True only when no important user decisions remain.
                Return the complete updated requirements.
                 '''),
                ('user',
                 '''
                 Existing Requirements:
                 {requirements}
                  User clarifications, keyed by the missing-information item:
                 {human_responses} 
                 '''
                )
            ]
        )

        llm = LLMModel().create_llm()
        chain = prompt | llm.with_structured_output(UpdateRequirements)
        requirement_updater_result = chain.invoke({
            'requirements': requirements,
            'human_responses': human_responses
        })
        answered_items = {
               item for item, answer in human_responses.items()
               if str(answer).strip()
           }
       
        requirement_updater_result["missing_information"] = [
            item
            for item in requirement_updater_result["missing_information"]
            if item not in answered_items
        ]
        requirement_updater_result["is_complete"] = (
            not requirement_updater_result["missing_information"]
        )
        state['requirements'] = requirement_updater_result
        return {'requirements' : requirement_updater_result}