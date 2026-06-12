pipeline {
    agent any
    environment {
        DOCKERHUB_USER = 'maryamyaqoob8381'
        IMAGE_NAME     = 'sentiment-api'
        REGISTRY_CRED  = 'dockerhub-credentials'
    }
    stages {
        stage('Fetch') {
            steps {
                checkout scm: [
                    $class: 'GitSCM', 
                    branches: [[name: '*/main']], 
                    extensions: [], 
                    userRemoteConfigs: [[url: 'https://github.com/Maryam-Yaqoob/selfhealing-mlops-FA23-BAI-025.git']]
                ]
            }
        }
        stage('Build and Run') {
            steps {
                sh "docker build -t ${DOCKERHUB_USER}/${IMAGE_NAME}:unstable ."
                sh "docker rm -f sentiment-test-app || true"
                sh "docker run -d --name sentiment-test-app -p 5000:5000 -v /var/log/app:/app/logs ${DOCKERHUB_USER}/${IMAGE_NAME}:unstable"
                sh "sleep 15"
            }
        }
        stage('Unit Test') { steps { sh "docker exec sentiment-test-app pytest tests/test_api.py" } }
        stage('UI Test') { steps { sh "docker exec sentiment-test-app pytest tests/test_ui.py" } }
        stage('Build and Push') {
            steps {
                sh "docker rm -f sentiment-test-app || true"
                withCredentials([usernamePassword(credentialsId: "${REGISTRY_CRED}", passwordVariable: 'DOCKER_PASS', usernameVariable: 'DOCKER_USER')]) {
                    sh 'echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin'
                    sh "docker push ${DOCKERHUB_USER}/${IMAGE_NAME}:unstable"
                    
                    sh "git checkout stable-fallback"
                    sh "docker build -t ${DOCKERHUB_USER}/${IMAGE_NAME}:stable ."
                    sh "docker push ${DOCKERHUB_USER}/${IMAGE_NAME}:stable"
                    sh "git checkout main"
                }
            }
        }
        stage('Deploy to Minikube') {
            steps {
                sh "kubectl apply -f k8s/pvc.yaml"
                sh "kubectl apply -f k8s/blue-deployment.yaml"
                sh "kubectl apply -f k8s/green-deployment.yaml"
                sh "kubectl apply -f k8s/service.yaml"
            }
        }
    }
}
