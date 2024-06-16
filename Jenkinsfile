pipeline {
    agent {
        kubernetes {
            yaml '''
apiVersion: v1
kind: Pod
spec:
  serviceAccountName: jenkins
  containers:
  - name: maven
    image: maven:alpine
    command:
    - cat
    tty: true
  - name: python
    image: python:3.9-alpine
    command:
    - cat
    tty: true
  - name: ez-docker-helm-build
    image: ezezeasy/ez-docker-helm-build:1.41
    imagePullPolicy: Always
    securityContext:
      privileged: true
'''
        }
    }

    environment {
        DOCKER_IMAGE = "edmonp173/project_app"
    }

    stages {
        
        stage('Build docker images') {
            steps {
                container('ez-docker-helm-build') {
                    script {
                        // Build Python Docker image
                        sh "docker build -t ${DOCKER_IMAGE}:backend ./fast_api"
                       
                    }
                }
            }
        }

        stage('Push Docker Images') {
            steps {
                container('ez-docker-helm-build') {
                    script {
                        withDockerRegistry([credentialsId: 'dockerhub']) {
                            // Build and Push Docker images
    
                            sh "docker push ${DOCKER_IMAGE}:backend"
                        }
                    }
                }
            }
        }
    }
}
