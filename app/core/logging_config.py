import logging
from logging.handlers import RotatingFileHandler


def configure_logging():
    logging.basicConfig(level=logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    file_handler = RotatingFileHandler('celery.log', maxBytes=1024 * 1024 * 100, backupCount=20)
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    loggers = logging.getLogger()
    loggers.addHandler(file_handler)
    loggers.addHandler(console_handler)

    return loggers


logger = configure_logging()
