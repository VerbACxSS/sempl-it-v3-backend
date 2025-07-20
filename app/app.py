from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .services.analysis_service import AnalysisService
from .services.monitoring_service import MonitoringService
from .services.simplification_service import SimplificationService

load_dotenv()

from . import router


# Initialize the FastAPI application
app = FastAPI(title="VerbACxSS SEMPL-IT API", openapi_url="/api/openapi.json")

# Add middlewares (CORS)
app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

# Initialize services
app.state.analysis_service = AnalysisService()
app.state.monitoring_service = MonitoringService()
app.state.simplification_service = SimplificationService()

# Include routers
app.include_router(router.router, prefix='/api/v1', tags=["api"])
