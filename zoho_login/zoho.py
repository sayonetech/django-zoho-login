__author__ = 'user'
import requests
from urllib import urlencode

from django.utils.translation import ugettext_lazy as _

AUTH_TOKEN_CREATE_URL = "https://accounts.zoho.com/apiauthtoken/nb/create"
ERROR_MAP = {
    "NO_SUCH_USER": _("Username does not exist."),
    "INVALID_PASSWORD": _("Enter valid password."),
    "INVALID": _("Enter valid details."),
}


class ZohoException(Exception):
    """ Bad stuff happens.
    """


class ZohoApi(object):
    def __init__(self, username=None, password=None, token=None, **kwargs):
        self.username = username
        self.password = password
        self.token = token

    def create_auth_token(self):
        """
        https://www.zoho.com/people/help/api/auth-token.html
        :return:
        """
        result = {}
        params = {"SCOPE":"Zohopeople/peopleapi", "EMAIL_ID":self.username, "PASSWORD":self.password}
        self._do_request(AUTH_TOKEN_CREATE_URL, 'POST', params=params)
        token = self.response.get('AUTHTOKEN', False)
        result['status'] = 'success' if token else "error"
        if token:
            result['token'] = token
        else:
            result['message'] = ERROR_MAP.get(self.response.get('CAUSE', ERROR_MAP['INVALID']))
        return result

    def _do_request(self, req_url, method, params=None):
        if not params:
            params = {}
        if method == 'POST':
            data = requests.post(req_url, params)
            self.response = self._parse_response(data.text)

    def _parse_response(self, data):
        """ Dictionarize ticket opening response
        Example response::
            # #Sun Jun 27 20:10:30 PDT 2010 GETUSERNAME=null WARNING=null PASS_EXPIRY=-1 TICKET=3bc26b16d97473a1245dbf93a5dcd153 RESULT=TRUE
        """
        output = {}
        lines = data.split("\n")
        for line in lines:
            if line.startswith("#"):
                # Comment
                continue
            if line.strip() == "":
                # Empty line
                continue
            if not "=" in line:
                raise ZohoException("Bad ticket data:" + data)
            key, value = line.split("=")
            output[key] = value
        return output
