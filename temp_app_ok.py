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

app = Flask(__name__)

# 你的 LINE Bot 的 Channel Access Token 和 Channel Secret
LINE_CHANNEL_ACCESS_TOKEN = 'R2ofHIXEe9CX7NVkI3/1gpvsihyZFLWQ1K3cviGf23V9Vm2nMrinPT7IpTr1H9YCAQ/sjVfm0K0jXx9rVto1iMi4Tl0Uyna/cIoezl8Pi74lRqXHT1YENw8gGoW3CK1ngAdf7SQYOv514FUvERkA7gdB04t89/1O/w1cDnyilFU='
LINE_CHANNEL_SECRET = 'c3256685cb342904f8bcdeebcd533a2b'

configuration = Configuration(access_token=LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

@app.route("/callback", methods=['POST'])
def callback():
    # 確認請求來自 LINE 平台
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    # 回覆相同的訊息給用戶
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        line_bot_api.reply_message(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[TextMessage(text=event.message.text)]
            )
        )

if __name__ == "__main__":
    app.run(port=5000)