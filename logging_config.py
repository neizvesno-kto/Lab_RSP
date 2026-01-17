import logging
from logging.handlers import RotatingFileHandler

LOG_FORMAT = "%(asctime)s %(levelname)s %(name)s - %(message)s"

handler = RotatingFileHandler(
    "logs/application.log",
    maxBytes=1_000_000,
    backupCount=5,
    encoding="utf-8"
)

logging.basicConfig(
    level=logging.INFO,
    format=LOG_FORMAT,
    handlers=[handler]
)
