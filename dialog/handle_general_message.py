# 處理 User Message 為 General Message 的業務邏輯
# 處理訊息、回應訊息、詢問用戶

from handlers.line_bot_message_builder import create_text_message, create_flex_image_action_message
from handlers.script_translation import load_translations
from datetime import datetime, timezone

from services.firestore_service import add_chat_message
from services.llm_service import get_ai_assistant_response, conversation_review_card_generation

from config.config import Config

def general_msg_logic(user_data, message_data, chat_history, all_messages):
    native_lang = user_data.get('native_lang', 'zh-tw')
    translations = load_translations(native_lang)
    
    user_id = user_data['user_id']
    api_key = user_data['api_key']
    subscribe_expired_timestamp = user_data['subscribe_expired_timestamp']
    user_message = message_data['message']
    message_timestamp = message_data['message_timestamp']
    
    message_for_review_learning_card = Config.MESSAGES_FOR_REVIEW_LEARNING_CARD
    time_zone = Config.TIME_ZONE_UTC_PLUS_8
    
    
    # API Key 是否為空
    if not api_key or api_key == '':
        message_1_text = create_text_message(translations['alert_api_key_unset']['text'])
        all_messages.append(message_1_text)
        
        json_filename = "flex_image_action"
        img_url = "https://storage.googleapis.com/linebot_materials/onboarding-start.jpeg"
        # signed_img_url = generate_signed_url("linebot_materials","onboarding-start", 3600)
        aspectRatio = "200:60"
        action_text = "/language"
        message_2_flex = create_flex_image_action_message(json_filename, img_url, aspectRatio, action_text)
        all_messages.append(message_2_flex)
    
    # Subscribe Expire Time 是否為空值
    elif not subscribe_expired_timestamp:
        message_1_text = create_text_message(translations['alert_subscribe_unavailable']['text'])
        all_messages.append(message_1_text)
    
    # Subscribe Expire Time 是否過期
    elif subscribe_expired_timestamp < datetime.now(time_zone):
        message_1_text = create_text_message(translations['alert_subscribe_expired']['text'].format(subscribe_expired_timestamp=subscribe_expired_timestamp.strftime('%Y-%m-%d %H:%M')))
        all_messages.append(message_1_text)
    
    # 有 API KEY，且平台使用期間在合法期限內。開始聊天
    else:
        add_chat_message(user_id, message_data)
        
        # 讓 LLM API 處理回覆內容
        user_data, reply_content, reply_timestamp = get_ai_assistant_response(user_data, chat_history, user_message)
        message_1_text = create_text_message(reply_content)
        all_messages.append(message_1_text)
        
        # 組合 Assistant Message 回覆的訊息，存入 Chat History
        # 若 LLM 沒有成功回覆，還是會送通知給用戶，但不會存入 Chat History
        if not reply_timestamp == None:
            message_data = {
                'role': 2,    # 1: User, 2: Assistant
                'message': reply_content,   
                'message_timestamp': reply_timestamp
            }
            add_chat_message(user_id, message_data)
        
            # 更新用戶對話次數和最後對話時間
            user_data['conversation_count'] += 2        # 一則 User message，一則 Assistant message
            user_data['last_message_timestamp'] = message_timestamp     # user message 的 timestamp        
        
            # 判斷是否需要提供學習卡片
            if user_data['conversation_count'] % message_for_review_learning_card == 0:
                user_data, ai_suggestion = conversation_review_card_generation(user_data, chat_history)
                message_2_text = create_text_message(ai_suggestion)
                all_messages.append(message_2_text)
            
            
            
    return user_data, all_messages