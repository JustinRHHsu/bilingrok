from openai import OpenAI
from config.config import Config
from linebot.v3.messaging import (
    ApiClient, MessagingApi, TextMessage,
    ReplyMessageRequest, QuickReply, QuickReplyItem,
    MessageAction
)
import logging

def update_personalized_prompt(feedback_message, user_data):
    prompt = f"用戶提供了以下反饋，用於更新個性化偏好：\n\n{feedback_message}\n\n請生成更新後的個性化偏好。"

    try:
        client = OpenAI(api_key=Config.XAI_API_KEY, base_url="https://api.x.ai/v1")
        response = client.completions.create(
            model='grok-beta',
            prompt=prompt,
            max_tokens=150
        )
        new_personalized_prompt = response.choices[0].message
        return new_personalized_prompt
    
    except Exception as e:
        logging.error(f"Grok API 調用失敗: {e}")
        return user_data.get('personalized_prompt', '')


def provide_summary(reply_token, user_id, user_data, configuration):
    summary_prompt = f"請針對用戶最近的對話，使用 {user_data.get('native_language', 'Chinese')} 提供總結和糾正。"
    try:
        client = OpenAI(api_key=Config.XAI_API_KEY, base_url="https://api.x.ai/v1")
        response = client.chat.completitions.create(
            model="grok-beta",
            messages=summary_prompt,
            max_tokens=200
        )
        reply_content = response.choices[0].message
        
        with ApiClient(configuration) as api_client:
            line_bot_api = MessagingApi(api_client)
            text_messages = TextMessage(
                text=reply_content
            )
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=reply_token,
                    messages=[text_messages]
                )
            )

    except Exception as e:
        logging.error(f"Grok API 調用失敗: {e}")