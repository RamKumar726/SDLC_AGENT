from app.models.graph_state import graph_state
from langgraph.types import Command, interrupt

class HumanReviewNode:
    def __init__(self):
        pass

    def human_review(self, state: graph_state):
        response = {}
        missing_info = state['requirements']['missing_information']
        for item in missing_info:
            question = f"Please provide more details about: {item}"
            answer = interrupt({
                'message' : question
            })
            response[item] = str(answer).strip()
        state['human_responses'] = response
        return {"human_responses": response}