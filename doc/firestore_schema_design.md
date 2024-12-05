# To Be Update the database 

users (Collection)
├── user_123 (Document)
│   ├── user_id: "user_123"
│   ├── name: "Alice"
│   ├── gender: "female"
│   ├── mode: 1
│   ├── api_key_type: "type1"
│   ├── api_key: "abc123xyz"
│   ├── api_key_created_timestamp: 2024-12-05T10:00:00Z
│   ├── api_key_updated_timestamp: 2024-12-05T12:00:00Z
│   ├── personalized_prompt: "prompt1"
│   ├── prompt_tokens: 100
│   ├── completion_tokens: 50
│   ├── conversation_count: 10
│   ├── native_lang: "zh-tw"
│   ├── target_lang: "us-en"
│   ├── subscribe_item: "item1"
│   ├── subscribe_expired_timestamp: 2024-12-12T10:00:00Z
│   ├── credits: 100
│   ├── last_message_timestamp: 2024-12-05T11:00:00Z
│   ├── acc_created_timestamp: 2024-12-05T10:00:00Z
│   └── chat_history (Subcollection)
│       ├── auto_generated_id_1 (Document)
│       │   ├── message: "這是第一條訊息"
│       │   ├── timestamp: 2024-12-05T11:00:00Z
│       └── auto_generated_id_2 (Document)
│           ├── message: "關鍵字測試訊息"
│           ├── timestamp: 2024-12-05T11:30:00Z
├── user_456 (Document)
│   ├── user_id: "user_456"
│   ├── name: "Bob"
│   ├── gender: "male"
│   ├── mode: 1
│   ├── api_key_type: ""
│   ├── api_key: null
│   ├── api_key_created_timestamp: null
│   ├── api_key_updated_timestamp: null
│   ├── personalized_prompt: ""
│   ├── prompt_tokens: 0
│   ├── completion_tokens: 0
│   ├── conversation_count: 0
│   ├── native_lang: "zh-tw"
│   ├── target_lang: "us-en"
│   ├── subscribe_item: ""
│   ├── subscribe_expired_timestamp: null
│   ├── credits: 0
│   ├── last_message_timestamp: 2024-12-05T09:00:00Z
│   ├── acc_created_timestamp: 2024-12-04T08:00:00Z
│   └── chat_history (Subcollection)
│       └── auto_generated_id_1 (Document)
│           ├── message: "Hello! 我在測試聊天紀錄。"
│           ├── timestamp: 2024-12-05T09:00:00Z
├── user_789 (Document)
    ├── user_id: "user_789"
    ├── name: "Charlie"
    ├── gender: "male"
    ├── mode: 1
    ├── api_key_type: "type2"
    ├── api_key: "def456uvw"
    ├── api_key_created_timestamp: 2024-12-03T14:00:00Z
    ├── api_key_updated_timestamp: 2024-12-05T10:30:00Z
    ├── personalized_prompt: "prompt2"
    ├── prompt_tokens: 200
    ├── completion_tokens: 100
    ├── conversation_count: 20
    ├── native_lang: "zh-tw"
    ├── target_lang: "us-en"
    ├── subscribe_item: "item2"
    ├── subscribe_expired_timestamp: 2024-12-10T14:00:00Z
    ├── credits: 200
    ├── last_message_timestamp: 2024-12-05T10:30:00Z
    ├── acc_created_timestamp: 2024-12-03T14:00:00Z
    └── chat_history (Subcollection)
        ├── auto_generated_id_1 (Document)
        │   ├── message: "這是 Charlie 的第一條訊息。"
        │   ├── timestamp: 2024-12-03T15:00:00Z
        └── auto_generated_id_2 (Document)
            ├── message: "包含關鍵字的訊息。"
            ├── timestamp: 2024-12-04T16:00:00Z