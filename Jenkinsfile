def getGitBranchName() { 
                return scm.branches[0].name 
            }
def branchName
def targetBranch

pipeline{
    agent any

    environment {
              DOCKER_IMAGE_recommendation_system = 'brahim98/recommendation-system:v1.0.0-dev'

  }
     parameters {
       string(name: 'BRANCH_NAME', defaultValue: "${scm.branches[0].name}", description: 'Git branch name')
       string(name: 'CHANGE_ID', defaultValue: '', description: 'Git change ID for merge requests')
       string(name: 'CHANGE_TARGET', defaultValue: '', description: 'Git change ID for the target merge requests')
  }
    stages{

      stage('branch name') {
      steps {
        script {
          branchName = params.BRANCH_NAME
          echo "Current branch name: ${branchName}"
        }
      }
    }

    stage('target branch') {
      steps {
        script {
          targetBranch = branchName
          echo "Target branch name: ${targetBranch}"
        }
      }
    }
        stage('Git Checkout'){
            steps{
                git branch: 'main', credentialsId: 'git', url: 'https://github.com/SirineAmri/systemederecommantationIA.git'
	    }
        }
        
   /*     stage('Clean Build'){
            steps{
                sh 'rm -rf node_modules'
            }
        }*/

        stage('Install Dependencies') {
            steps {
                // Install required Python packages
                sh 'pip3 install -r requirements.txt'
            }
        }
           /*  stage('Run Script') {
            steps {
                // Run the converted Python script
                sh 'python3 traintest.py'
            }
        }*/
	    /*
         stage('Run Script') {
            steps {
                // Run the converted Python script and capture the output
                sh 'python3 traintest.py > output.log'
            }
        } */
        
  /*   stage('Archive Results') {
            steps {
                // Archive results for later viewing
                archiveArtifacts artifacts: 'output.html', allowEmptyArchive: false
            }
        }

 
        
        stage('Publish HTML Report') {
            steps {
                publishHTML([allowMissing: false,
                             alwaysLinkToLastBuild: true,
                             keepAll: true,
                             reportDir: '.',
                             reportFiles: 'output.html',
                             reportName: 'HTML Report',
                             reportTitles: 'Product Rating Tawasalna'])
            }
        }
*/

 stage('Build image recommendation') {
                steps {
                    script {
                // Build the Docker image for the Spring Boot apps
                sh "docker build -t $DOCKER_IMAGE_recommendation_system -f Dockerfile ."
              
            }
                }
            }


      stage('Push image recommendation') {
                steps {
                    script {
                        withDockerRegistry([credentialsId: 'docker-hub-creds',url: ""]) {
                            // Push the Docker image to Docker Hub

                        sh "docker push $DOCKER_IMAGE_recommendation_system"
                   
                        }
                    }
                }}








         stage('Deployment stage ') {
    steps {
    dir('ansible') {

        sh "sudo ansible-playbook -u root k8s.yml -i inventory/host.yml"
    }

}

}



	    
	    
	    



	    

	    
    }
}
    
