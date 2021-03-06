import os
import sys
import json
from flask import Flask, request, abort
# from dotenv import load_dotenv, find_dotenv
# load_dotenv(find_dotenv())

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, StickerMessage, TextSendMessage, StickerSendMessage,
    SourceUser, FollowEvent
)

from chatBot import ChatBot

app = Flask(__name__,  static_url_path='/static')

# Channel Secret
channel_secret = os.getenv('CHANNEL_SECRET', None)
# Channel Access Token
channel_access_token = os.getenv('CHANNEL_ACCESS_TOKEN', None)
# heroku App name
appName = os.getenv('HEROKU_APP_NAME', None)

if channel_secret is None:
    print('Specify CHANNEL_SECRET as environment variable.')
    sys.exit(1)
if channel_access_token is None:
    print('Specify CHANNEL_ACCESS_TOKEN as environment variable.')
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)

with open('./msg.json') as msg_file:
    msgJson = json.load(msg_file)


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
        abort(400)
    return 'OK'


@ handler.add(FollowEvent)
def handle_follow(event):
    # get user Profile and introduce the chat Bot
    if isinstance(event.source, SourceUser):
        profile = line_bot_api.get_profile(event.source.user_id)
        message = TextSendMessage(
            text=msgJson['greeting'] + profile.display_name + msgJson['greetingText'])
        line_bot_api.reply_message(event.reply_token, message)

# handle text message


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    text = event.message.text

    chatBot = ChatBot(text)
    reply_msg_function, func_name, msg = chatBot.judgeMsgAndGetReply()
    reply_msg_function(event.reply_token, func_name, msg)


@handler.add(MessageEvent, message=StickerMessage)
def handle_sticker(event):
    chatBot = ChatBot("")
    reply_msg_function, func_name, msg = chatBot.judgeMsgAndGetReply()
    reply_msg_function(event.reply_token, func_name, msg)


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

