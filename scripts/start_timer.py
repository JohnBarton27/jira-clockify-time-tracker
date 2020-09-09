import argparse

from lib.time_entry import TimeEntry

parser = argparse.ArgumentParser(description="Starts the initial Clockify timer")
args = parser.parse_args()

TimeEntry.start_clockify_timer()
