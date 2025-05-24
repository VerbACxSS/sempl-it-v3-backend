from italian_ats_evaluator import TextAnalyzer, SimplificationAnalyzer
from italian_ats_evaluator.models.SimplificationEvaluation import SimplificationEvaluation
from italian_ats_evaluator.models.TextEvaluation import TextEvaluation


class AnalysisService:
    def __init__(self):
        self.text_analyzer = TextAnalyzer()
        self.simplification_analyzer = SimplificationAnalyzer()

    def do_text_analysis(self, text: str) -> TextEvaluation:
        return self.text_analyzer.analyze(text)

    def do_text_comparison(self, text1: str, text2: str) -> SimplificationEvaluation:
        return self.simplification_analyzer.analyze(text1, text2)
