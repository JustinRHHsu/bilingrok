from handlers.text_message_handler import register_text_handler
# from .image_handler import register_image_handler
# from .audio_handler import register_audio_handler

def register_all_handlers(handler, configuration):
    print("=== Registering all message handlers ===")
    """註冊所有消息類型的處理程式"""
    register_text_handler(handler, configuration)
    print(f"=== Registered Text Message Handler ===")
    # register_image_handler(handler, configuration)
    # register_audio_handler(handler, configuration)