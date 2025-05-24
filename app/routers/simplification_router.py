import logging
import os
from typing import Annotated

from fastapi import APIRouter, HTTPException, Depends

from ..models.SimplificationRequest import SimplificationRequest
from ..models.SimplificationResponse import SimplificationResponse
from ..services.simplification_service import SimplificationService
from ..services.analysis_service import AnalysisService

# Initialize logging
LOGGER = logging.getLogger()
LOGGER.setLevel(logging.DEBUG)

router = APIRouter()

@router.post("/", response_model=SimplificationResponse)
async def simplify(request: SimplificationRequest,
                   analysis_service: Annotated[AnalysisService, Depends(AnalysisService)],
                   simplification_service: Annotated[SimplificationService, Depends(SimplificationService)]):
    try:
        LOGGER.info(request)

        # Simplify the text
        simplification_progress = simplification_service.simplify(request.text)
        simplified_text = simplification_progress['explain']

        # Compare the texts
        comparison = analysis_service.do_text_comparison(text1=request.text, text2=simplified_text)

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
        print(exception)
        LOGGER.error('An exception occurred:\n{}'.format(exception))
        raise HTTPException(status_code=500, detail="Prediction Exception")
