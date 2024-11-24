from linebot.v3 import WebhookHandler
from linebot.v3.messaging import Configuration
from linebot.v3.exceptions import InvalidSignatureError

from linebot.v3.webhooks import MessageEvent, TextMessageContent


from datetime import datetime

from config.config import Config
from services.line_service import line_bot_api

from services.firestore_service import get_or_create_user, update_user_data
from services.llm_service import handle_normal_conversation

from handlers.api_key_handler import handle_api_key_command
from handlers.feedback_handler import handle_feedback_command

configuration = Configuration(access_token=Config.LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(Config.LINE_CHANNEL_SECRET)



@handler.add(MessageEvent, message=TextMessageContent)
def handle_message_event(body, signature):
    handler.handle(body, signature)

def handle_message(event, configuration):
    user_id = event.source.user_id
    user_text = event.message.text.strip()
    reply_token = event.reply_token

    user_data = get_or_create_user(user_id)
    update_user_data(user_id, {'last_message_timestamp': datetime.datetime.utcnow()})

    if user_text.startswith('/api_key'):
        handle_api_key_command(user_text, user_id)
    elif user_text.startswith('/feedback'):
        handle_feedback_command(user_text, user_id)
    else:
        handle_normal_conversation(user_text, user_id, reply_token, configuration)
        
        
    