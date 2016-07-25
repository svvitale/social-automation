from django.contrib.auth import logout
from django.shortcuts import redirect, render_to_response
from django.views.generic import View
from django.conf import settings


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect(settings.LOGIN_URL)


class IndexView(View):
    def get(self, request):
        if request.user.is_authenticated():
            return redirect('/dashboard')
        else:
            return render_to_response('index.html')


class DashboardView(View):
    def get(self, request):
        return render_to_response('dashboard.html', {
            'user': request.user,
            'linked_providers': {link.provider for link in request.user.social_auth.all()},
        })
