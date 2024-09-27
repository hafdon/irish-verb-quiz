# logging_config.py
import logging
import os
import tempfile

def configure_logging():
    # Get a temporary directory
    temp_dir = tempfile.gettempdir()
    log_file_path = os.path.join(temp_dir, 'app.log')

    # Handle Exceptions When Configuring Logging
    try:
        logging.basicConfig(
            level=logging.DEBUG,  # Set to DEBUG to capture all levels of logs
            format='%(asctime)s - %(levelname)s - %(message)s',
            filename=log_file_path,
            filemode='a'
        )
    except PermissionError as e:
        # If logging to a file fails, log to stderr
        logging.basicConfig(
            level=logging.DEBUG,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        logging.error(f"Failed to write log to {log_file_path}: {e}")