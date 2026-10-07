from langgraph.graph import StateGraph, START, END
from app.workflow.nodes.requirement_updater_node import RequirementUpdaterNode
from app.workflow.nodes.requirement_analyzer_node import RequirementAnalyzerNode
from app.workflow.nodes.human_review_node import HumanReviewNode
from app.workflow.nodes.app_classifier_node import AppClassifierNode
from app.workflow.nodes.architecture_designer_node import ArchitectureDesignerNode
from app.models.graph_state import graph_state as GraphState
from app.workflow.helpers.requirement_rouer_edge import RequirementRouterEdge
from app.workflow.nodes.database_designer_node import DatabaseDesignerNode
from app.workflow.nodes.api_designer_node import APIDesignerNode
from app.workflow.nodes.implementation_planner_node import ImplementationPlannerNode
from langgraph.checkpoint.memory import InMemorySaver

class WorkflowGraph:
    def __init__(self):
        self.graph = StateGraph(GraphState)
        self.checkpoint = InMemorySaver()

    def build_graph(self):
        self.graph.add_node('requirement_analyzer', RequirementAnalyzerNode().requirement_analyzer)
        self.graph.add_node('requirement_updater', RequirementUpdaterNode().requirement_updater)
        self.graph.add_node('human_review', HumanReviewNode().human_review)
        self.graph.add_node('app_classifier', AppClassifierNode().app_classifier)
        self.graph.add_node('architecture_designer', ArchitectureDesignerNode().architecture_designer)
        self.graph.add_node('database_designer', DatabaseDesignerNode().database_designer)
        self.graph.add_node('api_designer', APIDesignerNode().api_designer)
        self.graph.add_node('implementation_planner', ImplementationPlannerNode().implementation_planner)

        self.graph.add_edge(START, 'requirement_analyzer')
        self.graph.add_conditional_edges('requirement_analyzer', 
                                         RequirementRouterEdge(GraphState).route, 
                                         {'complete': 'app_classifier',
                                          'incomplete': 'human_review'
                                         }
                                        )
        self.graph.add_edge('human_review', 'requirement_updater')
        self.graph.add_conditional_edges('requirement_updater', 
                                          RequirementRouterEdge(GraphState).route, 
                                          {'complete': 'app_classifier',
                                           'incomplete': 'human_review'
                                          }
                                         )
        self.graph.add_edge('app_classifier', 'architecture_designer')
        self.graph.add_edge('architecture_designer', 'database_designer')
        self.graph.add_edge('architecture_designer', 'api_designer')
        self.graph.add_edge(['api_designer', 'database_designer'], 'implementation_planner')
        self.graph.add_edge('implementation_planner', END)
        final_graph = self.graph.compile(checkpointer=self.checkpoint)
        return final_graph