pipeline {
agent any

// We can set a cron schedule here later (e.g., run every morning at 6 AM)

stages {
    stage('Verify Environment') {
        steps {
            // Since local Jenkins runs on Windows, we use 'bat' instead of 'sh'
            bat 'echo "Starting pipeline from Local Windows Jenkins!"'
        }
    }
    
    stage('Extract (E)') {
        steps {
            // This tells Jenkins to change into your specific project directory
            dir('E:\\Projects\\batch-elt-pipeline') {
                bat 'python scripts/extract.py'
            }
        }
    }
    
    stage('Transform (T)') {
        steps {
            dir('E:\\Projects\\batch-elt-pipeline') {
                bat 'python scripts/transform.py'
            }
        }
    }
}


}