import logging
import os

# Log configuration
logger = logging.getLogger("ELFBot")
logger.setLevel(os.getenv("LOG_LEVEL", "INFO"))

# Telegram bot configuration
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    logging.error(
        "BOT_TOKEN env var is not found, cannot start the bot without it, create it with @BotFather Telegram bot! "
    )
else:
    logging.info("BOT_TOKEN found, starting the bot")

# Model configuration
DEFAULT_MODEL_NAME = "LGBMClassifier"
MODEL_NAME = os.getenv("MODEL_NAME")
if not MODEL_NAME:
    MODEL_NAME = DEFAULT_MODEL_NAME
    logging.info(f"MODEL_NAME env var is not found, using default model {MODEL_NAME}")
else:
    logging.info(f"MODEL_NAME is {MODEL_NAME}")

# tmp file location
TMP_FILE_LOCATION= "./tools/TG_bot/tests/testout.o"


# docker configuration
FROM_DOCKER = os.getenv("FROM_DOCKER")
if not FROM_DOCKER:
    logging.info("Running locally")
    FROM_DOCKER = False
else:
    logging.info("Running from inside Docker")
    FROM_DOCKER = True
