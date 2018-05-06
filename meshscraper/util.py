import logging

def convert_to_pid(num):
    """Convert an int to a pid(Product ID)."""
    return format(str(num), '0>6')

def create_logger(logger_name, logger_level=20, log_file_path=None):
    """Configure and return a logger object.

    Args:
        logger_name: Name to give logger object
        logger_level: The logging level to configure the logger with.
        log_file_path: An absolute path to the desired log file.

    Returns:
        logger: A configured logger object.
    """
    logger = logging.getLogger(logger_name)
    logger.setLevel(logger_level)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Console output
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    if log_file_path:
        # File output
        file_handler = logging.FileHandler(log_file_path)
        file_handler.setFormatter(formatter)
        file_handler.setLevel(logging.ERROR)
        logger.addHandler(file_handler)

    return logger
