from datetime import datetime
import pytz
import re

from lib.exceptions import NoJiraKayFoundException
from lib.jira_api_call import JiraApiCall
from lib.api_call import RequestTypes
from lib.variable import Variable


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

    @property
    def worklog_comment(self):
        comment = {
            "version": 1,
            "type": "doc",
            "content": [
                {
                    "type": "paragraph",
                    "content": [
                        {
                            "type": "text",
                            "text": self.description
                        }
                    ]
                }
            ]
        }
        return comment

    def add_to_jira(self):
        """
        Adds this TimeEntry to its associated Jira issue.
        """
        if not self.jira_key:
            raise NoJiraKayFoundException("No Jira key associated with this TimeEntry, "
                                          "so it will not be added to Jira.")

        url = "rest/api/3/issue/{}/worklog".format(self.jira_key)
        localized_start = pytz.utc.localize(self.start)
        data = {
            "started": TimeEntry.time_format(localized_start),
            "timeSpentSeconds": self.duration.seconds,
            "comment": self.worklog_comment
        }
        response = JiraApiCall(RequestTypes.POST, url, data=data).exec()
        return response

    @staticmethod
    def time_format(dt):
        return "%s:%.3f%s" % (
            dt.strftime('%Y-%m-%dT%H:%M'),
            float("%.3f" % (dt.second + dt.microsecond / 1e6)),
            dt.strftime('%z')
        )

    @staticmethod
    def start_clockify_timer():
        """
        Starts a new Clockify Time Entry
        """
        clockify_api_token = Variable("CLOCKIFY_API_TOKEN")
