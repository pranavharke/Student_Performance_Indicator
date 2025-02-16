import logging, os
from datetime import datetime

# This file is responsible for setting up logging mechanism to track events, errors, and important runtime details
# Helps track errors, debug issues, and analyze behavior

# Create File path and file name current datetime format
LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"
# Define the path where logs will be stored (current working directory)
logs_Path = os.path.join(os.getcwd(), "logs", LOG_FILE)
# Ensure the logs directory exists; if not, create it
os.makedirs(logs_Path, exist_ok=True)

LOG_FILE_PATH = os.path.join(logs_Path, LOG_FILE)

logging.basicConfig(
    filename=LOG_FILE_PATH,
    # Defining log format (timestatmp lineno filename - levelname - errormessage)
    format="[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s",
    # Log level set to INFO for getting logs without overwhelming the logs with debugging details
    level=logging.INFO,
)


