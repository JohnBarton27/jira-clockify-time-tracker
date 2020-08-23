# Jira Clockify Time Tracker (JCTT)
Automatically add Clockify-tracked time entries to Jira Stories

## How it Works
This is a free library for mapping Clockify entries to Jira issues. To map your Clockify entries to Jira, add your 
Clockify and Jira account information to the local config file. A webhook from your Clockify account needs to kick off
a run of the main Python script (this can easily be achieved with a CI/CD tool like Jenkins or Atlassian Bamboo). 

## Running
### Unit Tests
Unit tests require the 'xmlrunner' module. Install by running `pip3 install xmlrunner`.

For code coverage, the 'coverage' module is required. Install by running `pip3 install coverage`.