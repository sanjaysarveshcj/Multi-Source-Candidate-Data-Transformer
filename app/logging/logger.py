import logging
from pathlib import Path

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

LOG_FILE = LOG_DIR / "application.log"

logger = logging.getLogger("candidate_transformer")

logger.setLevel(logging.INFO)

formatter = logging.Formatter(
    "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)

########################################
# File Handler
########################################

file_handler = logging.FileHandler(LOG_FILE)

file_handler.setFormatter(formatter)

########################################
# Console Handler
########################################

console_handler = logging.StreamHandler()

console_handler.setFormatter(formatter)

########################################

if not logger.handlers:

    logger.addHandler(file_handler)

    logger.addHandler(console_handler)