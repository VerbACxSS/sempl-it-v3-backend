import logging
from typing import Annotated

from fastapi import APIRouter, HTTPException, Depends

from app.models.SimplificationRequest import SimplificationRequest
from app.models.SimplificationResponse import SimplificationResponse
from app.services.analysis_service import AnalysisService
from app.services.monitoring_service import MonitoringService
from app.services.simplification_service import SimplificationService
from app.services.service_loader import get_analysis_service, get_monitoring_service, get_simplification_service

# Initialize logging
logger = logging.getLogger()

router = APIRouter()


@router.post("/", response_model=SimplificationResponse)
async def simplify(request: SimplificationRequest,
                   analysis_service: Annotated[AnalysisService, Depends(get_analysis_service)],
                   monitoring_service: Annotated[MonitoringService, Depends(get_monitoring_service)],
                   simplification_service: Annotated[SimplificationService, Depends(get_simplification_service)]):
    try:
        logger.info(request)

        # Simplify the text
        simplified_text, simplification_progress = simplification_service.simplify(request.text, request.target)

        # Compare the texts
        comparison = analysis_service.do_text_comparison(text1=request.text, text2=simplified_text)

        # Save the comparison result if consent is given
        if request.consent:
            monitoring_service.send_text_simplification_result(text_simplification_result=simplification_progress)

        # Return the simplification
        return SimplificationResponse(
            simplified_text=simplified_text,
            simplification_steps=simplification_progress,
            metrics1=comparison.reference_text_evaluation,
            metrics2=comparison.simplified_text_evaluation,
            similarity=comparison.similarity_evaluation,
            diff=comparison.diff_evaluation
        )
    except Exception as exception:
        logger.exception("An error occurred during text simplification.")
        raise HTTPException(status_code=500, detail="An error occurred during text simplificatio.")
