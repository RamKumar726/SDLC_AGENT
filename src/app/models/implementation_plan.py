from typing import TypedDict
class ImplementationTask(TypedDict):
    task: str
    description: str
    dependencies: list[str]
    priority: str

class ImplementationPhase(TypedDict):
    phase_name: str
    objective: str
    tasks: list[ImplementationTask]

class ImplementationPlan(TypedDict):
    phases: list[ImplementationPhase]
    estimated_timeline: str
    resource_requirements: str
    risk_assessment: str