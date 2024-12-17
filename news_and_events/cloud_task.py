from google.cloud import tasks_v2
from google.protobuf import timestamp_pb2
import datetime

def create_task(location: str):
    client = tasks_v2.CloudTasksClient()
    project = 'your-project-id'
    queue = 'your-queue-id'
    url = 'https://your-cloud-function-url/crawl_news'
    payload = {'location': location}
    
    parent = client.queue_path(project, 'us-central1', queue)
    task = {
        'http_request': {
            'http_method': tasks_v2.HttpMethod.POST,
            'url': url,
            'body': str(payload).encode()
        }
    }
    
    # Schedule task
    timestamp = timestamp_pb2.Timestamp()
    timestamp.FromDatetime(datetime.datetime.utcnow() + datetime.timedelta(minutes=5))
    task['schedule_time'] = timestamp
    
    response = client.create_task(request={"parent": parent, "task": task})
    return response
