import os

import requests
from .exceptions import PritunlErr
import sys
import hashlib
import hmac
import base64
import time
import uuid
from json import JSONDecodeError
import json

DEBUG = os.getenv("DEBUG", False)


class APICaller:
    def __init__(self, base_url, api_token, api_secret, headers={'Content-Type': 'application/json'}):
        self.base_url = base_url
        self.headers = headers
        self.api_token = api_token
        self.api_secret = api_secret
        self.url = None

    def call(self, method, path, data=None):
        if data is not None:
            data = json.dumps(data)
        auth_timestamp = str(int(time.time()))
        auth_nonce = uuid.uuid4().hex
        auth_string = '&'.join([self.api_token, auth_timestamp, auth_nonce,
                                method.upper(), f"/{path}"])

        hmacv = hmac.new(str.encode(self.api_secret), auth_string.encode('utf-8'), hashlib.sha256).digest()
        auth_signature = base64.b64encode(hmacv)
        auth_headers = {
            'Auth-Token': self.api_token,
            'Auth-Timestamp': auth_timestamp,
            'Auth-Nonce': auth_nonce,
            'Auth-Signature': auth_signature
        }

        auth_headers.update(self.headers)
        self.url = f"{self.base_url}/{path}"
        response = getattr(requests, method.lower())(
            self.url,
            verify=False,
            headers=auth_headers,
            data=data,
            timeout=30
        )

        if response.status_code == 200:
            try:
                return response.json()
            except JSONDecodeError:
                return response.content
        elif response.status_code == 401:
            raise PritunlErr("401 Unauthorized:{0}".format(self.url))
        else:
            raise PritunlErr("{0}:{1}".format(sys._getframe().f_code.co_name, self.url))
