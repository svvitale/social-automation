import base64
import hashlib
import hmac
import random
import string
import time
from urllib.parse import quote

from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
import requests


class TwitterApi(requests.Session):
    """ Wraps all required Twitter authentication into a requests Session object.  This object can be used for the
    typical HTTP operations (like GET, PUT, POST, DELETE) with no regard for Twitter authentication.  All authentication
    headers are injected as needed for each and every request. """

    def __init__(self, user):
        """ Constructor that takes a django user and extracts the needed pieces of OAuth information to perform API
        calls.

        :param user: Django user object.  Must have been connected to a python-social-auth Twitter provider.
        """
        # Call the base requests.Session constructor
        super().__init__()

        # Extract OAuth token data from the social auth backend
        try:
            self._twitter_acct_data = user.social_auth.get(provider='twitter').extra_data['access_token']
        except ObjectDoesNotExist:
            raise ValueError("No twitter account associated with this user.")

        # Set authorization data that is fixed for all requests
        self._twitter_auth_data = {
            'oauth_consumer_key': settings.SOCIAL_AUTH_TWITTER_KEY,
            'oauth_signature_method': 'HMAC-SHA1',
            'oauth_token': self._twitter_acct_data['oauth_token'],
            'oauth_version': '1.0'
        }

        # Go ahead and construct the signing key
        self._signing_key = settings.SOCIAL_AUTH_TWITTER_SECRET + "&" + self._twitter_acct_data['oauth_token_secret']

    def _sign_request(self, method, url, params=None):
        """ Twitter requires that all requests be "signed".  Full documentation here:
        https://dev.twitter.com/oauth/overview/creating-signatures

        :param method: HTTP method being used (GET, PUT, POST, DELETE typically)
        :param url: URL being called
        :param params: URL parameters
        :return: Signature value as described by the Twitter documentation
        """
        # Clear any previous signature
        if 'oauth_signature' in self._twitter_auth_data:
            del self._twitter_auth_data['oauth_signature']

        param_string_values = []

        if not params:
            params = {}

        # Combine URL parameters and known authorization headers (excluding the signature of course)
        params_and_headers = {**params, **self._twitter_auth_data}

        # Iterate over the parameters alphabetically, building the pieces of the "parameter string"
        for param_name in sorted(params_and_headers):
            param_string_values.append('{0}={1}'.format(param_name, quote(params_and_headers[param_name], safe='')))

        # Combine the pieces into the "parameter string"
        param_string = '&'.join(param_string_values)

        # Build the "signature base" from the method, url, and parameter string
        signature_base = '&'.join((method.upper(), quote(url, safe=''), quote(param_string, safe='')))

        # Use the signing key to HMAC encode the signature base
        signature = hmac.new(self._signing_key.encode(), signature_base.encode(), hashlib.sha1).digest()

        # Base64 encode the signature and add it to our auth headers
        self._twitter_auth_data['oauth_signature'] = base64.b64encode(signature)

    @property
    def _twitter_auth_header(self):
        """ Using the authorization data, build a formatted string to use as the Authorization OAuth header as
        described here: https://dev.twitter.com/oauth/overview/authorizing-requests

        :return: Authorization header as a string
        """
        auth_string_values = []

        for auth_key in sorted(self._twitter_auth_data):
            auth_string_values.append('{0}="{1}"'.format(auth_key, quote(self._twitter_auth_data[auth_key], safe='')))

        return 'OAuth ' + ', '.join(auth_string_values)

    def request(self, method, url, params=None, *args, **kwargs):
        """ Intercept all HTTP requests and ensure that they contain correct authorization headers and are signed.

        :param method: HTTP method being performed
        :param url: Target URL
        :param params: Any parameters required for this API call
        :return: Response object
        """
        # Add the variable authorization parameters
        self._twitter_auth_data.update({
            'oauth_nonce': ''.join(random.choice(string.ascii_letters + string.digits) for i in range(32)),
            'oauth_timestamp': str(int(round(time.time())))
        })

        # Sign the overall HTTP request
        self._sign_request(method, url, params)

        # Perform the HTTP operation
        return super().request(method, url, params, headers={'Authorization': self._twitter_auth_header})
