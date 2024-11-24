import os
import json
from datetime import datetime
from config.config import Config

from google.cloud import firestore, tasks_v2
from google.protobuf import timestamp_pb2
# Google Protocol Buffers（protobuf）的一部分，用於處理時間戳記。
# 它提供了 Timestamp 類別，該類別可以表示從 Unix 紀元（1970-01-01T00:00:00Z）以來的秒數和奈秒數


# 初始化 Cloud Tasks
client = tasks_v2.CloudTasksClient()
project = Config.GCP_PROJECT_ID
location = Config.QUEUE_LOCATION_MESSAGE_STORE
queue = Config.QUEUE_MESSAGE_STORE
parent = client.queue_path(project, location, queue)
TIME_SLOT_PROCESS_MESSAGES_TO_LLM = Config.TIME_SLOT_PROCESS_MESSAGES_TO_LLM


def create_or_update_task(user_id):
    # 任務名稱使用用戶 ID，確保每個用戶只有一個待執行任務
    task_name = f'msgstore-{user_id}'
    task_path = client.task_path(project, location, queue, task_name)

    # 嘗試刪除已有的任務（若存在）
    try:
        client.delete_task(request={"name": task_path})
    except:
        pass  # 任務可能不存在，忽略錯誤

    # 設定任務執行時間為現在 + n 秒
    d = datetime.datetime.utcnow() + datetime.timedelta(seconds=TIME_SLOT_PROCESS_MESSAGES_TO_LLM)
    timestamp_pb = timestamp_pb2.Timestamp()
    timestamp_pb.FromDatetime(d)

    # 任務 payload 可以包含 user_id
    payload = {'user_id': user_id}
    payload_json = json.dumps(payload)

    task = {
        'name': task_path,
        'schedule_time': timestamp_pb,
        'http_request': {  # 指定目標 Cloud Function 的 URL
            'http_method': tasks_v2.HttpMethod.POST,
            'url': os.getenv('TASK_HANDLER_URL'),  # 例如 'https://your-region-your-project.cloudfunctions.net/task_handler'
            'headers': {'Content-type': 'application/json'},
            'body': payload_json.encode()
        }
    }

    # 建立任務
    client.create_task(request={"parent": parent, "task": task})