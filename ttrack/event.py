from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class EventType(Enum):
    START = "start"
    STOP = "stop"


@dataclass
class Event:
    type: EventType
    time: datetime