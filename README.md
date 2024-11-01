
# Unified api (FastAPI)

A well strucutred FastAPI backend with Firestore database.

API documentation link -  https://unified-api-k4oqfffqma-el.a.run.app/redoc
\
Swagger link -  https://unified-api-k4oqfffqma-el.a.run.app/docs`

## Requirements
- Docker installed in local system (For windows users)
- Firestore database created in Google Cloud.
- Service account file from GCP. 

## Installation and run locally
### 1. Linux

```bash
# Create python virtual environment
python3 -m venv venv

# Activate the python virtual environment
source venv/bin/activate

# Install the requirements for the project into the virtual environment
pip3 install -r requirements.txt

# Run app locally
uvicorn main:app --reload
```

### 2. Windows
Run this project with docker only in windows
```bash
# Build dokcer image
docker build -t unified-app:latest .

# Run the container to start the app
docker run -p 8080:8080 --rm -d --name unfied-api unified-app:latest

```


### Deployment 

This project is deployed on Google Cloud Run (GCP Cloud Run) which is a managed compute platform that allows users to run containers on Google's infrastructure.

To deploy this project in GCP Cloud Run you need to run deploy.sh file.