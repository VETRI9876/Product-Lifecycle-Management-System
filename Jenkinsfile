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
                git 'https://github.com/your-username/my-flask-app.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    sh 'docker build -t my-flask-app .'
                }
            }
        }

        stage('Login to ECR') {
            steps {
                script {
                    sh '''
                    $(aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $ECR_URI)
                    '''
                }
            }
        }

        stage('Tag Docker Image') {
            steps {
                script {
                    sh "docker tag my-flask-app:$IMAGE_TAG $ECR_URI/$ECR_REPO:$IMAGE_TAG"
                }
            }
        }

        stage('Push to ECR') {
            steps {
                script {
                    sh "docker push $ECR_URI/$ECR_REPO:$IMAGE_TAG"
                }
            }
        }

        stage('Deploy to EKS') {
            steps {
                script {
                    sh "aws eks --region $AWS_REGION update-kubeconfig --name $CLUSTER_NAME"
                    sh "kubectl apply -f deployment.yaml"
                    sh "kubectl apply -f service.yaml"
                }
            }
        }

        stage('Verify Deployment') {
            steps {
                script {
                    sh 'kubectl get svc vetri-flask-service -o jsonpath=\'{.status.loadBalancer.ingress[0].hostname}\''
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
