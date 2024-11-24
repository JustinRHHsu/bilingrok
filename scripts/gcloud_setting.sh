# Operation command: bash ./scripts/gcloud_setting.sh
# 再次確認下方參數
# 設定 .env 文件的路徑變數
ENV_FILE_PATH="./config/.env"
# 啟用所需的 GCP 服務
SERVICE_FILE_PATH="./scripts/gcloud_service_enable_lists.txt"
CONFIG_FILE_PATH="./config/config.yaml"
ROLES_FILE_PATH="./scripts/gcloud_iam.txt"

# 開文件執行權限 chmod +x ./scripts/gcloud_setting.sh
# 執行此腳本文件 ./scripts/gcloud_setting.sh

####################
# 執本執行任務如下：
# 1. 讀入 config.yaml 和 .env 文件
# 2. 登入 gcloud
# 3. 設定 GCP project
# 4. 確認當前 gcloud 設定
# 5. 啟動專案所需的 gcloud services
# 6. 同步 .env 文件到 gcloud secret manager
# 7. 創建 service account 和設置權限
####################

# 定義顏色
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# 1. 讀入 config.yaml 和 .env 文件
echo "=========================="
echo "1. 讀取 config.yaml 文件"
if [ -f "$CONFIG_FILE_PATH" ]; then
  GCP_PROJECT_ID=$(grep 'GCP_PROJECT_ID:' "$CONFIG_FILE_PATH" | awk '{print $2}')
  SERVICE_ACCOUNT_NAME=$(grep 'SERVICE_ACCOUNT_NAME:' "$CONFIG_FILE_PATH" | awk '{print $2}')
  SERVICE_ACCOUNT_DESCRIPTION=$(grep 'SERVICE_ACCOUNT_DESCRIPTION:' "$CONFIG_FILE_PATH" | awk -F': ' '{print $2}')
  SERVICE_ACCOUNT_DISPLAY_NAME=$(grep 'SERVICE_ACCOUNT_DISPLAY_NAME:' "$CONFIG_FILE_PATH" | awk -F': ' '{print $2}')
  echo -e "${GREEN}成功: 讀取 config.yaml 文件${NC}"
  echo "GCP_PROJECT_ID: $GCP_PROJECT_ID"
  echo "SERVICE_ACCOUNT_NAME: $SERVICE_ACCOUNT_NAME"
  echo "SERVICE_ACCOUNT_DESCRIPTION: $SERVICE_ACCOUNT_DESCRIPTION"
  echo "SERVICE_ACCOUNT_DISPLAY_NAME: $SERVICE_ACCOUNT_DISPLAY_NAME"
else
  echo -e "${RED}錯誤: config.yaml 文件不存在或無法讀取${NC}"
  exit 1
fi

# Load .env file and set variables in the environment
if [ -f "$ENV_FILE_PATH" ]; then
  export $(grep -v '^#' "$ENV_FILE_PATH" | xargs)
  echo -e "${GREEN}成功: 讀取 .env 文件${NC}"
else
  echo -e "${RED}錯誤: .env 文件不存在或無法讀取${NC}"
  exit 1
fi

# 2. 登入 gcloud
# 確認 gcloud 登入並設定專案
echo "=========================="
echo "2. 登入 gcloud"
echo "正在進行 gcloud 登入..."
if gcloud auth login; then
  echo -e "${GREEN}成功: gcloud 登入成功${NC}"
else
  echo -e "${RED}錯誤: gcloud 登入失敗${NC}"
  exit 1
fi

# 3. 設定 GCP project
echo "=========================="
echo "3. 設定 GCP project"
echo "正在設定 GCP 專案為 '$GCP_PROJECT_ID'..."
if gcloud config set project $GCP_PROJECT_ID; then
  echo -e "${GREEN}成功: GCP Project ID 設定成功${NC}"
else
  echo -e "${RED}錯誤: GCP Project ID 設定失敗${NC}"
  exit 1
fi

# 4. 確認當前 gcloud 設定
# 顯示 gcloud 設定資訊
echo "=========================="
echo "4. 確認當前 gcloud 專案設定"
echo "顯示當前登入的帳戶..."
gcloud config get-value account

echo "顯示當前設定的 GCP 專案..."
gcloud config get-value project

# 5. 啟動專案所需的 gcloud services
# 啟動 gcloud 服務
echo "=========================="
echo "5. 啟動專案所需的 gcloud services"
if [ -f "$SERVICE_FILE_PATH" ]; then
  echo "開始啟用 gcloud 相關服務..."
  while IFS= read -r service; do
    # 忽略註解行
    if [[ $service == \#* ]] || [[ -z $service ]]; then
      continue
    fi
    if gcloud services enable "$service"; then
      echo -e "${GREEN}成功: 啟用 $service 服務${NC}"
    else
      echo -e "${RED}錯誤: 啟用 $service 服務失敗${NC}"
      exit 1
    fi
  done < "$SERVICE_FILE_PATH"
  echo -e "${GREEN}成功: 所有服務啟用完成${NC}"
else
  echo -e "${RED}錯誤: gcloud_service_enable_lists.txt 文件不存在或無法讀取${NC}"
  exit 1
fi

# 6. 同步 .env 文件到 gcloud secret manager
# 同步 .env 文件到 gcloud secret manager
echo "=========================="
echo "6. 同步 .env 文件到 gcloud secret manager"
# 初始化結果變數
results=()

# 讀取 .env 文件並上傳到 gcloud secret manager
while IFS= read -r line; do
  # 跳過以 # 開頭的行
  if [[ $line == \#* ]]; then
    continue
  fi

  # 解析環境變數名稱和值
  IFS='=' read -r key value <<< "$line"

  # 上傳到 gcloud secret manager
  if [[ -n $key && -n $value ]]; then
    temp_file=$(mktemp)
    echo "$value" > "$temp_file"
    if gcloud secrets describe "$key" &> /dev/null; then
      # 如果 secret 已存在，則更新值
      if gcloud secrets versions add "$key" --data-file="$temp_file"; then
        results+=("${GREEN}成功: 更新 $key${NC}")
      else
        results+=("${RED}錯誤: 更新 $key 失敗${NC}")
      fi
    else
      # 如果 secret 不存在，則創建
      if gcloud secrets create "$key" --data-file="$temp_file" --replication-policy="automatic"; then
        results+=("${GREEN}成功: 創建 $key${NC}")
      else
        results+=("${RED}錯誤: 創建 $key 失敗${NC}")
      fi
    fi
    rm "$temp_file"
  fi
done < "$ENV_FILE_PATH"

# 輸出總結
echo "====== 上傳結果總結 ======"
for result in "${results[@]}"; do
  echo -e "$result"
done


# 7. 創建新的服務帳戶並設置權限
echo "=========================="
echo "7. 創建新的服務帳戶並設置權限"
echo "Creating a new service account"

# 檢查服務帳戶是否已存在
if gcloud iam service-accounts list --filter="email:$SERVICE_ACCOUNT_NAME@$GCP_PROJECT_ID.iam.gserviceaccount.com" --format="value(email)" | grep -q "$SERVICE_ACCOUNT_NAME@$GCP_PROJECT_ID.iam.gserviceaccount.com"; then
  echo -e "${YELLOW}警告: 服務帳戶已存在，跳過創建步驟${NC}"
else
  if gcloud iam service-accounts create $SERVICE_ACCOUNT_NAME \
    --description="$SERVICE_ACCOUNT_DESCRIPTION" \
    --display-name="$SERVICE_ACCOUNT_DISPLAY_NAME"; then
    echo -e "${GREEN}成功: 新服務帳戶已創建${NC}"
  else
    echo -e "${RED}錯誤: 新服務帳戶創建失敗${NC}"
    exit 1
  fi
fi

# 獲取新服務帳戶的電子郵件地址
echo "Getting the email address of the new service account"
SERVICE_ACCOUNT_EMAIL="$SERVICE_ACCOUNT_NAME@$GCP_PROJECT_ID.iam.gserviceaccount.com"
echo "New service account email address: $SERVICE_ACCOUNT_EMAIL"

# 設置權限
echo "Setting permissions for the new service account"
if [ -f "$ROLES_FILE_PATH" ]; then
  while IFS= read -r role; do
    # 忽略註解行和空白行
    if [[ $role == \#* ]] || [[ -z $role ]]; then
      continue
    fi
    if gcloud projects add-iam-policy-binding $GCP_PROJECT_ID \
      --member="serviceAccount:$SERVICE_ACCOUNT_NAME@$GCP_PROJECT_ID.iam.gserviceaccount.com" \
      --role="$role"; then
      echo -e "${GREEN}成功: 設置 $role 權限${NC}"
    else
      echo -e "${RED}錯誤: 設置 $role 權限失敗${NC}"
      exit 1
    fi
  done < "$ROLES_FILE_PATH"
  echo -e "${GREEN}成功: 所有權限設置完成${NC}"
else
  echo -e "${RED}錯誤: gcloud_iam.txt 文件不存在或無法讀取${NC}"
  exit 1
fi