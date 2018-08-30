import logging
from .bot import VkBot


# FIXME: Make logging optional.
logging.basicConfig(
    level=logging.DEBUG,
    format="%(relativeCreated)6d %(threadName)s %(levelname)s: %(message)s"
)
