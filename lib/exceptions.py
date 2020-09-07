

class JiraApiTokenNotSetException(Exception):
    """
    Raised when attempting to perform a Jira API REST call, but the JIRA_API_TOKEN variable has not been set.
    """
    pass


class JiraEmailNotSetException(Exception):
    """
    Raised when attempting to perform a Jira API REST call, but the JIRA_EMAIL variable has not been set.
    """
    pass


class JiraHostnameNotSetException(Exception):
    """
    Raised when attempting to perform a Jira API REST call, but the JIRA_HOSTNAME variable has not been set.
    """
    pass


class NoJiraKayFoundException(Exception):
    """
    Raised when parsing a TimeEntry, but no Jira Key was found.
    """
    pass


class ClockifyApiKeyNotSetException(Exception):
    """
    Raised when attempting to perform a Clockify REST API call, but the CLOCKIFY_API_KEY variable has not been set.
    """
    pass
