from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class EventName(str, Enum):
    START = "start"
    STOP = "stop"


@dataclass
class Event:
    event: EventName
    time: datetime