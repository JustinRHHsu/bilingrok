import os
from datetime import timezone, timedelta
from dotenv import load_dotenv
import yaml
from google.cloud import secretmanager
from google.auth import default
from google.oauth2 import service_account
import logging
from google.cloud import firestore

# 讀取 config.yaml 文件
with open('config/config.yaml', 'r') as file:
    yaml_config = yaml.safe_load(file)

# 根據 SECRET_KEY_ENV 判斷是否加載本地 .env 文件
if yaml_config['SECRET_KEY_ENV'] == 'LOCAL':
    if os.path.exists("config/.env"):
        logging.info("Accessed .env file successful!")
        load_dotenv("config/.env")
    else:
        logging.info("Accessed .env file FAIL! Turn to accessing GCP")
        yaml_config['DEBUG_MODE'] = False
        yaml_config['SECRET_KEY_ENV'] = 'GCP'
        yaml_config['ENVIRONMENT'] = 'PROD'

def access_secret_version(project_id, secret_id, version_id="latest"):
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"
    response = client.access_secret_version(request={"name": name})
    secret_key = response.payload.data.decode("UTF-8").strip()
    print(f"Accessing secret from Secret Manager: {secret_key}")
    return secret_key

def get_gcp_credential():
    if yaml_config['SECRET_KEY_ENV'] == 'GCP' and yaml_config['ENVIRONMENT'] == 'PROD':
        logging.info("Accessing GCP Secret Manager...")
        # 已部署到雲端，應用程式會自動使用雲端提供的預設憑證
        cred, project = default()
        return cred
    elif yaml_config['SECRET_KEY_ENV'] == 'LOCAL' or yaml_config['ENVIRONMENT'] == 'DEV':
        # 本地端已下載 secret key 的 json 檔路徑，生成憑證
        cred = service_account.Credentials.from_service_account_file(yaml_config['GCP_SA_SECRET_FILE'])
        return cred
    else:
        logging.error("Error: No GCP credential found.")
        return None

class Config:
    PORT = yaml_config['CONTAINER_PORT']
    DEBUG = yaml_config['DEBUG_MODE']
    NUMBER_OF_MESSASES_FROM_CHAT_HISTORY = yaml_config['NUMBER_OF_MESSASES_FROM_CHAT_HISTORY']
    MESSAGES_FOR_REVIEW_LEARNING_CARD = yaml_config['MESSAGES_FOR_REVIEW_LEARNING_CARD']
    FLEX_LIBRARY_PATH = yaml_config['FLEX_LIBRARY_PATH']
    TIME_ZONE_UTC_PLUS_8 = timezone(timedelta(hours=8))
    PROMPT_TEMPLATE_PATH = yaml_config['PROMPT_TEMPLATE_PATH']
    AGENT_CHARACTER_PATH = yaml_config['AGENT_CHARACTER_PATH']
    
    # 判斷 Secret Key 的儲存環境，決定向 .env 或 GCP Secret Manager 取得敏感資訊
    SECRET_KEY_ENV = yaml_config['SECRET_KEY_ENV'].strip()
    
    if SECRET_KEY_ENV == 'GCP':
        logging.info("Accessing GCP Secret Manager...")
        print(f"[Secret Key Source]: GCP")
        GCP_PROJECT_ID = yaml_config['GCP_PROJECT_ID'].strip()
        LINE_CHANNEL_ACCESS_TOKEN = access_secret_version(GCP_PROJECT_ID, 'LINE_CHANNEL_ACCESS_TOKEN')
        LINE_CHANNEL_SECRET = access_secret_version(GCP_PROJECT_ID, 'LINE_CHANNEL_SECRET')
        GROK_API_KEY = access_secret_version(GCP_PROJECT_ID, 'XAI_API_KEY')
        DB_NAME = yaml_config['DB_NAME'].strip()
        SERVICE_ACCOUNT_NAME = yaml_config['SERVICE_ACCOUNT_NAME'].strip()
        SERVICE_ACCOUNT_EMAIL = f"{SERVICE_ACCOUNT_NAME}@{GCP_PROJECT_ID}.iam.gserviceaccount.com"
        GCP_CRED = get_gcp_credential()
    elif SECRET_KEY_ENV == 'LOCAL':
        logging.info("Accessing local .env file...")
        print(f"[Secret Key Source]: .env")
        LINE_CHANNEL_ACCESS_TOKEN = os.getenv('STG_LINE_CHANNEL_ACCESS_TOKEN')
        LINE_CHANNEL_SECRET = os.getenv('STG_LINE_CHANNEL_SECRET')
        GROK_API_KEY = os.getenv('XAI_API_KEY')
        DB_NAME = yaml_config['DB_NAME'].strip()
        GCP_PROJECT_ID = yaml_config['GCP_PROJECT_ID'].strip()
        GCP_CRED = get_gcp_credential()
        
    # Cloud Task
    # TIME_SLOT_PROCESS_MESSAGES_TO_LLM = yaml_config.get('TIME_SLOT_PROCESS_MESSAGES_TO_LLM', 5)
    # SESSION_EXPIRED_TIME = yaml_config.get('SESSION_EXPIRED_TIME', 600)
    
    # Message Queue
    # QUEUE_MESSAGE_STORE = yaml_config['QUEUE_MESSAGE_STORE']
    # QUEUE_LOCATION_MESSAGE_STORE = yaml_config['QUEUE_LOCATION_MESSAGE_STORE']
        
class DB:
    def init_firestore_db():
        if yaml_config['ENVIRONMENT'] == 'PROD':
            print(f"[PROD] Access: GCP Firestore with 'GCP Default Credentials'")
            db = firestore.Client(project=yaml_config['GCP_PROJECT_ID'], database=yaml_config['DB_NAME'])
            return db
        elif yaml_config['ENVIRONMENT'] == 'DEV':
            print(f"[DEV] Access: GCP Firestore with 'Service Account Credentials(.json)'")
            cred = service_account.Credentials.from_service_account_file(yaml_config['GCP_SA_SECRET_FILE'])
            db = firestore.Client(project=yaml_config['GCP_PROJECT_ID'], credentials=cred, database=yaml_config['DB_NAME'])
            return db
        else:
            logging.error("Error: No Firestore database found.")
            return None