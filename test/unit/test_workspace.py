import unittest
from unittest.mock import call, patch, MagicMock

from lib.workspace import Workspace


class TestWorkspace(unittest.TestCase):

    def setUp(self) -> None:
        clockify_api_exec_patch = patch("lib.workspace.ClockifyApiCall.exec")
        self.m_clockify_api_exec = clockify_api_exec_patch.start()
        self.addCleanup(clockify_api_exec_patch.stop)

    def test_init(self):
        """Workspace.__init__"""
        ws = Workspace("My Workspace", "123abc")

        self.assertEqual(ws.name, "My Workspace")
        self.assertEqual(ws.id, "123abc")

    def test_str(self):
        """Workspace.__str__"""
        ws = Workspace("My Workspace", "123abc")

        self.assertEqual(str(ws), "My Workspace")

    def test_repr(self):
        """Workspace.__repr__"""
        ws = Workspace("My Workspace", "123abc")

        self.assertEqual(repr(ws), "My Workspace")

    def test_eq_equal(self):
        """Workspace.__eq__.equal"""
        ws1 = Workspace("My Workspace", "123abc")
        ws2 = Workspace("My Workspace", "123abc")

        self.assertEqual(ws1, ws2)

    def test_eq_diff_ids(self):
        """Workspace.__eq__.diff_ids"""
        ws1 = Workspace("My Workspace", "123abc")
        ws2 = Workspace("My Workspace", "def456")

        self.assertNotEqual(ws1, ws2)

    def test_hash(self):
        """Workspace.__hash__"""
        ws = Workspace("My Workspace", "123abc")

        self.assertEqual(hash(ws), hash("123abc"))

    @patch("lib.workspace.Workspace._get_from_json")
    def test_get_all(self, m_from_json):
        """Workspace.get_all"""
        response = MagicMock()
        self.m_clockify_api_exec.return_value = response
        response.json.return_value = [
            {"name": "WS1"},
            {"name": "WS2"}
        ]

        ws1 = MagicMock()
        ws2 = MagicMock()
        m_from_json.side_effect = [ws1, ws2]

        workspaces = Workspace.get_all()

        m_from_json.assert_has_calls([call({"name": "WS1"}), call({"name": "WS2"})], any_order=True)

        self.assertEqual(len(workspaces), 2)
        self.assertTrue(ws1 in workspaces)
        self.assertTrue(ws2 in workspaces)

    def test_get_from_json(self):
        """Workspace._get_from_json"""
        json = {
            "name": "My Workspace",
            "id": "123abc"
        }

        ws = Workspace._get_from_json(json)

        self.assertEqual(ws.name, "My Workspace")
        self.assertEqual(ws.id, "123abc")

if __name__ == '__main__':
    import xmlrunner
    unittest.main(testRunner=xmlrunner.XMLTestRunner(output='test-reports'))
