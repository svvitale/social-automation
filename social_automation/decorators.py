from functools import wraps
import json as jsonlib

from django.http import HttpResponse
from django.http import JsonResponse


def json(func):
    @wraps(func)
    def wrapper(self, request, *args, **kwargs):
        # Deserialize the body
        payload = jsonlib.loads(request.body.decode())

        # Call the view function
        response = func(self, request, json=payload, *args, **kwargs)

        # If the view returned an HTTP Response, pass it through
        if isinstance(response, HttpResponse):
            return response
        elif response is None:
            # Empty response
            return HttpResponse()
        else:
            # Assume we got back a native python object that needs to be serialized
            return JsonResponse(response)

    return wrapper
