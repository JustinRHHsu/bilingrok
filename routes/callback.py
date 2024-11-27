import json
from flask import Blueprint, request, abort, current_app
from linebot.v3 import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError

from linebot.v3.messaging import Configuration

# from handlers.message_handler import handle_message_event
from handlers.handler_registry import register_all_handlers
from config.config import Config

callback_route = Blueprint('callback_route', __name__)



# LINE_CHANNEL_ACCESS_TOKEN = 'R2ofHIXEe9CX7NVkI3/1gpvsihyZFLWQ1K3cviGf23V9Vm2nMrinPT7IpTr1H9YCAQ/sjVfm0K0jXx9rVto1iMi4Tl0Uyna/cIoezl8Pi74lRqXHT1YENw8gGoW3CK1ngAdf7SQYOv514FUvERkA7gdB04t89/1O/w1cDnyilFU='
# LINE_CHANNEL_SECRET = 'c3256685cb342904f8bcdeebcd533a2b'

# Line API configuration
# print(f"LINE_CHANNEL_ACCESS_TOKEN: {Config.LINE_CHANNEL_ACCESS_TOKEN}")
configuration = Configuration(access_token=Config.LINE_CHANNEL_ACCESS_TOKEN)
print(f"LINE_CHANNEL_ACCESS_TOKEN: {Config.LINE_CHANNEL_ACCESS_TOKEN}")
print("=== This key from secret manager ===")
# configuration = Configuration(access_token=LINE_CHANNEL_ACCESS_TOKEN)

# print(f"LINE_CHANNEL_SECRET: {Config.LINE_CHANNEL_SECRET}")
handler = WebhookHandler(Config.LINE_CHANNEL_SECRET)
print(f"LINE_CHANNEL_SECRET: {Config.LINE_CHANNEL_SECRET}")
print("=== This key from secret manager ===")
# handler = WebhookHandler(LINE_CHANNEL_SECRET)


# 註冊所有消息處理程式，ex: Text Message, Image Meesage, Audio Message
register_all_handlers(handler, configuration)


@callback_route.route("/callback", methods=['POST'])
def callback():
    # signature = request.headers['X-Line-Signature']
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)

    try:
        print("=== Starting to handle Webhook Event ===")
        handler.handle(body, signature)
        print("=== Webhook Event Signature Verified ===")
    except InvalidSignatureError:
        print("=== Invalid Signature Error ===")
        current_app.logger.info("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)
    except Exception as e:
        print(f"=== An error occurred: {e} ===")
        current_app.logger.error(f"An error occurred: {e}")
        abort(500)
    
    print("=== Webhook Event handled successfully ===")    
    return 'OK', 200



@callback_route.route("/whoareyou", methods=['GET'])
def whoareyou():
    return "Hello, I'm a Chatbot!"