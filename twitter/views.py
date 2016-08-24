import re

import requests
from django.views.generic import View

from social_automation.decorators import json
from social_automation.responses import APIResponse
from .twitter import TwitterApi


class FollowFromUrlView(View):
    @json
    def post(self, request, json=None):

        twitter = TwitterApi(request.user)

        response = requests.get(json['url'])

        if response.status_code != requests.codes.ok:
            return APIResponse("Requested URL could not be loaded", status=response.status_code)

        follow_set = set()

        # Search for all URLs resembling a twitter user
        for match in re.finditer(r'http(?:s)?://(?:www\.)?twitter\.com/([\w]+)', response.text):

            # Get just the twitter handle
            screen_name = match.group(1)

            # Skip duplicates
            if screen_name in follow_set:
                continue

            # Follow the user on twitter
            response = twitter.post(
                url='https://api.twitter.com/1.1/friendships/create.json',
                params={
                    'screen_name': screen_name,
                    'follow': 'true'
                }
            )

            # Process the response to verify that it worked
            # 200 - Success
            # 403 - User does not exist
            if response.status_code not in (requests.codes.ok, requests.codes.forbidden):
                return APIResponse("Error following user: {0}".format(screen_name), status=response.status_code)

            # Add this handle to our followed set
            follow_set.add(screen_name)

        # Tell the user what we did
        return {
            'msg': 'Found and followed {0} twitter accounts'.format(len(follow_set))
        }
