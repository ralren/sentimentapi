import tornado.ioloop
import tornado.web
import time
import settings
import requests
import base64
import hmac
import json
import hashlib
import os
import uritools
from collections import OrderedDict
import indicoio

access_token = settings.get('ACCESS_TOKEN')
indicoio.config.api_key = settings.get('indico_api_key')


def get_buzz_comments(buzz_id, response_dict):
    buzz_url = 'http://www.buzzfeed.com/api/v1/comments/%s' % (buzz_id)
    r = requests.get(buzz_url)
    comments = r.json()['comments']
    total = r.json()['total_count']
    count = len(comments)
    page = 2 #start looping on the second page

    while count < total:
        buzz_url = 'http://www.buzzfeed.com/api/v1/comments/%s?p=%s' % (buzz_id, str(page))
        r = requests.get(buzz_url)
        comments.extend(r.json()['comments'])
        count = len(comments)
        page += 1

    for comment in comments:
        score = indicoio.sentiment(comment['blurb'])
        if (score < .4):
            response_dict['negative'] += 1
        elif (score < .6):
            response_dict['neutral'] += 1
        else:
            response_dict['positive'] += 1
        response_dict['total'] += 1

    return response_dict


def get_fb_comments(fb_id, response_dict):
    fb_url = 'https://graph.facebook.com/v2.4/%s/comments?access_token=%s&format=json&method=get' % (fb_id, access_token)
    r = requests.get(fb_url)
    comments = r.json()['data']

    while "next" in r.json()['paging']:
        token = r.json()['paging']['cursors']['after']
        fb_url = 'https://graph.facebook.com/v2.4/%s/comments?access_token=%s&format=json&method=get&after=%s&limit=25' % (fb_id, access_token, token)
        r = requests.get(fb_url)
        comments.extend(r.json()['data'])

    for comment in comments:
        score = indicoio.sentiment(comment['message'])
        if (score < .4):
            response_dict['negative'] += 1
        elif (score < .6):
            response_dict['neutral'] += 1
        else:
            response_dict['positive'] += 1
        response_dict['total'] += 1

    return response_dict


class SentimentHandler(tornado.web.RequestHandler):
    def get(self, author, buzz_slug):
        buzz = self.get_buzz(author, buzz_slug)
        fb = self.get_fb(author, buzz_slug)
        sentiment_dict = get_fb_comments(fb['id'], get_buzz_comments(buzz['id'],{'positive': 0, 'negative': 0, 'neutral': 0, 'total' : 0}))
        self.write(json.dumps(sentiment_dict))


    def get_buzz(self, author, buzz_slug):
        sig_param = {
            'url': '/%s/%s' % (author, buzz_slug),
        }
        params = self.get_signature(path='/buzz', params=sig_param)
        r = requests.get("http://www.buzzfeed.com/buzzfeed/api/v2/buzz", params=params)
        json_data = r.text
        parsed_json = json.loads(json_data)
        return parsed_json['buzz']


    def get_signature(method='GET', path='/', params=None):
        BUZZ_API_VERSION = 'v2'
        api_key = settings.get('API_KEY')
        api_key_secret = settings.get('SECRET')
        if params is None:
            params = {}

        params.update({
            'api_key': api_key,
            'request_time': int(time.time()),
        })

        sorted_params = sorted(params.items())
        query_string = '&'.join(['%s=%s' % (k, uritools.uriencode(str(v))) for (k, v) in sorted_params if v])
        path = os.path.join('/buzzfeed/api', BUZZ_API_VERSION, path.strip('/'))

        string_to_sign = "GET\n%s\n%s" % (path, query_string)
        signature = base64.b64encode(hmac.new(api_key_secret, msg=string_to_sign, digestmod=hashlib.sha256).digest())
        sorted_params.append(('signature', signature))
        new_parms = OrderedDict(sorted_params)
        return new_parms


    def get_fb(self, author, buzz_slug):
        buzz_url = 'http://www.buzzfeed.com/%s/%s' % (author, buzz_slug)
        fb_url = 'https://graph.facebook.com/v2.4/%s?access_token=%s&format=json&method=get' % (buzz_url, access_token)
        r = requests.get(fb_url)
        fb = r.json()['og_object']
        return fb

application = tornado.web.Application([
    (r'/([\w-]+)/([\w-]+)$', SentimentHandler)
])

if __name__ == "__main__":
    application.listen(27000)
    tornado.ioloop.IOLoop.current().start()
