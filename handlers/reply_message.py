# 組裝成 Messenging API 的格式，並回傳給用戶

from linebot.v3.messaging import (
    ApiClient, MessagingApi, 
    TextMessage, ImageMessage,
    ReplyMessageRequest, QuickReply, QuickReplyItem,
    MessageAction, FlexMessage
)



def TO_BE_DELETE_reply_message(reply_contents, reply_token, configuration):
    
    for content in reply_contents:
        print(f"=== Each Reply Content ===")
        print(content)
        print("==============================")
        
    with ApiClient(configuration) as api_client:
        
        line_bot_api = MessagingApi(api_client)
        
        # TBD - 這裡要改成動態生成
        quick_reply = QuickReply(items=[
            QuickReplyItem(
                type="action",
                action=MessageAction(label="中文", text="中文")
            ),
            QuickReplyItem(
                type="action",
                action=MessageAction(label="English", text="English")
            )
        ])
        
        text_messages = [
            TextMessage(
                text=content,
                quick_reply=quick_reply
            ) for content in reply_contents
        ]
        
        line_bot_api.reply_message(
            ReplyMessageRequest(
                reply_token=reply_token,
                messages=text_messages
            )
        )
        
        
        
        
# def reply_message_with_quick_reply(reply_token, configuration, reply_contents, quick_reply_items=None, img_reply_msg_list=None, flex_msg_list=None):
def line_reply_message(reply_token, configuration, all_messages):    
    
    if not all_messages:
        message = "Error(481): Response error! Please contact with administrator"
        all_messages[message]
        return
    
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        
        # 只保留前 5 則訊息
        all_messages = all_messages[:5]
        
        line_bot_api.reply_message(
            ReplyMessageRequest(
                reply_token=reply_token,
                messages=all_messages
            )
        )