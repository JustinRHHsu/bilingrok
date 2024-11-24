

# Overall #
啟動一個新專案時，需要：


# 說明 #

啟動一個新專案時，都會有一個 './config' 資料夾
- config
-- .env 環境變數
-- config.yaml 專案參數
-- config.py 初始化程式
'config.py' 會把 .env 和 config.yaml 的環境變數和專案參數讀取並初始化







# 建立虛擬環境 (OK)
1. 建立專案虛擬環境 `python3.10 -m venv venv`
2. 啟動虛擬環境 `source venv/bin/activate`
3. 檢查 python 執行環境 `which python`
    -- 路徑是否在專案 venv 內
4. 檢查 python 執行版本 `python --version`
    -- 版本是否正確
5. 設置 vscode 的 python 執行環境
    - `ctrl+shift+p` 選擇 `>Python Select Interpreter` 
    - 確認設置是 `python3.10.15(venv)`
6. (選項)刪除 venv，重新建立虛擬環境 `rm -rf venv`


# 安裝依賴項 (OK)
1. 先安裝通用的依賴項 packages
    - 檢查 `./scripts/dependency_packages.txt` 列出常用的 dependency packages (也可以直接 `pip install -r dependency_packages.txt` 安裝)
    - 權限 `chmod +x ./scripts/install_general_packages.sh`
    - 執行 `./scripts/install_general_packages.sh`
2. 再邊開發邊安裝 `pip install package_name`
3. 若有完整的 requirements.txt，直接執行 `pip install -r requirements.txt`


# 建立依賴項安裝檔清單 (OK)
- 安裝 `pip install pipreqs`
- `pipreqs . --force` 將專案虛擬環境中，已安裝的套件，輸出成 requirements.txt --force 強制覆蓋
- (選項)`pip freeze>requirements.txt`



# 開發



# gcloud 專案設定 (剩部署到雲端待測試)
gcloud_setting.sh 
目標：設定 gcloud 所需的服務和權限
1. 讀入 config.yaml 和 .env 文件
2. 登入 gcloud
3. 設定 GCP project
4. 確認當前 gcloud 設定
5. 啟動專案所需的 gcloud services
6. 同步 .env 文件到 gcloud secret manager
7. 創建 service account 和設置權限

更新範圍：
1. 更新專案參數  `config.yaml`
2. 更新本地環境變數 `.env`
3. 安裝 package `dependency_packages.txt`
4. 啟用 service `gcloud_service_enable_lists.txt`
5. 更新 iam 權限 `gcloud_iam.txt`

更新參數：
1. `./config/config.yaml` 更新環境參數
    - DEBUG_MODE: True       # True, False
    - SECRET_KEY_ENV: LOCAL  # GCP, LOCAL
    - ENVIRONMENT: DEV       # DEV, PROD
2. `./scripts/gcloud_setting.sh` 檢查參數

開文件執行權限 chmod +x ./scripts/gcloud_setting.sh
執行此腳本文件 ./scripts/gcloud_setting.sh



# 建立 .Dockerfile 和 .dockerignore
1. 自動產生
    - `ctrl+shift+p` 選擇 `>Docker: Add Dockerfile to Workspace` 
2. 檢查 .Dockerfile
    -  OS, EXPOSE
3. 更新 .dockerignore
    - 語法
        - **/temp            ：忽略所有目錄中的 temp 目錄
        - **/secrets.dev.yaml：忽略所有目錄中的 secrets.dev.yaml 文件
        - *.log              ：忽略所有 .log 文件
        - .env               ：忽略所有 .env 文件
        - path/to/folder/*   ：忽略 logs 資料夾底下的所有檔案
    - 常用
        - __*/               ：忽略 __ 開頭的資料夾
        - .*/*               ：忽略 . 開頭的資料夾
        - sa-*/*
        - **/venv
        - **/scripts
        - **.gitignore
        - **.dockerignore



# Docker Build and Run (OK)
docker_build_and_run.sh
目標：設定 gcloud 所需的服務和權限
1. Build Docker Image
2. Run Docker Image

更新參數：
1. `./config/config.yaml` 更新環境參數
    - DEBUG_MODE: True       # True, False
    - SECRET_KEY_ENV: LOCAL  # GCP, LOCAL
    - ENVIRONMENT: DEV       # DEV, PROD
2. `./scripts/docker_build_and_run.sh` 檢查參數

開文件執行權限 chmod +x ./scripts/docker_build_and_run.sh
執行此腳本文件 ./scripts/docker_build_and_run.sh



# Git
git_init.sh
目標：設定 gcloud 所需的服務和權限
1. Build Docker Image
2. Run Docker Image




# Cloud Build


# Cloud Deply


# Domain Name Setting