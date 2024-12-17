

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




# gcloud 專案設定 (OK)
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



# 建立 .gitignore (OK)
建立 .gitignore
- 語法
    - *.log              ：忽略特定文件
    - **/temp            ：忽略特定目錄
    - folder_name/       ：忽略 logs 資料夾底下的所有檔案
    - *$py.class         ：忽略特定文件類型，忽略所有以 $py.class 結尾的文
    - .vscode            ：忽略特定工具或編輯器的設定文件
    - __pycache__        ：忽略特定模式的文件
- 常用
    - __pycache__
    - .vscode
    - .env
    - sa-*
    - .gitignore
- 用 git 特定情況指令
    - `git rm -r --cached .`    :清除 Git 的快取，讓 Git 重新應用 .gitignore 規則
    - `git add .`               :把 .根目錄底下的變更，添加到 stage 暫存區 `command+G+S`
    - `git commit -m "message"` :提交變更                              `command+G+C`
    - `git push origin <branch>`:推送到遠端 repo                       `command+G+P`


# 初始化 git (OK)
git_init.sh
目標：設定 gcloud 所需的服務和權限
1. 檢查是否已安裝 GitHub CLI
2. 檢查遠端儲存庫是否存在
3. 初始化 Git 儲存庫
4. 使用 GitHub CLI 創建遠端儲存庫
5. 推送本地分支到遠端儲存庫


# 開發階段使用 git 管理 (OK)
- 初始化 Git 儲存庫 `git init`
- 設定使用者名稱 `git config --global user.name "Your Name"`
- 設定使用者電子郵件 `git config --global user.email "your.email@example.com"`
- 檢查 Git 狀態 `git status`
- 添加文件到暫存區 `git add .`
- 提交變更 `git commit -m "Your commit message"`
- 查看提交歷史 `git log`
- 推送本地 main 分支到遠端儲存庫 `git push -u origin main`
- clone 遠端儲存庫到本地 `git clone https://github.com/YourUsername/YourRepository.git`
- 從遠端儲存庫拉取變更  `git pull origin main`

# Developer Day to Day (OK)
O. VSCode 快速鍵
    `command+g+s` + `command+g+m` + `command+g+c` + `command+g+p`
A. 開始新功能或修復 bug 前
- 本地創建新分支                     `git checkout -b feature/new-feature`  or `hotfix/issue-number` or `bugs/issue-number`
- 切換到該分支                       `git checkout feature/new-feature`
B. 開發和提交變更
- 添加文件到暫存區                    `git add .`
- 提交變更                           `git commit -m "Add new feature"`
- 發佈分支 (Publish Branch)
C. 拉取最新的 main 分支變更
- 切換分支                           `git checkout main`
- 先從遠端拉取最新的 main 分支變更      `git pull origin main`      TBD
D. 合併分支
- 切換分支                          `git checkout feature/new-feature`
- 將 main 分支的最新變更合併到你的分支  `git merge main`            TBD
E. 解決衝突
- 合併過程中出現衝突，手動解決衝突後，標記為已解決並提交    `git add .`
- 提交變更                                          `git commit -m "Resolve merge conflicts"`
F.推送分支到遠端儲存庫 (開發到一個段落/結束每天工作任務時)
- 將你的分支推送到遠端儲存庫              `git push origin feature/new-feature`
G. 創建 Pull Request 、代碼審查、合併 (TBD)
- Create a Pull Request
- Merge Pull Request
- Create Merge Commit
- Delete Branch
- 從 Github 平台中點選 Pull Request，向 Tech Lead 請求合併到 main 分支中
- 代碼審查、合併
H. 合併完成後，才可以刪除本地和遠端分支
- 刪除本地分支      `git branch -d feature/new-feature`
- 刪除遠端分支      `git push origin -delete feature/new-feature`
I. 更新本地 main 分支
- 切換分支      `git checkout main`
- 拉取最新變更   `git pull origin main`
註：new-feature 未開發和測試完成，但需要保存進度或與團隊共享的情況下
- 添加文件到暫存區                    `git add .`
- 提交變更                           `git commit -m "WIP: Add new feature"`
- 將你的分支推送到遠端儲存庫            `git push origin feature/new-feature`




# Cloud Build (OK)
1. Cloud Build 設置
    - Host Connection
        - region
    - Repositories
        - 類型：github
    - Triggers
        - repositories
        - branch
        - trigger scope and action
        - trigger cloudbuild.yaml
        - service account
註：目前 gcloud CLI 不支持，需要手動設置


2. 自動產生 cloudbuild.yaml 配置檔
generate_cloudbuild_yaml.sh
情況：環境變數、系統參數、Docker Build, Cloud Build, Cloud Run 參數變更，就需重新產生
目標：生成 cloudbuild.yaml 文件。從 config.yaml 和 .env 文件中讀取參數和環境變數，保持在構建(Docker Build)和部署(Docker Run)過程中的一致性
執本執行任務如下：
    1. 檢查 cloudbuild.yaml 文件是否已存在
    2. 建立新 cloudbuild.yaml 文件
    3. 讀取 config.yaml 參數，組裝 substitutions
    4. 讀取 .env 文件，組裝 secretManager 和 secretEnv
    5. 組裝 Service Account，插入到 cloudbuild.yaml



# CI/CD
1. git push 同步並推送程式碼到 Cloud Build
    - 快速鍵:SMCP `ctrl+shift+S` + `ctrl+shift+M` + `ctrl+shift+C` +`ctrl+shift+P`
    - 同步到 github 後，會觸發 Cloud Build 的腳本，執行 cloudbuild.yaml 設置的內容和步驟
2. 查看 Cloud Build History，是否正確編譯完成
3. 查看 Cloud Run Log 是否所有 Test Case 都通過


# SDLC 開發測試流程
- DEV
- STAGING
- PRODUCTION


# Domain Name Setting
情況：新增對外開放域名時
- 到 Cloud Run 設置 Manage Custom Domain
- 到 DNS 設置與 Google Domain 的配置