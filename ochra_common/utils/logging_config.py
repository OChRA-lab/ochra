import logging

# Filter to allow INFO level only
class InfoPassFilter(logging.Filter):
    def filter(self, record):
        return record.levelno == logging.INFO