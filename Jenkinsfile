pipeline {
    agent any

    triggers {
        // 1. Batch Processing: Run unconditionally once a week on Sunday around 8:00 AM
        cron('H 8 * * 0')
        
        // 2. CI/CD: Check GitHub for new code once a week on Sunday around 9:00 AM.
        // If there is a new commit, run the pipeline!
        pollSCM('H 9 * * 0')
    }

    environment {
        // Your exact Python path with double backslashes escaped for Jenkins
        PYTHON_PATH = 'C:\\Users\\MY DELL\\AppData\\Local\\Python\\pythoncore-3.14-64\\python.exe' 
        
        DB_USER = 'pipeline_user'
        DB_NAME = 'analytics_db'
        DB_HOST = 'localhost'
        DB_PORT = '5432'
        
        OPENWEATHER_API_KEY = credentials('OPENWEATHER_API_KEY')
        DB_PASSWORD = credentials('DB_PASSWORD')
    }

    stages {
        stage('Verify Environment & Install Libraries') {
            steps {
                bat 'echo "Starting pipeline pulled straight from GitHub with Jenkins Secrets!"'
                
                // We use the exact path to Python to install our required libraries
                bat '"%PYTHON_PATH%" -m pip install -r requirements.txt'
            }
        }
        
        stage('Extract (E)') {
            steps {
                // We use the exact path to Python to run the script
                bat '"%PYTHON_PATH%" scripts/extract.py'
            }
        }
        
        stage('Transform (T)') {
            steps {
                bat '"%PYTHON_PATH%" scripts/transform.py'
            }
        }
    }
}
