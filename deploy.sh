#!/bin/bash

PROJECT_ID="unified-api-440308"
IMAGE_NAME="unified-api:latest"
REGION="asia-south1"
SERVICE_NAME="unified-api"

gcloud config set project $PROJECT_ID
gcloud services enable run.googleapis.com
gcloud services enable artifactregistry.googleapis.com
gcloud services enable containerregistry.googleapis.com

docker build -t $IMAGE_NAME .
docker tag $IMAGE_NAME asia.gcr.io/$PROJECT_ID/$IMAGE_NAME
docker push asia.gcr.io/$PROJECT_ID/$IMAGE_NAME

gcloud run deploy $SERVICE_NAME \
  --image asia.gcr.io/$PROJECT_ID/$IMAGE_NAME \
  --platform managed \
  --region $REGION \
  --allow-unauthenticated

SERVICE_URL=$(gcloud run services describe $SERVICE_NAME --region $REGION --format "value(status.url)")

echo "Deployment complete! Service URL: $SERVICE_URL"
