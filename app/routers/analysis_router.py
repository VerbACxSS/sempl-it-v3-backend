import logging
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from app.models.AnalysisRequest import TextAnalysisRequest, ComparisonAnalysisRequest
from app.models.AnalysisResponse import TextAnalysisResponse, ComparisonAnalysisResponse
from app.services.analysis_service import AnalysisService

# Initialize logging
LOGGER = logging.getLogger()
LOGGER.setLevel(logging.DEBUG)

router = APIRouter()


@router.post("/text", response_model=TextAnalysisResponse)
async def analyze(request: TextAnalysisRequest,
                  analysis_service: Annotated[AnalysisService, Depends(AnalysisService)]):
    try:
        LOGGER.info(request)

        # Analyze the text
        text_evaluation = analysis_service.do_text_analysis(request.text)

        # Return the analysis
        return TextAnalysisResponse(
            text_evaluation=text_evaluation
        )
    except Exception as exception:
        print(exception)
        LOGGER.error('An exception occurred:\n{}'.format(exception))
        raise HTTPException(status_code=500, detail="Analysis Exception")


@router.post("/comparison", response_model=ComparisonAnalysisResponse)
async def analyze(request: ComparisonAnalysisRequest,
                  analysis_service: Annotated[AnalysisService, Depends(AnalysisService)]):
    try:
        LOGGER.info(request)

        # Compare the texts
        comparison = analysis_service.do_text_comparison(request.text1, request.text2)

        # Return the comparison
        return ComparisonAnalysisResponse(
            metrics1=comparison.reference_text_evaluation,
            metrics2=comparison.simplified_text_evaluation,
            similarity=comparison.similarity_evaluation,
            diff=comparison.diff_evaluation
        )
    except Exception as exception:
        print(exception)
        LOGGER.error('An exception occurred:\n{}'.format(exception))
        raise HTTPException(status_code=500, detail="Analysis Exception")
