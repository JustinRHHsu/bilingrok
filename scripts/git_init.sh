# Operation command: bash ./scripts/git_init.sh
# 再次確認下方參數
GIT_ACCOUNT="JustinRHHsu"
REPO_NAME="bilingrok"
REMOTE_URL="https://github.com/$GIT_ACCOUNT/$REPO_NAME.git"
REPO_VISIBILITY="private" # --public  --private
REPO_SOURCE="."
REPO_REMOTE="origin"
DEFAULT_BRANCH="main"

# 開文件執行權限 chmod +x ./scripts/git_init.sh
# 執行此腳本文件 ./scripts/git_init.sh

####################
# 執本執行任務如下：
# 1. 檢查是否已安裝 GitHub CLI
# 2. 檢查遠端儲存庫是否存在
# 3. 初始化 Git 儲存庫
# 4. 使用 GitHub CLI 創建遠端儲存庫
# 5. 推送本地分支到遠端儲存庫
####################

# 定義顏色
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color


# 1. 檢查是否已安裝 GitHub CLI
# 檢查是否已安裝 GitHub CLI
if ! command -v gh &> /dev/null; then
  echo -e "${GREEN}安裝 GitHub CLI...${NC}"
  if brew install gh; then
    echo -e "${GREEN}成功: 安裝 GitHub CLI${NC}"
  else
    echo -e "${RED}錯誤: 安裝 GitHub CLI 失敗${NC}"
    exit 1
  fi
else
  echo -e "${GREEN}GitHub CLI 已安裝${NC}"
fi


# 2. 檢查遠端儲存庫是否存在
if gh repo view $GIT_ACCOUNT/$REPO_NAME &> /dev/null; then
  echo -e "${GREEN}遠端儲存庫已存在${NC}"
else
  # 3. 初始化 Git 儲存庫
  if git init; then
    echo -e "${GREEN}成功: 初始化 Git 儲存庫${NC}"
  else
    echo -e "${RED}錯誤: 初始化 Git 儲存庫失敗${NC}"
    exit 1
  fi

  # 確保 GitHub CLI 已登錄
  if ! gh auth status &> /dev/null; then
    echo -e "${YELLOW}GitHub CLI 尚未登錄，正在登錄...${NC}"
    if ! (echo "GitHub.com" && echo "HTTPS" && echo "" && echo "" && echo "" && echo "" && echo "") | gh auth login; then
      echo -e "${RED}錯誤: GitHub CLI 登錄失敗${NC}"
      exit 1
    else
      echo -e "${GREEN}成功: GitHub CLI 登錄成功${NC}"
    fi
  else
    echo -e "${GREEN}GitHub CLI 已登錄${NC}"
  fi

  # 4. 使用 GitHub CLI 創建遠端儲存庫
  if gh repo create $REPO_NAME --$REPO_VISIBILITY --source=$REPO_SOURCE --remote=$REPO_REMOTE; then
    echo -e "${GREEN}成功: 創建遠端儲存庫${NC}"
  else
    echo -e "${RED}錯誤: 創建遠端儲存庫失敗${NC}"
    exit 1
  fi
fi


# 5. 推送本地分支到遠端儲存庫
echo -e "${YELLOW}是否推送本地分支到遠端儲存庫？ (Y/N)${NC}"
read -r answer
if [[ "$answer" =~ ^[Yy]$ ]]; then
  # 檢查是否有分支存在，若無則建立一個新的分支
  current_branch=$(git rev-parse --abbrev-ref HEAD)
  if [ "$current_branch" == "HEAD" ]; then
    git checkout -b "$DEFAULT_BRANCH"
    current_branch="$DEFAULT_BRANCH"
  fi

  # 確保有至少一次提交
  if [ -z "$(git log -1 --pretty=%B)" ]; then
    git commit --allow-empty -m "Initial commit"
  fi
  
  # 推送本地分支到遠端儲存庫
  if git push -u origin "$current_branch"; then
    echo -e "${GREEN}成功: 推送本地分支到遠端儲存庫${NC}"
  else
    echo -e "${RED}錯誤: 推送本地分支到遠端儲存庫失敗${NC}"
    exit 1
  fi
else
  echo -e "${YELLOW}已取消推送本地分支到遠端儲存庫${NC}"
  exit 0
fi