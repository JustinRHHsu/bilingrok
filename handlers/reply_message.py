from linebot.v3.messaging import (
    ApiClient, MessagingApi, TextMessage,
    ReplyMessageRequest, QuickReply, QuickReplyItem,
    MessageAction
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
        
        
        
        
def reply_message_with_quick_reply(reply_contents, reply_token, configuration, quick_reply_items=None):
    
    with ApiClient(configuration) as api_client:
        
        line_bot_api = MessagingApi(api_client)
        
        if quick_reply_items:
            quick_reply = QuickReply(items=[
                QuickReplyItem(
                    type="action",
                    action=MessageAction(label=item[1], text=item[0])
                ) for item in quick_reply_items
            ])
        else:
            quick_reply = None
        
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