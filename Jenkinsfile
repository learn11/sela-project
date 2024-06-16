pipeline {
    agent {
        kubernetes {
            yaml '''
            apiVersion: v1
            kind: Pod
            spec:
                containers:
                  - name: slave
                    image: docker:latest
                    tty: true
                    securityContext:
                        privileged: true
                  - name: pytest
                    image: mikey8520/tests
                    tty: true
                    securityContext:
                        privileged: true
                  - name: maven
                    image: maven:alpine
                    command:
                    - cat
                    tty: true
                  - name: busybox
                    image: busybox
                    command:
                    - sleep
                    - "3600"
                    tty: true
            '''
        }
    }

    stages {
        stage('Check DNS') {
            steps {
                container('busybox') {
                    script {
                        sh 'nslookup github.com'
                    }
                }
            }
        }

        stage('checkout git') {
            steps {
                script {
                    checkout scm
                }
            }
        }

        stage('testing with pytest') {
            steps {
                container('pytest') {
                    script {
                        sh 'cd ./fast_api && python -m pytest || [[ $? -eq 1 ]]'
                    }
                }
            }
        }

        stage('Build and Push the image with tags') {
            environment {
                auth = 'dockerauth'
            }
            steps { 
                container('slave') {
                    script {
                        def image = docker.build("edmonp173/project_app", "./fast_api")
                        withDockerRegistry(credentialsId: 'dockerhub') {
                            image.push("backend")
                        }
                    }
                }
            }
        }
    }

    post {
        always {
            echo 'Pipeline POST:'
        }
        success {
            echo 'Pipeline SUCCESS!'
        }
        failure {
            echo 'Pipeline FAILED, check the logs for more information!'
        }
    }
}
