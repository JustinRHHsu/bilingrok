#!/bin/bash
# 設定檔娛權限 chmod +x setup_gcloud.sh
# 執行檔案    ./setup_gcloud.sh

PROJECT_ID="photo-studio-435402"
GCP_REGION="us-central1"
NEW_SERVICE_ACCOUNT_NAME="sa-ci-cd-photo-studio"
NEW_SERVICE_ACCOUNT_DESCRIPTION="SA_Photo Studio"
NEW_SERVICE_ACCOUNT_DISPLAY_NAME="Photo Studio Service Account"
GITHUB_OWNER="JustinRHHsu"
GITHUB_REPO="photo-studio"
CONNECTION_NAME="github-photo-studio-cloudbuild"
TRIGGER_NAME="git-push"

# Login to Google Cloud
echo "Starting Google Cloud login…"
gcloud auth login
echo "Google Cloud login completed"

# Configure the project
echo "Setting Google Cloud Project to $PROJECT_ID"
gcloud config set project $PROJECT_ID
echo "Google Cloud Project set to $PROJECT_ID"

# Initialize Google Cloud
echo "Initializing Google Cloud"
gcloud init
echo "Google Cloud initialized"


# Enable Google Cloud APIs
echo "Enabling Google Cloud Project APIs"
gcloud services enable storage.googleapis.com
echo "Enabled storage.googleapis.com"
gcloud services enable cloudbuild.googleapis.com
echo "Enabled cloudbuild.googleapis.com"
gcloud services enable artifactregistry.googleapis.com
echo "Enabled artifactregistry.googleapis.com"
gcloud services enable run.googleapis.com
echo "Enabled run.googleapis.com"
gcloud services enable secretmanager.googleapis.com
echo "Enabled secretmanager.googleapis.com"
echo "Google Cloud Project APIs enabled"


# Create a new service account
echo "Creating a new service account"
gcloud iam service-accounts create $NEW_SERVICE_ACCOUNT_NAME \
  --description="$NEW_SERVICE_ACCOUNT_DESCRIPTION" \
  --display-name="$NEW_SERVICE_ACCOUNT_DISPLAY_NAME"
echo "New service account created"

# Get the email address of the new service account
echo "Getting the email address of the new service account"
NEW_SERVICE_ACCOUNT_EMAIL="$NEW_SERVICE_ACCOUNT_NAME@$PROJECT_ID.iam.gserviceaccount.com"
echo "New service account email address: $NEW_SERVICE_ACCOUNT_EMAIL"


# Permission Setup
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:$NEW_SERVICE_ACCOUNT_EMAIL" \
  --role='roles/editor' \
  --condition=None
  
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:$NEW_SERVICE_ACCOUNT_EMAIL" \
  --role="roles/cloudbuild.builds.editor" \
  --condition=None

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:$NEW_SERVICE_ACCOUNT_EMAIL" \
  --role="roles/cloudbuild.connectionAdmin" \
  --condition=None

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:$NEW_SERVICE_ACCOUNT_EMAIL" \
  --role="roles/artifactregistry.writer" \
  --condition=None

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:$NEW_SERVICE_ACCOUNT_EMAIL" \
  --role="roles/logging.logWriter" \
  --condition=None

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:$NEW_SERVICE_ACCOUNT_EMAIL" \
  --role="roles/storage.admin" \
  --condition=None

gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:$NEW_SERVICE_ACCOUNT_EMAIL" \
    --role="roles/secretmanager.admin" \
    --condition=None

gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:$NEW_SERVICE_ACCOUNT_EMAIL" \
    --role="roles/secretmanager.admin" \
    --condition=None

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:$NEW_SERVICE_ACCOUNT_EMAIL" \
  --role="roles/source.reader" \
  --condition=None

gcloud projects add-iam-policy-binding photo-studio-435402 \
  --member="serviceAccount:sa-photo-studio@photo-studio-435402.iam.gserviceaccount.com" \
  --role="roles/secretmanager.secretAccessor"

echo "Permission setup completed"

#####################################################
# 目前 Host Connection 和 Trigger 建立都有問題，待處理！
#####################################################
# Create a Host Connection
# echo "Creating a Host Connection"
# gcloud builds connections create github $CONNECTION_NAME \
#     --region="$GCP_REGION"
# echo "Host Connection created"


# Link Repository
# echo "Linking Repository"
# gcloud builds repositories create photo-studio \
#      --remote-uri="https://github.com/JustinRHHsu/photo-studio.git" \
#      --connection="github-cloudbuild" \
#      --region="us-central1"
# echo "Repository linked"

# 目前 GCP 不讓新客戶使用 Source Repositories，所以要用 GitHub 連接
# gcloud builds triggers create github \
#   --name="$TRIGGER_NAME" \
#   --repository="projects/$PROJECT_ID/locations/$GCP_REGION/connections/$CONNECTION_NAME/repositories/$GITHUB_REPO" \
#   --branch-pattern="^main$" \
#   --build-config="cloudbuild.yaml" \
#   --region="$GCP_REGION"
