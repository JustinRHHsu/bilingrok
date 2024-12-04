# 處理 User Message 為 Command Message 的業務邏輯
# 處理訊息、回應訊息、詢問用戶

from services.llm_service import check_llm_api, start_conversation_when_matched
from utils.gcs_funcs import generate_signed_url
import csv, json

from handlers.line_bot_message_builder import create_image_message, create_text_message, create_quick_reply_message, create_flex_message, create_flex_image_action_message
from handlers.script_translation import load_translations
import random
from datetime import datetime, timedelta, timezone
from config.config import Config

def command_logic(user_data, user_message, all_messages):
    native_lang = user_data.get('native_lang', 'zh-tw')
    translations = load_translations(native_lang)
    time_zone = Config.TIME_ZONE_UTC_PLUS_8
    
    # General: User Message 符合 API Key 格式(xai-開頭)，期望設置 API Key
    if user_message.startswith('xai-'):
        api_key = user_message.strip()
        api_key_length = 84  # 假設 api key 的總長度為 84 個字元
        
        # 檢查 API Key 長度是否符合
        if len(user_message) == api_key_length:
            # 檢查 API Key 是否有效
            if check_llm_api(api_key):
                
                # api_key 無值，新創建的 API Key
                if not user_data['api_key'] or user_data['api_key'] == '':
                    # API 通過驗證成功，更新 user_data
                    # xAI 註冊成功，取得 Bilingrok 7 天的使用，只有1次機會。所以，換 xAI API Key 並不會重新計算 7 天
                    user_data['api_key_type'] = "xai"
                    user_data['api_key'] = api_key
                    user_data['api_key_created_timestamp'] = datetime.now(time_zone)
                    user_data['api_key_updated_timestamp'] = datetime.now(time_zone)
                    user_data['subscribe_item'] = "xai-free"
                    user_data['subscribe_expired_timestamp'] = user_data['api_key_created_timestamp'] + timedelta(days=7)
                    user_data['credits'] = 0
                
                # api_key 已存在，拿新的 API Key 重新設置
                else:
                    user_data['api_key'] = api_key
                    user_data['api_key_updated_timestamp'] = datetime.now(time_zone)
                
                # 通知 API Key 更新成功！
                message_1_text = create_text_message(translations["api_key_set_success"]["text"])
                all_messages = [message_1_text]
                
                # 顯示配對語言夥伴的訊息
                message_2_text = create_text_message(translations["notify_start_matching"]["text"])
                all_messages = [message_2_text]
                
                img_url =  "https://storage.googleapis.com/linebot_materials/hey_small.jpeg"
                # signed_img_url = generate_signed_url("linebot_materials","onboarding-start", 3600)
                aspectRatio = "100:100"
                action_text = "/MatchPartner"
                message_3_text = create_flex_image_action_message("flex_image_action", img_url, aspectRatio, action_text)
                all_messages.append(message_3_text)     
                
            else:
                message_1_text = create_text_message(translations["api_key_verification_failed"]["text"])
                all_messages = [message_1_text]
        else:
            message_1_text = create_text_message(translations["api_key_format_error"]["text"])
            all_messages = [message_1_text]    
    
    
    # Command: 設定 API Key
    elif user_message.startswith('/onboarding'):
        
        json_filename = "flex_image_action"
        img_url = "https://storage.googleapis.com/linebot_materials/onboarding-start.jpeg"
        # signed_img_url = generate_signed_url("linebot_materials","onboarding-start", 3600)
        aspectRatio = "200:60"
        action_text = "/language"
        message_1_flex = create_flex_image_action_message(json_filename, img_url, aspectRatio, action_text)
        all_messages.append(message_1_flex)
    
    
    elif user_message.startswith('/sub: xai-free'):
        # 觸發：點選 subscribe 訂閱後，點選「領取試用！」
        # 處理：顯示系統訊息 - trial_offer_desc 獲得禮物卡、trial_steps 試用操作說明、free_trial 卡片 Flex 的連結
        
        message_1_text = create_text_message(translations["trial_offer_desc"]["text"])
        all_messages.append(message_1_text)
        
        message_2_text = create_text_message(translations["trial_steps"]["text"])
        all_messages.append(message_2_text)
        
        yt_url = "https://youtube.com/shorts/AEoeEIufl2E?feature=share"
        message_3_flex = create_text_message(translations["xai_api_yt_video_guide"]["text"].format(link=yt_url))
        all_messages.append(message_3_flex)
        
        flex_config = {
            "button_color": "#FF5722",
            "action_label": f'{translations["redeem_gift-xai"]["text"]}',
            "action_uri": "https://console.x.ai/"
        }
        message_4_flex = create_flex_message(translations["free_trial"]["text"], "flex_button_link", user_data['native_lang'], flex_config)
        all_messages.append(message_4_flex)
        
    
    # Command: 設定 Native Language
    elif user_message.startswith('/language'):
        text = translations["choose_language"]["text"]
        
        # 從 language_list.csv 讀取所有支援的語言列表
        language_list = []
        with open('./config/language_list.csv', newline='') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if not row or row[0].startswith('#'):
                    continue
                item = {"label": row[1], "text": f"/lang: {row[0]}"}
                language_list.append(item)

        message_1_quick_reply = create_quick_reply_message(text, language_list)
        all_messages.append(message_1_quick_reply)
    
    # Command: 處理取得的 Native Language，並詢問 Target Language (跟 /language 是連動的)
    elif user_message.startswith('/lang: '):
        native_lang = user_message.split('/lang: ')[1]  # e.g. 'zh-tw'
        valid_lang = False
        
        language_list = []
        with open('./config/language_list.csv', mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                language_list.append(row)
        
        for record in language_list:
            lang_code = record[0]
            if lang_code == native_lang:
                valid_lang = True
                break
        
        if valid_lang:
            user_data['native_lang'] = native_lang
            translations = load_translations(native_lang)
            
            def language_name_query(lang):
                language_name = None
                for lang in language_list:
                    if lang[0] == native_lang:
                        language_name = lang[1]
                        break
                return language_name
            
            native_language_name = language_name_query(native_lang)
            message_1_text = create_text_message(translations["confirm_native_language"]["text"].format(language_name=native_language_name))
            all_messages.append(message_1_text)
            message_2_text = create_text_message(translations["native_language_value"]["text"].format(language_name=native_language_name))
            all_messages.append(message_2_text)
            
            text = translations["practice_language"]["text"]
            learn_language_list = []
            with open('./config/language_list.csv', newline='') as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    if row[0] != native_lang:
                        learn_language_list.append({"label": row[1], "text": f"/learn: {row[0]}"})
                        
            message_3_quick_reply = create_quick_reply_message(text, learn_language_list)
            all_messages.append(message_3_quick_reply)
        
        else:
            text = translations["language_not_supported"]["text"]
            language_list = []
            with open('./config/language_list.csv', newline='') as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    if not row or row[0].startswith('#'):
                        continue
                    item = {"label": row[1], "text": f"/lang: {row[0]}"}
                    language_list.append(item)
            
            message_1_quick_reply = create_quick_reply_message(text, language_list)
            all_messages.append(message_1_quick_reply)
    
    # Command: 設定 Target Language (跟 /lang 是連動的)
    elif user_message.startswith('/learn: '):
        # 觸發：點選 /language 後，用戶點選「學習的目標語言」
        # 處理：顯示系統訊息 - confirm_target_language 確認目標語言、match_language_partner 說明此設置的目的、subscribe_offer 詢問訂閱項目(+ 帶入兩個訂閱項目選項)
        
        native_lang = user_data['native_lang']
        learn_lang = user_message.split('/learn: ')[1]
        valid_lang = False
        
        language_list = []
        with open('./config/language_list.csv', mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                language_list.append(row)
        
        # 檢查目標語言是否有效
        for record in language_list:
            lang_code = record[0]
            if lang_code == learn_lang:
                valid_lang = True
                break
        
        if valid_lang:
            user_data['target_lang'] = learn_lang
            
            def language_name_query(language_code):
                language_name = None
                for lang in language_list:
                    if lang[0] == language_code:
                        language_name = lang[1]
                        break
                return language_name
            
            native_language_name = language_name_query(native_lang)
            target_language_name = language_name_query(learn_lang)
            
            message_1_text = create_text_message(translations["confirm_target_language"]["text"].format(target_language_name=target_language_name))
            all_messages.append(message_1_text)
            
            message_2_text = create_text_message(translations["match_language_partner"]["text"].format(native_language_name=native_language_name, target_language_name=target_language_name))
            all_messages.append(message_2_text)
            
            text = translations["subscribe_offer"]["text"]
            items = [
                {"label": translations["quick_reply_btn_subscribe_now"]["text"], "text": "/sub: subscribe-now"},
                {"label": translations["quick_reply_btn_xai-free"]["text"], "text": "/sub: xai-free"}
            ]
            message_3_quick_reply = create_quick_reply_message(text, items)
            all_messages.append(message_3_quick_reply)
        
        else:
            text = translations["language_not_supported"]["text"]
            language_list = []
            with open('./config/language_list.csv', newline='') as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    if not row or row[0].startswith('#') or row[0] == native_lang:
                        continue
                    item = {"label": row[1], "text": f"/learn: {row[0]}"}
                    language_list.append(item)
            
            message_1_quick_reply = create_quick_reply_message(text, language_list)
            all_messages.append(message_1_quick_reply)
    
    # 點選購買時，兩個選項：立即訂閱*、稍後。稍後會直接連到 /api_instruction 的流程
    elif user_message == "/Subscribe":
        text = translations["subscribe_offer"]["text"]
        items = [
            {"label": translations["quick_reply_btn_subscribe_now"]["text"], "text": "/sub: subscribe-now"},
            {"label": translations["quick_reply_btn_membership"]["text"], "text": "/sub: membership"},
            {"label": translations["quick_reply_btn_xai-free"]["text"], "text": "/sub: xai-free"}
        ]
        message_1_quick_reply = create_quick_reply_message(text, items)
        all_messages.append(message_1_quick_reply)
        
    
    elif user_message == "/sub: subscribe-now":
        # 觸發：點選 subscribe 訂閱後，點選「立即訂閱」
        # 處理：顯示系統訊息 - flex_purchase 訂閱卡片 Flex 的連結、special_offer 特別優惠(+back 快速回覆返回按鈕)
        alt_text = translations["subscription_type"]["text"]
        json_filename = "flex_purchase"
        message_1_flex = create_flex_message(alt_text, json_filename, user_data['native_lang'])
        all_messages.append(message_1_flex)
        
        text = translations["special_offer"]["text"]
        purchase_items = [
            {"label": translations["back"]["text"], "text": "/Subscribe"}
        ]
        message_2_quick_reply = create_quick_reply_message(text, purchase_items)
        all_messages.append(message_2_quick_reply)
    
    
    # 查詢會員資訊
    elif user_message == "/sub: membership":
        sub_item = user_data['subscribe_item']
        sub_expire_time = user_data['subscribe_expired_timestamp']
        sub_expire_time = sub_expire_time.strftime('%Y-%m-%d %H:%M') + " (UTC+8)"
        
        # 從 subscribe_items.json 中讀取資料
        with open('./config/subscribe/subscribe_items.json', 'r', encoding='utf-8') as file:
            subscribe_items = json.load(file)['subscribe_items']
        
        # 找尋符合 sub_item 的 key，並把 name 取回來儲存成 sub_name
        sub_name = next((item['name'] for item in subscribe_items if item['code'] == sub_item), "Unknown Subscription")
        
        message_1_text = create_text_message(translations["query_membership"]["text"].format(sub_name=sub_name, sub_expire_time=sub_expire_time))
        all_messages.append(message_1_text)
    
    
    
    # 暫時未用
    elif user_message == "/sub: later":
        message_1_text = create_text_message(translations["gift_offer"]["text"])
        all_messages.append(message_1_text)
        
        message_2_text = create_text_message(translations["trial_steps"]["text"])
        all_messages.append(message_2_text)
        
        message_3_flex = create_flex_message(translations["free_trial"]["text"], "flex_xai_gift", user_data['native_lang'])
        all_messages.append(message_3_flex)
    
    
    elif user_message == "/ShareToFriend":
        message_1_text = create_text_message(translations["share_to_friend"]["text"])
        all_messages.append(message_1_text)
        
        message_2_text = create_text_message(translations["share_to_friend_guide"]["text"])
        all_messages.append(message_2_text)
    
    
    elif user_message == "/Hey":
        text = translations["Hey"]["text"]
        topic_items = translations["topic_items"]["text"]
        
        # 過濾掉長度大於 20 的項目
        filtered_topic_items = [item for item in topic_items if len(item) <= 20]
        sampled_items = random.sample(filtered_topic_items, 3)
        
        items = [{"label": item, "text": item} for i, item in enumerate(sampled_items)]
        
        message_1_quick_reply = create_quick_reply_message(text, items)
        all_messages.append(message_1_quick_reply)
    
    
    elif user_message == "/MatchPartner":
        start_conversation = start_conversation_when_matched(user_data)
        
        try:
            start_conversation = eval(start_conversation)
            if isinstance(start_conversation, list):
                # 逐一取出 start_conversation 中的對話內容，並轉換成 Text Message
                for message in start_conversation:
                    message_text = create_text_message(message)
                    all_messages.append(message_text)
            else:
                # 若 start_conversation 不是 list，則轉換成 Text Message
                message_text = create_text_message("Hey!")
                all_messages.append(message_text)
        except:
            # 若 start_conversation 不能被 eval，則轉換成 Text Message
            message_text = create_text_message("Hey!")
            all_messages.append(message_text)
    
    else:
        message_1_text = create_text_message(translations["unknown_command"]["text"])
        all_messages = [message_1_text]
    
    
    return user_data, all_messages