import logging
import os

import requests

from app.models.AnalysisResponse import TextAnalysisResponse, ComparisonAnalysisResponse
from app.models.SimplificationResponse import SimplificationProgress


class MonitoringService:
    def __init__(self):
        self.base_url=os.getenv("MONITORING_ENDPOINT", "http://localhost:30011/api/v1")
        self.api_key=os.getenv("MONITORING_API_KEY", "123456789")
        self.logger = logging.getLogger()

    def send_text_analysis_result(self, text_analysis_result: TextAnalysisResponse) -> None:
        try:
            requests.post(url=f"{self.base_url}/monitoring/text-analysis",
                          json=text_analysis_result.model_dump(mode="json"),
                          headers={"Authorization": f"Bearer {self.api_key}"})
        except Exception as exception:
            self.logger.exception("Failed to send text analysis result.")

    def send_texts_comparison_analysis_result(self, texts_comparison_analysis_result: ComparisonAnalysisResponse) -> None:
        try:
            requests.post(url=f"{self.base_url}/monitoring/comparison-analysis",
                          json=texts_comparison_analysis_result.model_dump(mode="json"),
                          headers={"Authorization": f"Bearer {self.api_key}"})
        except Exception as exception:
            self.logger.exception("Failed to send texts comparison analysis result.")

    def send_text_simplification_result(self, text_simplification_result: SimplificationProgress) -> None:
        try:
            requests.post(url=f"{self.base_url}/monitoring/text-simplification",
                          json=text_simplification_result,
                          headers={"Authorization": f"Bearer {self.api_key}"})
        except Exception as exception:
            self.logger.exception("Failed to send text simplification result.")