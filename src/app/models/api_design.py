from typing import TypedDict

class APISchema(TypedDict):
    method: str
    authentication_required: bool
    path : str
    description: str
    request_body: list[str]
    response_body: str

class APIDesigner(TypedDict):
    style : str
    api_endpoints: list[APISchema]
    base_url: str
    authentication_mechanism: str