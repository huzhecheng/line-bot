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

# 新聞


def news():
    url = os.environ.get('Firebase_Url')
    fb = firebase.FirebaseApplication(url)
    content = fb.get('/news', None)
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
    elif message.startswith("匯率:"):
        keyword = message.split(':')[1]
        content = currency(keyword)
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=content))
        return 0
    elif message.startswith("天氣:"):
        keyword = message.split(':')[1]
        content = wheather(keyword)
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=content))
        return 0
    elif message == "看新聞":
        content = news()
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=content))
        return 0
    elif message == "使用說明":
        button_template = TemplateSendMessage(
            alt_text='使用說明',
            template=ButtonsTemplate(
                title='請選擇:',
                text='我有什麼能夠為您服務的嗎？',
                thumbnail_image_url='https://cdn0.iconfinder.com/data/icons/streamline-emoji-1/48/092-robot-face-1-256.png',
                actions=[
                    MessageTemplateAction(
                        label='看電影',
                        text='最新電影'
                    ),
                    MessageTemplateAction(
                        label='查天氣',
                        text='查天氣'
                    ),
                    MessageTemplateAction(
                        label='查匯率',
                        text='查匯率'
                    ),
                    MessageTemplateAction(
                        label='看新聞',
                        text='看新聞'
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, button_template)
        return 0
    elif message == "查天氣":
        imagemap_message = ImagemapSendMessage(
            base_url='https://firebasestorage.googleapis.com/v0/b/linebot-version2-0.appspot.com/o/taiwanmap.jpg?alt=media&token=81bdb790-4a35-4d30-ac47-8a5c31cbd308#',
            alt_text='taiwanmap',
            base_size=BaseSize(height=1040, width=1040),
            actions=[
                MessageImagemapAction(
                    text='天氣:連江縣',
                    area=ImagemapArea(
                         x=149, y=85, width=80, height=80
                    )
                ),
                MessageImagemapAction(
                    text='天氣:金門縣',
                    area=ImagemapArea(
                         x=149, y=261, width=80, height=80
                    )
                ),
                MessageImagemapAction(
                    text='天氣:澎湖縣',
                    area=ImagemapArea(
                         x=150, y=450, width=80, height=80
                    )
                ),
                MessageImagemapAction(
                    text='天氣:基隆市',
                    area=ImagemapArea(
                         x=741, y=13, width=80, height=80
                    )
                ),
                MessageImagemapAction(
                    text='天氣:臺北市',
                    area=ImagemapArea(
                         x=684, y=42, width=80, height=80
                    )
                ),
                MessageImagemapAction(
                    text='天氣:新北市',
                    area=ImagemapArea(
                         x=695, y=118, width=80, height=80
                    )
                ),
                MessageImagemapAction(
                    text='天氣:桃園市',
                    area=ImagemapArea(
                         x=598, y=54, width=80, height=80
                    )
                ),
                MessageImagemapAction(
                    text='天氣:新竹市',
                    area=ImagemapArea(
                         x=523, y=107, width=80, height=80
                    )
                ),
                MessageImagemapAction(
                    text='天氣:新竹縣',
                    area=ImagemapArea(
                         x=611, y=156, width=80, height=80
                    )
                ),
                MessageImagemapAction(
                    text='天氣:宜蘭縣',
                    area=ImagemapArea(
                         x=725, y=199, width=80, height=80
                    )
                ),
                MessageImagemapAction(
                    text='天氣:苗栗縣',
                    area=ImagemapArea(
                         x=503, y=210, width=80, height=80
                    )
                ),
                MessageImagemapAction(
                    text='天氣:臺中市',
                    area=ImagemapArea(
                         x=469, y=296, width=80, height=80
                    )
                ),
                MessageImagemapAction(
                    text='天氣:彰化縣',
                    area=ImagemapArea(
                         x=393, y=361, width=80, height=80
                    )
                ),
                MessageImagemapAction(
                    text='天氣:南投縣',
                    area=ImagemapArea(
                         x=553, y=410, width=80, height=80
                    )
                ),
                MessageImagemapAction(
                    text='天氣:花蓮縣',
                    area=ImagemapArea(
                         x=658, y=412, width=80, height=80
                    )
                ),
                MessageImagemapAction(
                    text='天氣:雲林縣',
                    area=ImagemapArea(
                         x=336, y=450, width=80, height=80
                    )
                ),
                MessageImagemapAction(
                    text='天氣:嘉義市',
                    area=ImagemapArea(
                         x=409, y=489, width=80, height=80
                    )
                ),
                MessageImagemapAction(
                    text='天氣:嘉義縣',
                    area=ImagemapArea(
                         x=466, y=540, width=80, height=80
                    )
                ),
                MessageImagemapAction(
                    text='天氣:臺南市',
                    area=ImagemapArea(
                         x=374, y=604, width=80, height=80
                    )
                ),
                MessageImagemapAction(
                    text='天氣:高雄市',
                    area=ImagemapArea(
                         x=455, y=648, width=80, height=80
                    )
                ),
                MessageImagemapAction(
                    text='天氣:臺東縣',
                    area=ImagemapArea(
                         x=571, y=659, width=80, height=80
                    )
                ),
                MessageImagemapAction(
                    text='天氣:屏東縣',
                    area=ImagemapArea(
                         x=450, y=778, width=80, height=80
                    )
                )
            ]
        )
        line_bot_api.reply_message(event.reply_token, imagemap_message)
        return 0
    elif message == "查匯率":
        imagemap_message = ImagemapSendMessage(
            base_url='https://firebasestorage.googleapis.com/v0/b/linebot-version2-0.appspot.com/o/country.jpg?alt=media&token=f90212e6-5342-45af-9a0f-d37e4ee5bf04#',
            alt_text='currencyflag',
            base_size=BaseSize(height=1040, width=1040),
            actions=[
                MessageImagemapAction(
                    text='匯率:美金',
                    area=ImagemapArea(
                         x=50, y=31, width=145, height=117
                    )
                ),
                MessageImagemapAction(
                    text='匯率:港幣',
                    area=ImagemapArea(
                         x=50, y=261, width=145, height=117
                    )
                ),
                MessageImagemapAction(
                    text='匯率:紐元',
                    area=ImagemapArea(
                         x=50, y=488, width=145, height=117
                    )
                ),
                MessageImagemapAction(
                    text='匯率:澳幣',
                    area=ImagemapArea(
                         x=50, y=715, width=145, height=117
                    )
                ),
                MessageImagemapAction(
                    text='匯率:英鎊',
                    area=ImagemapArea(
                         x=249, y=31, width=145, height=117
                    )
                ),
                MessageImagemapAction(
                    text='匯率:日圓',
                    area=ImagemapArea(
                         x=249, y=262, width=145, height=117
                    )
                ),
                MessageImagemapAction(
                    text='匯率:歐元',
                    area=ImagemapArea(
                         x=249, y=491, width=145, height=117
                    )
                ),
                MessageImagemapAction(
                    text='匯率:加拿大幣',
                    area=ImagemapArea(
                         x=249, y=717, width=145, height=117
                    )
                ),
                MessageImagemapAction(
                    text='匯率:印尼幣',
                    area=ImagemapArea(
                         x=450, y=30, width=145, height=117
                    )
                ),
                MessageImagemapAction(
                    text='匯率:瑞典幣',
                    area=ImagemapArea(
                         x=450, y=264, width=145, height=117
                    )
                ),
                MessageImagemapAction(
                    text='匯率:南非幣',
                    area=ImagemapArea(
                         x=450, y=488, width=145, height=117
                    )
                ),
                MessageImagemapAction(
                    text='匯率:瑞士法郎',
                    area=ImagemapArea(
                         x=450, y=717, width=145, height=117
                    )
                ),
                MessageImagemapAction(
                    text='匯率:韓元',
                    area=ImagemapArea(
                         x=650, y=30, width=145, height=117
                    )
                ),
                MessageImagemapAction(
                    text='匯率:越南盾',
                    area=ImagemapArea(
                         x=650, y=264, width=145, height=117
                    )
                ),
                MessageImagemapAction(
                    text='匯率:菲國比索',
                    area=ImagemapArea(
                         x=650, y=486, width=145, height=117
                    )
                ),
                MessageImagemapAction(
                    text='匯率:新加坡幣',
                    area=ImagemapArea(
                         x=650, y=717, width=145, height=117
                    )
                ),
                MessageImagemapAction(
                    text='匯率:泰幣',
                    area=ImagemapArea(
                         x=852, y=33, width=145, height=117
                    )
                ),
                MessageImagemapAction(
                    text='匯率:馬來幣',
                    area=ImagemapArea(
                         x=856, y=266, width=145, height=117
                    )
                ),
                MessageImagemapAction(
                    text='匯率:人民幣',
                    area=ImagemapArea(
                         x=852, y=479, width=145, height=117
                    )
                )
            ]
        )
        line_bot_api.reply_message(event.reply_token, imagemap_message)
        return 0


if __name__ == "__main__":
    app.run()
