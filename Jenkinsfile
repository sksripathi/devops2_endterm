pipeline {
    agent any

    environment {
        AWS_ACCESS_KEY_ID = credentials('AWS_ACCESS_KEY_ID')
        AWS_SECRET_ACCESS_KEY = credentials('AWS_SECRET_ACCESS_KEY')
        AWS_REGION = 'ap-south-1'
        S3_BUCKET_NAME = 'user-dashboard-dataset'
        DATASET_FILE = 'u.user'
    }

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
                pkill -f "app.py" || true
                sleep 2

                cd /var/lib/jenkins/workspace/UserDashboard-CICD

                nohup env \
                AWS_ACCESS_KEY_ID="$AWS_ACCESS_KEY_ID" \
                AWS_SECRET_ACCESS_KEY="$AWS_SECRET_ACCESS_KEY" \
                AWS_REGION="$AWS_REGION" \
                S3_BUCKET_NAME="$S3_BUCKET_NAME" \
                DATASET_FILE="$DATASET_FILE" \
                ./venv/bin/python app.py > app.log 2>&1 &

                sleep 5

                echo "===== APP LOG ====="
                cat app.log || true

                echo "===== RUNNING PROCESS ====="
                ps -ef | grep app.py || true

                echo "===== PORT STATUS ====="
                ss -tuln | grep 5000 || true
                '''
            }
        }
    }
}
