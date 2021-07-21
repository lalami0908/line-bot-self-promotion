from reply import (buttonsTemplate, textsMessage, taskTemplate)
import json
with open('./msg.json') as msg_file:
    msgJson = json.load(msg_file)


class ChatBot:
    # mapping: 中文訊息 -> 英文 function name
    templateMap = {

    }

    textMap = {

    }

    taskMap = {
    }

    def __init__(self, msg):
        self.msg = msg

    def judgeMsgAndGetReply(self):
        reply_msg_function = None
        function_name = None
        if self.msg in self.templateMap:
            reply_msg_function = buttonsTemplate
            function_name = self.templateMap.get(self.msg)

        elif self.msg in self.textMap:
            reply_msg_function = textsMessage
            function_name = self.textMap.get(self.msg)

        elif self.msg in self.taskMap:
            reply_msg_function = taskTemplate
            function_name = self.taskMap.get(self.msg)
        # invailed input will return main function buttons template
        else:
            reply_msg_function = buttonsTemplate
            function_name = "mainFunction"
        return reply_msg_function, function_name
