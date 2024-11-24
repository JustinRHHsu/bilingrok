# from services.firestore_service import update_user_data, get_or_create_user
from services.line_service import line_bot_api
from utils.prompt_utils import update_personalized_prompt
from config.config import Config

from linebot.models import TextSendMessage

def handle_feedback_command(user_data, user_text, user_id):
    
    feedback_message = user_text.replace('/feedback', '').strip()
    # user_data = get_or_create_user(user_id)
    
    personalized_prompt = update_personalized_prompt(feedback_message, user_data)
    
    """
    update_user_data(user_id, {
        'personalized_prompt': personalized_prompt,
        'system_prompt': Config.BASE_PROMPT.format(
            native_language='Chinese',
            learn_language='English',
            personalized_prompt=personalized_prompt
        )
    })
    """
    
    user_data['personalized_prompt'] = personalized_prompt
    
    
    reply_text = '感謝您的反饋，您的偏好已更新。'
    # line_bot_api.push_message(user_id, TextSendMessage(text=reply_text))
    
    return user_data