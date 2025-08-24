# Import constants and utility functions from the project
from src.datascienceproject.constant import *  # Import all constants
from src.datascienceproject.utils.common import read_yaml, create_directories  # Import specific utility functions
from src.datascienceproject import logger  # Import logger
import os  # For path operations

from src.datascienceproject.entity.config_entity import (DataIngestionConfig)

class ConfigurationManager:
    def __init__(self,
                 config_filepath=CONFIG_FILE_PATH,
                 params_filepath=PARAMS_FILE_PATH,
                 schema_filepath=SCHEMA_FILE_PATH):
        
        # Log the actual paths being used
        logger.debug(f"Config file path: {config_filepath}")
        logger.debug(f"Params file path: {params_filepath}")
        logger.debug(f"Schema file path: {schema_filepath}")
        
        # Verify file existence
        if not os.path.exists(config_filepath):
            raise FileNotFoundError(f"Configuration file not found at: {config_filepath}")
            
        # Convert paths to strings for read_yaml
        self.config = read_yaml(str(config_filepath))
        self.params = read_yaml(str(params_filepath))
        self.schema = read_yaml(str(schema_filepath))

        create_directories([self.config.artifacts_root])

    def get_data_ingestion_config(self) -> DataIngestionConfig:
        config = self.config.data_ingestion
        create_directories([config.root_dir])

        data_ingestion_config = DataIngestionConfig(
            root_dir=config.root_dir,
            source_URL=config.source_URL,
            local_data_file=config.local_data_file,
            unzip_dir=config.unzip_dir
        )
        return data_ingestion_config