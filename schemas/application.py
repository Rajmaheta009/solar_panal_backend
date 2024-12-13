from pydantic import BaseModel

class ApplicationBase(BaseModel):
    type: str
    InnerHtmlText: str

class ApplicationCreate(ApplicationBase):
    pass

class ApplicationUpdate(ApplicationBase):
    pass
