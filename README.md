# User Analytics Dashboard

## Project Overview
This project is a Flask dashboard for a university DevOps end-term assignment. It loads a dataset from AWS S3 when the local file is missing and otherwise uses the local copy.

## Folder Structure
- app.py: Flask application entry point
- analysis.py: Dataset loading and S3 download logic
- templates/index.html: Dashboard layout
- static/style.css: Dark blue dashboard styling
- static/script.js: Counter and Chart.js rendering logic
- data/u.user: Local dataset file
- screenshots/: Placeholder directory for screenshots

## Requirements
- Flask
- Pandas
- boto3

## Installation
```bash
pip install -r requirements.txt
```

## AWS Configuration
Set the following environment variables before running the app:

```bash
set AWS_ACCESS_KEY_ID=your_access_key
set AWS_SECRET_ACCESS_KEY=your_secret_key
set AWS_REGION=ap-south-1
set S3_BUCKET_NAME=your_bucket_name
set DATASET_FILE=u.user
```

## How to Run
```bash
python app.py
```
Then open http://127.0.0.1:5000 in your browser.

## Screenshots Placeholder
Add screenshots to the screenshots folder after running the app.
