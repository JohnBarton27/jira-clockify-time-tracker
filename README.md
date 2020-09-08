# Jira Clockify Time Tracker (JCTT)
Automatically add Clockify-tracked time entries to Jira Stories

## How it Works
This is a free library for mapping Clockify entries to Jira issues. To map your Clockify entries to Jira, add your 
Clockify and Jira account information to the local config file. A webhook from your Clockify account needs to kick off
a run of the main Python script (this can easily be achieved with a CI/CD tool like Jenkins or Atlassian Bamboo). 

## Running
### Environment Variables
In order to be able to add time entries to Jira, the following environment variables must be set:

- `JIRA_EMAIL` - Email address of the user who will authenticate against the Jira REST API
- `JIRA_API_TOKEN` - A Jira REST API token for the user with the above `JIRA_EMAIL`, used for authenticating against the Jira REST API
- `JIRA_HOSTNAME` - Base hostname for your Jira instance

You must also set the following environment variables in order to make calls to start/stop timers in Clockify:

- `CLOCKIFY_API_TOKEN` - Your Clockify API token

### Unit Tests
Unit tests require the 'xmlrunner' module. Install by running `pip3 install xmlrunner`.

For code coverage, the 'coverage' module is required. Install by running `pip3 install coverage`.

For SonarQube analysis, the sonar-scanner needs to be installed and on the user's PATH, along with a correctly-set `SONAR_TOKEN` environment variable.

## Integration with Git Commit Messages
JCCT can be used to automatically generate Clockify time entries, based on your Git commit history.