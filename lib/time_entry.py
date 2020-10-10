from datetime import datetime, timedelta
import pytz
import re

from lib.exceptions import NoJiraKayFoundException
from lib.api_call import RequestTypes
from lib.clockify_api_call import ClockifyApiCall
from lib.jira_api_call import JiraApiCall
from lib.workspace import Workspace


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

    def __str__(self):
        return self.description

    def __repr__(self):
        return self.description

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
        
        if TimeEntry._entry_with_description_exists(self.description, self.jira_key):
            print(f"Found an existing TimeEntry with duplicate description ({self.description}). Skipping this Entry.")
            return

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
    def _entry_with_description_exists(description: str, jira_key: str):
        all_entries = TimeEntry.get_all_from_jira(jira_key)

        return any(te.description == description for te in all_entries)

    @staticmethod
    def get_from_json(json: dict):
        """
        Given a JSON representation of a TimeEntry (usually, from the Jira REST API), return the TimeEntry object.

        Args:
            json (dict): JSON containing all necessary pieces of a TimeEntry

        Returns:
            TimeEntry: TimeEntry object based on the given JSON
        """
        start_str = json["started"]
        description = TimeEntry._get_description_from_json(json["comment"])
        duration = json["timeSpentSeconds"]

        start = datetime.strptime(start_str, "%Y-%m-%dT%H:%M:%S.000-0400")
        end = start + timedelta(seconds=duration)

        return TimeEntry(start, end, description)

    @staticmethod
    def _get_description_from_json(comment_json):
        text_list = comment_json["content"][0]["content"][0]["text"]

        return "".join(text_list)

    @staticmethod
    def get_all_from_jira(jira_key: str):
        """
        Get all existing TimeEntries from Jira
        Args:
            jira_key (str): Key of the Jira issue to get all Time Entries for

        Returns:
            list: List of TimeEntry objects
        """
        url = "rest/api/3/issue/{}/worklog".format(jira_key)
        response = JiraApiCall(RequestTypes.GET, url).exec()
        json_entries = response.json()["worklogs"]
        entries = []

        for json_entry in json_entries:
            entries.append(TimeEntry.get_from_json(json_entry))
        return entries

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
        # TODO add support for multiple Workspaces
        workspace = Workspace.get_all()[0]

        current_time = datetime.now().astimezone(pytz.utc)

        data = {
            "start": current_time.strftime("%Y-%m-%dT%H:%M:%SZ")
        }

        response = ClockifyApiCall(RequestTypes.POST, "workspaces/{}/time-entries".format(workspace.id), data=data)\
            .exec().json()
        return response
