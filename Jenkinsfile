pipeline {
agent any

stages {

    stage('Checkout') {
        steps {
            checkout scm
        }
    }

    stage('Environment Check') {
        steps {
            bat 'git --version'
            bat 'docker --version'
            bat '"C:\\Users\\aashi\\AppData\\Local\\Programs\\DockerDesktop\\resources\\bin\\docker-compose.exe" version'
        }
    }

    stage('Automated Tests') {
        parallel {

            stage('Library Service Tests') {
                steps {
                    dir('library-service') {
                        bat '"C:\\Users\\aashi\\AppData\\Local\\Python\\bin\\python.exe" -m pytest -v'
                    }
                }
            }

            stage('Inventory Service Tests') {
                steps {
                    dir('inventory-service') {
                        bat '"C:\\Users\\aashi\\AppData\\Local\\Python\\bin\\python.exe" -m pytest -v'
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