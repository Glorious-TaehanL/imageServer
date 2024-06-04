pipeline {
    agent any

    environment {
        imagename = "rendezvousted/imageserver"
        registryCredential = 'rendezvousted'
        version = '0.2.0'
    }

    stages {

        // Docker build
        stage('Build Docker') {
          steps {
            echo 'Building Docker image'
            script {
                dockerImage = docker.build("${imagename}:${version}", "--no-cache .")
            }
          }
          post {
            failure {
              error 'Docker build failed. This pipeline stops here...'
            }
          }
        }

        // Docker push
        stage('Push Docker') {
          steps {
            echo 'Pushing Docker image'
            script {
                docker.withRegistry('', registryCredential) {
                    dockerImage.push("${version}")  // e.g., "1.0"
                }
            }
          }
          post {
            failure {
              error 'Docker push failed. This pipeline stops here...'
            }
          }
        }

    }
    
    post {
        always {
            echo 'Pipeline finished'
        }
    }
}
