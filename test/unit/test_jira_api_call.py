from requests.auth import HTTPBasicAuth
import unittest
from unittest.mock import MagicMock, patch, PropertyMock

from lib.jira_api_call import JiraApiCall
from lib.api_call import RequestTypes
from lib.exceptions import JiraEmailNotSetException, JiraApiTokenNotSetException, JiraHostnameNotSetException


class TestJiraApiCall(unittest.TestCase):

    def setUp(self) -> None:
        var_value_patch = patch("lib.variable.Variable.value", new_callable=PropertyMock)
        self.m_var_value = var_value_patch.start()
        self.addCleanup(var_value_patch.stop)

    def test_init_no_data(self):
        """JiraApiCall.__init__.no_data"""
        api_call = JiraApiCall(RequestTypes.GET, "sample")

        self.assertEqual(api_call.type, RequestTypes.GET)
        self.assertEqual(api_call.url, "sample")
        self.assertIsNone(api_call.data)

    def test_init_with_data(self):
        """JiraApiCall.__init__.with_data"""
        api_call = JiraApiCall(RequestTypes.POST, "sample", data={"name": "John"})

        self.assertEqual(api_call.type, RequestTypes.POST)
        self.assertEqual(api_call.url, "sample")
        self.assertEqual(api_call.data, {"name": "John"})

    def test_jira_email(self):
        """JiraApiCall.jira_email"""
        api_call = JiraApiCall(RequestTypes.GET, "sample")
        self.m_var_value.return_value = "test@mycf.co"

        self.assertEqual(api_call.jira_email, "test@mycf.co")

    def test_jira_token(self):
        """JiraApiCall.jira_token"""
        api_call = JiraApiCall(RequestTypes.GET, "sample")
        self.m_var_value.return_value = "abc123"

        self.assertEqual(api_call.jira_email, "abc123")

    def test_jira_hostname(self):
        """JiraApiCall.jira_hostname"""
        api_call = JiraApiCall(RequestTypes.GET, "sample")
        self.m_var_value.return_value = "mediayoucanfeel.atlassian.net"

        self.assertEqual(api_call.jira_email, "mediayoucanfeel.atlassian.net")

    @patch("lib.jira_api_call.JiraApiCall.jira_hostname", new_callable=PropertyMock)
    @patch("lib.jira_api_call.JiraApiCall.jira_token", new_callable=PropertyMock)
    @patch("lib.jira_api_call.JiraApiCall.jira_email", new_callable=PropertyMock)
    def test_validate_environment_valid(self, m_jira_email, m_jira_token, m_jira_hostname):
        """JiraApiCall.validate_environment.valid"""
        api_call = JiraApiCall(RequestTypes.GET, "sample")

        m_jira_email.return_value = "test@mycf.co"
        m_jira_token.return_value = "abc123"
        m_jira_hostname.return_value = "mycf.atlassian.net"

        api_call.validate_environment()

        m_jira_email.assert_called()
        m_jira_token.assert_called()
        m_jira_hostname.assert_called()

    @patch("lib.jira_api_call.JiraApiCall.jira_hostname", new_callable=PropertyMock)
    @patch("lib.jira_api_call.JiraApiCall.jira_token", new_callable=PropertyMock)
    @patch("lib.jira_api_call.JiraApiCall.jira_email", new_callable=PropertyMock)
    def test_validate_environment_no_email(self, m_jira_email, m_jira_token, m_jira_hostname):
        """JiraApiCall.validate_environment.no_email"""
        api_call = JiraApiCall(RequestTypes.GET, "sample")

        m_jira_email.return_value = None
        m_jira_token.return_value = "abc123"
        m_jira_hostname.return_value = "mycf.atlassian.net"

        self.assertRaises(JiraEmailNotSetException, api_call.validate_environment)

        m_jira_email.assert_called()
        m_jira_token.assert_not_called()
        m_jira_hostname.assert_not_called()

    @patch("lib.jira_api_call.JiraApiCall.jira_hostname", new_callable=PropertyMock)
    @patch("lib.jira_api_call.JiraApiCall.jira_token", new_callable=PropertyMock)
    @patch("lib.jira_api_call.JiraApiCall.jira_email", new_callable=PropertyMock)
    def test_validate_environment_no_token(self, m_jira_email, m_jira_token, m_jira_hostname):
        """JiraApiCall.validate_environment.no_token"""
        api_call = JiraApiCall(RequestTypes.GET, "sample")

        m_jira_email.return_value = "test@mycf.co"
        m_jira_token.return_value = None
        m_jira_hostname.return_value = "mycf.atlassian.net"

        self.assertRaises(JiraApiTokenNotSetException, api_call.validate_environment)

        m_jira_email.assert_called()
        m_jira_token.assert_called()
        m_jira_hostname.assert_not_called()

    @patch("lib.jira_api_call.JiraApiCall.jira_hostname", new_callable=PropertyMock)
    @patch("lib.jira_api_call.JiraApiCall.jira_token", new_callable=PropertyMock)
    @patch("lib.jira_api_call.JiraApiCall.jira_email", new_callable=PropertyMock)
    def test_validate_environment_no_hostname(self, m_jira_email, m_jira_token, m_jira_hostname):
        """JiraApiCall.validate_environment.no_hostname"""
        api_call = JiraApiCall(RequestTypes.GET, "sample")

        m_jira_email.return_value = "test@mycf.co"
        m_jira_token.return_value = "abc123"
        m_jira_hostname.return_value = None

        self.assertRaises(JiraHostnameNotSetException, api_call.validate_environment)

        m_jira_email.assert_called()
        m_jira_token.assert_called()
        m_jira_hostname.assert_called()

    @patch("lib.jira_api_call.JiraApiCall.jira_hostname", new_callable=PropertyMock)
    @patch("lib.jira_api_call.JiraApiCall.jira_token", new_callable=PropertyMock)
    @patch("lib.jira_api_call.JiraApiCall.jira_email", new_callable=PropertyMock)
    @patch("requests.get")
    @patch("lib.jira_api_call.JiraApiCall.validate_environment")
    def test_exec(self, m_val_env, m_get, m_jira_email, m_jira_token, m_jira_hostname):
        """JiraApiCall.exec"""
        api_call = JiraApiCall(RequestTypes.GET, "sample")

        m_val_env.return_value = None

        m_response = MagicMock()
        m_get.return_value = m_response

        m_jira_email.return_value = "test@mycf.co"
        m_jira_token.return_value = "abc123"
        m_jira_hostname.return_value = "mycf.atl.net/"
        auth = HTTPBasicAuth("test@mycf.co", "abc123")

        response = api_call.exec()

        m_get.assert_called_with("mycf.atl.net/sample", headers={"X-Atlassian-Token": "no-check"}, auth=auth, json=None)
        self.assertEqual(response, m_response)


if __name__ == '__main__':
    import xmlrunner
    unittest.main(testRunner=xmlrunner.XMLTestRunner(output='test-reports'))
