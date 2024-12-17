import logging
from openai import OpenAI

logger = logging.getLogger(__name__)

# base_url=f"https://{location}-aiplatform.googleapis.com/v1beta1/projects/{PROJECT_ID}/locations/{location}/endpoints/openapi",
# "google": "https://generativelanguage.googleapis.com/v1beta/openai/", 

class LLMService:
    def __init__(self, api_type, api_key, model):
        self.api_type = api_type
        self.api_key = api_key
        self.model = model
        self.setup_api()

    def setup_api(self):
        base_urls = {
            "openai": "https://api.openai.com/v1",
            "google": "https://generativelanguage.googleapis.com/v1beta/openai/",
            "xai": "https://api.x.ai/v1"
        }

        if self.api_type in base_urls:
            self.client = OpenAI(
                api_key=self.api_key,
                base_url=base_urls[self.api_type]
            )
        else:
            raise ValueError(f"Unsupported api_type: {self.api_type}")


    def completion(self, messages, user_data, max_tokens=4096, temperature=0.7, timeout=300):
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=max_tokens,
                temperature=temperature,
                timeout=timeout
            )
            reply_content = response.choices[0].message.content
            reply_timestamp = int(f"{response.created}000")  # 將秒轉換為毫秒
            prompt_tokens = response.usage.prompt_tokens
            completion_tokens = response.usage.completion_tokens

            user_data['prompt_tokens'] += prompt_tokens
            logging.info(f"Prompt tokens: {prompt_tokens}")
            user_data['completion_tokens'] += completion_tokens
            logging.info(f"Completion tokens: {completion_tokens}")

            return user_data, reply_content, reply_timestamp

        except Exception as e:
            logger.error(
                f"[LLM API Error] 請求失敗 - 錯誤訊息: {str(e)}, "
                f"錯誤類型: {type(e).__name__}"
            )
            reply_content = "[System] Sorry, I'm having trouble understanding you right now. Please try again later."
            reply_timestamp = None
            return user_data, reply_content, reply_timestamp

