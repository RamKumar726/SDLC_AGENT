from typing import TypedDict

class DatabaseEntity(TypedDict):
    name: str
    purpose: str
    attributes: list[str]
    relationships: list[str]
    indexes: str

class DatabaseSchema(TypedDict):
    database_type: str
    database_name: str
    entities: list[DatabaseEntity]
    relationships: list[str]
    indexing_strategy: str  