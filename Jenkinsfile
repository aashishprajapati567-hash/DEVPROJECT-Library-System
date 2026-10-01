pipeline {
    agent any

    environment {
        DOCKER_PATH = "C:\\Users\\aashi\\AppData\\Local\\Programs\\DockerDesktop\\resources\\bin"
        PYTHON_PATH = "C:\\Users\\aashi\\AppData\\Local\\Python\\bin"

        PATH = "${env.PYTHON_PATH};${env.DOCKER_PATH};${env.PATH}"
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Environment Check') {
            steps {
                bat 'whoami'
                bat 'git --version'

                bat 'where python'
                bat 'python --version'

                bat 'python -m pytest --version'

                bat 'where docker'
                bat 'docker --version'

                bat '"C:\\Users\\aashi\\AppData\\Local\\Programs\\DockerDesktop\\resources\\bin\\docker-compose.exe" version'
            }
        }

        stage('Automated Tests') {
            parallel {

                stage('Library Service Tests') {
                    steps {
                        dir('library-service') {
                            bat 'python -m pytest -v'
                        }
                    }
                }

                stage('Inventory Service Tests') {
                    steps {
                        dir('inventory-service') {
                            bat 'python -m pytest -v'
                        }
                    }
                }
            }
        }

        stage('Build Docker Images') {
            steps {
                bat '"C:\\Users\\aashi\\AppData\\Local\\Programs\\DockerDesktop\\resources\\bin\\docker-compose.exe" -f docker-compose.yml build'
            }
        }

        stage('Tag Images') {
            steps {
                bat 'docker tag devproject-library-service:latest localhost:5000/library-service:latest'
                bat 'docker tag devproject-inventory-service:latest localhost:5000/inventory-service:latest'
            }
        }

        stage('Push Images to Artifact Repository') {
            steps {
                bat 'docker push localhost:5000/library-service:latest'
                bat 'docker push localhost:5000/inventory-service:latest'
            }
        }

        stage('Deploy with Docker Compose') {
            steps {
                bat '"C:\\Users\\aashi\\AppData\\Local\\Programs\\DockerDesktop\\resources\\bin\\docker-compose.exe" -p devproject -f docker-compose.yml up -d'
            }
        }

        stage('Check Services') {
            steps {
                bat '"C:\\Users\\aashi\\AppData\\Local\\Programs\\DockerDesktop\\resources\\bin\\docker-compose.exe" -p devproject -f docker-compose.yml ps'
            }
        }
    }
}