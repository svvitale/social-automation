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
    @staticmethod
    def standard_response_data(request):
        return {
            'user': request.user,
            'linked_providers': {link.provider for link in request.user.social_auth.all()},
        }

    def get(self, request):
        return render_to_response('dashboard.html', DashboardView.standard_response_data(request))


class TwitterView(View):
    def get(self, request):

        response_data = DashboardView.standard_response_data(request)
        response_data.update({
            'current_page': 'twitter'
        })

        return render_to_response('twitter.html', response_data)


class FacebookView(View):
    def get(self, request):

        response_data = DashboardView.standard_response_data(request)
        response_data.update({
            'current_page': 'facebook'
        })

        return render_to_response('facebook.html', response_data)


class LinkedInView(View):
    def get(self, request):

        response_data = DashboardView.standard_response_data(request)
        response_data.update({
            'current_page': 'linkedin'
        })

        return render_to_response('linkedin.html', response_data)
