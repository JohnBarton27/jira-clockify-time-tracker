from datetime import datetime, timedelta
import pytz
import unittest
from unittest.mock import patch, MagicMock, PropertyMock

from lib.time_entry import TimeEntry
from lib.api_call import RequestTypes


class TestTimeEntry(unittest.TestCase):

    def setUp(self) -> None:
        ws_get_all_patch = patch("lib.time_entry.Workspace.get_all")
        self.m_ws_get_all = ws_get_all_patch.start()
        self.addCleanup(ws_get_all_patch.stop)

        clockify_api_exec_patch = patch("lib.time_entry.ClockifyApiCall.exec")
        self.m_clockify_api_exec = clockify_api_exec_patch.start()
        self.addCleanup(clockify_api_exec_patch.stop)

    def test_init(self):
        """TimeEntry.__init__"""
        start = datetime(year=2020, month=8, day=16, hour=18)
        end = datetime(year=2020, month=8, day=16, hour=18, minute=30)
        description = "TEST-123 I'm doing some work"

        te = TimeEntry(start, end, description)

        self.assertEqual(te.start, start)
        self.assertEqual(te.end, end)
        self.assertEqual(te.description, description)

    def test_duration(self):
        """TimeEntry.duration"""
        start = datetime(year=2020, month=8, day=16, hour=18)
        end = datetime(year=2020, month=8, day=16, hour=18, minute=30)
        description = "TEST-123 I'm doing some work"

        te = TimeEntry(start, end, description)

        thirty_min = timedelta(minutes=30)
        self.assertEqual(te.duration, thirty_min)

    def test_jira_key_start(self):
        """TimeEntry.jira_key.start"""
        start = datetime(year=2020, month=8, day=16, hour=18)
        end = datetime(year=2020, month=8, day=16, hour=18, minute=30)
        description = "TEST-123 I'm doing some work"

        te = TimeEntry(start, end, description)

        self.assertEqual(te.jira_key, "TEST-123")

    def test_jira_key_middle(self):
        """TimeEntry.jira_key.middle"""
        start = datetime(year=2020, month=8, day=16, hour=18)
        end = datetime(year=2020, month=8, day=16, hour=18, minute=30)
        description = "I'm doing some TEST-123 work"

        te = TimeEntry(start, end, description)

        self.assertEqual(te.jira_key, "TEST-123")

    def test_jira_key_multiple(self):
        """TimeEntry.jira_key.multiple"""
        start = datetime(year=2020, month=8, day=16, hour=18)
        end = datetime(year=2020, month=8, day=16, hour=18, minute=30)
        description = "TEST-123 I'm doing some TEST-124 work"

        te = TimeEntry(start, end, description)

        self.assertEqual(te.jira_key, "TEST-123")

    def test_jira_key_none(self):
        """TimeEntry.jira_key.none"""
        start = datetime(year=2020, month=8, day=16, hour=18)
        end = datetime(year=2020, month=8, day=16, hour=18, minute=30)
        description = "I'm doing some work"

        te = TimeEntry(start, end, description)

        self.assertIsNone(te.jira_key)

    def test_worklog_comment(self):
        """TimeEntry.worklog_comment"""
        start = datetime(year=2020, month=8, day=16, hour=18)
        end = datetime(year=2020, month=8, day=16, hour=18, minute=30)
        description = "I'm doing some work"

        te = TimeEntry(start, end, description)

        correct_wl_comment = {
            "version": 1,
            "type": "doc",
            "content": [
                {
                    "type": "paragraph",
                    "content": [
                        {
                            "type": "text",
                            "text": "I'm doing some work"
                        }
                    ]
                }
            ]
        }
        wl_comment = te.worklog_comment

        self.assertEqual(wl_comment, correct_wl_comment)

    @patch("lib.time_entry.TimeEntry.worklog_comment", new_callable=PropertyMock)
    @patch("lib.time_entry.TimeEntry.jira_key", new_callable=PropertyMock)
    @patch("lib.time_entry.TimeEntry.time_format")
    @patch("lib.time_entry.JiraApiCall.exec")
    @patch("lib.time_entry.JiraApiCall.__init__")
    def test_add_to_jira(self, m_jac_init, m_exec, m_time_format, m_jira_key, m_wlog_comment):
        """TimeEntry.add_to_jira"""
        start = datetime(year=2020, month=8, day=16, hour=18)
        end = datetime(year=2020, month=8, day=16, hour=18, minute=30)
        description = "TEST-123 I'm doing some work"

        te = TimeEntry(start, end, description)

        m_time_format.return_value = "2020-08-16"
        m_jac_init.return_value = None
        m_exec.return_value = MagicMock()
        m_jira_key.return_value = "TEST-123"
        m_wlog_comment.return_value = "COMMENT"

        correct_data = {
            "started": "2020-08-16",
            "timeSpentSeconds": 1800,
            "comment": "COMMENT"
        }

        response = te.add_to_jira()

        m_time_format.assert_called_with(pytz.utc.localize(start))
        m_jac_init.assert_called_with(RequestTypes.POST, "rest/api/3/issue/TEST-123/worklog", data=correct_data)
        m_exec.assert_called()

        self.assertEqual(response, m_exec.return_value)

    def test_time_format(self):
        """TimeEntry.time_format.no_seconds"""
        start = datetime(year=2020, month=8, day=16, hour=18, minute=15, tzinfo=pytz.utc)

        correct_tf = "2020-08-16T18:15:0.000+0000"
        returned_tf = TimeEntry.time_format(start)

        self.assertEqual(returned_tf, correct_tf)

    def test_start_clockify_timer(self):
        """TimeEntry.start_clockify_timer"""
        ws = MagicMock()
        ws.id = 12345
        api_response = MagicMock()
        api_json = MagicMock()
        api_response.json.return_value = api_json

        self.m_ws_get_all.return_value = [ws]
        self.m_clockify_api_exec.return_value = api_response

        returned_val = TimeEntry.start_clockify_timer()

        self.assertEqual(returned_val, api_json)


if __name__ == '__main__':
    import xmlrunner
    unittest.main(testRunner=xmlrunner.XMLTestRunner(output='test-reports'))
