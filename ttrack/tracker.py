import csv
import logging
from datetime import datetime
from pathlib import Path

from ttrack.event import EventType


logger = logging.getLogger(__name__)


class Tracker:

    def set_database(self, location: Path):
        self.db_location = location
        location.mkdir(parents=True, exist_ok=True)
    
    def start(self, name: str):
        last_event, time = self.parse_last_event(name)
        if last_event and last_event == EventType.START:
            logger.error(f"Timer '{name}' already started at {time}")
            return None
        logger.info(f"Starting timer {name}")
        self.write_event(name, EventType.START, datetime.now())
    
    def stop(self, name: str):
        last_event, time = self.parse_last_event(name)
        if not last_event or last_event == EventType.STOP:
            logger.error(f"Timer '{name}' hasn't started yet")
            return None
        logger.info(f"Stopping time {name}")
        self.write_event(name, EventType.STOP, datetime.now())
    
    def info(self, name: str):
        file_path = self.db_location / f"{name}.csv"
        if not file_path.exists():
            return None
    
    def write_event(self, name: str, event: EventType, time: datetime):
        file_path = self.db_location / f"{name}.csv"
        write_header = not file_path.exists()
        with open(file_path, "a", newline="", encoding="utf8") as file:
            writer = csv.DictWriter(file, fieldnames=["event", "time"])
            if write_header:
                writer.writeheader()
            writer.writerow({"event": event.value, "time": time.isoformat()})
    
    def parse_events(self, name: str) -> list[tuple[EventType, datetime]]:
        file_path = self.db_location / f"{name}.csv"

        if not file_path.exists():
            return []

        events: list[tuple[EventType, datetime]] = []
        with open(file_path, newline="", encoding="utf8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                events.append((EventType(row["event"]), datetime.fromisoformat(row["time"])))
        return events
    
    def parse_last_event(self, name: str) -> tuple[EventType, datetime] | None:
        file_path = self.db_location / f"{name}.csv"

        if not file_path.exists():
            return None

        with open(file_path, "rb") as f:
            f.seek(0, 2)  # move to end
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

        # decode and parse CSV row
        row = next(csv.DictReader(
            [line.decode("utf8")],
            fieldnames=["event", "time"],
        ))

        return EventType(row["event"]), datetime.fromisoformat(row["time"])
    