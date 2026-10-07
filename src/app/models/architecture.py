from typing import TypedDict

class ArchitectureComponent(TypedDict):
    name: str
    technology: str
    reponsensibility: str
    reason: str

class ArchitectureDesign(TypedDict):
    
    architecture_style: str

    frontend: ArchitectureComponent

    backend: list[ArchitectureComponent]

    database: ArchitectureComponent

    authentication: ArchitectureComponent

    caching: ArchitectureComponent

    storage: ArchitectureComponent

    external_services: list[ArchitectureComponent]

    deployment: ArchitectureComponent

    security_considerations: list[str]