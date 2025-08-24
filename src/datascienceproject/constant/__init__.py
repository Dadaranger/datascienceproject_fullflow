from pathlib import Path
import os

# Get the project root directory
ROOT_DIR = Path(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

# Define config paths relative to root directory
CONFIG_FILE_PATH = ROOT_DIR / "configs" / "config.yaml"
PARAMS_FILE_PATH = ROOT_DIR / "params.yaml"
SCHEMA_FILE_PATH = ROOT_DIR / "schema.yaml"