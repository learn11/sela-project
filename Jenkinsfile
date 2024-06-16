pipeline {
    agent any
    
    environment {
        KUBECONFIG = credentials('kubeconfig-credentials-id') // Replace with your Jenkins Kubeconfig credentials ID
    }
    
    stages {
        stage('Deploy MongoDB') {
            steps {
                script {
                    // Create a Kubernetes YAML file for MongoDB deployment
                    writeFile file: 'mongodb-deployment.yaml', text: '''
apiVersion: v1
kind: Pod
metadata:
  name: mongodb
spec:
  containers:
  - name: mongodb
    image: mongo:latest
    ports:
    - containerPort: 27017
                    '''
                    
                    // Apply the deployment to the Kubernetes cluster
                    sh 'kubectl apply -f mongodb-deployment.yaml'
                }
            }
        }
        
        stage('Check MongoDB Status') {
            steps {
                script {
                    // Check if the MongoDB pod is running
                    timeout(time: 3, unit: 'MINUTES') {
                        waitUntil {
                            script {
                                def status = sh(script: "kubectl get pods mongodb -o jsonpath='{.status.phase}'", returnStdout: true).trim()
                                return status == 'Running'
                            }
                        }
                    }
                }
            }
        }
    }
    
    post {
        always {
            // Clean up the MongoDB pod after the job completes
            sh 'kubectl delete pod mongodb'
        }
        success {
            echo 'MongoDB pod is running successfully!'
        }
        failure {
            echo 'Failed to deploy or verify MongoDB pod!'
        }
    }
}
