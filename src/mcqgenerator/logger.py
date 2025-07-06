import logging
import os
from datetime import datetime

# Always use the project root for logs, regardless of where the script is run from
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


log_path = os.path.join(PROJECT_ROOT, "logs")
os.makedirs(log_path, exist_ok=True)

# Use a fixed log file name for easier debugging
LOG_FILEPATH = os.path.join(log_path, "app.log")

# Remove all handlers associated with the root logger object (for notebook/script reruns)
for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)

logging.basicConfig(
    level=logging.INFO,
    filename=LOG_FILEPATH,
    filemode='a',
    format="[%(asctime)s] %(lineno)d %(name)s - %(levelname)s - %(message)s"
)

# Force a log write and flush to ensure file creation
def ensure_log_file():
    logging.info("Logger initialized and log file should be created.")
    for handler in logging.root.handlers:
        handler.flush()

ensure_log_file()
