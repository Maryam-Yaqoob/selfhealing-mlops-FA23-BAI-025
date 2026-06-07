pipeline {
    agent any

    environment {
        DOCKERHUB_USER = "maryamyaqoob8381"
        IMAGE_NAME = "sentiment-api"
        UNSTABLE_IMAGE = "${DOCKERHUB_USER}/${IMAGE_NAME}:unstable"
        STABLE_IMAGE = "${DOCKERHUB_USER}/${IMAGE_NAME}:stable"
    }

    stages {
        stage('Fetch') {
            steps {
                checkout scm
            }
        }

        stage('Build and Run') {
            steps {
                sh '''
                    docker rm -f sentiment-test || true
                    docker build -t sentiment-api-test .
                    docker run -d --name sentiment-test -p 5000:5000 sentiment-api-test
                    sleep 20
                '''
            }
        }

        stage('Unit Test') {
            steps {
                sh '''
                    docker run --rm --network host \
                    -e BASE_URL=http://localhost:5000 \
                    sentiment-api-test pytest tests/test_api.py
                '''
            }
        }

        stage('UI Test') {
            steps {
                sh '''
                    docker run --rm --network host \
                    -e BASE_URL=http://localhost:5000 \
                    sentiment-api-test pytest tests/test_ui.py
                '''
            }
        }

        stage('Build and Push') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-creds',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {
                    sh '''
                        echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
                        docker build -t $UNSTABLE_IMAGE .
                        docker build -t $STABLE_IMAGE ./stable-fallback
                        docker push $UNSTABLE_IMAGE
                        docker push $STABLE_IMAGE
                    '''
                }
            }
        }

        stage('Deploy to Minikube') {
            steps {
                sh '''
                    kubectl apply -f k8s/pvc.yaml
                    kubectl apply -f k8s/blue-deployment.yaml
                    kubectl apply -f k8s/green-deployment.yaml
                    kubectl apply -f k8s/service.yaml
                '''
            }
        }
    }

    post {
        always {
            sh 'docker rm -f sentiment-test || true'
        }
    }
}
