from src.MultilingualSummarizer.components.model_evaulation import ModelEvaluation
from src.MultilingualSummarizer.logging import logger
from src.MultilingualSummarizer.config.configuration import ConfigurationManager


class ModelEvaluationPipeline:
    def __init__(self):
        pass

    def initiate_model_evaluation(self):
        config = ConfigurationManager()
        model_evaluation_config = config.get_model_evaluation_config()
        model_evaluation = ModelEvaluation(config=model_evaluation_config)
        model_evaluation.evaluate()