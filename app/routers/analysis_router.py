import logging
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from app.models.AnalysisRequest import TextAnalysisRequest, ComparisonAnalysisRequest
from app.models.AnalysisResponse import TextAnalysisResponse, ComparisonAnalysisResponse
from app.services import get_analysis_service, get_monitoring_service, MonitoringService
from app.services.analysis_service import AnalysisService

# Initialize logging
logger = logging.getLogger()

router = APIRouter()


@router.post("/text", response_model=TextAnalysisResponse)
async def analyze_text(request: TextAnalysisRequest,
                       analysis_service: Annotated[AnalysisService, Depends(get_analysis_service)],
                       monitoring_service: Annotated[MonitoringService, Depends(get_monitoring_service)]):
    try:
        logger.info(request)

        # Analyze the text
        text_evaluation = analysis_service.do_text_analysis(request.text)

        # Build the response
        response = TextAnalysisResponse(text=request.text, text_evaluation=text_evaluation)

        # Save the text analysis result if consent is given
        if request.consent:
            monitoring_service.send_text_analysis_result(text_analysis_result=response)

        # Return the response
        return response
    except Exception as exception:
        logger.exception("An error occurred during text analysis.")
        raise HTTPException(status_code=500, detail="An error occurred during text analysis.")


@router.post("/comparison", response_model=ComparisonAnalysisResponse)
async def compare_texts(request: ComparisonAnalysisRequest,
                        analysis_service: Annotated[AnalysisService, Depends(get_analysis_service)],
                        monitoring_service: Annotated[MonitoringService, Depends(get_monitoring_service)]):
    try:
        logger.info(request)

        # Compare the texts
        comparison = analysis_service.do_text_comparison(request.text1, request.text2)

        # Build the response
        response = ComparisonAnalysisResponse(
            text1=request.text1,
            text2=request.text2,
            metrics1=comparison.reference_text_evaluation,
            metrics2=comparison.simplified_text_evaluation,
            similarity=comparison.similarity_evaluation,
            diff=comparison.diff_evaluation
        )

        # Save the comparison result if consent is given
        if request.consent:
            monitoring_service.send_texts_comparison_analysis_result(texts_comparison_analysis_result=response)

        # Return the response
        return response
    except Exception as exception:
        logger.exception("An exception occurred during comparison analysis.")
        raise HTTPException(status_code=500, detail="An exception occurred during comparison analysis.")
