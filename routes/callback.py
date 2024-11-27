import json
from flask import Blueprint, request, abort, current_app
from linebot.v3 import WebhookHandler
from linebot.v3.messaging import Configuration
from linebot.v3.exceptions import InvalidSignatureError
# from handlers.message_handler import handle_message_event
from handlers.handler_registry import register_all_handlers
from config.config import Config

callback_route = Blueprint('callback_route', __name__)


# Line API configuration
print(f"LINE_CHANNEL_ACCESS_TOKEN: {Config.LINE_CHANNEL_ACCESS_TOKEN}")
configuration = Configuration(access_token=Config.LINE_CHANNEL_ACCESS_TOKEN)
print(f"LINE_CHANNEL_SECRET: {Config.LINE_CHANNEL_SECRET}")
handler = WebhookHandler(Config.LINE_CHANNEL_SECRET)

# 註冊所有消息處理程式，ex: Text Message, Image Meesage, Audio Message
register_all_handlers(handler, configuration)


@callback_route.route("/callback", methods=['POST'])
def callback():
    
    
    # signature = request.headers['X-Line-Signature']
    signature = request.headers.get('X-Line-Signature')
    if not signature:
        current_app.logger.error("Missing X-Line-Signature header.")
        abort(400)
    print(f"=== Webhook Event Signature ===\n{signature}")
    
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