pipeline {
agent any

environment {
    DOCKER_BIN = 'C:\\Users\\aashi\\AppData\\Local\\Programs\\DockerDesktop\\resources\\bin'
    PYTHON_BIN = 'C:\\Users\\aashi\\AppData\\Local\\Python\\bin'
}

stages {

    stage('Checkout') {
        steps {
            checkout scm
        }
    }

    stage('Environment Check') {
        steps {
            bat 'git --version'
            bat '"%DOCKER_BIN%\\docker.exe" --version'
            bat '"%DOCKER_BIN%\\docker-compose.exe" version'
            bat '"%PYTHON_BIN%\\python.exe" --version'
        }
    }

    stage('Automated Tests') {
        parallel {

            stage('Library Service Tests') {
                steps {
                    dir('library-service') {
                        bat '"%PYTHON_BIN%\\python.exe" -m pytest -v'
                    }
                }
            }

            stage('Inventory Service Tests') {
                steps {
                    dir('inventory-service') {
                        bat '"%PYTHON_BIN%\\python.exe" -m pytest -v'
                    }
                }
            }
        }
    }

    stage('Build Docker Images') {
        steps {
            bat '"%DOCKER_BIN%\\docker-compose.exe" -f docker-compose.yml build'
        }
    }

    stage('Tag Images') {
        steps {
            bat '"%DOCKER_BIN%\\docker.exe" tag devproject-library-service:latest localhost:5000/library-service:latest'
            bat '"%DOCKER_BIN%\\docker.exe" tag devproject-inventory-service:latest localhost:5000/inventory-service:latest'
        }
    }

    stage('Push Images to Artifact Repository') {
        steps {
            bat '"%DOCKER_BIN%\\docker.exe" push localhost:5000/library-service:latest'
            bat '"%DOCKER_BIN%\\docker.exe" push localhost:5000/inventory-service:latest'
        }
    }

    stage('Deploy with Docker Compose') {
        steps {
            bat '"%DOCKER_BIN%\\docker-compose.exe" -p devproject -f docker-compose.yml up -d'
        }
    }

    stage('Check Services') {
        steps {
            bat '"%DOCKER_BIN%\\docker-compose.exe" -p devproject -f docker-compose.yml ps'
        }
    }
}

}