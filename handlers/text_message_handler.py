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
from services.llm_service import handle_normal_conversation, conversation_review_card_generation, check_llm_api

# from handlers.api_key_handler import handle_api_key_command
# from handlers.feedback_handler import handle_feedback_command
from handlers.reply_message import reply_message_with_quick_reply

# from services.cloud_task_service import create_or_update_task

from handlers.load_animation import send_loading_animation


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
        if user_message.startswith('/'):
            
            # Command: 設定 API Key
            if user_message.startswith('/api_key'):
                send_loading_animation(configuration, user_id, 5)
                reply_contents.append('Please enter your API Key...(e.g. xai-xxxxxxx).')
                
                
                reply_contents.append('Don''t have an API Key? No worries! Get one from the link. Elon Musk donates USD 25 monthly before the end in 2024 to support us!')
                reply_contents.append('https://accounts.x.ai/sign-in')
                
            
            # Command: Onboarding Start    
            elif user_message.startswith('/Bilingrok'):
                # 1. 詢問用戶熟悉的語言，想要學習的語言
                # 2. 從 label 表讀出用戶熟悉的語言的對話腳本，自我介紹
                # 3. 詢問用戶想要學習的語言，並告知可以在哪裡改
                # 4. 設置 API Key 儲存點數
                # 5. 設置完成，開始對話
                # 6. 蒐集意見
                pass
            
            # Command: 設定 Native Language
            elif user_message.startswith('/language'):
                # (1) (動畫)用戶體驗：處理中
                send_loading_animation(configuration, user_id, 5)
                # (4) (詢問)用戶體驗：需要再徵詢我的意見
                reply_contents.append('Choose the language you’re most comfortable with...(Please select an option below)')
                
                # (5) (選項)用戶體驗：針對徵詢的意見，提供我有這些選項
                # 組合 Quick Reply 的選項
                # 從 language_list.csv 讀取所有支援的語言列表
                language_list = []
                with open('./config/language_list.csv', newline='') as csvfile:
                    reader = csv.reader(csvfile)
                    for row in reader:
                        row[0] = f"/lang: {row[0]}"     # 加上 '/lang:' 前綴，是為了接續下一個 command 的操作：組合 /lang {native_lang}，觸發下個 {target_lang} 的設置
                        language_list.append(row)
                # (6) (決策)用戶體驗：我選擇了這個選項，代替我發出給系統看得懂的指令
                quick_reply_items = language_list
                
                
            # Command: 處理取得的 Native Language，並詢問 Target Language (跟 /language 是連動的)
            elif user_message.startswith('/lang: '):
                # 兩個步驟：
                # 1. 回應用戶剛選擇的 native_lang
                # 2. 詢問用戶要學習的語言 target_lang
                # (1) (動畫)用戶體驗：處理中
                send_loading_animation(configuration, user_id, 5)
                
                # 資料處理。擷取用戶選擇的 native_lang
                native_lang = user_message.split('/lang: ')[1]      # e.g. 'zh-tw'
                
                # 1. 查詢用戶剛選擇的 native_lang
                language_list = []
                with open('./config/language_list.csv', mode='r', encoding='utf-8') as file:
                    reader = csv.reader(file)
                    for row in reader:
                        language_list.append(row)                            
                
                # 查詢用戶選取的 native_lang 對應的語言名稱 language_code
                def get_language_name(code):
                    for item in language_list:
                        if item[0] == code:
                            return item[1]
                    return None
                
                # 取得 native_lang 對應的語言名稱 language code
                language_code = get_language_name(native_lang)
                
                if language_code:       # 用戶選擇 native language 是有在支援的語言列表中
                    # 把前面 native_lang 儲存到 user_data
                    user_data['native_lang'] = native_lang
                    # (2) (回應)用戶體驗：確認我的選擇
                    reply_contents.append(f"Awesome! I can also speak a little {language_code} 🤏.")
                    # (3) (說明)用戶體驗：我的選擇，代表系統會給我的價值
                    reply_contents.append(f"This way, I can help you organize NOTES in {language_code}, so you can review vocabulary, phrases, or common expressions from our conversations!!")
                else:                   # 用戶選擇 native language 不在支援的語言列表中
                    reply_contents.append('Sorry, we haven''t support this language yet. Please try again.')
                
                
                # (4) (詢問)用戶體驗：需要再徵詢我的意見
                # 2. 詢問用戶要學習的語言 target_lang
                # 設置 reply_message
                reply_contents.append(f"Which language would you like to practice? I’ll chat with you in that language! (Please select an option below)")
                
                # (5) (選項)用戶體驗：針對徵詢的意見，提供我有這些選項
                # 從 language_list.csv 讀取語言列表，把 native_lang 過濾掉
                language_list = []
                with open('./config/language_list.csv', newline='') as csvfile:
                    reader = csv.reader(csvfile)
                    for row in reader:
                        if row[0] != native_lang:           # 把 native_lang 過濾掉
                            row[0] = f"/learn: {row[0]}"
                            language_list.append(row)
                # (6) (決策)用戶體驗：我選擇了這個選項，代替我發出給系統看得懂的指令
                quick_reply_items = language_list
            
                
            # Command: 設定 Target Language (跟 /lang 是連動的)
            elif user_message.startswith('/learn: '):
                # (1) (動畫)用戶體驗：處理中
                send_loading_animation(configuration, user_id, 5)
                
                # 資料處理。擷取用戶選擇的 learn_lang
                learn_lang = user_message.split('/learn: ')[1]
                
                # 查詢用戶選取 tartget language 的語言名稱
                language_list = []
                with open('./config/language_list.csv', mode='r', encoding='utf-8') as file:
                    reader = csv.reader(file)
                    for row in reader:
                        language_list.append(row)
                
                # 查詢用戶選取的 learn_lang 對應的語言名稱 language code
                def get_language_name(code):
                    for item in language_list:
                        if item[0] == code:
                            return item[1]
                    return None
                
                # 取得 learn_lang 對應的語言名稱 language code
                language_code = get_language_name(learn_lang)
                
                if language_code:       # 用戶選擇 learn language 是有在支援的語言列表中
                    user_data['target_lang'] = learn_lang
                    # (2) (回應)用戶體驗：確認我的選擇
                    reply_contents.append(f"I'm glad to hear you want to learn {language_code}!")
                    # (3) (回應)用戶體驗：我的選擇，代表系統會給我的價值
                    reply_contents.append(f"Bilingrok will match you with the ideal language partner. 🌟")
                    # (4) (詢問)用戶體驗：需要再徵詢我的意見
                    # 引導填入 API Key，接入 command (跟 /api_key 是連動的)
                    reply_contents.append(f"/purchase")
                
                else:                # 用戶選擇 learn language 不在支援的語言列表中 
                    reply_contents.append('Sorry, we haven''t support this language yet. Please try again.')
            
            
            # Command: 設定購買服務的類型  
            elif user_message.startswith('/purchase'):
                # (1) 動畫
                send_loading_animation(configuration, user_id, 5)
                
                # (4) 詢問 
                reply_contents.append('選擇您想訂閱的服務類型？')
                
                # (5) 選擇: Premium, Xai(Free)
                    # /pushcase: Premium
                    # /pushcase: Xai(Free)
                # (6) 決策
                
                
                pass
                
                
            # Command: 設定 API Key    
            elif user_message.startswith('/feedback'):
                # TBD
                # user_data, reply_content = handle_feedback_command(user_data, user_message, user_id)
                pass
                
            else:
                reply_contents.append('Unknown command. Please check the command and try again.')
                
                
        # Normal Conversation - 和 Companion 對話、練習語言
        else:
            # 進入對話，先回覆 Loading 畫面
            send_loading_animation(configuration, user_id)
            
            # General: User Message 符合 API Key 格式(xai-開頭)，期望設置 API Key
            # API Key 的檢查包括：格式、長度、是否有效，三項檢查
            if user_message.startswith('xai-'):
                api_key = user_message
                api_key_length = 84  # 假設 api key 的總長度為 84 個字元
                
                # 檢查 API Key 長度是否符合
                if len(user_message) == api_key_length:
                    # 檢查 API Key 是否有效
                    if check_llm_api(api_key):
                        user_data['api_key'] = api_key
                        reply_contents.append("API Key set successfully! Thanks Elon Musk donates USD 25 monthly before the end in 2024 to support us.")
                    else:
                        reply_contents.append("API Key verification failed. Please check and try again.")
                else:
                    reply_contents.append("Please enter the correct API Key format. (e.g. xai-xxxxxxx)")
                    
            
            # 一般訊息    
            else:
                # user_message 存入 Chat History
                # Chat History 只存用戶和 AI 聊天的 General Message，不存 Command Message
                add_chat_message(user_id, message_data)    
                
                # 建立或更新 Cloud Task，讓 Message 定時 30 秒後，一呼叫 LLM API 處理
                # create_or_update_task(user_id)
                # 要先儲存下來
                
                # 讓 LLM API 處理回覆內容
                user_data, reply_content, reply_timestamp = handle_normal_conversation(user_data, chat_history, user_message)
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