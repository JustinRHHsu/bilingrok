# 處理 User Message 為 Command Message 的業務邏輯
# 處理訊息、回應訊息、詢問用戶


from services.llm_service import check_llm_api
from utils.gcs_funcs import generate_signed_url
import csv

from handlers.line_bot_message_builder import create_image_message, create_text_message, create_quick_reply_message, create_flex_message

def command_logic(user_data, user_message):
    
    all_messages = []
    
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
                message_1_text = create_text_message("API Key set successfully! Thanks Elon Musk donates USD 25 monthly before the end in 2024 to support us.")
                all_messages = [message_1_text]
            else:
                message_1_text = create_text_message("API Key verification failed. Please check and try again.")
                all_messages = [message_1_text]
        else:
            message_1_text = create_text_message("Please enter the correct API Key format. (e.g. xai-xxxxxxx)")
            all_messages = [message_1_text]    
    
    
    
    # Command: 設定 API Key
    elif user_message.startswith('/api_key'):
        meesage_1_text = create_text_message("Please enter your API Key...(e.g. xai-xxxxxxx).")
        all_messages = [meesage_1_text]
        message_2_text = create_text_message("Don''t have an API Key? No worries! Get one from the link. Elon Musk donates USD 25 monthly before the end in 2024 to support us!")
        all_messages.append(message_2_text)
        message_3_text = create_text_message("https://accounts.x.ai/sign-in")
        all_messages.append(message_3_text)
        

    
    # Command: 設定 Native Language
    elif user_message.startswith('/language'):
        # (4) (詢問)用戶體驗：需要再徵詢我的意見
        text = "Choose the language you’re most comfortable with...(Please select an option below)"
        
        # (5) (選項)用戶體驗：針對徵詢的意見，提供我有這些選項
        # 組合 Quick Reply 的選項
        # 從 language_list.csv 讀取所有支援的語言列表
        language_list = []
        with open('./config/language_list.csv', newline='') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if not row or row[0].startswith('#'):
                    continue
                item = {'label': row[1], 'text': f"/lang: {row[0]}"}
                language_list.append(item)

        print(f"quick_reply_items={language_list}")
        message_1_qucik_reply = create_quick_reply_message(text, language_list)
    
        all_messages.append(message_1_qucik_reply)

    
        
    # Command: 處理取得的 Native Language，並詢問 Target Language (跟 /language 是連動的)
    elif user_message.startswith('/lang: '):
        # 資料處理。擷取用戶選擇的 native_lang
        native_lang = user_message.split('/lang: ')[1]      # e.g. 'zh-tw'
        valid_lang = False
        
        language_list = []
        with open('./config/language_list.csv', mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                language_list.append(row)
        
        # 判斷每筆記錄的第一列是否在 native_lang 列表中
        for record in language_list:
            lang_code = record[0]
            if lang_code not in native_lang:
                valid_lang = False
            else:
                valid_lang = True
                break
        
        if valid_lang:       # 用戶選擇 native language 是有在支援的語言列表中
            # 把前面 native_lang 儲存到 user_data
            user_data['native_lang'] = native_lang
            
            language_name = None
            for lang in language_list:
                if lang[0] == native_lang:
                    language_name = lang[1]
                    break
            
            # (2) (回應)用戶體驗：確認我的選擇
            message_1_text = create_text_message(f"Awesome! I can also speak a little {language_name} 🤏.")
            all_messages.append(message_1_text)
            # (3) (說明)用戶體驗：我的選擇，代表系統會給我的價值
            message_2_text = create_text_message(f"This way, I can help you organize NOTES in {language_name}, so you can review vocabulary, phrases, or common expressions from our conversations!!")
            all_messages.append(message_2_text)
            
            # (4) (詢問)用戶體驗：需要再徵詢我的意見
            text = f"Which language would you like to practice? I’ll chat with you in that language! (Please select an option below)"
            # (5) (選項)用戶體驗：針對徵詢的意見，提供我有這些選項
            
            # 從 language_list.csv 讀取語言列表，把 native_lang 過濾掉
            learn_language_list = []
            with open('./config/language_list.csv', newline='') as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    if row[0] != native_lang:  # 把 native_lang 過濾掉
                        learn_language_list.append({'label': row[1], 'text': f"/learn: {row[0]}"})
                        
            # (6) (決策)用戶體驗：我選擇了這個選項，代替我發出給系統看得懂的指令
            message_3_quick_reply = create_quick_reply_message(text, learn_language_list)
            all_messages.append(message_3_quick_reply)
            
        # 用戶選擇 native language 不在支援的語言列表中
        else:                   
            text = "Sorry, we haven''t support this language yet. Please try again."
            
            language_list = []
            with open('./config/language_list.csv', newline='') as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    if not row or row[0].startswith('#'):
                        continue
                    item = {'label': row[1], 'text': f"/lang: {row[0]}"}
                    language_list.append(item)
            
            message_1_qucik_reply = create_quick_reply_message(text, language_list)

            all_messages.append(message_1_qucik_reply)
        
        
    # Command: 設定 Target Language (跟 /lang 是連動的)
    elif user_message.startswith('/learn: '):
        # 資料處理。擷取用戶選擇的 learn_lang
        native_lang = user_data['native_lang']
        learn_lang = user_message.split('/learn: ')[1]
        valid_lang = False
        
        language_list = []
        with open('./config/language_list.csv', mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                language_list.append(row)
        
        # 判斷每筆記錄的第一列是否在 learn_lang 列表中
        for record in language_list:
            lang_code = record[0]
            if lang_code not in learn_lang:
                valid_lang = False
            else:
                valid_lang = True
                break
        
        if valid_lang:       # 用戶選擇 learn language 是有在支援的語言列表中
            user_data['target_lang'] = learn_lang
            
            language_name = None
            for lang in language_list:
                if lang[0] == learn_lang:
                    language_name = lang[1]
                    break
            
            # (2) (回應)用戶體驗：確認我的選擇
            message_1_text = create_text_message(f"I'm glad to hear you want to learn {language_name}!")
            all_messages.append(message_1_text)
            # (3) (回應)用戶體驗：我的選擇，代表系統會給我的價值
            message_2_text = create_text_message(f"Bilingrok will match you with the ideal language partner. 🌟")
            all_messages.append(message_2_text)
            # (4) (詢問)用戶體驗：需要再徵詢我的意見
            # 引導填入 API Key，接入 command (跟 /api_key 是連動的)
            text = "Lastly, would you like to subscribe to Bilingrok? Now we offer you a special discount."
            items = [
                {'label': 'Subscribe Now!', 'text': '/sub: subscribe-now'},
                {'label': 'later', 'text': '/sub: later'}
            ]
            message_3_quick_reply = create_quick_reply_message(text, items)
            all_messages.append(message_3_quick_reply)
        
        # 用戶選擇 learn language 不在支援的語言列表中 
        else:
            text = "Sorry, we haven''t support this language yet. Please try again."
            
            language_list = []
            with open('./config/language_list.csv', newline='') as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    if not row or row[0].startswith('#') or row[0] == native_lang:
                        continue
                    item = {'label': row[1], 'text': f"/learn: {row[0]}"}
                    language_list.append(item)
            
            message_1_qucik_reply = create_quick_reply_message(text, language_list)

            all_messages.append(message_1_qucik_reply)
    
    
    
    elif user_message == "/purchase":
        
        text = "Would you like to subscribe to Bilingrok? Now we offer you a special discount."
        items = [
            {'label': 'Subscribe Now!', 'text': '/sub: subscribe-now'},
            {'label': 'later', 'text': '/sub: later'}
        ]
        message_3_quick_reply = create_quick_reply_message(text, items)
        all_messages.append(message_3_quick_reply)
        
        
    
    elif user_message == "/sub: subscribe-now":
        
        # 組裝 Flex Message
        alt_text = "Subscription Type"
        json_filename = "flex_purchase"
        message_1_flex = create_flex_message(alt_text, json_filename)
        all_messages.append(message_1_flex)
        
        # 回到上一步
        text = "This is the spcial offer for you! We cannot wait to match you with a language partner! 🌟"
        purchase_items = [
            {'label': 'back ↩️', 'text': '/purchase'}
        ]
        
        message_2_quick_reply = create_quick_reply_message(text, purchase_items)
        all_messages.append(message_2_quick_reply)
        
        
    elif user_message == "/sub: later":
        message_1_text = create_text_message("Uh-oh! We are sorry to hear that...😢")
        all_messages.append(message_1_text)
        
        message_2_text = create_text_message("or we send you a gift - 7-day free trial value USD 25.00! 🎁")
        all_messages.append(message_2_text)
        
        message_3_text = create_text_message(f"3 steps:\n1. Register xAI account\n2. Generate API Key\n3. paste API key on the chat\nand start enjoy the 7-days free trial! 🎉🎉🎉")
        all_messages.append(message_3_text)
        
        message_4_flex = create_flex_message("7-day Free Trial", "flex_xai_gift")
        all_messages.append(message_4_flex)
    
        
    # Command: 設定 API Key    
    elif user_message.startswith('/feedback'):
        # TBD
        # user_data, reply_content = handle_feedback_command(user_data, user_message, user_id)
        pass
        
    else:
        message_1_text = create_text_message('Unknown command. Please check the command and try again.')
        all_messages = [message_1_text]
    
    
    
    return user_data, all_messages