from pydantic import BaseModel

class PageContentRequest(BaseModel):
    page_id: int
    content: str
