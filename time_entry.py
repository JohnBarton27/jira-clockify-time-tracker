from datetime import datetime
import re


class TimeEntry:

    def __init__(self, start: datetime, end: datetime, description: str):
        """
        Constructor for TimeEntry

        Args:
            start (datetime): Start of the TimeEntry
            end (datetime): End of the TimeEntry
            description (str): Description of the TimeEntry (should include a Jira key for mapping to a Jira issue)
        """
        self.start = start
        self.end = end
        self.description = description

    @property
    def duration(self):
        """
        Gets the duration (length) of this TimeEntry, as a timedelta

        Returns:
            timedelta: Duration of this time entry
        """
        return self.end - self.start

    @property
    def jira_key(self):
        """
        Gets the key of the first Jira issue associated with this TimeEntry, if there is one.

        Returns:
            str: Jira key associated with this TimeEntry
        """
        key = re.search(r'((([A-Z]{1,10})-?)[A-Z]+-\d+)', self.description)

        if not key:
            return None

        return key.group(1)
