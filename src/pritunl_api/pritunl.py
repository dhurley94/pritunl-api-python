#!/usr/bin/python
import json
import sys
import sys
import hashlib
import hmac
import base64
import time
import uuid
import random
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from .exceptions import PritunlErr
from .handler import APICaller

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


class Pritunl:
    def __init__(self, url, token, secret):
        """
        The base Pritunl class.

        :param url: A Pritunl server URL (ex: https://pritunl.com)
        :param token: An administrators token
        :param secret: An administrators secret
        """
        self.BASE_URL = url
        self.API_TOKEN = token
        self.API_SECRET = secret

        self.api_caller = APICaller(base_url=self.BASE_URL, api_token=self.API_TOKEN, api_secret=self.API_SECRET)

        # Sub classes
        self.server = self.Server(self)
        self.organization = self.Organization(self)
        self.user = self.User(self)
        self.key = self.Key(self)
        self.log = self.Log(self)
        self.link = self.Link(self)
        self.host = self.Host(self)
        self.route = self.Route(self)

    class Key:
        def __init__(self, root):
            self.r = None
            self.root = root
            self.api_caller = root.api_caller

        def get(self, org_id=None, usr_id=None):
            self.r = self.api_caller.call(method="GET", path="key/{0}/{1}.tar".format(org_id, usr_id))
            return self.r

    class User:
        def __init__(self, root):
            self.r = None
            self.data_template = None
            self.headers = None
            self.root = root
            self.data_template = {
                'name': 'default_name',
                'email': None,
                'disabled': False,
            }
            self.api_caller = root.api_caller

        def get(self, org_id=None, usr_id=None):
            if org_id and not usr_id:
                self.r = self.api_caller.call(method="GET", path="user/{0}".format(org_id))
            elif org_id and usr_id:
                self.r = self.api_caller.call(method="GET", path="user/{0}/{1}".format(org_id, usr_id))
            return self.r

        def post(self, org_id=None, data=None):
            self.r = self.api_caller.call(method="POST", path="user/{0}".format(org_id),
                                          data=data)
            return self.r

        def put(self, org_id=None, usr_id=None, data=None):
            self.r = self.api_caller.call(method="PUT", path="user/{0}/{1}".format(org_id, usr_id),
                                          data=data)
            return self.r

        def delete(self, org_id=None, usr_id=None):
            """

            :param org_id:
            :param usr_id:
            :return:
            """
            self.r = self.api_caller.call(method="DELETE", path="user/{0}/{1}".format(org_id, usr_id))
            return self.r

    class Organization:
        """
        Represents a Pritunl organization
        """
        def __init__(self, root):
            self.r = None
            self.data_template = {
                'name': 'default_organization',
                'auth_api': False
            }
            self.root = root
            self.api_caller = root.api_caller

        def get(self):
            return self.api_caller.call(method="GET", path="organization")

        def post(self, data=None):
            """

            :param data:
            :return:
            """
            if data is None:
                data = self.data_template
            print(data)
            self.r = self.api_caller.call(method="POST", path="organization",
                                          data=data)
            return self.r

        def put(self, org_id=None, data=None):
            """
            Update an organization
            :param org_id:
            :param data:
            :return:
            """
            self.r = self.api_caller.call(method="POST", path="organization/{0}".format(org_id),
                                          data=data)
            return self.r

        def delete(self, org_id=None):
            """
            Delete an organization
            :param org_id:
            :return:
            """
            self.r = self.api_caller.call(method="DELETE", path="organization/{0}".format(org_id))
            return self.r

    class Server:
        def __init__(self, root):
            """
            The root Pritunl object
            :param root:
            """
            self.r = None
            self.root = root
            self.data_template = {
                'name': 'default_server',
                'network': '10.{0}.{1}.0/24'.format(random.randrange(1, 254), random.randrange(1, 254)),
                'groups': [],
                'network_mode': 'tunnel',
                'network_start': None,
                'network_end': None,
                'restrict_routes': True,
                'ipv6': False,
                'ipv6_firewall': True,
                'bind_address': None,
                'port': random.randrange(1025, 20000),
                'protocol': 'tcp',
                'dh_param_bits': 1536,
                'multi_device': False,
                'dns_ervers': ['8.8.8.8'],
                'search_domain': '',
                'otp_auth': False,
                'cipher': 'aes128',
                'hash': 'sha1',
                'jumbo_frames': False,
                'lzo_compression': False,
                'inter_client': True,
                'ping_interval': 10,
                'ping_timeout': 60,
                'link_ping_interval': 1,
                'link_ping_timeout': 5,
                'onc_hostname': None,
                'allowed_devices': None,
                'max_clients': 10,
                'replica_count': 1,
                'vxlan': True,
                'dns_mapping': False,
                'debug': False,
                'policy': None
            }
            self.api_caller = root.api_caller

        def get(self, srv_id=None, org=None, out=None):
            if srv_id and not org and not out:
                self.r = self.api_caller.call(method="GET", path="server/{0}".format(srv_id))
            elif srv_id and org and not out:
                self.r = self.api_caller.call(method="GET", path="server/{0}/organization".format(srv_id))
            elif srv_id and out and not org:
                self.r = self.api_caller.call(method="GET", path="server/{0}/output".format(srv_id))
            else:
                self.r = self.api_caller.call(method="GET", path="server")
            return self.r

        def delete(self, srv_id=None, org_id=None, out=None):
            if srv_id and not out and not org_id:
                self.r = self.api_caller.call(method="DELETE", path="server/{0}".format(srv_id))
            if srv_id and out and not org_id:
                self.r = self.api_caller.call(method="DELETE", path="server/{0}/output".format(srv_id))
            if srv_id and org_id and not out:
                self.r = self.api_caller.call(method="DELETE",
                                              path="server/{0}/organization/{1}".format(srv_id, org_id))
            return self.r

        def put(self, srv_id=None, operation=None, org_id=None, data=None):
            """

            :param srv_id:
            :param operation:
            :param org_id:
            :param data:
            :return:
            """
            if operation and not data and srv_id and not org_id:
                self.r = self.api_caller.call(method="PUT",
                                              path="server/{0}/operation/{1}".format(srv_id, operation))
            if srv_id and data and not operation and not org_id:
                self.r = self.api_caller.call(method="PUT",
                                              path="server/{0}".format(srv_id),
                                              data=data)
            if srv_id and org_id and not data and not operation:
                self.r = self.api_caller.call(method="PUT",
                                              path="server/{0}/organization/{1}".format(srv_id, org_id)
                                              )
            return self.r

        def post(self, data=None):
            """

            :param data:
            :return:
            """
            self.data_template.update(data)
            self.r = self.r = self.api_caller.call(method="POST", path="server",
                                                   data=self.data_template)
            return self.r

    class Route:
        def __init__(self, root):
            self.r = None
            self.root = root
            self.data_template = {
                "network": "",
                "comment": "",
                "metric": 2,
                "nat": True,
                "nat_interface": "",  # optional
                "nat_netmap": "",  # map two pritunl servers
                "advertise": False,
                "net_gateway": False
            }
            self.api_caller = root.api_caller

        def get(self, srv_id=None):
            """

            :param srv_id:
            :return:
            """
            self.r = self.api_caller.call(method="GET", path="server/{0}/route".format(srv_id))
            return self.r

        def post(self, srv_id=None, data=None):
            """

            :param srv_id:
            :param data:
            :return:
            """
            self.data_template.update(data)
            self.r = self.api_caller.call(method="POST", path="server/{0}/route".format(srv_id),
                                          data=self.data_template)
            return self.r

        def put(self, srv_id=None, route_net=None, data=None):
            """

            :param srv_id:
            :param route_net:
            :param data:
            :return:
            """
            self.data_template.update(data)
            self.r = self.api_caller.call(method="PUT", path="server/{0}/route/{1}".format(srv_id, route_net),
                                          data=self.data_template)
            return self.r

        def delete(self, srv_id=None, route_net=None):
            """

            :param srv_id:
            :param route_net:
            :param data:
            :return:
            """

            self.r = self.api_caller.call(method="DELETE", path="server/{0}/route/{1}".format(srv_id, route_net))
            return self.r

    class Host:
        def __init__(self, root):
            self.r = None
            self.root = root
            self.api_caller = root.api_caller

        def get(self, srv_id=None):
            """

            :param srv_id:
            :return:
            """
            self.r = self.api_caller.call(method="GET", path="server/{0}/host".format(srv_id))
            return self.r

        def put(self, srv_id=None, host_id=None):
            """

            :param srv_id:
            :param host_id:
            :return:
            """
            self.r = self.api_caller.call(method="PUT", path="server/{0}/host/{1}".format(srv_id, host_id))
            return self.r

        def delete(self, srv_id=None, host_id=None):
            """

            :param srv_id:
            :param host_id:
            :return:
            """
            self.r = self.api_caller.call(method="DELETE", path="server/{0}/host/{1}".format(srv_id, host_id))
            return self.r

    class Link:
        def __init__(self, root):
            self.r = None
            self.root = root
            self.api_caller = root.api_caller

        def get(self, srv_id=None):
            """

            :param srv_id:
            :return:
            """
            self.r = self.api_caller.call(method="GET", path="server/{0}/link".format(srv_id))
            return self.r

    class Bandwidth:
        def __init__(self, root):
            self.r = None
            self.root = root
            self.api_caller = root.api_caller

        def get(self, srv_id=None, period="300"):
            """

            :return:
            """
            self.r = self.api_caller.call(method="GET", path="server/{0}/bandwidth/{1}".format(srv_id, period))
            return self.r

    class Log:
        def __init__(self, root):
            self.r = None
            self.root = root
            self.api_caller = root.api_caller

        def get(self):
            self.r = self.api_caller.call(method="GET", path="log")
            return self.r

        # not really sure what this is supposed to return
        # def get(self):
        #     self.r = self.api_caller.call(method="GET", path="logs")
        #     return self.r

    def test(self):
        pass

    def ping(self):
        if 'OK' in str(self.api_caller.call(method="GET", path="ping"), encoding='utf-8'):
            return True
        return False

    def check(self):
        if 'OK' in str(self.api_caller.call(method="GET", path="check"), encoding='utf-8'):
            return True
        return False

    def setting(self):
        self.r = self.api_caller.call(method="GET", path="settings")
        return self.r

    def last_response(self):
        return self.r.json()

    def auth_request(self, method, path, headers=None, data=None):
        auth_timestamp = str(int(time.time()))
        auth_nonce = uuid.uuid4().hex
        auth_string = '&'.join([self.API_TOKEN, auth_timestamp, auth_nonce,
                                method.upper(), path] + ([data] if data else []))

        hmacv = hmac.new(str.encode(self.API_SECRET), auth_string.encode('utf-8'), hashlib.sha256).digest()

        auth_signature = base64.b64encode(hmacv)
        auth_headers = {
            'Auth-Token': self.API_TOKEN,
            'Auth-Timestamp': auth_timestamp,
            'Auth-Nonce': auth_nonce,
            'Auth-Signature': auth_signature
        }

        return getattr(requests, method.lower())(
            self.BASE_URL + path,
            verify=False,
            headers=auth_headers,
            data=data,
            timeout=30
        )
