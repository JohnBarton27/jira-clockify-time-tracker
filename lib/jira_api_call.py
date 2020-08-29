from enum import Enum
import requests
from requests.auth import HTTPBasicAuth

from lib.variable import Variable
from lib.exceptions import JiraApiTokenNotSetException, JiraEmailNotSetException, JiraHostnameNotSetException


class RequestTypes(Enum):

    GET = 1
    PUT = 2
    POST = 3
    DELETE = 4

    @property
    def requests_function(self):
        if self.name == "GET":
            return requests.get
        elif self.name == "PUT":
            return requests.put
        elif self.name == "POST":
            return requests.post
        elif self.name == "DELETE":
            return requests.delete


class JiraApiCall:

    # Environment Variable Names
    jira_email_var_name = "JIRA_EMAIL"
    jira_token_var_name = "JIRA_API_TOKEN"
    jira_hostname_var_name = "JIRA_HOSTNAME"

    def __init__(self, req_type: RequestTypes, url: str):
        self.type = req_type
        self.url = url

    @property
    def jira_email(self):
        return Variable(JiraApiCall.jira_email_var_name).value

    @property
    def jira_token(self):
        return Variable(JiraApiCall.jira_token_var_name).value

    @property
    def jira_hostname(self):
        jira_hostname = Variable(JiraApiCall.jira_hostname_var_name).value
        if not jira_hostname:
            return None

        # Make sure hostname end has a trailing slash
        if not jira_hostname.endswith("/"):
            jira_hostname = "{}/".format(jira_hostname)

        return jira_hostname

    def validate_environment(self):
        # Jira Email
        if not self.jira_email:
            raise JiraEmailNotSetException("{} environment variable not set - unable to perform Jira REST API  calls!"
                                           .format(JiraApiCall.jira_email_var_name))

        # Jira Token
        if not self.jira_token:
            raise JiraApiTokenNotSetException("{} environment variable not set - unable to perform Jira REST API calls!"
                                              .format(JiraApiCall.jira_token_var_name))

        # Jira Hostname
        if not self.jira_hostname:
            raise JiraHostnameNotSetException("{} environment variable not set - unable to perform Jira REST API calls!"
                                              .format(JiraApiCall.jira_hostname_var_name))

    def exec(self):
        self.validate_environment()

        header = {"X-Atlassian-Token": "no-check"}
        auth = HTTPBasicAuth(self.jira_email, self.jira_token)
        full_url = "{}{}".format(self.jira_hostname, self.url)
        response = self.type.requests_function(full_url, headers=header, auth=auth)
        return response
