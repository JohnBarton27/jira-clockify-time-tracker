pipeline {
    agent any
    stages {
        stage ('Test') {
            steps {
                sh 'export PYTHONPATH=$(pwd); python test/unit/run_tests.py'
                junit 'test-reports/*.xml'
            }
        }
        stage ('Analyze') {
            steps {
                sh 'python run_analysis.py $BRANCH_NAME'
            }
        }
        stage ('Clean') {
            steps {
                sh 'rm -rf *; rm -rf *.git'
            }
        }
    }
}
