import logging
from logging.handlers import RotatingFileHandler

# Настраиваем логгер (независимо от Flask)
logger = logging.getLogger('rekbot')
logger.setLevel(logging.INFO)

file_handler = RotatingFileHandler(
    'logs/rekbot.log',
    maxBytes=5242880,
    backupCount=10
)
file_handler.setFormatter(logging.Formatter(
    '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]',
    datefmt='%d-%m-%Y %H:%M:%S'
))
file_handler.setLevel(logging.INFO)

logger.addHandler(file_handler)
