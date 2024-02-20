import logging
from typing import NamedTuple
from ..constants import MISSING

class LoggingObject(NamedTuple):

    handler: logging.Handler = MISSING
    formatter: logging.Formatter = MISSING
    level: int = MISSING
    root: bool = True
