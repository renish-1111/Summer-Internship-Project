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
                script {
                        echo 'Building the application...'
                        sh "docker compose down"
                        dockerBuild(
                            imageName: 'si-front-app',
                            dockerfile: 'Dockerfile',
                            context: 'frontend',
                            tag: 'latest',
                            registry: 'renishponkiya',
                            push: true,
                            credentialsId: 'dockerCred'
                        )
                        dockerBuild(
                            imageName: 'si-back-app',
                            dockerfile: 'Dockerfile',
                            context: 'backend',
                            tag: 'latest',
                            registry: 'renishponkiya',
                            push: true,
                            credentialsId: 'dockerCred'
                        )
                }
            }
        }
        stage('Deploy') {
            steps {
                script{
                    dockerDeploy()
                    echo "Complete"
                }
            }
        }
    }
}
