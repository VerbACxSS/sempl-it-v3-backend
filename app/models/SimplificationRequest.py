from pydantic import BaseModel, Field


class SimplificationRequest(BaseModel):
    text: str = Field(max_length=3000)
