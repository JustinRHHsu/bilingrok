# from google.cloud import firestore
import datetime
from config.config import Config, DB
# from google.oauth2 import service_account
import json
import logging

number_of_recent_messages = Config.NUMBER_OF_MESSASES_FROM_CHAT_HISTORY

db = DB.init_firestore_db()
# db = firestore.Client(project=Config.GCP_PROJECT_ID, credentials=Config.GCP_CRED, database=Config.DB_NAME)

def get_or_create_user(user_id):
    user_ref = db.collection('users').document(user_id)
    profile_ref = user_ref.collection('profile').document('info')
    profile_doc = profile_ref.get()
    print(f"Access: User {user_id} profile: {profile_doc}")
    logging.info(f"Access: User {user_id} /profile: {profile_doc}")

    # 如果用戶資料已存在，則回傳用戶資料
    if profile_doc.exists:
        profile_data = profile_doc.to_dict()
        chat_history = get_recent_messages(user_id, number_of_recent_messages)
        return profile_data, chat_history
    
    # 如果用戶資料不存在，則建立用戶資料
    else:
        profile_data = {
            'user_id': user_id,
            'mode': 1,
            'name': '',
            'gender': '',
            'grok_api_key': Config.GROK_API_KEY,
            'api_key_update_timestamp': datetime.datetime.utcnow(),
            'prompt_tokens': 0,
            'completion_tokens': 0,
            'personalized_prompt': '',
            'conversation_count': 0,
            'native_lang': 'zh-tw',
            'target_lang': 'us-en',
            'last_message_timestamp': datetime.datetime.utcnow()
        }
        profile_ref.set(profile_data)
        logging.info(f"Create: User {user_id} profile: {profile_data}")
        return profile_data, []

def update_user_profile(user_id, data):
    profile_ref = db.collection('users').document(user_id).collection('profile').document('info')
    profile_ref.update(data)
    logging.info(f"Update: User {user_id} profile: {data}")

def add_chat_message(user_id, chat_data):
    chat_history_ref = db.collection('users').document(user_id).collection('chat_history')
    chat_history_ref.add(chat_data)
    logging.info(f"Save: {user_id}'s message to Chat History collection.")


def get_recent_messages(user_id, limit=10):
    
    chat_history_ref = db.collection('users').document(user_id).collection('chat_history')
    # Retrieve the most recent messages from the chat history for memory
    recent_messages = chat_history_ref.order_by('message_timestamp', direction=firestore.Query.DESCENDING).limit(limit).stream()
    
    recent_chat_history = []
    for message in recent_messages:
        message_dict = message.to_dict()
        # print(f"Message: {message_dict}")
        recent_chat_history.append(message_dict)
    
    # print("====== Recent Chat History ======")
    # print(json.dumps(recent_chat_history, indent=4, ensure_ascii=False))
    
    logging.info(f"Access: recent {limit} messages from  {user_id}'s chat history.")
    
    return recent_chat_history