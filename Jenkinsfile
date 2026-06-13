pipeline {
    agent any
    options {
        timeout(time: 15, unit: 'MINUTES')
    }
    stages {
        stage('Clean and Fetch') {
            steps {
                cleanWs()
                git branch: 'main', url: 'https://github.com/Maryam-Yaqoob/selfhealing-mlops-FA23-BAI-025.git'
            }
        }
        stage('Build and Push') {
            steps {
                sh 'docker builder prune -f'
                sh 'docker image prune -f'
                sh 'docker build -t maryamyaqoob8381/sentiment-api:unstable .'
                withCredentials([usernamePassword(credentialsId: 'dockerhub-credentials', passwordVariable: 'DOCKER_PASSWORD', usernameVariable: 'DOCKER_USERNAME')]) {
                    sh 'echo $DOCKER_PASSWORD | docker login -u $DOCKER_USERNAME --password-stdin'
                    sh 'docker push maryamyaqoob8381/sentiment-api:unstable'
                }
            }
        }
        stage('Deploy to K8s') {
            steps {
                sh 'kubectl apply -f k8s/pvc.yaml --kubeconfig=/var/jenkins_home/.kube/config'
            }
        }
    }
}
