pipeline {
    agent any
    stages {
        stage ('Test') {
            steps {
                sh 'export PYTHONPATH=$(pwd); python test/unit/run_tests.py'
                step([$class: 'Publisher', reportFilenamePattern: 'test-reports/*.xml'])
            }
        }
        stage ('Clean') {
            steps {
                sh 'rm -rf *; rm -rf *.git'
            }
        }
    }
}
