import csv
import logging
from datetime import datetime
from pathlib import Path
from dataclasses import asdict

from ttrack.event import Event, EventName
from ttrack.timespan import Timespan


logger = logging.getLogger(__name__)


class Tracker:

    def set_database(self, location: Path):
        self.db_location = location
        location.mkdir(parents=True, exist_ok=True)
    
    def start(self, name: str):
        last_event = self.parse_last_event(name)
        if last_event and last_event.event == EventName.START:
            logger.error(f"Timer '{name}' already started at {last_event.time}")
            return
        logger.info(f"Starting timer {name}")
        self.write_event(name, Event(EventName.START, datetime.now()))
    
    def stop(self, name: str):
        last_event = self.parse_last_event(name)
        if last_event is None:
            logger.error(f"Timer '{name}' hasn't started yet")
            return
        if last_event.event == EventName.STOP:
            logger.error(f"Timer '{name}' already stopped at {last_event.time}")
            return
        logger.info(f"Stopping time {name}")
        self.write_event(name, Event(EventName.STOP, datetime.now()))
    
    def info(self, name: str):
        file_path = self.db_location / f"{name}.csv"
        if not file_path.exists():
            return None
    
    def write_event(self, name: str, event: Event):
        file_path = self.db_location / f"{name}.csv"
        write_header = not file_path.exists()
        with open(file_path, "a", newline="", encoding="utf8") as file:
            writer = csv.DictWriter(file, fieldnames=["event", "time"])
            if write_header:
                writer.writeheader()
            writer.writerow(asdict(event))
    
    def get_events(self, name: str) -> list[Event]:
        file_path = self.db_location / f"{name}.csv"
        if not file_path.exists():
            return []

        events: list[Event] = []
        with open(file_path, newline="", encoding="utf8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                events.append(Event.from_csv_row(row))
        return events
    
    def parse_last_event(self, name: str) -> Event | None:
        file_path = self.db_location / f"{name}.csv"

        if not file_path.exists():
            return None

        with open(file_path, "rb") as f:
            f.seek(0, 2)
            pos = f.tell()

            if pos == 0:
                return None

            line = b""
            while pos > 0:
                pos -= 1
                f.seek(pos)
                byte = f.read(1)
                if byte == b"\n" and line:
                    break
                line = byte + line

        decoded = line.decode("utf8").strip()

        # reject header-only or empty last line
        if not decoded or decoded == "event,time":
            return None

        row = next(csv.DictReader(
            [decoded],
            fieldnames=["event", "time"],
        ))

        return Event.from_csv_row(row)
