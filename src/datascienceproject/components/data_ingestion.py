import os
import urllib.request as request
from src.datascienceproject import logger
import zipfile
from src.datascienceproject.entity.config_entity import (DataIngestionConfig)

class DataIngestion:
    def __init__(self, config: DataIngestionConfig):
        self.config = config
    
    def verify_zip_file(self, file_path: str) -> bool:
        """
        Verify if the file is a valid ZIP file
        """
        try:
            with open(file_path, 'rb') as f:
                # Check ZIP file signature (PK\x03\x04)
                is_zip = f.read(4).startswith(b'PK\x03\x04')
                if not is_zip:
                    logger.error(f"File {file_path} does not have a valid ZIP signature")
                return is_zip
        except Exception as e:
            logger.error(f"Error verifying ZIP file: {str(e)}")
            return False
    
    def download_file(self):
        """
        Downloads file from source URL if it doesn't exist locally
        """
        try:
            file_path = str(self.config.local_data_file)
            if not os.path.exists(file_path):
                # Create directory if it doesn't exist
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                
                logger.info(f"Downloading from {self.config.source_URL} to {file_path}")
                filename, headers = request.urlretrieve(
                    url=self.config.source_URL,
                    filename=file_path
                )
                logger.info(f"File downloaded successfully to: {filename}")
                logger.debug(f"Download headers: {headers}")
            
            # Verify the file whether it was just downloaded or existed before
            if not self.verify_zip_file(file_path):
                # If file exists but is invalid, try to download again
                logger.warning("Invalid ZIP file detected, attempting to download again...")
                if os.path.exists(file_path):
                    os.remove(file_path)
                filename, headers = request.urlretrieve(
                    url=self.config.source_URL,
                    filename=file_path
                )
                if not self.verify_zip_file(file_path):
                    raise Exception("Failed to download a valid ZIP file")
            
        except Exception as e:
            logger.error(f"Error downloading file: {str(e)}")
            raise e

    def extract_zip_file(self):
        """
        Extracts the zip file into the specified directory
        """
        try:
            file_path = str(self.config.local_data_file)
            unzip_path = str(self.config.unzip_dir)
            
            # Verify zip file before attempting to extract
            if not self.verify_zip_file(file_path):
                raise Exception("Cannot extract: Invalid ZIP file")
            
            os.makedirs(unzip_path, exist_ok=True)
            
            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                # List contents before extracting
                logger.info(f"ZIP file contains: {zip_ref.namelist()}")
                zip_ref.extractall(unzip_path)
            logger.info(f"File extracted successfully to: {unzip_path}")
        except Exception as e:
            logger.error(f"Error extracting file: {str(e)}")
            raise e