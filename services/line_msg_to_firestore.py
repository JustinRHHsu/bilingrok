import base64
import json
from google.cloud import firestore


def linebot_to_firestore(event, context):
    """Triggered from a message on a Cloud Pub/Sub topic.
    Args:
         event (dict): Event payload.
         context (google.cloud.functions.Context): Metadata for the event.
    """
    # Decode the Pub/Sub message
    pubsub_message = base64.b64decode(event['data']).decode('utf-8')
    message_data = json.loads(pubsub_message)
    
    # Extract necessary information from the message
    user_id = message_data['events'][0]['source']['userId']
    message_text = message_data['events'][0]['message']['text']
    timestamp = message_data['events'][0]['timestamp']
    
    # Initialize Firestore client
    db = firestore.Client()
    
    # Reference to the chat_history collection
    chat_history_ref = db.collection('bilingrok').document('chat_history')
    
    # Add the message to Firestore
    chat_history_ref.set({
        'user_id': user_id,
        'message_text': message_text,
        'timestamp': timestamp
    }, merge=True)

    print(f"Message from {user_id} saved to Firestore.")