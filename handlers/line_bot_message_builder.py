# line_bot_message_builder.py
# 組裝 LINE 發送的消息

import os, json, re
from linebot.v3.messaging import (
    TextMessage, ImageMessage, FlexMessage, QuickReply, QuickReplyItem, MessageAction
)

from linebot.v3.messaging import (
    FlexMessage,
    MessageAction,
    FlexContainer
)
from config.config import Config
from handlers.script_translation import load_translations

"""
# 定義文字內容
text_content = "這是一則文字訊息"

# 調用 create_text_message 函數
text_message = create_text_message(text_content)
"""

def create_text_message(text):
    """
    建立文字訊息。
    :param text: 要傳送的文字內容。
    :return: TextMessage 物件。
    """
    return TextMessage(text=text)


"""

# 定義圖片的 URL
original_url = "https://example.com/original.jpg"
preview_url = "https://example.com/preview.jpg"

# 調用 create_image_message 函數
image_message = create_image_message(original_url, preview_url)

"""
def create_image_message(original_url, preview_url):
    """
    建立圖片訊息。
    :param original_url: 原始圖片的 URL。
    :param preview_url: 預覽圖片的 URL。
    :return: ImageMessage 物件。
    """
    return ImageMessage(
        original_content_url=original_url,
        preview_image_url=preview_url
    )





def create_flex_message(alt_text, json_filename, native_lang='en-us', flex_config={}):
    """
    建立 Flex Message。
    :param alt_text: Flex Message 的替代文字。
    :param json_filename: Flex Message 的內容檔案名稱。
    :param native_lang: 用戶的母語，預設為 'en-us'。
    :return: FlexMessage 物件。
    """
    # 從 JSON 檔案讀取 Flex Message 結構
    with open(f'{Config.FLEX_LIBRARY_PATH}/{json_filename}.json', 'r', encoding='utf-8') as f:
        flex_message_json = json.load(f)

    # 將 JSON 轉換為字串格式
    flex_message_str = json.dumps(flex_message_json)
    
    # 檢查是否包含 placeholder
    if re.search(r'\{.*?\}', flex_message_str):
        # 讀取翻譯檔案
        translations = load_translations(native_lang)

        # 替換 translations 中的 placeholder
        for key, value in translations.items():
            placeholder = f"{{{key}}}"
            if placeholder in flex_message_str:
                print(f"## Replacing placeholder: {placeholder} with {value['text']}")
                flex_message_str = flex_message_str.replace(placeholder, value['text'])

        # 替換 flex_config 中的 placeholder
        for key, value in flex_config.items():
            placeholder = f"{{{key}}}"
            if placeholder in flex_message_str:
                print(f"## Replacing placeholder: {placeholder} with {value}")
                flex_message_str = flex_message_str.replace(placeholder, value)

    # 將 JSON 字串轉換為 FlexContainer 物件
    flex_container = FlexContainer.from_json(flex_message_str)

    # 建立 FlexMessage 物件
    flex_message = FlexMessage(
        alt_text=alt_text, 
        contents=flex_container
    )

    return flex_message
    


"""
yt_url = "https://www.youtube.com/watch?v=Ff-D38eCJ5s"
video_preview_image_url = "https://i.ytimg.com/vi/JF0Z6U4S9Ko/hqdefault.jpg"
message_3_flex = create_flex_youtube_message("flex_youtube", yt_url, video_preview_image_url)
all_messages.append(message_3_flex)
"""
def create_flex_youtube_message(json_filename, video_url, video_preview_image_url=None):
    """
    建立 Flex YouTube Message。
    :param json_filename: Flex Message 的內容檔案名稱。
    :param video_url: YouTube 影片的 URL。
    :param video_preview_image_url: 預覽圖片的 URL，非必填。
    :return: FlexMessage 物件。
    """
    # 從 JSON 檔案讀取 Flex Message 結構
    with open(f'{Config.FLEX_LIBRARY_PATH}/{json_filename}.json', 'r', encoding='utf-8') as f:
        flex_message_json = json.load(f)

    # 替換 video_url
    flex_message_json['hero']['url'] = video_url

    # 如果提供了 video_preview_image_url，則替換
    if video_preview_image_url:
        flex_message_json['hero']['previewUrl'] = video_preview_image_url

    # 將 JSON 轉換為字串格式
    flex_message_str = json.dumps(flex_message_json)
    
    print(f"## Flex Message String: {flex_message_str}")

    # 將 JSON 字串轉換為 FlexContainer 物件
    flex_container = FlexContainer.from_json(flex_message_str)

    # 建立 FlexMessage 物件
    flex_message = FlexMessage(
        alt_text="YouTube Video",
        contents=flex_container
    )

    return flex_message



def create_flex_image_action_message(json_filename, img_url, aspectRatio, action_text):
    
    print(f"[create_flex_image_action_message] img_url: {img_url}, aspectRatio: {aspectRatio}, action_text: {action_text}")
    # 從 JSON 檔案讀取 Flex Message 結構
    with open(f'{Config.FLEX_LIBRARY_PATH}/{json_filename}.json', 'r', encoding='utf-8') as f:
        flex_message_json = json.load(f)
    print(f"[create_flex_image_action_message] flex_message_json: {flex_message_json}")
    
    # 替換參數
    flex_message_json['hero']['url'] = img_url
    flex_message_json['hero']['aspectRatio'] = aspectRatio
    flex_message_json['hero']['action']['text'] = action_text
    print(f"[create_flex_image_action_message] flex_message_json: {flex_message_json}")
    
    # 將 JSON 轉換為字串格式
    flex_message_str = json.dumps(flex_message_json)
    print(f"[create_flex_image_action_message] flex_message_str: {flex_message_str}")
    
    # print(f"## Flex Message String: {flex_message_str}")

    # 將 JSON 字串轉換為 FlexContainer 物件
    flex_container = FlexContainer.from_json(flex_message_str)
    print(f"[create_flex_image_action_message] flex_container: {flex_container}")

    # 建立 FlexMessage 物件
    flex_message = FlexMessage(
        alt_text="Onboarding...",
        contents=flex_container
    )
    print(f"[create_flex_image_action_message] flex_message: {flex_message}")

    return flex_message


"""
# 定義快速回覆項目
text = "請選擇一個選項："

items = [
    {'label': '選項1', 'text': '這是選項1'},
    {'label': '選項2', 'text': '這是選項2'}
]

# 調用 create_quick_reply_message 函數
message = create_quick_reply_message(text, items)

"""
def create_quick_reply_message(text, items):
    """
    建立帶有快速回覆選項的文字訊息。
    :param text: 要傳送的文字內容。
    :param items: 快速回覆項目的列表，每項應為包含 'label' 和 'text' 的字典。
    :return: 帶有快速回覆的 TextMessage 物件。
    """
    quick_reply_items = [
        QuickReplyItem(
            action=MessageAction(label=item['label'], text=item['text'])
        ) for item in items
    ]
    quick_reply = QuickReply(items=quick_reply_items)
    return TextMessage(
        text=text,
        quick_reply=quick_reply
    )
