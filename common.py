import re
import configparser
import time
import json
import base64
import hmac, hashlib
import urllib.parse
import urllib.request
import ssl
from functools import wraps


config = configparser.ConfigParser()
config.read('naver.ini')
CUSTOMER_ID = config['DEFAULT'].get('CUSTOMER_ID')
API_KEY = config['DEFAULT'].get('API_KEY')
SECRET_KEY = config['DEFAULT'].get('SECRET_KEY')

if CUSTOMER_ID is None:
    raise Exception('CUSTOMER_ID를 설정해주십시오.')
if API_KEY is None:
    raise Exception('API_KEY를 설정해주십시오.')
if SECRET_KEY is None:
    raise Exception('SECRET_KEY를 설정해주십시오.')

CUSTOMER_ID = re.sub('^\'|^\"|\'$|\"$', '', CUSTOMER_ID)
API_KEY = re.sub('^\'|^\"|\'$|\"$', '', API_KEY)
SECRET_KEY = re.sub('^\'|^\"|\'$|\"$', '', SECRET_KEY)


##############################################################################
# 공통 함수                                                                  #
##############################################################################


def naver(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        customer_id = CUSTOMER_ID
        api_key = API_KEY
        secret_key = SECRET_KEY

        unix_epoch = int(time.time())
        data = f(*args, **kwargs)
        x_signature = signature(
                secret_key,
                unix_epoch,
                data.get('method'),
                data.get('path')
        )

        if data.get('method') == "GET":
            if 'query' in data:
                url = 'https://api.naver.com'+\
                        data.get('path')+\
                        "?%s" % data.get('query')

                response = request(
                        data.get('method'),
                        url,
                        unix_epoch,
                        api_key,
                        customer_id,
                        x_signature
                )
        else:
            raise NotImplementedError
        return response

    return decorated


def signature(secretkey, unix_epoch, method, path):
    message = str(unix_epoch) + "." + method.upper() + "." + path
    sig = hmac.new(
            secretkey.encode('utf-8'),
            message.encode('utf-8'),
            hashlib.sha256).digest()
    return base64.b64encode(sig).decode()


def request(method, url, unix_epoch, api_key, customer_id, signature):
    req = urllib.request.Request(url)
    req.add_header("Content-type","application/json;charset=UTF-8")
    req.add_header("X-Timestamp", str(unix_epoch))
    req.add_header("X-API-KEY", api_key)
    req.add_header("X-Customer", customer_id)
    req.add_header("X-Signature", signature)
    req.get_method = lambda: method

    #skipping for ssl cert.
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    try:
        resp = urllib.request.urlopen(req, context=ctx)

    except urllib.request.HTTPError as e:
        print(e.code)
        print(e.reason)
    except urllib.request.URLError as e:
        print(e.errno)
        print(e.reason)
    else:
        # 200
        decoded_resp = resp.read().decode(resp.headers.get_content_charset())
        response = json.loads(decoded_resp)
        return response

