
# OpenAI SDK
from openai import OpenAI

client = OpenAI(
    api_key="OPENAI_API_KEY",
    base_url=https://api.openai.com/v1/chat/completions
)

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {
            "role": "user",
            "content": "Say this is a test",
        }
    ], 
)
print(response.choices[0].message)


# Google Gemini Compatible with OpenAI SDK
from openai import OpenAI

client = OpenAI(
    api_key="GEMINI_API_KEY",
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

response = client.chat.completions.create(
    model="gemini-1.5-flash",
    n=1,
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {
            "role": "user",
            "content": "Explain to me how AI works"
        }
    ]
)

print(response.choices[0].message)



# xAI Grok Compatible with OpenAI SDK

import os
from openai import OpenAI

XAI_API_KEY = os.getenv("XAI_API_KEY")
client = OpenAI(
    api_key=XAI_API_KEY,
    base_url="https://api.x.ai/v1",
)

completion = client.chat.completions.create(
    model="grok-beta",
    messages=[
        {"role": "system", "content": "You are Grok, a chatbot inspired by the Hitchhikers Guide to the Galaxy."},
        {"role": "user", "content": "What is the meaning of life, the universe, and everything?"},
    ],
)

print(completion.choices[0].message)


# xAI Grok Compatible with Anthropic SDK

import os
from anthropic import Anthropic

XAI_API_KEY = os.getenv("XAI_API_KEY")
client = Anthropic(
    api_key=XAI_API_KEY,
    base_url="https://api.x.ai",
)
message = client.messages.create(
    model="grok-beta",
    max_tokens=128,
    system="You are Grok, a chatbot inspired by the Hitchhiker's Guide to the Galaxy.",
    messages=[
        {
            "role": "user",
            "content": "What is the meaning of life, the universe, and everything?",
        },
    ],
)
print(message.content)



