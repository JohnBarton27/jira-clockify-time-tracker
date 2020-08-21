from datetime import datetime, timedelta
import unittest

from time_entry import TimeEntry


class TestTimeEntry(unittest.TestCase):

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


if __name__ == '__main__':
    import xmlrunner
    unittest.main(testRunner=xmlrunner.XMLTestRunner(output='test-reports'))
