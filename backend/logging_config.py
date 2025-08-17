import logging
from pathlib import Path

# Ensure logs directory exists
LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

LOG_FILE = LOG_DIR / "app.log"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] [%(name)s] %(message)s",
    handlers=[
        logging.StreamHandler(),               # console
        logging.FileHandler(LOG_FILE, "a", "utf-8"),  # file
    ],
)

# Convenience logger
logger = logging.getLogger("finance_agent")
