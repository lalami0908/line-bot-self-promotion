from reply import (buttonsTemplate, textsMessage)
import json
import requests
from bs4 import BeautifulSoup
with open('./msg.json') as msg_file:
    msgJson = json.load(msg_file)


def crawler(url, selectStr):
    res = requests.get(url, verify=False)
    soup = BeautifulSoup(res.text, 'html.parser')
    content = ""
    for index, data in enumerate(soup.select(selectStr)[:3]):
        content += data.text.replace("\n", "")
        content += "\n"
        content += data['href']
        content += "\n"
    return content


def getUdnNews():
    url = 'https://udn.com/news/index'
    selectStr = 'div.focus a'
    content = crawler(url, selectStr)
    return content


def getTechNews():
    url = 'https://technews.tw/'
    selectStr = 'h1.entry-title a'
    content = crawler(url, selectStr)
    return content


class ChatBot:
    def __init__(self, msg):
        self.msg = msg
    # mapping: 中文訊息 -> 英文 function name
    templateMap = {
        msgJson['mainFunction']: "mainFunction",
        msgJson['selfIntroduction']: "selfIntroduction",
        msgJson['professionalAbility']: "professionalAbility",
        msgJson['otherTool']: "otherTool",
        msgJson['experience']: "experience",
        msgJson['project']: "project",
    }

    textMap = {
        msgJson['education']: "education",
        msgJson['owlsomeIntern']: "owlsomeIntern",
        msgJson['gssIntern']: "gssIntern",
        msgJson['projectProcessManagement']: "projectProcessManagement",
        msgJson['dynamicVehicleScheduling']: "dynamicVehicleScheduling",
        msgJson['personality']: "personality",
        msgJson['BinanceTelebot']: "BinanceTelebot",
        msgJson['QAsystem']: "QAsystem",
        msgJson['supplyAndDemandPlatform']: "supplyAndDemandPlatform",
        msgJson['ability']: "ability"
    }

    taskMap = {
        msgJson['tool1']: getUdnNews,
        msgJson['tool2']: getTechNews
    }

    def judgeMsgAndGetReply(self):
        reply_msg_function = None
        function_name = None
        msg = None
        if self.msg in self.templateMap:
            reply_msg_function = buttonsTemplate
            function_name = self.templateMap.get(self.msg)

        elif self.msg in self.textMap:
            reply_msg_function = textsMessage
            function_name = self.textMap.get(self.msg)

        elif self.msg in self.taskMap:
            reply_msg_function = textsMessage
            function_name = ""
            function = self.taskMap.get(self.msg)
            msg = function()
            print(msg)

        # invailed input will return main function buttons template
        else:
            reply_msg_function = buttonsTemplate
            function_name = "mainFunction"
        return reply_msg_function, function_name, msg
