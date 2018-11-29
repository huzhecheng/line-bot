import os
from urllib.request import urlopen
from urllib.parse import unquote
from firebase import firebase
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi(os.environ.get('Channel_Access_Token'))
# Channel Secret
handler = WebhookHandler(os.environ.get('Channel_Secret'))


# 監聽所有來自 /callback 的 Post Request


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

# 電影


def movie():
    url = os.environ.get('Firebase_Url')
    fb = firebase.FirebaseApplication(url)
    content = fb.get('/movie', None)
    return content

# 匯率


def currency(keyword):
    url = os.environ.get('Firebase_Url')
    fb = firebase.FirebaseApplication(url)
    content = ''
    dic = fb.get('/currency', None)
    if keyword in dic:
        content = dic[keyword]
    return content

# 天氣


def wheather(keyword):
    url = os.environ.get('Firebase_Url')
    fb = firebase.FirebaseApplication(url)
    content = ''
    dic = fb.get('/wheather', None)
    if keyword in dic:
        content = dic[keyword]
    return content

# 處理訊息


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = event.message.text
    if message == "最新電影":
        content = movie()
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=content))
        return 0
    if message.startswith("匯率:"):
        keyword = message.split(':')[1]
        content = currency(keyword)
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=content))
        return 0
    if message.startswith("天氣:"):
        keyword = message.split(':')[1]
        content = wheather(keyword)
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=content))
        return 0
    if message == "教學":
        button_template = TemplateSendMessage(
            alt_text='教學',
            template=ButtonsTemplate(
                title='請選擇:',
                text='我有什麼能夠為您服務的嗎？',
                thumbnail_image_url='https://cdn0.iconfinder.com/data/icons/streamline-emoji-1/48/092-robot-face-1-256.png',
                actions=[
                    MessageTemplateAction(
                        label='最新電影',
                        text='最新電影'
                    ),
                    MessageTemplateAction(
                        label='天氣資訊',
                        text='輸入「天氣:城市」，Ex:天氣:臺北市'
                    ),
                    MessageTemplateAction(
                        label='查詢匯率',
                        text='輸入「匯率:幣別」，Ex:匯率:美金'
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, button_template)
        return 0


if __name__ == "__main__":
    app.run()
