from pydantic import BaseModel, Field


class TextAnalysisRequest(BaseModel):
    text: str = Field(max_length=3000)


class ComparisonAnalysisRequest(BaseModel):
    text1: str = Field(max_length=3000)
    text2: str = Field(max_length=3000)
