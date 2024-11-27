Project description
PyPI version

SDK of the LINE Messaging API for Python.

Introduction
The LINE Messaging API SDK for Python makes it easy to develop bots using LINE Messaging API, and you can create a sample bot within minutes.

Documentation
See the official API documentation for more information

English: https://developers.line.biz/en/docs/messaging-api/overview/

Japanese: https://developers.line.biz/ja/docs/messaging-api/overview/

Requirements
Python >= 3.9

Installation
$ pip install line-bot-sdk
Synopsis
Usage:

from flask import Flask, request, abort

from linebot.v3 import (
    WebhookHandler
)
from linebot.v3.exceptions import (
    InvalidSignatureError
)
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage
)
from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent
)

app = Flask(__name__)

configuration = Configuration(access_token='YOUR_CHANNEL_ACCESS_TOKEN')
handler = WebhookHandler('YOUR_CHANNEL_SECRET')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        app.logger.info("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        line_bot_api.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[TextMessage(text=event.message.text)]
            )
        )

if __name__ == "__main__":
    app.run()
API
See linebot/v3/messaging/docs . Other docs are in linebot/v3/<feature>/docs/*.md.

Webhook
WebhookParser
※ You can use WebhookParser

__init__(self, channel_secret)
parser = linebot.v3.WebhookParser('YOUR_CHANNEL_SECRET')
parse(self, body, signature, as_payload=False)
Parses the webhook body, and returns a list of Event objects or a WebhookPayload object (depending on as_payload). If the signature does NOT match, InvalidSignatureError is raised.

events = parser.parse(body, signature)

for event in events:
    do_something(event)
payload = parser.parse(body, signature, as_payload=True)

for event in payload.events:
    do_something(payload.event, payload.destination)
WebhookHandler
※ You can use WebhookHandler

__init__(self, channel_secret)
handler = linebot.v3.WebhookHandler('YOUR_CHANNEL_SECRET')
handle(self, body, signature)
Handles webhooks with handlers added by the decorators add and default. If the signature does NOT match, InvalidSignatureError is raised.

handler.handle(body, signature)
add(self, event, message=None)
Add a handler method by using this decorator.

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        ReplyMessageRequest(
            reply_token=event.reply_token,
            messages=[TextMessage(text=event.message.text)]
        )
    )
When the event is an instance of MessageEvent and event.message is an instance of TextMessage, this handler method is called.

@handler.add(MessageEvent)
def handle_message(event, destination):
    # do something
If the arity of the handler method is more than one, a destination property in a webhook request is passed to it as the second argument.

@handler.add(FollowEvent)
def handle_follow():
    # do something
If the arity of the handler method is zero, the handler method is called with no arguments.

default(self)
Set the default handler method by using this decorator.

@handler.default()
def default(event):
    print(event)
If there is no handler for an event, this default handler method is called.

WebhookPayload
https://developers.line.biz/en/reference/messaging-api/#request-body

WebhookPayload
destination

events: list[Event]

Webhook event object
https://developers.line.biz/en/reference/messaging-api/#webhook-event-objects

Hints
Examples
aiohttp-echo
Sample echo-bot with asynchronous processings.

fastapi-echo
Sample echo-bot using FastAPI

flask-echo
Sample echo-bot using Flask

flask-kitchensink
Sample bot using Flask

rich-menu
Switching richmenu script

simple-server-echo
Sample echo-bot using wsgiref.simple_server

How to deserializes JSON to FlexMessage or RichMenu
line-bot-python-sdk provides from_json method for each model. It deserializes the JSON into the specified model. Thus, you can send a JSON designed with Flex Message Simulator.

bubble_string = """{ type:"bubble", ... }"""
message = FlexMessage(alt_text="hello", contents=FlexContainer.from_json(bubble_string))
line_bot_api.reply_message(
    ReplyMessageRequest(
        reply_token=event.reply_token,
        messages=[message]
    )
)
How to get x-line-request-id header and error message
You may need to store the x-line-request-id header obtained as a response from several APIs. In this case, please use ~_with_http_info functions. You can get headers and status codes. The x-line-accepted-request-id or content-type header can also be obtained in the same way.

response = line_bot_api.reply_message_with_http_info(
    ReplyMessageRequest(
        reply_token=event.reply_token,
        messages=[TextMessage(text='see application log')]
    )
)
app.logger.info("Got response with http status code: " + str(response.status_code))
app.logger.info("Got x-line-request-id: " + response.headers['x-line-request-id'])
app.logger.info("Got response with http body: " + str(response.data))
You can get error messages from ApiException when you use MessagingApi. Each client defines its own exception class.

from linebot.v3.messaging import ApiException, ErrorResponse
try:
    line_bot_api.reply_message_with_http_info(
        ReplyMessageRequest(
            reply_token='invalid-reply-token',
            messages=[TextMessage(text='see application log')]
        )
    )
except ApiException as e:
    app.logger.info("Got response with http status code: " + str(e.status))
    app.logger.info("Got x-line-request-id: " + e.headers['x-line-request-id'])
    app.logger.info("Got response with http body: " + str(ErrorResponse.from_json(e.body)))
When you need to get x-line-accepted-request-id header from error response, you can get it: e.headers['x-line-accepted-request-id'].

Help and media
FAQ: https://developers.line.biz/en/faq/

News: https://developers.line.biz/en/news/

Versioning
This project respects semantic versioning

See http://semver.org/

Version 3.x
LINE’s SDK developer team decided to generate SDK code based on OpenAPI spec. https://github.com/line/line-openapi

As a result, LINE bot sdk 3.x is not compatible with 2.x. It can follow the future API changes very quickly.

We will be maintaining only linebot.v3 going forward. To utilize the latest features, we recommend you gradually transition to linebot.v3 modules in your application, although you can still continue to use the 2.x linebot modules.

While we won’t update linebot modules anymore, users can still continue to use the version 2.x linebot modules. We also welcome pull requests for the version 2.x and 3.x modules.

How to suppress deprecation warnings
If you keep using old line-bot-sdk library (version < 3.x) but use 3.x, you’ll get

LineBotSdkDeprecatedIn30: Call to deprecated method get_bot_info. (Use 'from linebot.v3.messaging import MessagingApi' and 'MessagingApi(...).get_bot_info(...)' instead. See https://github.com/line/line-bot-sdk-python/blob/master/README.rst for more details.) -- Deprecated since version 3.0.0.
If it’s noisy, you can suppress this warning as follows.

import warnings
from linebot import LineBotSdkDeprecatedIn30

## your code here
...

if __name__ == '__main__':
    warnings.filterwarnings("ignore", category=LineBotSdkDeprecatedIn30)
Contributing
Please check CONTRIBUTING before making a contribution.

For SDK developers
First install for development.

$ pip install -r requirements-dev.txt
You can generate new or fixed models and APIs by this command.

$ python generate-code.py
When you update line-bot-sdk-python version, please update linebot/__about__.py and generate code again.

If you edit README.rst, you should execute the following command to check the syntax of README.

$ python -m readme_renderer README.rst
Run tests
Test by using tox. We test against the following versions.

3.9

3.10

3.11

3.12

To run all tests and to run flake8 against all versions, use:

tox
To run all tests against version 3.10, use:

$ tox -e py3.10
To run a test against version 3.10 and against a specific file, use:

$ tox -e py3.10 -- tests/test_webhook.py
License
Copyright (C) 2016 LINE Corp.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.