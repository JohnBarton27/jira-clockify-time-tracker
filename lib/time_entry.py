from datetime import datetime
import re

from lib.exceptions import NoJiraKayFoundException
from lib.jira_api_call import JiraApiCall, RequestTypes


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

    def add_to_jira(self):
        """
        Adds this TimeEntry to its associated Jira issue.
        """
        if not self.jira_key:
            raise NoJiraKayFoundException("No Jira key associated with this TimeEntry, "
                                          "so it will not be added to Jira.")

        url = "rest/api/3/issue/{}".format(self.jira_key)
        response = JiraApiCall(RequestTypes.GET, url).exec()
        return response
