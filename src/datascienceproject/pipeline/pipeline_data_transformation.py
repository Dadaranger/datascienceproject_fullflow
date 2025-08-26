from src.datascienceproject.config.configuration import ConfigurationManager
from src.datascienceproject.components.data_transformation import DataTransformation
from src.datascienceproject import logger
from pathlib import Path

STAGE_NAME = "Data Transformation Stage"

class DataTransformationTrainingPipeline:
    def __init__(self):
        """Initialize the Data Transformation Training Pipeline"""
        logger.info(f">>>>>> {STAGE_NAME} started <<<<<<")

    def initiate_data_transformation(self):
        """
        Initiate the data transformation process

        Returns:
            None
        """
        try:
            with open(Path("artifacts/data_validation/status.txt"), 'r') as file:
                status = file.read().split(" ")[-1].strip()
            if status =="True":
                config = ConfigurationManager()
                data_transformation_config = config.get_data_transformation_config()

                    # Create data transformation object
                data_transformation = DataTransformation(config=data_transformation_config)

                    # Split data
                data_transformation.split_data()
                    
                logger.info(f">>>>>> {STAGE_NAME} completed <<<<<<\n\nx==========x")
            else:
                raise Exception("Your data schema is not validated")
        except Exception as e:
            print(e)

if __name__ == '__main__':
    try:
        logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
        obj = DataTransformationTrainingPipeline()
        obj.initiate_data_transformation()
        logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
    except Exception as e:
        logger.exception(e)
        raise e