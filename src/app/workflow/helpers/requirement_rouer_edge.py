from app.models.graph_state import graph_state

class RequirementRouterEdge:
    def __init__(self, graph_state: graph_state):
        self.graph_state = graph_state

    def route(self, graph_state: graph_state) -> str:
        if graph_state['requirements']['is_complete']:
            return 'complete'
        else :
            return 'incomplete'
