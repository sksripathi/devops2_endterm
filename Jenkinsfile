pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/sksripathi/devops2_endterm.git'
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                python3 -m venv venv
                . venv/bin/activate
                pip install --upgrade pip
                pip install -r requirements.txt
                '''
            }
        }

        stage('Test') {
            steps {
                sh '''
                . venv/bin/activate
                python -c "import app"
                '''
            }
        }

        stage('Deploy') {
            steps {
                sh '''
                pkill -f "python3 app.py" || true
                nohup python3 app.py > app.log 2>&1 &
                '''
            }
        }
    }
}
