import requests, time, os, base64, hmac, hashlib, json
from collections import OrderedDict

import settings

BUZZ_API_VERSION = 'v2'
api_key = settings.get('API_KEY')
api_key_secret = settings.get('SECRET')
 
def get_signature(method='GET', path='/', params=None):
  import uritools
  if params is None:
      params = {}
 
  params.update({
      'api_key': api_key,
      'request_time': int(time.time()),
  })
 
  sorted_params = sorted(params.items())
  query_string = '&'.join(['{}={}'.format(k, uritools.uriencode(str(v))) for (k, v) in sorted_params if v])
  path = os.path.join('/buzzfeed/api', BUZZ_API_VERSION, path.strip('/'))
 
  string_to_sign = "GET\n{}\n{}".format(path, query_string)
  signature = base64.b64encode(hmac.new(api_key_secret, msg=string_to_sign, digestmod=hashlib.sha256).digest())
  sorted_params.append(('signature', signature))
  new_parms = OrderedDict(sorted_params)
  return new_parms
 
def get_images_from_article_url(url):
  sig_param = {
    'url': url,
  }
  params = get_signature(path='/buzz', params=sig_param)
  r = requests.get("http://www.buzzfeed.com/buzzfeed/api/v2/buzz", params=params)
  json_data = r.text
  parsed_json = json.loads(json_data)
  print parsed_json

get_images_from_article_url('/briangalindo/looking-back-at-the-totally-buggin-clueless-premiere')