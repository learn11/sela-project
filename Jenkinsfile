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
        MONGO_URL = 'mongodb://mongodb-service.default:27017/mydb'  // MongoDB connection URL
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

        stage('Deploy MongoDB') {
            steps {
                script {
                    def mongodbDeployment = '''
apiVersion: apps/v1
kind: Deployment
metadata:
  name: mongodb-deployment
spec:
  replicas: 1
  selector:
    matchLabels:
      app: mongodb
  template:
    metadata:
      labels:
        app: mongodb
    spec:
      containers:
      - name: mongo
        image: mongo:4.2
        ports:
        - containerPort: 27017
        env:
        - name: MONGO_INITDB_ROOT_USERNAME
          value: root
        - name: MONGO_INITDB_ROOT_PASSWORD
          value: edmon
        volumeMounts:
        - name: mongodb-data
          mountPath: /data/db
      volumes:
      - name: mongodb-data
        emptyDir: {}
'''
                    def mongodbService = '''
apiVersion: v1
kind: Service
metadata:
  name: mongodb-service
spec:
  type: ClusterIP
  selector:
    app: mongodb
  ports:
  - port: 27017
    targetPort: 27017
'''

                    writeFile file: 'mongodb-deployment.yaml', text: mongodbDeployment
                    writeFile file: 'mongodb-service.yaml', text: mongodbService
                    sh 'kubectl apply -f mongodb-deployment.yaml'
                    sh 'kubectl apply -f mongodb-service.yaml'
                }
            }
        }

        stage('Run Tests') {
            steps {
                container('python') {
                    dir("${env.APP_DIR}") {
                        sh "pytest --junitxml=test-results.xml"
                    }
                }
            }
        }

        stage('Publish Test Results') {
            steps {
                junit 'fast_api/test-results.xml'
            }
        }

        stage('Clean Up') {
            steps {
                script {
                    sh 'kubectl delete -f mongodb-deployment.yaml'
                    sh 'kubectl delete -f mongodb-service.yaml'
                }
            }
        }
    }
}
