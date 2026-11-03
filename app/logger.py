import logging

logging.basicConfig(
    level=logging.INFO,
)

logger = logging.getLogger(
    "nfl_dashboard"
)
from app.logger import logger

logger.info(
    "Training completed"
)