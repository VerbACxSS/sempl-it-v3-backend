from italian_ats_evaluator.models.DiffEvaluation import DiffEvaluation
from italian_ats_evaluator.models.SimilarityEvaluation import SimilarityEvaluation
from italian_ats_evaluator.models.TextEvaluation import TextEvaluation
from pydantic import BaseModel, Field


class SimplificationProgress(BaseModel):
    target: str = Field(default='expert', serialization_alias="target")
    original: str = Field(default='', serialization_alias="original")
    proofreading: str = Field(default='', serialization_alias="proofreading")
    lex: str = Field(default='', serialization_alias="lex")
    connectives: str = Field(default='', serialization_alias="connectives")
    expressions: str = Field(default='', serialization_alias="expressions")
    sentence_splitter: str = Field(default='', serialization_alias="sentence_splitter")
    verbs: str = Field(default='', serialization_alias="verbs")
    sentence_reorganizer: str = Field(default='', serialization_alias="sentence_reorganizer")
    explain: str = Field(default='', serialization_alias="explain")

    def __getitem__(self, item):
        return getattr(self, item)

    def update(self, data: dict):
        for key, value in data.items():
            setattr(self, key, value)


class SimplificationResponse(BaseModel):
    simplified_text: str = Field(serialization_alias="simplifiedText")
    simplification_steps: SimplificationProgress = Field(serialization_alias="simplificationSteps")
    metrics1: TextEvaluation = Field(serialization_alias="metrics1")
    metrics2: TextEvaluation = Field(serialization_alias="metrics2")
    similarity: SimilarityEvaluation = Field(serialization_alias="similarity")
    diff: DiffEvaluation = Field(serialization_alias="diff")
