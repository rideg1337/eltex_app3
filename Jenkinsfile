pipeline {
    agent any

    environment {
        IMAGE_NAME = "rideg/eltex-app"
    }

    stages {
        stage('Clone') {
            steps {
                git branch: 'main', url: 'https://github.com/rideg1337/eltex_app3.git'
            }
        }

        stage('Build Docker') {
            steps {
                sh "docker build -t $IMAGE_NAME ."
            }
        }

        stage('Inject .env') {
            steps {
                withCredentials([file(credentialsId: 'eltex-env', variable: 'ENV_FILE')]) {
                    sh 'cp $ENV_FILE .env'
                }
            }
        }

        stage('Run app') {
            steps {
                sh "docker run -d --rm --env-file .env -p 5055:5055 $IMAGE_NAME"
            }
        }
    }
}
