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
print(f"Configuration: {Config.LINE_CHANNEL_SECRET}")
handler = WebhookHandler(Config.LINE_CHANNEL_SECRET)

# 註冊所有消息處理程式，ex: Text Message, Image Meesage, Audio Message
register_all_handlers(handler, configuration)


@callback_route.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    # current_app.logger.info(f"\n=== Request body ===\n{body}")

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        current_app.logger.info("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)
    except Exception as e:
        current_app.logger.error(f"An error occurred: {e}")
        abort(500)
    return 'OK', 200



@callback_route.route("/whoareyou", methods=['GET'])
def whoareyou():
    return "Hello, I'm a Chatbot!"