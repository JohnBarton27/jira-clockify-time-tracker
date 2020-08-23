pipeline {
    agent any
    stages {
        stage ('Test') {
            steps {
                bash '''#!/bin/bash
                         export PYTHONPATH=$(pwd)
                         python test/unit/run_tests.py
                '''
                junit 'test-reports/*.xml'
            }
        }
        stage ('Analyze') {
            steps {
                bash '''$!/bin/bash
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
