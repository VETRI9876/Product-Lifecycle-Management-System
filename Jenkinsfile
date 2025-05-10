pipeline {
    agent any

    environment {
        AWS_REGION = 'eu-north-1'  
        CLUSTER_NAME = 'my-app-cluster'  
        ECR_REPO = 'vetri-flask-repo'  
        ECR_URI = '409784048198.dkr.ecr.eu-north-1.amazonaws.com' 
        IMAGE_TAG = 'latest'  
    }

    stages {
        stage('Clone Repository') {
            steps {
                git branch: 'main', url: 'https://github.com/VETRI9876/Product-Lifecycle-Management-System.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    bat 'docker build -t my-flask-app .'
                }
            }
        }

        stage('Login to ECR') {
            steps {
                script {
                    bat '''
                    for /f "tokens=*" %%i in ('aws ecr get-login-password --region %AWS_REGION%') do docker login --username AWS --password %%i %ECR_URI%
                    '''
                }
            }
        }

        stage('Tag Docker Image') {
            steps {
                script {
                    bat "docker tag my-flask-app:%IMAGE_TAG% %ECR_URI%/%ECR_REPO%:%IMAGE_TAG%"
                }
            }
        }

        stage('Push to ECR') {
            steps {
                script {
                    bat "docker push %ECR_URI%/%ECR_REPO%:%IMAGE_TAG%"
                }
            }
        }

        stage('Deploy to EKS') {
            steps {
                script {
                    bat "aws eks --region %AWS_REGION% update-kubeconfig --name %CLUSTER_NAME%"
                    bat "kubectl apply -f deployment.yaml"
                    bat "kubectl apply -f service.yaml"
                }
            }
        }

        stage('Verify Deployment') {
            steps {
                script {
                    bat "kubectl get svc vetri-flask-service -o jsonpath=\"{.status.loadBalancer.ingress[0].hostname}\""
                }
            }
        }
    }

    post {
        success {
            echo 'Deployment to EKS was successful!'
        }
        failure {
            echo 'Deployment failed. Please check the logs.'
        }
    }
}
