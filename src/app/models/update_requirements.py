from typing import TypedDict

class UpdateRequirements(TypedDict):
    project_goal: str
    target_users: list[str]
    core_features: list[str]
    functional_requirements: list[str]
    non_functional_requirements: list[str]
    missing_information: list[str]
    is_complete: bool
