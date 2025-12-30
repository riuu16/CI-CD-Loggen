import logging
import os

# Create logs directory if not exists
if not os.path.exists("logs"):
    os.makedirs("logs")

# Logger configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("logs/app.log"),
        logging.StreamHandler()
    ]
)

# Create logger
logger = logging.getLogger("MyLogger")

# Log messages
logger.info("Application started")
logger.warning("This is a warning message")
logger.error("This is an error message")

print("Logging completed. Check logs/app.log")
