pipeline {
    agent {
        kubernetes {
            yaml """
apiVersion: v1
kind: Pod
spec:
  serviceAccountName: jenkins
  containers:
  - name: python
    image: python:3.9
    command:
    - cat
    tty: true
  - name: mongo
    image: mongo:4.2
    ports:
    - containerPort: 27017
"""
        }
    }

    environment {
        APP_DIR = 'fast_api'
    }

    stages {
        stage('Clone Repository') {
            steps {
                container('python') {
                    git url: 'https://github.com/learn11/sela-project.git', branch: 'main'
                }
            }
        }

        stage('Install Dependencies') {
            steps {
                container('python') {
                    dir("${env.APP_DIR}") {
                        sh 'pip install -r requirements.txt'
                    }
                }
            }
        }

        stage('Run Tests') {
            steps {
                container('python') {
                    dir("${env.APP_DIR}") {
                        sh 'pytest --junitxml=test-results.xml'
                    }
                }
            }
        }

        stage('Publish Test Results') {
            steps {
                junit 'fastapi_app/test-results.xml'
            }
        }
    }
}
