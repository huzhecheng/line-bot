import os
import datetime
from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.parse import unquote
from firebase import firebase
from flask import Flask, request, abort

app = Flask(__name__)

dateNow = ((datetime.datetime.now()) +
           datetime.timedelta(hours=8))  # Taiwan is UTC+8
print("Taiwan time is : {}".format(dateNow))


def movie():
    html = urlopen('https://movies.yahoo.com.tw/').read().decode('utf-8')
    print('Start parsing movie ...')
    soup = BeautifulSoup(html, features='lxml')
    a_tag = soup.find_all('a', {'class': 'gabtn text_truncate_1'})
    content = ''
    for data in a_tag:
        title = data.text.strip()
        href = data['href']
        content += '{}\n{}\n'.format(title, unquote(href))
    return content


def currency():
    html = urlopen(
        'https://rate.bot.com.tw/xrt?Lang=zh-TW').read().decode('utf-8')
    print('Start parsing currency ...')
    soup = BeautifulSoup(html, features='lxml')
    trs = soup.select('tbody tr')
    obj = {}
    for td in trs:
        key = td.find('td', {'data-table': '幣別'}).find('div',
                                                       {'class': 'visible-phone print_hide'}).text.strip().split(" ")[0]
        value = '現金買入:{}\n現金賣出:{}\n即期買入:{}\n即期賣出:{}'.format(
            td.find('td', {'data-table': '本行現金買入'}).text,
            td.find('td', {'data-table': '本行現金賣出'}).text,
            td.find('td', {'data-table': '本行即期買入'}).text,
            td.find('td', {'data-table': '本行即期賣出'}).text)
        obj = dict(obj, **{key: value})
    return obj


def wheather():
    html = urlopen(
        'https://www.cwb.gov.tw/V7/forecast/f_index.htm?_=1543388415456').read().decode('utf-8')
    print('Start parsing wheather ...')
    soup = BeautifulSoup(html, features='lxml')
    trs = soup.select('tr[id$=List]')
    obj = {}
    for tr in trs:
        data = tr.text.strip().split()
        key = data[0]
        value = '溫度:{}\n降雨機率:{}\n舒適度:{}'.format(
            data[1],
            data[2],
            tr.img['alt'])
        obj = dict(obj, **{key: value})
    return obj


def news():
    html = urlopen('http://www.ltn.com.tw/').read().decode('utf-8')
    print('Start parsing news ...')
    soup = BeautifulSoup(html, features='lxml')
    lis = soup.select('.nownews_content ul li')
    content = ''
    for li in lis:
        li.select_one('.time').decompose()
        title = li.text
        href = li.a['href']
        content += '{}\n{}\n'.format(title, unquote(href))
    return content


# Firebase
url = os.environ.get('Firebase_Url')
fb = firebase.FirebaseApplication(url)
# save data
fb.post('time', dateNow.strftime('%Y-%m-%d %H:%M:%S'),
        headers={'X-HTTP-Method-Override': 'PUT'})
fb.post('movie', movie(), headers={'X-HTTP-Method-Override': 'PUT'})
fb.post('currency', currency(), headers={'X-HTTP-Method-Override': 'PUT'})
fb.post('wheather', wheather(), headers={'X-HTTP-Method-Override': 'PUT'})
fb.post('news', news(), headers={'X-HTTP-Method-Override': 'PUT'})

if __name__ == "__main__":
    app.run()
