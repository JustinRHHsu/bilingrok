# from services.firestore_service import update_user_data
from services.line_service import line_bot_api
import datetime

from linebot.models import TextSendMessage

def handle_api_key_command(user_data, user_text, user_id):
    grok_api_key = user_text.replace('api_key', '').strip()
    
    """
    update_user_data(user_id, {
        'grok_api_key': grok_api_key,
        'api_created_date': datetime.datetime.utcnow()
    })
    """
    
    user_data['grok_api_key'] = grok_api_key
    user_data['api_created_date'] = datetime.datetime.utcnow()
    
    
    reply_text = '您的 Grok API 密鑰已更新!'
    # line_bot_api.push_message(user_id, TextSendMessage(text=reply_text))
    
    return user_data