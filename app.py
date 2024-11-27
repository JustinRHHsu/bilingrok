from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

app = Flask(__name__)

# 你的 LINE Bot 的 Channel Access Token 和 Channel Secret
LINE_CHANNEL_ACCESS_TOKEN = 'R2ofHIXEe9CX7NVkI3/1gpvsihyZFLWQ1K3cviGf23V9Vm2nMrinPT7IpTr1H9YCAQ/sjVfm0K0jXx9rVto1iMi4Tl0Uyna/cIoezl8Pi74lRqXHT1YENw8gGoW3CK1ngAdf7SQYOv514FUvERkA7gdB04t89/1O/w1cDnyilFU='
LINE_CHANNEL_SECRET = 'c3256685cb342904f8bcdeebcd533a2b'

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
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

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # 回覆相同的訊息給用戶
    reply_message = TextSendMessage(text=event.message.text)
    line_bot_api.reply_message(event.reply_token, reply_message)

if __name__ == "__main__":
    app.run(port=5000)