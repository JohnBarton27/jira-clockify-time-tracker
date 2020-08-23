pipeline {
    agent any
    stages {
        stage ('Test') {
            steps {
                sh '''#!/bin/bash
                      export PYTHONPATH=$(pwd)
                      python test/unit/run_tests.py
                '''
                junit 'test-reports/*.xml'
            }
        }
        stage ('Analyze') {
            steps {
                sh '''#!/bin/bash
                      source ~/.bashrc
                      python scripts/run_analysis.py $BRANCH_NAME
                '''
            }
        }
        stage ('Clean') {
            steps {
                sh 'rm -rf *; rm -rf *.git'
            }
        }
    }
}
