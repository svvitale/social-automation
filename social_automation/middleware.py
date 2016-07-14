from django.conf import settings
from django.http import HttpResponseRedirect
import re


class DisableCSRFOnDebug:
    def process_request(self, request):
        if settings.DEBUG:
            setattr(request, '_dont_enforce_csrf_checks', True)


class LoginRequiredMiddleware:
    """
    Middleware that requires a user to be authenticated to view any page other
    than LOGIN_URL. Exemptions to this requirement can optionally be specified
    in settings via a list of regular expressions in LOGIN_EXEMPT_URLS (which
    you can copy from your urls.py).
    Requires authentication middleware and template context processors to be
    loaded. You'll get an error if they aren't.
    """
    @property
    def exempt_url_regexes(self):
        exempt_url_regexes = [re.compile(settings.LOGIN_URL)]
        if hasattr(settings, 'LOGIN_EXEMPT_URLS'):
            exempt_url_regexes += [re.compile(expr) for expr in settings.LOGIN_EXEMPT_URLS]

        return exempt_url_regexes

    def process_request(self, request):

        assert hasattr(request, 'user'), "The Login Required middleware requires authentication middleware to be\
         installed. Edit your MIDDLEWARE_CLASSES setting to insert\
         'django.contrib.auth.middleware.AuthenticationMiddleware'. If that doesn't work, ensure your\
         TEMPLATE_CONTEXT_PROCESSORS setting includes 'django.core.context_processors.auth'."

        if not request.user.is_authenticated():
            if not any(regex.match(request.path_info) for regex in self.exempt_url_regexes):
                return HttpResponseRedirect(settings.LOGIN_URL)


class SSLMiddleware(object):
    def process_request(self, request):
        if not any([settings.SSL_NOT_REQUIRED, request.is_secure(), request.META.get("HTTP_X_FORWARDED_PROTO", "") == 'https']):
            url = request.build_absolute_uri(request.get_full_path())
            secure_url = url.replace("http://", "https://")
            return HttpResponseRedirect(secure_url)
