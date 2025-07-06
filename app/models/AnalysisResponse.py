from italian_ats_evaluator.models.DiffEvaluation import DiffEvaluation
from italian_ats_evaluator.models.SimilarityEvaluation import SimilarityEvaluation
from italian_ats_evaluator.models.TextEvaluation import TextEvaluation
from pydantic import BaseModel, Field


class TextAnalysisResponse(BaseModel):
    text: str = Field(serialization_alias="text")
    text_evaluation: TextEvaluation = Field(serialization_alias="textEvaluation")


class ComparisonAnalysisResponse(BaseModel):
    text1: str = Field(serialization_alias="text1")
    text2: str = Field(serialization_alias="text2")
    metrics1: TextEvaluation
    metrics2: TextEvaluation
    similarity: SimilarityEvaluation
    diff: DiffEvaluation
