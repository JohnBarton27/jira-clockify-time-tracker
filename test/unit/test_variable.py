import unittest
from unittest.mock import patch

from lib.variable import Variable


class TestVariable(unittest.TestCase):

    def setUp(self) -> None:
        getenv_patch = patch("lib.variable.os.getenv")
        self.m_getenv = getenv_patch.start()
        self.addCleanup(getenv_patch.stop)

    def test_init_minimal(self):
        """Variable.__init__.minimal"""
        v = Variable("home")

        self.assertEqual(v.name, "home")
        self.assertIsNone(v._value)

    def test_init_with_value(self):
        """Variable.__init__.with_value"""
        v = Variable("home", "~")

        self.assertEqual(v.name, "home")
        self.assertEqual(v._value, "~")

    def test_str(self):
        """Variable.__str__"""
        v = Variable("home")

        self.assertEqual(str(v), "home")

    def test_repr(self):
        """Variable.__repr__"""
        v = Variable("home")

        self.assertEqual(repr(v), "home")

    def test_eq_equal(self):
        """Variable.__eq__.equal"""
        v1 = Variable("home")
        v2 = Variable("home")

        self.assertEqual(v1, v2)

    def test_eq_neq(self):
        """Variable.__eq__.neq"""
        v1 = Variable("home")
        v2 = Variable("HOME")

        self.assertNotEqual(v1, v2)

    def test_hash(self):
        """Variable.__hash__"""
        v = Variable("home")

        self.assertEqual(hash(v), hash("home"))

    def test_value_populated(self):
        """Variable.value.populated"""
        v = Variable("home", "~")

        self.assertEqual(v.value, "~")
        self.m_getenv.assert_not_called()

    def test_value_unpopulated(self):
        """Variable.value.unpopulated"""
        v = Variable("home")

        self.m_getenv.return_value = "~"

        self.assertEqual(v.value, "~")
        self.m_getenv.assert_called_with("home")

    def test_value_unpopulated_not_set(self):
        """Variable.value.unpopulated_not_set"""
        v = Variable("home")

        self.m_getenv.return_value = None

        self.assertIsNone(v.value)
        self.m_getenv.assert_called_with("home")


if __name__ == '__main__':
    import xmlrunner
    unittest.main(testRunner=xmlrunner.XMLTestRunner(output='test-reports'))
