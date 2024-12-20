from pydantic import BaseModel

class MenuRequest(BaseModel):
    name: str
