from pydantic import BaseModel

class NewsCreate(BaseModel):
    title: str
    description: str
    picture: str