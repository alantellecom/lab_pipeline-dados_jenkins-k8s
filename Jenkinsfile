pipeline {
  
    environment {
        CLUSTER = ""
        CLUSTER_ZONE = ""
        JENKINS_CRED = "robotic-tide-284315"
        TAG_IMAGE = 'env.GIT_COMMIT'
    }

    agent {
        kubernetes {
        label 'pipeline'
        defaultContainer 'jnlp'
        yamlFile 'pipeline_jobs.yaml'
        
        }
    }

    stages {

        stage("Checkout Code") {
            steps {
            checkout scm
            }
        }  

        stage('Download Dataset') {

            steps {
                container('kubectl') {
                    sh 'cd ./etl_scripts/featurestore'
                    sh 'curl -o iris.txt  https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data'
                }
            }
        }
    
        stage('Pre-Processing') {
     
            steps {
                container('python') {
                    sh 'pip install -r etl_scripts/etl_preproc/requirements.txt'
                    sh 'python etl_scripts/etl_preproc/etl_preprocessing.py'
                    sh 'tail etl_scripts/featurestore/irisEncoder.txt'
                } 
            }
        }

        stage('Traning Model') {
     
            steps {
                container('python') {
                    sh 'pip install -r etl_scripts/traning_model/requirements.txt'
                    sh 'python etl_scripts/traning_model/ml_sklearn.py'
                } 
            }
        }

        stage('Validate Model') {
     
            steps {
                container('python') {
                    sh 'pip install -r etl_scripts/validate_model/requirements.txt'
                    sh 'python etl_scripts/validate_model/validateModel.py'
                    sh 'ls deployApi/apiIris/'
                } 
            }
        }
  
        stage('Build Image') {
     
            steps {
                container('gcloud') {
                    sh 'gcloud config set project robotic-tide-284315'
                    sh "gcloud auth activate-service-account jenkins@robotic-tide-284315.iam.gserviceaccount.com --key-file=key-gcp.json"
                    sh "PYTHONUNBUFFERED=1 gcloud builds submit --config deployApi/apiIris/cloudbuild.yaml --substitutions=TAG_NAME=${env.GIT_COMMIT} deployApi/apiIris/"       
                } 
            }
        }

        stage('Deploy Model API') {
     
            steps {
                container('kubectl') {
                  
                    sh './verify_secret.sh'
                    sh "sed -i 's#tag#${env.GIT_COMMIT}#g' deployApi/apiIris/k8s-artifacts/backend.yaml"
                    sh 'kubectl apply -f deployApi/apiIris/k8s-artifacts/'
                    
                } 
            }
        }

    }

}

  