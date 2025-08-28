from src.datascienceproject.config.configuration import ConfigurationManager
from src.datascienceproject.components.model_evaluation import ModelEvaluation
from src.datascienceproject import logger
from pathlib import Path

STAGE_NAME = "Model Evaluation Stage "

class ModelEvaluationPipeline:
    def __init__(self):
        pass

    def initiate_model_evaluation(self):
        config = ConfigurationManager()
        model_evaluation_config = config.get_model_evaluation_config()
        model_evaluation = ModelEvaluation(config=model_evaluation_config)
        model_evaluation.log_into_mlflow()