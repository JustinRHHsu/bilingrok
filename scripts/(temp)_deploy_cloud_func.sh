#!/bin/bash
# chmod +x ./utils/scripts/deploy_cloud_func.sh
# utils/scripts/deploy_cloud_func.sh



: <<'EOF'
# 本地端測試
gcloud auth login
gcloud config set project bilingrok
gcloud config list project
gcloud config get-value project
gcloud config get-value account

functions-framework --target=add_chat_history --source=cloud_function/save_linebot_message/main.py --debug

curl -X POST http://127.0.0.1:8080 \
     -H "Content-Type: application/json" \
     -d '{
           "role": "user",
           "user_id": "U545e0dd39d2a2ce9a1aabae6ca0b20ed",
           "message": "Hello, world!",
           "timestamp": "2024-11-20T14:02:56Z",
           "reply_token": "abcd1234"
         }'


# 部署到雲端
# chmod +x ./utils/scripts/deploy_cloud_func.sh
# utils/scripts/deploy_cloud_func.sh

# 部署後測試
curl -X POST https://asia-east1-bilingrok.cloudfunctions.net/add_chat_history \
     -H "Content-Type: application/json" \
     -d '{
           "role": "user",
           "user_id": "U545e0dd39d2a2ce9a1aabae6ca0b20ed",
           "message": "Test from Postman! - v1",
           "timestamp": "{{timestamp}}",
           "reply_token": "abcd1234"
         }'

EOF



# 設定參數
REGION="asia-east1"
FUNCTION_NAME="add_chat_history"
RUNTIME="python310"
TRIGGER="--trigger-http"
ENTRY_POINT="add_chat_history"
ALLOW_UNAUTH="--allow-unauthenticated"
SOURCE_PATH="cloud_function/save_linebot_message"
GCP_PROJECT_ID="bilingrok"


# 確保已經使用 gcloud 命令行工具進行了身份驗證
gcloud auth login

# 部署 Cloud Function
gcloud functions deploy $FUNCTION_NAME \
    --runtime $RUNTIME \
    $TRIGGER \
    $ALLOW_UNAUTH \
    --entry-point $ENTRY_POINT \
    --region $REGION \
    --source $SOURCE_PATH \
    --set-env-vars GCP_PROJECT_ID=$GCP_PROJECT_ID