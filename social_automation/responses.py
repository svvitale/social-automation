import requests
from django.http import JsonResponse


class APIResponse(JsonResponse):
    def __init__(self, msg_or_data, *args, **kwargs):
        if isinstance(msg_or_data, dict):
            super().__init__(msg_or_data, *args, **kwargs)
        else:
            super().__init__({'msg': msg_or_data}, *args, **kwargs)


class ErrorResponse(APIResponse):
    def __init__(self, msg_or_data, *args, **kwargs):
        super().__init__(msg_or_data, status=requests.codes.bad_request, *args, **kwargs)


class UnauthorizedResponse(APIResponse):
    def __init__(self, msg_or_data, *args, **kwargs):
        super().__init__(msg_or_data, status=requests.codes.unauthorized, *args, **kwargs)


class ForbiddenResponse(APIResponse):
    def __init__(self, msg_or_data, *args, **kwargs):
        super().__init__(msg_or_data, status=requests.codes.forbidden, *args, **kwargs)


class NotFoundResponse(APIResponse):
    def __init__(self, msg_or_data, *args, **kwargs):
        super().__init__(msg_or_data, status=requests.codes.not_found, *args, **kwargs)
