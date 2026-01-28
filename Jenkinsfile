pipeline {
    agent any

    options {
        timeout(time: 20, unit: 'MINUTES')
    }

    environment {
        IMAGE_NAME = "nandinistr23/flask-blog"
        IMAGE_TAG  = "latest"
        SONAR_HOME = tool "sonar"
    }

    stages {

        stage('Checkout') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/Nandini-project/CDAC_FINAL-_PROJECT.git'
            }
        }

        stage('SonarQube Analysis') {
            steps {
                withSonarQubeEnv("sonar") {
                    withCredentials([
                        string(credentialsId: 'sonar-token', variable: 'SONAR_TOKEN')
                    ]) {
                        sh """
                          $SONAR_HOME/bin/sonar-scanner \
                          -Dsonar.projectName=flask_blog \
                          -Dsonar.projectKey=flask_blog \
                          -Dsonar.login=$SONAR_TOKEN
                        """
                    }
                }
            }
        }

        stage('SonarQube Quality Gate') {
            steps {
                timeout(time: 5, unit: 'MINUTES') {
                    waitForQualityGate abortPipeline: true
                }
            }
        }

        stage('Trivy FS Scan (Source Code)') {
            steps {
                sh '''
                  trivy fs \
                  --exit-code 1 \
                  --severity HIGH,CRITICAL \
                  .
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t $IMAGE_NAME:$IMAGE_TAG .'
            }
        }

        stage('Trivy Image Scan') {
            steps {
                sh '''
                  trivy image \
                  --exit-code 0 \
                  --severity HIGH,CRITICAL \
                  $IMAGE_NAME:$IMAGE_TAG
                '''
            }
        }

        stage('Push Image to DockerHub') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'dockerhub',
                        usernameVariable: 'DOCKER_USER',
                        passwordVariable: 'DOCKER_PASS'
                    )
                ]) {
                    sh '''
                      echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin
                      docker push $IMAGE_NAME:$IMAGE_TAG
                    '''
                }
            }
        }

        stage('Deploy') {
            steps {
                sh '''
                  docker compose pull
                  docker compose up -d --force-recreate
                '''
            }
        }
    }

    post {
        success {
            echo "✅ Pipeline completed successfully!"
        }
        failure {
            echo "❌ Pipeline failed. Check logs."
        }
    }
}
