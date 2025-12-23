from pydantic import BaseModel


class LLmModel(BaseModel):
    question: str

class VideoModel(BaseModel):
    url:str
