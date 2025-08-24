import os
from src.datascienceproject import logger
from src.datascienceproject.entity.config_entity import (DataValidationConfig)
import pandas as pd
from pathlib import Path

class DataValiadtion:
    def __init__(self, config: DataValidationConfig):
        self.config = config
        # Create the directory for status file if it doesn't exist
        #create_directories([Path(self.config.root_dir)])

    def validate_all_columns(self)-> bool:
        try:
            validation_status = True
            validation_message = []

            # Read CSV with proper separator
            data = pd.read_csv(self.config.unzip_data_dir, sep=";")
            all_cols = list(data.columns)
            all_schema = self.config.all_schema.keys()

            # Check for missing columns
            missing_cols = set(all_schema) - set(all_cols)
            if missing_cols:
                validation_status = False
                validation_message.append(f"Missing columns: {missing_cols}")

            # Check for extra columns
            extra_cols = set(all_cols) - set(all_schema)
            if extra_cols:
                validation_status = False
                validation_message.append(f"Extra columns: {extra_cols}")

            # Check data types
            for col in all_cols:
                if col in all_schema:
                    expected_type = self.config.all_schema[col]
                    actual_type = str(data[col].dtype)
                    if expected_type != actual_type:
                        validation_status = False
                        validation_message.append(f"Type mismatch for '{col}': expected {expected_type}, got {actual_type}")

            # Write validation status and details
            with open(self.config.STATUS_FILE, 'w') as f:
                f.write(f"Validation status: {validation_status}\n")
                if validation_message:
                    f.write("\nValidation details:\n")
                    f.write("\n".join(validation_message))

            return validation_status
        
        except Exception as e:
            logger.error(f"Error occurred during data validation: {e}")
            raise e