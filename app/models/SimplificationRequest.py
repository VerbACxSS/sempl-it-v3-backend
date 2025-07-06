from pydantic import BaseModel, Field


class SimplificationRequest(BaseModel):
    text: str = Field(max_length=3000)
    target: str = Field(default="expert", pattern="^(expert|common)$")
    consent: bool = Field(default=False)
