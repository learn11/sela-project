pipeline {
    agent {
        kubernetes {
            label 'jenkins-slave-pipeline-a'
            defaultContainer 'custom'
            yaml """
apiVersion: v1
kind: Pod
spec:
  serviceAccountName: jenkins-sa
  containers:
  - name: custom
    image: edmon/inbound-agent-root:latest
    command:
    - cat
    tty: true
"""
        }
    }

    environment {
        GITHUB_TOKEN = credentialsId: 'github'
        GITHUB_USER = 'edmonp173'
        REPO = 'learn11/sela-project'
    }

    stages {
        stage('Setup Git') {
            steps {
                catchError {
                    container('custom') {
                        sh 'git config --global --add safe.directory /home/jenkins/agent/workspace/sela-project'
                    }
                }
            }
        }

        stage('Clone and Switch to Feature Branch') {
            steps {
                catchError {
                    container('custom') {
                        sh '''
                            cd /home/jenkins/agent/workspace
                            git clone https://${GITHUB_TOKEN}@github.com/${REPO}.git
                            cd Persudoku
                            git fetch origin
                            if git rev-parse --quiet --verify feature; then
                                git checkout feature
                            else
                                git checkout -b feature
                            fi
                            git checkout main -- .
                            git add .
                            git pull origin main
                            git config --global user.email "edmonp173@gmail.com"
                            git config --global user.name "edmonp173"
                            git commit -m "Copy files from main branch to feature branch" || true
                            git push origin feature
                        '''
                    }
                }
            }
        }

        stage('Install Requirements') {
            steps {
                catchError {
                    container('custom') {
                        dir('/home/jenkins/agent/workspace/sela-project') {
                            sh "pip install -r fast_api/requirements.txt"
                        }
                    }
                }
            }
        }

        stage('Run Pytest') {
            steps {
                catchError {
                    container('custom') {
                        dir('/home/jenkins/agent/workspace/sela-project') {
                            sh "pytest --junitxml=test-results.xml fast-api/config-test.py"
                        }
                    }
                }
            }
        }

        stage('Manual Approval') {
            when {
                beforeAgent true
                expression { true }
            }
            steps {
                script {
                    def manualApprovalGranted = input message: 'Approve deployment to main?', ok: 'Approve'

                    if (manualApprovalGranted) {
                        container('custom') {
                            dir('/home/jenkins/agent/workspace/sela-project') {
                                def commitHash = sh(script: 'git rev-parse HEAD', returnStdout: true).trim()
                                sh """
                                curl -X POST \
                                -u ${GITHUB_USER}:${GITHUB_TOKEN} \
                                -H 'Content-Type: application/json' \
                                -d '{"state": "success", "description": "Manual approval granted", "context": "jenkins/manual-approval"}' \
                                https://api.github.com/repos/${REPO}/statuses/${commitHash}
                                """

                                sh 'git checkout main'
                                sh 'git branch -D feature'
                                sh "git push origin --delete feature"
                                build job: 'app', parameters: []
                            }
                        }
                    } else {
                        container('custom') {
                            dir('/home/jenkins/agent/workspace/sela-project') {
                                sh 'git checkout feature'
                                sh 'git reset --hard HEAD~1'
                                sh 'git push origin feature --force'
                            }
                        }
                    }
                }
            }
        }
    }
}