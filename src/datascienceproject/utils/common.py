"""
This module provides utility functions for common file operations in the data science project.
It includes functions for:
1. Reading and parsing YAML configuration files
2. Creating directory structures
3. Handling JSON file operations (save and load)
4. Saving binary files for model artifacts

The module uses:
- ConfigBox for dictionary-like access to configuration
- ensure_annotations for runtime type checking
- logging for operation tracking
- joblib for binary file operations

All functions include error handling and logging for better debugging and monitoring.
"""

# System and file operation imports
import os
from anyio import Path  # For async/sync path operations

# Data handling imports
import yaml  # For YAML file operations
import json  # For JSON file operations
import joblib  # For saving/loading binary files

# Project specific imports
from src.datascienceproject import logger  # Custom logger

# Type checking and data structure imports
from ensure import ensure_annotations  # For runtime type checking
from box import ConfigBox  # For dot notation access to dictionaries
from typing import Any  # For type hinting
from box.exceptions import BoxValueError  # For ConfigBox error handling

# Decorator for runtime type checking
@ensure_annotations  # Ensures type hints are enforced at runtime
def read_yaml(path_to_yaml: str) -> ConfigBox:
    """
    Reads a YAML file and returns its contents as a dictionary.

    Args:
        path_to_yaml (str): path to the YAML file to read.

    Raises:
        ValueError: If the YAML file is not found or cannot be read.

    Returns:
        ConfigBox: ConfigBox Type that allows dot notation access
    """
    try:
        # Open and read the YAML file using context manager for proper resource handling
        with open(path_to_yaml) as yaml_file:
            # Parse YAML content safely to prevent code execution
            content = yaml.safe_load(yaml_file)
            logger.info(f"YAML file {path_to_yaml} loaded successfully.")
            # Convert to ConfigBox for dot notation access (e.g., config.key instead of config['key'])
            return ConfigBox(content)
    except BoxValueError:
        # Log error and re-raise as ValueError for better error handling
        raise ValueError("yaml file is empty")
    except Exception as e:
        raise e
    
@ensure_annotations
def create_directories(path_to_directories: list, verbose=True):
    """Creates a list of directories if they do not exist.

    Args:
        path_to_directories (list): A list of directory paths to create.
        verbose (bool): Whether to log directory creation messages. Defaults to True.
    """
    # Iterate through each directory path in the list
    for path in path_to_directories:
        # Create directory if it doesn't exist, do nothing if it does
        os.makedirs(path, exist_ok=True)
        # Log directory creation if verbose mode is enabled
        if verbose:
            logger.info(f"created directory at: {path}")

@ensure_annotations
def save_json(path: Path, data: dict):
    """Saves a dictionary to a JSON file.

    Args:
        path (Path): The path where the JSON file will be saved.
        data (dict): The dictionary to save.
    """
    # Open file in write mode and use context manager for proper resource handling
    with open(path, 'w') as json_file:
        # Dump dictionary to JSON with proper indentation for readability
        json.dump(data, json_file, indent=4)
    
    # Log successful save operation
    logger.info(f"JSON file saved at: {path}")

@ensure_annotations
def load_json(path: Path) -> ConfigBox:
    """Loads a JSON file and returns its contents as a ConfigBox object.

    Args:
        path (Path): The path to the JSON file to load.

    Returns:
        ConfigBox: Data as class attributes for dot notation access
    """
    # Open and read JSON file using context manager
    with open(path) as json_file:
        # Parse JSON content into Python dictionary
        content = json.load(json_file)
    
    # Log successful load operation
    logger.info(f"JSON file loaded successfully from: {path}")
    # Convert to ConfigBox for dot notation access
    return ConfigBox(content)

@ensure_annotations
def save_bin(data: Any, path: Path):
    """Save data as a binary file using joblib.

    Args:
        data (Any): Any Python object to be saved as binary (models, arrays, etc.)
        path (Path): Path where the binary file will be saved
    
    Returns:
        Any: Returns the data that was saved
    """
    # Use joblib to save data in binary format (efficient for numpy arrays and scikit-learn models)
    joblib.dump(value=data, filename=path)
    # Log successful save operation
    logger.info(f"Binary file saved at: {path}")
    return data

@ensure_annotations
def load_bin(path: Path) -> Any:
    """load binary data

    Args:
        path (Path): path to binary file

    Returns:
        Any: object stored in the file
    """
    data = joblib.load(path)
    logger.info(f"binary file loaded from: {path}")
    return data