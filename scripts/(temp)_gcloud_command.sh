#!/bin/bash
# chmod +x ./utils/scripts/gcloud_command.sh
# utils/scripts/gcloud_command.sh


if gcloud config set project bilingrok; then
  echo "成功設定 GCP 專案"
else
  echo "設定 GCP 專案失敗"
  exit 1
fi

# 啟用所需的 GCP 服務
if gcloud services enable firestore.googleapis.com; then
  echo "成功啟用 Firestore 服務"
else
  echo "啟用 Firestore 服務失敗"
  exit 1
fi

if gcloud services enable cloudfunctions.googleapis.com; then
  echo "成功啟用 Cloud Functions 服務"
else
  echo "啟用 Cloud Functions 服務失敗"
  exit 1
fi

# 獲取腳本所在的目錄
SCRIPT_DIR=$(dirname "$0")

# 載入 .env 文件中的變數
if [ -f "$SCRIPT_DIR/../../config/.env" ]; then
  source "$SCRIPT_DIR/../../config/.env"
else
  echo ".env 文件不存在或無法讀取"
  exit 1
fi

# 檢查是否成功讀取到變數
if [ -z "$QUEUE_MESSAGE_STORE" ] || [ -z "$QUEUE_LOCATION_MESSAGE_STORE" ] || [ -z "$GCP_PROJECT_ID" ]; then
  echo "未能從 .env 文件中讀取到必要的變數"
  exit 1
fi



### Script 1 - 建立 Cloud Tasks 的佇列 ###

# 設定變數
GCP_PROJECT_ID=$GCP_PROJECT_ID
QUEUE_NAME=$QUEUE_MESSAGE_STORE
LOCATION=$QUEUE_LOCATION_MESSAGE_STORE

# 檢查 queue 是否存在
EXISTING_QUEUE=$(gcloud tasks queues describe $QUEUE_NAME --location=$LOCATION --project=$GCP_PROJECT_ID --format="value(name)")


# 如果 queue 不存在，則建立它
if [ -z "$EXISTING_QUEUE" ]; then
  echo "Queue '$QUEUE_NAME' 不存在，正在建立..."
  if gcloud tasks queues create $QUEUE_NAME --location=$LOCATION --project=$GCP_PROJECT_ID; then
    echo "Queue '$QUEUE_NAME' 已建立。"
  else
    echo "Queue '$QUEUE_NAME' 建立失敗。"
    exit 1
  fi
else
  echo "Queue '$QUEUE_NAME' 已存在。"
fi