import datetime
import csv

from config.config import Config

from linebot.v3.webhooks import MessageEvent, TextMessageContent
from linebot.v3.messaging import (
    ApiClient, MessagingApi, TextMessage,
    ReplyMessageRequest, QuickReply, QuickReplyItem,
    MessageAction
)

from services.firestore_service import get_or_create_user, add_chat_message, update_user_profile, get_recent_messages
from services.llm_service import get_ai_assistant_response, conversation_review_card_generation, check_llm_api

# from handlers.api_key_handler import handle_api_key_command
# from handlers.feedback_handler import handle_feedback_command
from handlers.reply_message import reply_message_with_quick_reply

# from services.cloud_task_service import create_or_update_task

from handlers.load_animation import send_loading_animation
from dialog.handle_command_message import command_logic


def register_text_handler(handler, configuration):
    @handler.add(MessageEvent, message=TextMessageContent)
    def handle_message(event):
        
        # 取得 Line Webhook 資料
        user_id = event.source.user_id
        role = 1
        user_message = event.message.text.strip()
        reply_token = event.reply_token
        message_timestamp = event.timestamp     # linebot timestamp in milliseconds
        
        # TBD
        # waiting_message_time_slot = Config.TIME_SLOT_PROCESS_MESSAGES_TO_LLM
        # session_expired_time = Config.SESSION_EXPIRED_TIME
        
        # 初始化設定
        message_for_review_learning_card = Config.MESSAGES_FOR_REVIEW_LEARNING_CARD
        
        # 組合聊天訊息格式
        message_data = {
            'role': role,    # 1: User, 2: Assistant
            'message': user_message,
            'reply_token': reply_token,
            'message_timestamp': message_timestamp
        }
        
        # 獲取用戶資料和聊天記錄
        user_data, chat_history = get_or_create_user(user_id)
        
        # Save user message to chat history
        # TBD 是否可以用 Cloud Task 異步處理
        # add_chat_message(user_id, message_data)    
        
        # TBD 
        # 更新用戶資訊
        
        reply_contents = []
        quick_reply_items = []
        
        # 訊息進來先判斷 message 類型： command message or general message
        # 各種 message 的判斷，都把要給用戶看的訊息，透過 append() 加入到 reply_contents[] 中
        # 如果有需要 quick reply 的，也是先組裝好 quick_reply_items[]
        # 最後呼叫 reply_message_with_quick_reply() 函數，回傳給用戶
        # Commnad Message
        if user_message.startswith('/') or user_message.startswith('xai-'):

            send_loading_animation(configuration, user_id)
            user_data, reply_contents, quick_reply_items = command_logic(user_message, user_data, reply_contents, quick_reply_items)
            
        # Normal Conversation - 和 Companion 對話、練習語言
        else:
            # 進入對話，先回覆 Loading 畫面
            send_loading_animation(configuration, user_id)

            # user_message 存入 Chat History
            # Chat History 只存用戶和 AI 聊天的 General Message，不存 Command Message
            add_chat_message(user_id, message_data)    
            
            # 建立或更新 Cloud Task，讓 Message 定時 30 秒後，一呼叫 LLM API 處理
            # create_or_update_task(user_id)
            # 要先儲存下來
            
            # 讓 LLM API 處理回覆內容
            user_data, reply_content, reply_timestamp = get_ai_assistant_response(user_data, chat_history, user_message)
            reply_contents.append(reply_content)    
            
            # 組合 Assistant Message 回覆的訊息，存入 Chat History
            message_data = {
                'role': 2,    # 1: User, 2: Assistant
                'message': reply_contents[0],   
                'message_timestamp': reply_timestamp
            }
            add_chat_message(user_id, message_data)
            
            # 更新用戶對話次數和最後對話時間
            user_data['conversation_count'] += 2        # 一則 User message，一則 Assistant message
            user_data['last_message_timestamp'] = message_timestamp     # user message 的 timestamp        
            
            
            # 判斷是否需要提供學習卡片
            # 如果 user_data['conversation_count'] 的值 / 10 的餘數為 0，則提供對話摘要
            # 每 10 條對話提供一次，提供一個對話學習卡片
            if user_data['conversation_count'] % message_for_review_learning_card == 0:
                user_data, ai_suggestion = conversation_review_card_generation(user_data, chat_history)
                reply_contents.append(ai_suggestion)
        
        


        # 更新用戶資料
        # 上面處理完 message 的各種判斷後，把蒐集到的用戶資料，更新到 Firestore
        update_user_profile(user_id, user_data)
        
        # 回覆用戶訊息
        # 回傳給用戶的訊息，是否需要提供 Quick Reply。有的話，傳入有包含組裝 quick_reply_items 的 reply_message 函數
        if quick_reply_items:
            reply_message_with_quick_reply(reply_contents, reply_token, configuration, quick_reply_items)
        else:
            reply_message_with_quick_reply(reply_contents, reply_token, configuration)