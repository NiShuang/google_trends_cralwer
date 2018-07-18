# -*- coding: UTF-8 -*-
'''
使用requests，先获取每个词的token，再获取数据。
日期参数（start_date，end_date）必须是最近三十天，所以在爬虫的方法里写死了。
'''
import sys
import json
import time
import urllib
import requests
import ssl
import datetime
import calendar
from functools import wraps

reload(sys)
sys.setdefaultencoding("utf-8")

now = datetime.datetime.now()
month = (now.month + 10) % 12 + 1
year = now.year - month / 12
day = min(now.day, calendar.monthrange(year, month)[1])
before = now.replace(year=year, month=month, day=day)
start_date = before.strftime('%Y-%m-%d')
end_date = now.strftime('%Y-%m-%d')
#查询日期必须是最近三十天
def google_index():
    ssl.wrap_socket = sslwrap(ssl.wrap_socket)
    keys = ['insta360', 'samsung gear 360', 'theta s', 'Giroptic', 'GoPro Fusion']
    result = get_google_trend(keys)
    jsonResult = json.dumps(result)
    print jsonResult
    return jsonResult

#得到每个词的token
def get_token(keys):
    q = ''
    for key in keys:
        q += key + ','
    if len(q)  > 0:
        q = q[:-1]
    headers = {}
    headers['Host'] = 'trends.google.com'
    headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0'
    headers['Referfer'] = 'https://trends.google.com/trends/explore?date=today%201-m&q=' + urllib.quote(q)
    headers['Cookie'] = '__utmt=1; __utma=10102256.539038748.1495043708.1495043708.1495435554.2; __utmb=10102256.8.9.1495435587029; __utmc=10102256; __utmz=10102256.1495043708.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); NID=103=JBmZSCUdgzRzy0ZMp31uy5nS1gwKm-imoboVE3nf2HrEX-UXQO95jS1NNaaFE1bkUkQ5MQkc-lveM2g3h4evgY12Bs4UpJS4PbUXBuwiM7CkqAwo8TfRrVPa-wH7uieP'
    headers['Connection'] = 'keep-alive'
    headers['Accept'] = 'application/json, text/plain, */*'
    headers['Accept-Language'] = 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3'
    headers['Accept-Encoding'] = 'gzip, deflate, sdch, br'
    headers['x-client-data'] = 'CJG2yQEIpbbJAQjEtskBCPucygEIqZ3KAQ=='
    req = {}
    req['category'] = 0
    req['property'] = ''
    req['comparisonItem'] = []
    for key in keys:
        req['comparisonItem'].append({"geo": "","keyword":  urllib.quote(key).replace(' ', '+'),"time":"today+1-m"})
    value = {}
    value['hl'] = 'zh-CN'
    value['tz'] = '-480'
    value['req'] = str(req).replace(' ','')
    url = 'https://trends.google.com/trends/api/explore?'
    for index in value:
        url = url + index + '=' + value[index] + '&'
    results = requests.get(url, headers=headers, verify=False, allow_redirects=False)
    page = results.content
    jsonData = page[5:]
    data = json.loads(jsonData, encoding="utf-8")
    the_token = data['widgets'][0]['token']
    return the_token

#获取数据
def get_google_trend(keys):
    token = get_token(keys)
    q = ''
    for key in keys:
        q += key + ','
    if len(q) > 0:
        q = q[:-1]
    headers = {}
    headers['Host'] = 'trends.google.com'
    headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0'
    headers['Referfer'] = 'https://trends.google.com/trends/explore?date=today%201-m&q=' + urllib.quote(q)
    headers['Cookie'] = '__utmt=1; __utma=10102256.539038748.1495043708.1495043708.1495435554.2; __utmb=10102256.9.9.1495435587029; __utmc=10102256; __utmz=10102256.1495043708.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); NID=103=JBmZSCUdgzRzy0ZMp31uy5nS1gwKm-imoboVE3nf2HrEX-UXQO95jS1NNaaFE1bkUkQ5MQkc-lveM2g3h4evgY12Bs4UpJS4PbUXBuwiM7CkqAwo8TfRrVPa-wH7uieP'
    headers['Connection'] = 'keep-alive'
    headers['Accept'] = 'application/json, text/plain, */*'
    headers['Accept-Language'] = 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3'
    headers['Accept-Encoding'] = 'gzip, deflate, sdch, br'
    headers['x-client-data'] = 'CJG2yQEIpbbJAQjEtskBCPucygEIqZ3KAQ=='


    req = {}
    req['time'] = start_date + "+" + end_date
    req['resolution'] = "DAY"
    req['locale'] = "zh-CN"
    req['comparisonItem'] = []
    for key in keys:
        req['comparisonItem'].append({"geo": {}, "complexKeywordsRestriction": {"keyword": [{"type": "BROAD", "value": urllib.quote(key).replace(' ','+')}]}})
    req['requestOptions'] = {"property":"","backend":"IZG","category":0}
    value = {}
    value['hl'] = 'zh-CN'
    value['tz'] = '-480'
    value['req'] = str(req).replace(' ','')
    value['token'] = token
    url = 'https://trends.google.com/trends/api/widgetdata/multiline?'
    for index in value:
        url = url + index + '=' + value[index] + '&'
    results = requests.get(url, headers=headers, verify=False)
    page = results.content
    jsonData = page[5:]
    data = json.loads(jsonData, encoding="utf-8")
    items = data['default']['timelineData']
    result = []
    for item in items:
        timestamp = int(item['time'])
        time_temp = time.localtime(timestamp)
        date = time.strftime("%Y-%m-%d", time_temp)
        values = item['value']
        for index in range(len(values)):
            temp = {'key': keys[index], 'date': date, 'google_index': values[index]}
            result.append(temp)
    return result


def sslwrap(func):
    @wraps(func)
    def bar(*args, **kw):
        kw['ssl_version'] = ssl.PROTOCOL_TLSv1
        return func(*args, **kw)
    return bar


if __name__ == '__main__':
    google_index()
