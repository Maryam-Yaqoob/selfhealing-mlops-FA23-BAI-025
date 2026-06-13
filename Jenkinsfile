pipeline {
    agent any

    environment {
        DOCKERHUB_USER = 'maryamyaqoob8381'
        IMAGE_NAME     = 'sentiment-api'
        UNSTABLE_TAG   = "${DOCKERHUB_USER}/${IMAGE_NAME}:unstable"
        STABLE_TAG     = "${DOCKERHUB_USER}/${IMAGE_NAME}:stable"
        APP_CONTAINER  = 'sentiment-app-test'
        KUBECONFIG_PATH = '/var/jenkins_home/.kube/config'
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
                    docker rm -f ${APP_CONTAINER} || true
                    docker build -t ${UNSTABLE_TAG} .
                    docker run -d --name ${APP_CONTAINER} -p 5050:5000 ${UNSTABLE_TAG}
                    sleep 20
                '''
            }
        }

        stage('Unit Test') {
            steps {
                sh '''
                    docker run --rm --network container:${APP_CONTAINER} \
                        -v $WORKSPACE/tests:/tests \
                        python:3.10-slim sh -c "pip install --no-cache-dir pytest requests && pytest /tests/test_api.py -v"
                '''
            }
        }

        stage('UI Test') {
            steps {
                sh '''
                    docker run --rm --network container:${APP_CONTAINER} \
                        -v $WORKSPACE/tests:/tests \
                        ${UNSTABLE_TAG} sh -c "pip install --no-cache-dir pytest selenium && pytest /tests/test_ui.py -v"
                '''
            }
        }

        stage('Build and Push') {
            steps {
                script {
                    sh '''
                        docker build -t ${UNSTABLE_TAG} .

                        rm -rf stable-fallback-src
                        git clone -b stable-fallback $(git config --get remote.origin.url) stable-fallback-src
                        docker build -t ${STABLE_TAG} stable-fallback-src
                    '''
                    docker.withRegistry('', 'docker-hub-credentials-id') {
                        sh '''
                            docker push ${UNSTABLE_TAG}
                            docker push ${STABLE_TAG}
                        '''
                    }
                }
            }
        }

        stage('Deploy to Minikube') {
            steps {
                sh '''
                    kubectl apply -f k8s/pvc.yaml --kubeconfig=${KUBECONFIG_PATH} --validate=false
                    kubectl apply -f k8s/blue-deployment.yaml --kubeconfig=${KUBECONFIG_PATH} --validate=false
                    kubectl apply -f k8s/green-deployment.yaml --kubeconfig=${KUBECONFIG_PATH} --validate=false
                    kubectl apply -f k8s/service.yaml --kubeconfig=${KUBECONFIG_PATH} --validate=false
                '''
            }
        }
    }

    post {
        always {
            sh 'docker rm -f ${APP_CONTAINER} || true'
        }
    }
}
