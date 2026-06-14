import logging
import os


class Logger:
    def __init__(self):
        os.makedirs("logs", exist_ok=True)
        logging.basicConfig(
            filename="logs/server.log",
            level=logging.INFO,
            format="%(asctime)s | %(levelname)s | %(message)s"
        )

    def info(self, message):
        logging.info(message)

    def error(self, message):
        logging.error(message)
