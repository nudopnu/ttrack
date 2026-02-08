from datetime import timedelta, datetime
from dataclasses import dataclass

from ttrack.event import EventType


@dataclass
class TrackerInfo:
    totalDuration: timedelta

    @classmethod
    def from_events(events: list[tuple[EventType, datetime]]):
        events_before_today = []
        events_today = []
        today = datetime.today()

        for event, time in event:
            if time < today:
                events_before_today.append((event, time))
            else:
                events_today.append((event, time))
        for event, time in events_today:
            
