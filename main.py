from src.datascienceproject import logger
from src.datascienceproject.pipeline.pipeline_data_ingestion import DataIngestionTrainingPipeline
from src.datascienceproject.pipeline.pipline_data_validation import DataValidationTrainingPipeline
from src.datascienceproject.pipeline.pipeline_data_transformation import DataTransformationTrainingPipeline
from src.datascienceproject.pipeline.pipeline_model_trainer import ModelTrainingPipeline

logger.info("Welcome to our custom logging setup!")

STAGE_NAME = "Data Ingestion Stage"
if __name__ == "__main__":
    try:
        logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
        pipeline = DataIngestionTrainingPipeline()
        pipeline.initiate_data_ingestion()
        logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
    except Exception as e:
        logger.error(f"Error in data ingestion process: {str(e)}")
        raise e

STAGE_NAME = "Data Validation Stage"
if __name__ == "__main__":
    try:
        logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
        pipeline = DataValidationTrainingPipeline()
        pipeline.initiate_data_validation()
        logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
    except Exception as e:
        logger.error(f"Error in data validation process: {str(e)}")

STAGE_NAME = "Data Transformation Stage"
if __name__ == '__main__':
    try:
        logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
        obj = DataTransformationTrainingPipeline()
        obj.initiate_data_transformation()
        logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
    except Exception as e:
        logger.exception(e)
        raise e

STAGE_NAME = "Model Training Stage"
if __name__ == "__main__":
    try:
        logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
        pipeline = ModelTrainingPipeline()
        pipeline.initiate_model_training()
        logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
    except Exception as e:
        logger.error(f"Error in model training process: {str(e)}")
        raise e