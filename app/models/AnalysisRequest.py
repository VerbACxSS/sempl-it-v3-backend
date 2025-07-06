from pydantic import BaseModel, Field


class TextAnalysisRequest(BaseModel):
    text: str = Field(max_length=3000)
    consent: bool = Field(default=False)


class ComparisonAnalysisRequest(BaseModel):
    text1: str = Field(max_length=3000)
    text2: str = Field(max_length=3000)
    consent: bool = Field(default=False)
