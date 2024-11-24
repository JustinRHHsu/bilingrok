# Operation command: bash ./scripts/docker_build_and_run.sh
# 再次確認下方參數

# Docker Image 設定
IMAGE_NAME="bilingrok"
IMAGE_VERSION="v0.0.1"
DOCKERFILE_PATH="."
DOCKERFILE_NAME="Dockerfile"

# Docker Container 設定
CONTAINER_NAME="bilingrok"
HOST_PORT="5000"
CONTAINER_PORT="5000"
ENV_FILE="config/.env"

# 開文件執行權限 chmod +x ./scripts/docker_build_and_run.sh
# 執行此腳本文件 ./scripts/docker_build_and_run.sh

####################
# 執本執行任務如下：
# 1. Build Docker Image
# 2. Run Docker Image
####################

# 定義顏色
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color


# 1. Build Docker Image
# 建立 Docker image
docker build -t $IMAGE_NAME:$IMAGE_VERSION -f $DOCKERFILE_PATH/$DOCKERFILE_NAME $DOCKERFILE_PATH

# 確認是否成功建立
if [ $? -eq 0 ]; then
  echo -e "${GREEN}Docker image $IMAGE_NAME:$IMAGE_VERSION 建立成功${NC}"
else
  echo -e "${RED}錯誤: Docker image $IMAGE_NAME:$IMAGE_VERSION 建立失敗${NC}"
  exit 1
fi


# 2. Run Docker Image
# 檢查是否有同名的 container
if [ "$(docker ps -aq -f name=$CONTAINER_NAME)" ]; then
  echo -e "${YELLOW}警告: 已存在同名的 container，將其刪除${NC}"
  docker rm -f $CONTAINER_NAME
  if [ $? -eq 0 ]; then
    echo -e "${GREEN}成功: 已刪除同名的 container${NC}"
  else
    echo -e "${RED}錯誤: 刪除同名的 container 失敗${NC}"
    exit 1
  fi
fi

# 執行 Docker container
docker run -d -p $HOST_PORT:$CONTAINER_PORT --name $CONTAINER_NAME --env-file $ENV_FILE $IMAGE_NAME:$IMAGE_VERSION

# 確認是否成功建立
if [ $? -eq 0 ]; then
  echo -e "${GREEN}Docker image $IMAGE_NAME:$IMAGE_VERSION 建立成功${NC}"
else
  echo -e "${RED}錯誤: Docker image $IMAGE_NAME:$IMAGE_VERSION 建立失敗${NC}"
  exit 1
fi