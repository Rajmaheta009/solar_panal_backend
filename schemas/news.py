from pydantic import BaseModel

class NewsCreate(BaseModel):
    title: str
    description: str
    picture: str

class NewsResponse(BaseModel):
    id: int
    title: str
    description: str
    picture: str

    class Config:
        orm_mode = True
