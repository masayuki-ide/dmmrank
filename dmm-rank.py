from bs4 import BeautifulSoup
from requests_oauthlib import OAuth1Session
from TwitterAPI import TwitterAPI
import urllib.request as req
import requests
import os.path
import tweepy
import os
import random

#認証を行う
consumer_key = "17ErzxsisvnJcmDELYkuSaq4n"
consumer_secret = "40rU30yZViSSnkq6AavW41F9EJY137EK7aegfpyTWk1Lptt8ou"
access_token = "1011141972055080960-zP6mwsnl4ECwTkN1FD3lOvOR2bJsa4"
access_secret = "5HZkH5jEGgfxhWW2xIFY8R1xEPChSDapDjIVsNeFggZ48"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth)

# ツイート投稿用のURL
url = "https://api.twitter.com/1.1/statuses/update_with_media.json"


APPID = "YHhCqqXCAF6zCGAWd9WK"
AFFILIATEID = "deeei-999"
url = "http://www.dmm.co.jp/digital/videoa/-/list/=/article=keyword/id=6565/sort=ranking/"

savename = "salelist.xml"
# if not os.path.exists(savename):
#     req.urlretrieve(url, savename)
req.urlretrieve(url, savename)

#BeautifulSoupで解析
xml = open(savename, "r", encoding="utf-8").read()
soup = BeautifulSoup(xml, 'html.parser')

sale_list =[]
for item_tag in soup.find_all(class_='d-item'):
    for list_tag in item_tag.find_all(id='list'):
        for tmb_tag in list_tag.find_all(class_='tmb'):
            for a_tag in tmb_tag.find_all('a'):
                p = a_tag['href'].find('detail/=/cid=')#38?
                n = a_tag['href'].find('/?i3_ref')
                str_href = a_tag['href']
                c_id = str_href[p + 13 :n]
                sale_list.append(c_id)

# print(sale_list)
n = random.randrange(len(sale_list))
# n = 0
item_id = sale_list[n]
print(item_id)
#取得
html = req.urlopen("https://api.dmm.com/affiliate/v3/ItemList?api_id=" + APPID + "&affiliate_id=" + AFFILIATEID + "%20&site=DMM.R18&service=digital&floor=videoa&hits=20&sort=rank&cid=" + item_id + "&output=xml")
soup_result = BeautifulSoup(html, "html5lib")

# print("所得したデータを表示します")
# print(soup_result.prettify())

try:
    title = soup_result.title.string
    title = (title[:40] + "..動画はこちら→")if len(title) > 75 else title #タイトル４０字過ぎたら省略
    afi_url = soup_result.affiliateurlsp.string
    print(afi_url)
    photoURL = soup_result.imageurl.large.string
    # genre_tag = soup_result.find("genre")
    # print(genre_tag.find("name"))
    content = title + ' ' + afi_url
    print("ツイート内容：{}".format(content))
    request = requests.get(photoURL, stream=True)
    filename = "temp.jpg"
    if request.status_code == 200:
        print("status_code == 200")
        with open(filename, 'wb') as image:
            for chunk in request:
                image.write(chunk)
        api.update_with_media(filename, status= content)
        print("ツイートに成功")
        os.remove(filename)
    else:
        print("画像のダウンロード失敗")
except Exception as e:
    print(e)

print("プログラム終了")
