import logging

import re
from openai import OpenAI
from config.config import Config
from services.line_service import line_bot_api
# from services.firestore_service import update_user_data, get_or_create_user
from utils.prompt_utils import provide_summary
from prompts.prompt_loader import load_prompts
from datetime import datetime 

# 設定 logging
logging.basicConfig(
    level=logging.ERROR,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# 建立 logger
logger = logging.getLogger(__name__)

def handle_normal_conversation(user_data, chat_history, user_message):
    
    prompt_template = load_prompts('system_prompt')
    sys_prompt = load_dynamic_variables_into_prompt(prompt_template, user_data)
    
    messages=[
        {"role": "system", "content": sys_prompt},
        *transform_chat_history(chat_history),
        {"role": "user", "content": user_message}
    ]
    # print(f"=== Messages prepared into LLM ===\n{messages}\n =====================")

    try:
        client = OpenAI(api_key=Config.GROK_API_KEY, 
                        base_url="https://api.x.ai/v1"
                        )
        
        response = client.chat.completions.create(
            model='grok-beta',
            messages=messages,
            max_tokens=100,
            temperature=0.5,
        )
        # print(f"=== response ===\n{response}\n =====================")
        
        reply_content = response.choices[0].message.content
        reply_timestamp = int(f"{response.created}000")     # Grok API timestamp in seconds, so add 3 zeros to convert to milliseconds  
        prompt_tokens = response.usage.prompt_tokens
        completion_tokens = response.usage.completion_tokens
        
        user_data['prompt_tokens'] += prompt_tokens
        print(f"Prompt tokens: {prompt_tokens}")
        logging.info(f"Prompt tokens: {prompt_tokens}")
        user_data['completion_tokens'] += completion_tokens
        print(f"Completion tokens: {completion_tokens}")
        logging.info(f"Completion tokens: {completion_tokens}")
        
        return user_data, reply_content, reply_timestamp
        
    except Exception as e:
        # 使用 logger 記錄錯誤
        logger.error(
            f"[Grok API Error] 請求失敗(回應) - 錯誤訊息: {str(e)}, "
            f"錯誤類型: {type(e).__name__}"
        )
        
        reply_content = "Sorry, I'm having trouble understanding you right now. Please try again later."
        
        return user_data, reply_content


def conversation_review_card_generation(user_data, chat_history):
    # 生成語言學習卡片，系統訊息，不儲存
    
    prompt_template = load_prompts('conversation_review_card_generation')
    sys_prompt = load_dynamic_variables_into_prompt(prompt_template, user_data)
    chat_history_str = "\n".join([f"{msg['role']}: {msg['message']}" for msg in chat_history])
    
    messages=[
        {"role": "system", "content": sys_prompt},
        {"role": "user", "content": chat_history_str}
    ]

    try:
        client = OpenAI(api_key=Config.GROK_API_KEY, 
                        base_url="https://api.x.ai/v1"
                        )
        
        response = client.chat.completions.create(
            model='grok-beta',
            messages=messages,
            max_tokens=4096,
            temperature=0.2,
        )
        
        ai_suggestion = response.choices[0].message.content
        prompt_tokens = response.usage.prompt_tokens
        completion_tokens = response.usage.completion_tokens
        
        user_data['prompt_tokens'] += prompt_tokens
        print(f"Prompt tokens: {prompt_tokens}")
        logging.info(f"Prompt tokens: {prompt_tokens}")
        user_data['completion_tokens'] += completion_tokens
        print(f"Completion tokens: {completion_tokens}")
        logging.info(f"Completion tokens: {completion_tokens}")
        
        return user_data, ai_suggestion
        
    except Exception as e:
        # 使用 logger 記錄錯誤
        logger.error(
            f"[Grok API Error] 請求失敗(卡片) - 錯誤訊息: {str(e)}, "
            f"錯誤類型: {type(e).__name__}"
        )
        
        reply_content = "Sorry, I'm having trouble understanding you right now. Please try again later."
        
        return user_data, reply_content



def transform_chat_history(chat_history):
    
    # Check if chat_history is a list of dictionaries containing 'message_timestamp' key
    if not all(isinstance(message, dict) and 'message_timestamp' in message for message in chat_history):
        raise ValueError("Each item in chat_history must be a dictionary containing 'message_timestamp' key")
    
    # Sort chat history by message timestamp in ascending order to maintain the order of conversation (最舊到最新)
    sorted_chat_history = sorted(chat_history, key=lambda x: x['message_timestamp'])
    # print(f"=== sorted_chat_history ===\n{sorted_chat_history}\n =====================")
    
    transformed_history = []
    role_map = {'1': 'user', '2': 'assistant'}
    
    for message in sorted_chat_history:
        role = role_map.get(message['role'], 'user')
        content = message['message']
        transformed_history.append({"role": role, "content": content})
    
    return transformed_history


def load_dynamic_variables_into_prompt(system_prompt, user_data):
    # Find all placeholders in the format {variable}
    placeholders = re.findall(r'\{(.*?)\}', system_prompt)
    system_prompt_load_dynamic = system_prompt

    # Replace placeholders with actual user data if available
    for placeholder in placeholders:
        if placeholder in user_data:
            # print(f"=== Placeholder = {placeholder} &&& user_data = {user_data[placeholder]} =====================")
            system_prompt_load_dynamic = system_prompt_load_dynamic.replace(f'{{{placeholder}}}', str(user_data[placeholder]))
            
    # print(f"=== System Prompt Load Dynamic ===\n{system_prompt_load_dynamic}\n=====================")

    return system_prompt_load_dynamic




def check_llm_api(api_key):
    try:
        client = OpenAI(api_key=api_key, base_url="https://api.x.ai/v1")
        test_message = [{"role": "system", "content": "Hello, how are you?"}]
        
        response = client.chat.completions.create(
            model='grok-beta',
            messages=test_message,
            max_tokens=10,
            temperature=0.5,
            timeout=5  # 設置超時時間為5秒
        )
        
        if response and response.choices:
            return True
        else:
            print("錯誤了")
            return False
    except Exception as e:
        print(f"錯誤 Error: {e}")
        return False