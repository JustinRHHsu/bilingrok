# This script is used to run the service with Docker locally.
# 
# Please Run service with below command:
# 
# chmod +x scripts/local_linebot-flask_with_docker.sh
# ./scripts/local_linebot-flask_with_docker.sh
#
# Then, use postman to test the API service with below URL

# 更改工作目錄到 /photo-studio/linebot-flask
cd "$(dirname "$0")/.."

# 設定變數
IMAGE_NAME="bilingrok"
CONTAINER_NAME="linebot-bilingrok"
HOST_PORT=5000
CONTAINER_PORT=5000
DOCKERFILE="Dockerfile"
IMAGE_TAG="v0.0.1"
ENV_PATH="/Users/JustinHsu/aiagent/grok-lang-companion/config/.env"

# 顯示執行訊息
echo "Starting linebot flask app with Docker..."

# 建立 Docker image
echo "Starting Docker build..."
docker build -t $IMAGE_NAME:$IMAGE_TAG . -f $DOCKERFILE --progress=plain
echo "Docker build completed"

# 檢查是否有同名容器在運行
if [ "$(docker ps -q -f name=$CONTAINER_NAME)" ]; then
    echo "Stopping existing container..."
    docker stop $CONTAINER_NAME
    docker rm $CONTAINER_NAME  # 刪除已停止的容器
fi

# 檢查是否有同名已停止的容器
if [ "$(docker ps -a -q -f name=$CONTAINER_NAME)" ]; then
    echo "Removing existing container..."
    docker rm $CONTAINER_NAME
fi

# 運行容器 -d: 在背景運行
docker run \
    --name $CONTAINER_NAME \
    -p $HOST_PORT:$CONTAINER_PORT \
    --env-file $ENV_PATH \
    $IMAGE_NAME:$IMAGE_TAG
    