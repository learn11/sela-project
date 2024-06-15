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
        MONGO_URL = 'mongodb://mongo:27017/mydatabase'  // MongoDB connection URL
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

        stage('Start MongoDB') {
            steps {
                container('mongo') {
                    sh 'echo "MongoDB is ready!"'
                    // Optionally, you can add more initialization steps if needed
                }
            }
        }

        stage('Run Tests') {
            steps {
                container('python') {
                    dir("${env.APP_DIR}") {
                        sh "pytest --junitxml=test-results.xml --mongo-url=${env.MONGO_URL}"
                    }
                }
            }
        }

        stage('Publish Test Results') {
            steps {
                junit 'fast_api/test-results.xml'
            }
        }
    }
}
