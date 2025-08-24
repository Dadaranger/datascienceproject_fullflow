from src.datascienceproject.config.configuration import ConfigurationManager
from src.datascienceproject.components.data_ingestion import DataIngestion
from src.datascienceproject import logger

STAGE_NAME = "Data Ingestion Stage"

class DataIngestionTrainingPipeline:
    def __init__(self):
        """Initialize the Data Ingestion Training Pipeline"""
        logger.info(f">>>>>> {STAGE_NAME} started <<<<<<")
    
    def initiate_data_ingestion(self):
        """
        Initiate the data ingestion process
        
        Returns:
            None
        """
        try:
            config = ConfigurationManager()
            data_ingestion_config = config.get_data_ingestion_config()
            
            # Create data ingestion object
            data_ingestion = DataIngestion(config=data_ingestion_config)
            
            # Download and extract file
            logger.info("Downloading file...")
            data_ingestion.download_file()
            
            logger.info("Extracting file...")
            data_ingestion.extract_zip_file()
            
            logger.info(f">>>>>> {STAGE_NAME} completed <<<<<<\n\nx==========x")
            
        except Exception as e:
            logger.error(f"Error in {STAGE_NAME}: {str(e)}")
            raise e

if __name__ == '__main__':
    try:
        logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
        obj = DataIngestionTrainingPipeline()
        obj.initiate_data_ingestion()
        logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
    except Exception as e:
        logger.exception(e)
        raise e