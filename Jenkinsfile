@Library("Shared") _
pipeline {
    agent {label "vinod"}

    stages {
        stage('Code') {
            steps {
                script{
                    echo 'Writing application code...'
                    clone("https://github.com/renish-1111/Summer-Internship-Project.git","main")
                    echo "Code Cloning Suceesful"
                }
            }
        }
        stage('Build') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerCred', usernameVariable: 'dockerUsername', passwordVariable: 'dockerPassword')]) {
                    echo 'Building the application...'
                    sh "docker compose down"
                    sh "docker build -t ${dockerUsername}/si-front-app:latest frontend/"
                    sh "docker build -t ${dockerUsername}/si-back-app:latest backend/"
                    echo 'Build Complete'
                }
            }
        }
        stage('Push') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerCred', usernameVariable: 'dockerUsername', passwordVariable: 'dockerPassword')]) {
                    sh "docker login -u ${dockerUsername} -p ${dockerPassword}"
                    echo 'Push image...'
                    sh "docker image push ${dockerUsername}/si-front-app:latest"
                    sh "docker image push ${dockerUsername}/si-back-app:latest"
                    echo 'Push Complete'
                }
            }
        }
        stage('Test') {
            steps {
                echo 'Running tests...'
            }
        }
        stage('Deploy') {
            steps {
                echo 'Deploying application...'
                sh "docker compose up -d"
            }
        }
    }
}
