from langchain_groq import ChatGroq
from app.configuration.config import Config
from app.llm.llm_model import LLMModel
from app.workflow.nodes.requirement_analyzer_node import RequirementAnalyzerNode

analyzer = RequirementAnalyzerNode()
res = analyzer.requirement_analyzer({
    'user_idea': 'A mobile app that helps users track their daily water intake and provides reminders to stay hydrated.',
    'requirements': None,
    'human_response': '',
    'current_question': '',
    'app_classification': None,
    'architecture_design': None,
    'database_schema': None,
    'api_design': None,
    'implementation_plan': None,
    'human_responses': {}
})

print(res)