# line_bot_message_builder.py
# 組裝 LINE 發送的消息

import os, json
from linebot.v3.messaging import (
    TextMessage, ImageMessage, FlexMessage, QuickReply, QuickReplyItem, MessageAction
)

from linebot.v3.messaging import (
    FlexMessage,
    MessageAction,
    FlexContainer
)
from config.config import Config

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





def create_flex_message(alt_text, json_filename):
    """
    建立 Flex Message。
    :param alt_text: Flex Message 的替代文字。
    :param json_filename: Flex Message 的內容檔案名稱。
    :return: FlexMessage 物件。
    """
    
    print(f"==== create_flex_message() =====")
    
    # 從 JSON 檔案讀取 Flex Message 結構
    with open(f'{Config.FLEX_LIBRARY_PATH}/{json_filename}.json', 'r', encoding='utf-8') as f:
        flex_message_json = json.load(f)

    # 將 JSON 轉換為字串格式
    flex_message_str = json.dumps(flex_message_json)

    # 將 JSON 字串轉換為 FlexContainer 物件
    flex_container = FlexContainer.from_json(flex_message_str)

    # 建立 FlexMessage 物件
    flex_message = FlexMessage(
        alt_text=alt_text, 
        contents=flex_container
    )

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