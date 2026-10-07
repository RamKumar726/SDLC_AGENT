
from typing import TypedDict
from app.models.requirements import Requirements
from app.models.app_classification import AppClassification
from app.models.architecture import ArchitectureDesign
from app.models.database import DatabaseSchema
from app.models.api_design import APIDesigner
from app.models.implementation_plan import ImplementationPlan

class graph_state(TypedDict):
    user_idea : str 
    requirements: Requirements 
    human_response: str
    current_question: str
    app_classification: AppClassification
    architecture_design: ArchitectureDesign
    database_schema: DatabaseSchema
    api_design: APIDesigner
    implementation_plan: ImplementationPlan
    human_responses : dict[str,str]
