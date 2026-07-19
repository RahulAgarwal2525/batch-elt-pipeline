pipeline {
    agent any

    // This block injects environment variables before the stages run
    environment {
        // Non-secret variables can be written in plain text
        DB_USER = 'pipeline_user'
        DB_NAME = 'analytics_db'
        DB_HOST = 'localhost'
        DB_PORT = '5432'
        
        // Secrets are securely pulled from the Jenkins vault using their ID
        OPENWEATHER_API_KEY = credentials('OPENWEATHER_API_KEY')
        DB_PASSWORD = credentials('DB_PASSWORD')
    }

    stages {
        stage('Verify Environment') {
            steps {
                bat 'echo "Starting pipeline pulled straight from GitHub with Jenkins Secrets!"'
            }
        }
        
        stage('Extract (E)') {
            steps {
                // Python will automatically find the credentials injected above!
                bat 'python scripts/extract.py'
            }
        }
        
        stage('Transform (T)') {
            steps {
                bat 'python scripts/transform.py'
            }
        }
    }
}