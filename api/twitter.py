# -*- coding: utf-8 -*-
from util.env import settings
import json
from requests_oauthlib import OAuth1Session


class Twtter(object):

    def __init__(self):
        self.tw = OAuth1Session(settings.CONSUMER_KEY, settings.CONSUMER_SECRET, settings.ACCESS_TOKEN, settings. ACCESS_SECRET)

    def tweet(self, text):
        URL = 'https://api.twitter.com/1.1/statuses/update.json'

        # Tweetを作成
        payload = {'status': text}
        res = self.tw.post(URL, params=payload)

        # レスポンスコードを返す
        return res.text

    def get_tweet(self, user_id):
        URL = 'https://api.twitter.com/1.1/statuses/user_timeline.json'

        payload = {'user_id': user_id}
        res = self.tw.get(URL, params=payload)

        return json.loads(res.text)

    def stream(self, screen_name, callback):
        URL = 'https://stream.twitter.com/1.1/statuses/filter.json'

        payload = {'follow': self.get_user_id(screen_name)}
        res = self.tw.post(URL, params=payload, stream=True)

        for line in res.iter_lines():
            msg = ""
            try:
                msg = json.loads(line.decode('utf-8'))
            except Exception as e:
                msg = False
                pass
            if msg:
                callback(msg)

    def get_user_id(self, screen_name):
        URL = 'https://api.twitter.com/1.1/statuses/user_timeline.json'

        payload = {'screen_name': screen_name, 'count': 1}
        res = self.tw.get(URL, params=payload)

        return json.loads(res.text)[0]['user']['id_str']
twitter = Twtter()
