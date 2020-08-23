import argparse
import subprocess
import os


parser = argparse.ArgumentParser(description="Runs SonarQube analysis for Jira Clockify Time Tracker.")
parser.add_argument("branch_name", help="Git branch being analyzed")

args = parser.parse_args()
branch = args.branch_name

# Run Tests (for Coverage report)
coverage_cmd = "coverage run --source=. test/unit/run_tests.py"
coverage_proc = subprocess.Popen(coverage_cmd.split(" "), shell=False)
coverage_proc.communicate()

coverage_xml_cmd = "coverage xml"
coverage_xml_proc = subprocess.Popen(coverage_xml_cmd.split(" "), shell=False)
coverage_xml_proc.communicate()

options = {
    "sonar.projectKey": "jira-clockify-time-tracker",
    "sonar.organization": "johnbarton27",
    "sonar.host.url": "https://sonarcloud.io",
    "sonar.branch.name": branch,
    "sonar.sources": ["lib"],
    "sonar.tests": "test",
    "sonar.exclusions": ["scripts/"],
    "sonar.python.coverage.reportPaths": "coverage.xml"
}

command = "sonar-scanner -X "

for option in options:
    if isinstance(options[option], list):
        options[option] = ",".join(options[option])
    command += "-D{0}={1} ".format(option, options[option])

command = command.strip()
print(command)
proc = subprocess.Popen(command, shell=True)
proc.communicate()
