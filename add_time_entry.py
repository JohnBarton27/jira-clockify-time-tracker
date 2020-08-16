import argparse

parser = argparse.ArgumentParser(description="Add time entry to Jira")
parser.add_argument("start_time", help="Start time of time entry [format: YYYY-MM-DDTHH:MM:SSZ]")
parser.add_argument("end_time", help="End time of time entry [format: YYYY-MM-DDTHH:MM:SSZ]")
parser.add_argument("description", help="Description of the time entry (used to determine Jira issue key)")

args = parser.parse_args()

