from src.datascienceproject import logger
from src.datascienceproject.pipeline.pipeline_data_ingestion import DataIngestionTrainingPipeline

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
