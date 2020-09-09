import unittest

from lib.clockify_user import ClockifyUser


class TestClockifyUser(unittest.TestCase):

    def test_init(self):
        """ClockifyUser.__init__"""
        user = ClockifyUser("Username", "123abc")

        self.assertEqual(user.name, "Username")
        self.assertEqual(user.id, "123abc")

    def test_str(self):
        """ClockifyUser.__str__"""
        user = ClockifyUser("Username", "123abc")

        self.assertEqual(str(user), "Username")

    def test_repr(self):
        """ClockifyUser.__repr__"""
        user = ClockifyUser("Username", "123abc")

        self.assertEqual(repr(user), "Username")

    def test_eq_equal(self):
        """ClockifyUser.__eq__.equal"""
        user1 = ClockifyUser("Username", "123abc")
        user2 = ClockifyUser("Username", "123abc")

        self.assertEqual(user1, user2)

    def test_eq_diff_ids(self):
        """ClockifyUser.__eq__.diff_ids"""
        user1 = ClockifyUser("Username", "123abc")
        user2 = ClockifyUser("Username", "def456")

        self.assertNotEqual(user1, user2)

    def test_hash(self):
        """ClockifyUser.__hash__"""
        user = ClockifyUser("Username", "123abc")

        self.assertEqual(hash(user), hash("123abc"))


if __name__ == '__main__':
    import xmlrunner
    unittest.main(testRunner=xmlrunner.XMLTestRunner(output='test-reports'))
