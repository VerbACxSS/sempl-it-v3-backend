from fastapi import Request

from app.services.analysis_service import AnalysisService
from app.services.monitoring_service import MonitoringService
from app.services.simplification_service import SimplificationService


def get_analysis_service(request: Request) -> AnalysisService:
    return request.app.state.analysis_service


def get_monitoring_service(request: Request) -> MonitoringService:
    return request.app.state.monitoring_service


def get_simplification_service(request: Request) -> SimplificationService:
    return request.app.state.simplification_service

