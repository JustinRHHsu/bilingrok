import logging

import re
from openai import OpenAI
from config.config import Config
# from services.firestore_service import update_user_data, get_or_create_user
from utils.prompt_utils import provide_summary
from prompts.prompt_loader import load_prompts
from datetime import datetime 

from services.llm.LLM_Services import LLMService


# 設定 logging
logging.basicConfig(
    level=logging.ERROR,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# 建立 logger
logger = logging.getLogger(__name__)

# 呼叫 LLM 生成 Conversation 回應
def get_ai_assistant_response(user_data, chat_history, user_message):
    
    # Load System Prompt Template
    dir_sys_prompt = Config.PROMPT_TEMPLATE_PATH
    prompt_template = load_prompts(dir_sys_prompt, "system_prompt")
    # print(f"[DEBUG] prompt_template: {prompt_template}")
    
    # Laod Agent Prompt
    dir_agent_prompt = Config.AGENT_CHARACTER_PATH
    agent_character_prompt = load_prompts(dir_agent_prompt, "agent_justin")
    agent_character_data = {"agent_character": agent_character_prompt}
    # print(f"[DEBUG] agent_character_data: {agent_character_data}")
    
    # 把 system_prompt_template 裡的 user_data 和 agent_character_data 帶進去，達到個人化效果
    sys_prompt = load_dynamic_variables_into_prompt(prompt_template, user_data, agent_character_data)
    # print(f"[DEBUG] sys_prompt: {sys_prompt}")
    
    messages=[
        {"role": "system", "content": sys_prompt},
        *transform_chat_history(chat_history),
        {"role": "user", "content": user_message}
    ]
    # print(f"[DEBUG] messages: {messages}")
    
    try:
        api_key_type = user_data.get('api_key_type')
        api_key = Config.API_KEYS.get(api_key_type, Config.MAIN_LLM_PROVIDER)
        model = Config.MAIN_MODEL_SERVICE_BY_PROVIDER.get(api_key_type, Config.MAIN_LLM_MODEL)
        
        llm_service = LLMService(api_type=api_key_type, api_key=api_key, model=model)
        user_data, ai_suggestion, reply_timestamp = llm_service.completion(messages, user_data)
        return user_data, ai_suggestion, reply_timestamp
          
        
    except Exception as e:
        # 使用 logger 記錄錯誤
        logger.error(
            f"[Grok API Error] 請求失敗(回應) - 錯誤訊息: {str(e)}, "
            f"錯誤類型: {type(e).__name__}"
        )
        
        reply_content = "[System] Sorry, I'm having trouble understanding you right now. Please try again later."
        reply_timestamp = None
        
        return user_data, reply_content, reply_timestamp

# 呼叫 LLM 生成學習卡片
def conversation_review_card_generation(user_data, chat_history):
    # 生成語言學習卡片，系統訊息，不儲存
    
    dir_sys_prompt = Config.PROMPT_TEMPLATE_PATH
    prompt_template = load_prompts(dir_sys_prompt, 'conversation_review_card_generation')
    sys_prompt = load_dynamic_variables_into_prompt(prompt_template, user_data)
    chat_history_str = "\n".join([f"{msg['role']}: {msg['message']}" for msg in chat_history])
    
    messages=[
        {"role": "system", "content": sys_prompt},
        {"role": "user", "content": chat_history_str}
    ]

    try:
        # 使用新的 LLMService 類別
        api_key_type = user_data.get('api_key_type')
        api_key = Config.API_KEYS.get(api_key_type, Config.MAIN_LLM_PROVIDER)
        model = Config.MAIN_MODEL_SERVICE_BY_PROVIDER.get(api_key_type, Config.MAIN_LLM_MODEL)
        
        llm_service = LLMService(api_type=api_key_type, api_key=api_key, model=model)
        user_data, ai_suggestion, _ = llm_service.completion(messages, user_data)
        return user_data, ai_suggestion
        
        
    except Exception as e:
        # 使用 logger 記錄錯誤
        logger.error(
            f"[Grok API Error] 請求失敗(卡片) - 錯誤訊息: {str(e)}, "
            f"錯誤類型: {type(e).__name__}"
        )
        
        reply_content = "Sorry, I'm having trouble understanding you right now. Please try again later."
        
        return user_data, reply_content


# 呼叫 LLM 生成話題開啟聊天
def start_conversation_when_matched(user_data):
    # 生成話題開啟聊天
    dir_sys_prompt = Config.PROMPT_TEMPLATE_PATH
    prompt_template_name = 'conversation_starter'
    prompt_template = load_prompts(dir_sys_prompt, prompt_template_name)
    
    dir_agent_prompt = Config.AGENT_CHARACTER_PATH
    agent_character_prompt = load_prompts(dir_agent_prompt, "agent_justin")
    agent_character_data = {"agent_character": agent_character_prompt}
    
    sys_prompt = load_dynamic_variables_into_prompt(prompt_template, user_data, agent_character_data)
    user_message = "Start generating the starting conversation:"
    
    messages=[
        {"role": "system", "content": sys_prompt},
        {"role": "user", "content": user_message}
    ]
    
    try:
        api_key_type = user_data.get('api_key_type')
        api_key = Config.API_KEYS.get(api_key_type, Config.MAIN_LLM_PROVIDER)
        model = Config.MAIN_MODEL_SERVICE_BY_PROVIDER.get(api_key_type, Config.MAIN_LLM_MODEL)
        
        llm_service = LLMService(api_type=api_key_type, api_key=api_key, model=model)
        _, ai_suggestion, _ = llm_service.completion(messages, user_data)
        return ai_suggestion
        
        
        
    except Exception as e:
        # 使用 logger 記錄錯誤
        logger.error(
            f"[Grok API Error] 請求失敗(卡片) - 錯誤訊息: {str(e)}, "
            f"錯誤類型: {type(e).__name__}"
        )
        
        reply_content = "Sorry, I'm having trouble understanding you right now. Please try again later."
        
        return reply_content




def transform_chat_history(chat_history):
    
    # Check if chat_history is a list of dictionaries containing 'message_timestamp' key
    if not all(isinstance(message, dict) and 'message_timestamp' in message for message in chat_history):
        raise ValueError("Each item in chat_history must be a dictionary containing 'message_timestamp' key")
    
    # Sort chat history by message timestamp in ascending order to maintain the order of conversation (最舊到最新)
    sorted_chat_history = sorted(chat_history, key=lambda x: x['message_timestamp'])
    
    transformed_history = []
    role_map = {'1': 'user', '2': 'assistant'}
    
    for message in sorted_chat_history:
        role = role_map.get(message['role'], 'user')
        content = message['message']
        transformed_history.append({"role": role, "content": content})
    
    return transformed_history


def load_dynamic_variables_into_prompt(system_prompt, user_data, extra_data={}):
    # Find all placeholders in the format {variable}
    placeholders = re.findall(r'\{(.*?)\}', system_prompt)
    system_prompt_load_dynamic = system_prompt

    # Replace placeholders with actual extra data if available
    for placeholder in placeholders:
        if placeholder in extra_data:
            system_prompt_load_dynamic = system_prompt_load_dynamic.replace(f'{{{placeholder}}}', str(extra_data[placeholder]))

    # Replace placeholders with actual user data if available
    for placeholder in placeholders:
        if placeholder in user_data:
            system_prompt_load_dynamic = system_prompt_load_dynamic.replace(f'{{{placeholder}}}', str(user_data[placeholder]))
            
    return system_prompt_load_dynamic


# 檢查 LLM API 金鑰是否有效
# (### TO BE UPDATED)
def check_llm_api(api_key):
    try:
        key = api_key.strip()
        client = OpenAI(api_key=key, 
                        base_url="https://api.x.ai/v1"
                        )
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
            print(" response.choices 錯誤了")
            return False
    except Exception as e:
        print(f"錯誤 Error: {e}")
        return False