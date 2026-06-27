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
                # Stop any previous Flask process safely.
                pkill -f "app.py" || true
                sleep 2

                # Start the application with the virtual environment Python.
                nohup env \
                    AWS_ACCESS_KEY_ID="$AWS_ACCESS_KEY_ID" \
                    AWS_SECRET_ACCESS_KEY="$AWS_SECRET_ACCESS_KEY" \
                    AWS_REGION="$AWS_REGION" \
                    S3_BUCKET_NAME="$S3_BUCKET_NAME" \
                    DATASET_FILE="$DATASET_FILE" \
                    venv/bin/python app.py > app.log 2>&1 &

                sleep 5

                # Print the deployment log for debugging.
                echo "--- app.log ---"
                cat app.log || true

                # Show running Flask process.
                echo "--- Running processes ---"
                ps -ef | grep app.py | grep -v grep || true

                # Show whether port 5000 is listening.
                echo "--- Port 5000 ---"
                ss -tulnp | grep 5000 || true

                # Fail the job if the application did not start.
                if ! ps -ef | grep "app.py" | grep -v grep > /dev/null; then
                    echo "Flask app failed to start. See app.log for details."
                    exit 1
                fi
                '''
            }
        }
    }
}
