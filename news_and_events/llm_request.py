
import requests

def llm_request(location: str):
    url = 'https://your-cloud-function-url/get_news'
    response = requests.get(url, params={'location': location})
    if response.status_code == 200:
        return response.json()
    else:
        return {"status": "error", "message": response.text}