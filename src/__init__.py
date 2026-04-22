import logging
import os
from logging.handlers import RotatingFileHandler

os.makedirs("./logs/", exist_ok=True)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


file_handler = RotatingFileHandler("./logs/bot.log", maxBytes=1_000_000, backupCount=5)
file_formatter = logging.Formatter(
    "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)

console_handler = logging.StreamHandler()
console_handler.setFormatter(file_formatter)
logger.addHandler(console_handler)

logger.info("Bot package initialized successfully.")
