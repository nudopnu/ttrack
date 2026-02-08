from argparse import ArgumentParser, Namespace
from pathlib import Path
from datetime import timedelta

from ttrack.tracker import Tracker
from ttrack.timespan import Timespan


def main():
    tracker = Tracker()
    
    def start(args: Namespace):
        data_dir = args.data_dir
        name = args.name
        tracker.set_database(data_dir)
        tracker.start(name)

    def stop(args: Namespace):
        data_dir = args.data_dir
        name = args.name
        tracker.set_database(data_dir)
        tracker.stop(name)

    def list(args: Namespace):
        data_dir = args.data_dir
        name = args.name
        tracker.set_database(data_dir)
        events = tracker.get_events(name)
        for event in events:
            print(f"{event.event}\t{event.time}")
    
    def summary(args: Namespace):
        data_dir = args.data_dir
        name = args.name
        tracker.set_database(data_dir)
        events = tracker.get_events(name)        
        spans = Timespan.from_events(events)
        total_duration = sum((span.duration() for span in spans), start=timedelta(0))
        duration_today= sum((span.duration() for span in spans if span.started_today()), start=timedelta(0))
        print(f"Total duration:\t{total_duration}")
        print(f"Duration today:\t{duration_today}")


    parser = ArgumentParser()
    parser.add_argument("-dd", "--data-dir", type=Path, default=Path.home() / "ttrack", help="Directory for persistent application data (default: ~/ttrack)")
    subparsers = parser.add_subparsers(dest="command", required=True)

    start_parser = subparsers.add_parser("start", help="Start a timer")
    start_parser.add_argument("name", help="The name of the timer")
    start_parser.set_defaults(func=start)

    stop_parser = subparsers.add_parser("stop", help="Stop a timer")
    stop_parser.add_argument("name", help="The name of the timer")
    stop_parser.set_defaults(func=stop)

    list_parser = subparsers.add_parser("list", help="List all events of a timer")
    list_parser.add_argument("name", help="The name of the timer")
    list_parser.set_defaults(func=list)

    summary_parser = subparsers.add_parser("summary", help="Prints out a summary of given timer")
    summary_parser.add_argument("name", help="The name of the timer")
    summary_parser.set_defaults(func=summary)

    return parser.parse_args()

if __name__ == "__main__":
    args = main()
    args.func(args)
