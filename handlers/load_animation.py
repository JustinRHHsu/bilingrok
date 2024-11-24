from linebot.v3.messaging import ApiClient, MessagingApi
from linebot.v3.messaging.models.show_loading_animation_request import ShowLoadingAnimationRequest


def send_loading_animation(configuration, user_id, loading_seconds=5):
    """
    發送載入動畫給指定的用戶。

    :param configuration: 已建立的 Configuration 物件
    :param user_id: 用戶的 ID
    :param loading_seconds: 載入動畫的持續時間（秒），範圍為 5 到 60 秒
    """
    # 檢查 loading_seconds 是否在有效範圍內
    if not (5 <= loading_seconds <= 60):
        raise ValueError("loading_seconds 必須在 5 到 60 秒之間")

    # Enter a context with an instance of the API client
    with ApiClient(configuration) as api_client:
        # Create an instance of the API class
        api_instance = MessagingApi(api_client)
        show_loading_animation_request = ShowLoadingAnimationRequest(chatId=user_id, loadingSeconds=loading_seconds)

        try:
            api_response = api_instance.show_loading_animation(show_loading_animation_request)
            # print("The response of MessagingApi->show_loading_animation:\n")
            # print(api_response)
            
        except Exception as e:
            print("Exception when calling MessagingApi->show_loading_animation: %s\n" % e)