import argparse
from datetime import datetime

from lib.time_entry import TimeEntry

parser = argparse.ArgumentParser(description="Add time entry to Jira")
parser.add_argument("start_time", help="Start time of time entry [format: YYYY-MM-DDTHH:MM:SSZ]")
parser.add_argument("end_time", help="End time of time entry [format: YYYY-MM-DDTHH:MM:SSZ]")
parser.add_argument("description", help="Description of the time entry (used to determine Jira issue key)")

args = parser.parse_args()

# Create TimeEntry Object
start_dt = datetime.strptime(args.start_time, "%Y-%m-%dT%H:%M:%SZ")
end_dt = datetime.strptime(args.end_time, "%Y-%m-%dT%H:%M:%SZ")
te = TimeEntry(start_dt, end_dt, args.description)

# Create TimeEntry in Jira
