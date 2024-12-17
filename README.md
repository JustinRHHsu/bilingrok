# Bilingrok Language Partner Service
Bilingrok is a language learning application that pairs users with language practice partners through the LINE platform, helping users practice languages in natural conversations.

Bilingrok is a language learning application available on the LINE platform, which has 194 million monthly active users. It connects users with language practice partners—just like chatting with friends—enabling natural conversations to practice languages and build friendships.

Whether you're one of the 10 million foreign workers across APAC countries (excluding China) or someone eager to learn a second or third language, Bilingrok makes it easy to chat and improve your language skills through LINE's real-time messaging.


## Project Structure
project/
│
├── app.py
├── config.py
├── routes/
│   └── callback.py
├── handlers/
│   ├── message_handler.py
│   ├── api_key_handler.py
│   └── feedback_handler.py
├── services/
│   ├── firestore_service.py
│   ├── line_service.py
│   └── openai_service.py
└── utils/
    └── prompt_utils.py


## Environment Setup
### 1. Create Virtual Environment

```python3.10 -m venv venv```
```source venv/bin/activate```

### 2. Install Dependencies
pip install -r requirements.txt

### 3. Configure Environment Variables
Create a .env file in the config folder and fill in the relevant environment variables.

### 4. Configure GCP
Run the gcloud_setting.sh script to configure the necessary services and permissions for GCP.
```chmod +x scripts/gcloud_setting.sh```
```./scripts/gcloud_setting.sh```

## CI/CD
Every push to GitHub triggers Cloud Build for automatic building and deployment.

## Language Configuration
Language configuration files are located in the translations folder, supporting multiple languages.

## Documentation
Firestore Schema Design
Language Translation Configuration

## License
This project is licensed under the Apache 2.0 License.
