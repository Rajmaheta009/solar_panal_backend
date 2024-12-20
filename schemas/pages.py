from pydantic import BaseModel

class PageRequest(BaseModel):
    menu_id: int
    title: str
