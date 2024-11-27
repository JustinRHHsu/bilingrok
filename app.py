from config.config import Config
from flask import Flask, request, abort
from linebot.v3 import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage
)
from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent
)

# 初始化 Flask
app = Flask(__name__)

# LINE API 設定
CHANNEL_SECRET = Config.LINE_CHANNEL_SECRET
CHANNEL_ACCESS_TOKEN = Config.LINE_CHANNEL_ACCESS_TOKEN

# 初始化 Webhook Handler
handler = WebhookHandler(CHANNEL_SECRET)

# 初始化 Messaging API 設定
configuration = Configuration(access_token=CHANNEL_ACCESS_TOKEN)

@app.route("/callback", methods=['POST'])
def callback():
    # 取得 X-Line-Signature header 值
    signature = request.headers['X-Line-Signature']
    
    # 取得請求內容
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    
    # 處理 webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        app.logger.info("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)
        
    return 'OK'

@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        line_bot_api.reply_message(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[TextMessage(text=event.message.text)]
            )
        )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=Config.PORT, debug=Config.DEBUG)
