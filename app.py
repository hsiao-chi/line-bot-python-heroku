# encoding: utf-8
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('gHsZCt17+VcM/XoK8Bw2zrd+yKNIDH/RxlpWIsN5vpybMVwIqBKvykooJTBHHqYLTwQIF1JrPNH/QvNAWIZFF2abPucIBPVm2qDzQcH1HFNZB0roxPrQpoa6dPp4qvDqXAwClWQIAM1vWsFbwLLI+wdB04t89/1O/w1cDnyilFU=') #Your Channel Access Token
handler = WebhookHandler('3e004ec129a589b5feaf1c3d44c7315a') #Your Channel Secret

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

@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    text = event.message.text #message from user

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=text)) #reply the same message from user
    

import os
if __name__ == "__main__":
    app.run(host='0.0.0.0',port=os.environ['PORT'])
