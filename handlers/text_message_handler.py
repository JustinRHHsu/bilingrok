from linebot.v3.webhooks import MessageEvent, TextMessageContent

from services.firestore_service import get_or_create_user, update_user_profile

from handlers.reply_message import line_reply_message
from handlers.load_animation import send_loading_animation
from dialog.handle_command_message import command_logic
from dialog.handle_general_message import general_msg_logic


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
        # message_for_review_learning_card = Config.MESSAGES_FOR_REVIEW_LEARNING_CARD
        all_messages = []
        
        # 組合聊天訊息格式
        message_data = {
            'role': role,    # 1: User, 2: Assistant
            'message': user_message,
            'reply_token': reply_token,
            'message_timestamp': message_timestamp
        }
        
        # 獲取用戶資料和聊天記錄
        user_data, chat_history = get_or_create_user(user_id)
        
        api_key = user_data.get('api_key', '')
        subscribe_expire_time = user_data.get('subscribe_expired_timestamp', '')
        
        
        # Save user message to chat history
        # TBD 是否可以用 Cloud Task 異步處理
        # add_chat_message(user_id, message_data)    
        
        # TBD 
        # 更新用戶資訊
        
        
        # 訊息進來先判斷 message 類型： command message or general message
        # 各種 message 的判斷，都把要給用戶看的訊息，透過 append() 加入到 reply_contents[] 中
        # 如果有需要 quick reply 的，也是先組裝好 quick_reply_items[]
        # 最後呼叫 reply_message_with_quick_reply() 函數，回傳給用戶
        # Commnad Message
        if user_message.startswith('/') or user_message.startswith('xai-'):
            send_loading_animation(configuration, user_id, 5)
            user_data, all_messages = command_logic(user_data, user_message, all_messages)
            
            
        # Normal Conversation - 和 Companion 對話、練習語言
        else:
            
            send_loading_animation(configuration, user_id)
            user_data, all_messages = general_msg_logic(user_data, message_data, chat_history, all_messages)
            
        
        # 更新用戶資料
        # 上面處理完 message 的各種判斷後，把蒐集到的用戶資料，更新到 Firestore
        update_user_profile(user_id, user_data)
        
        # 回覆用戶訊息
        # 回傳給用戶的訊息，是否需要提供 Quick Reply。有的話，傳入有包含組裝 quick_reply_items 的 reply_message 函數
        # print(f"##Reply Messages: {all_messages}")
        
        line_reply_message(reply_token, configuration, all_messages)