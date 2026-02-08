from argparse import ArgumentParser, Namespace
from pathlib import Path

from ttrack.tracker import Tracker

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
        events = tracker.parse_events(name)
        for event, time in events:
            print(f"{event.value}\t{time}")
    
    def info(args: Namespace):
        data_dir = args.data_dir
        name = args.name
        tracker.set_database(data_dir)
        events = tracker.parse_events(name)        


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

    return parser.parse_args()

if __name__ == "__main__":
    args = main()
    args.func(args)
