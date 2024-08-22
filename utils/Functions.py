import logging


def create_logger(filename: str) -> logging.Logger:
    logger = logging.getLogger(filename)
    if not logger.handlers:
        handler = logging.FileHandler(
            filename=f'logs/{filename}.log', encoding='utf-8', mode='w')
        handler.setLevel(logging.DEBUG)
        logger.addHandler(handler)
        logger.setLevel(logging.DEBUG)
    return logger
