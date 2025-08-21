# Import required system and logging modules
import os        # For file and directory operations
import sys       # For system-specific parameters and functions
import logging   # For logging functionality

# Define the logging format string
# %(asctime)s - Timestamp of the log
# %(levelname)s - Level of the log (INFO, ERROR, etc.)
# %(module)s - Module where the log originated
# %(message)s - The actual log message
logging_str="[%(asctime)s] %(levelname)s in %(module)s: %(message)s"

# Define the directory where log files will be stored
log_dir="logs"
# Create the full path for the log file by joining directory and filename
log_filepath=os.path.join(log_dir, "logging.log")
# Create the logs directory if it doesn't exist (exist_ok=True prevents errors if directory exists)
os.makedirs(log_dir, exist_ok=True)

# Configure the basic logging settings
# level=logging.INFO - Set logging level to INFO (will log all INFO, WARNING, ERROR, and CRITICAL messages)
# format=logging_str - Use the format string defined above
# handlers - Define where the logs should be output:
#   - FileHandler: Write logs to the specified file
#   - StreamHandler: Also write logs to standard output (console)
logging.basicConfig(level=logging.INFO, format=logging_str, handlers=[
    logging.FileHandler(log_filepath),
    logging.StreamHandler(sys.stdout)
])

# Create a logger instance with a custom name for this project
# This logger can be imported and used by other modules in the project
logger = logging.getLogger("datasciencelogger")