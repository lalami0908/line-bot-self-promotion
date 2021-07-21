from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.models import (
    TextMessage, ButtonsTemplate, TemplateSendMessage, MessageTemplateAction, ImageSendMessage, StickerSendMessage
)

import os
import sys
import json
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


def createImgUrl(ImgfileName):
    return 'https://' + appName + '.herokuapp.com' + ImgfileName


def buttonsTemplate(reply_token, func_name):
    image_url = createImgUrl(msgJson[func_name + 'ImgUrl'])
    buttons_template = ButtonsTemplate(title=msgJson[func_name + 'Title'], text=msgJson[func_name+'Text'],
                                       thumbnail_image_url=image_url,
                                       actions=[MessageTemplateAction(label=i, text=i) for i in msgJson[func_name+'Button']])
    template_message = TemplateSendMessage(
        alt_text=msgJson[func_name+'Title'], template=buttons_template)

    line_bot_api.reply_message(reply_token, template_message)


def textsMessage(reply_token, func_name):
    messages = [TextMessage(text=i) for i in msgJson[func_name+'Texts']]

    if msgJson.get(func_name + 'ImgUrl') != None:
        image_url = createImgUrl(msgJson[func_name + 'ImgUrl'])
        image = ImageSendMessage(
            original_content_url=image_url, preview_image_url=image_url)
        messages.append(image)

    line_bot_api.reply_message(reply_token, messages)


def taskTemplate(reply_token, func_name, image_url=None):
    print("taskTemplate")
