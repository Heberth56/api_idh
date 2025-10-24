from pydantic import BaseModel


class LLmModel(BaseModel):
    question: str
