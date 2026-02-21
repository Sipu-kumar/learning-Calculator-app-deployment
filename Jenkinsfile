pipeline {
    agent any

    stages {
        stage('Checkout Code') {
            steps {
                git branch: 'main', url: 'https://github.com/RvM07/pipeline.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                echo 'Building Flask Docker Image...'
                bat 'docker build -t flask-app .'
            }
        }

        stage('Stop Old Container') {
            steps {
                bat 'docker stop flask-container || exit 0'
                bat 'docker rm flask-container || exit 0'
            }
        }

        stage('Run New Container') {
            steps {
                bat 'docker run -d -p 5000:5000 --name flask-container flask-app'
            }
        }

        stage('Test Application') {
            steps {
                bat 'curl http://localhost:5000'
            }
        }

        stage('Deploy Success') {
            steps {
                echo 'Deployment completed successfully!'
            }
        }
    }
}
