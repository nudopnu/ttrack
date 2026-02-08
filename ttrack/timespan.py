from datetime import datetime, date
from dataclasses import dataclass

from ttrack.event import Event, EventName


@dataclass
class Timespan:
    start_event: Event
    stop_event: Event

    def started_today(self):
        return self.start_event.time.date() == date.today()
    
    def duration(self):
        return self.stop_event.time - self.start_event.time
    
    @classmethod
    def from_events(self, events: list[Event]):
        spans: list[Timespan] = []

        current_start = None
        for event in events:
            if event.event == EventName.START:
                current_start = event
                continue
            if event.event == EventName.STOP:
                assert current_start
                spans.append(Timespan(current_start, event))
                current_start = None
        if current_start:
            spans.append(Timespan(current_start, Event(EventName.STOP, datetime.now())))
        return spans
