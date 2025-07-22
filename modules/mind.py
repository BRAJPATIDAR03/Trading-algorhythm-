import logging
import sys

def setup_logger():
    """
    Configures and returns a logger instance that writes to both a file
    and the console.
    """
    # Create a logger object with the name of our algorithm
    logger = logging.getLogger('SurferAlgorithm')
    logger.setLevel(logging.INFO) # Set the minimum level of messages to log

    # Prevent duplicate logs if the function is called multiple times
    if logger.hasHandlers():
        logger.handlers.clear()

    # Create a formatter to define the log message structure
    formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - [%(module)s.%(funcName)s] - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Create a file handler to write logs to a file
    file_handler = logging.FileHandler('surfer_activity.log')
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)

    # Create a console handler to print logs to the console
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    # Add the handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger

# Create a single, globally accessible logger instance
LOGGER = setup_logger()