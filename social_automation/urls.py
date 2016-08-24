"""social_automation URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static

from social_automation.views import IndexView, DashboardView, LogoutView, TwitterView, FacebookView, LinkedInView

urlpatterns = [

    url('^api/twitter/?', include('twitter.urls')),
    url('^api/facebook/?', include('facebook.urls')),
    url('^api/linkedin/?', include('linkedin.urls')),

    url(r'^auth/', include('social.apps.django_app.urls', namespace='social')),

    url(r'^dashboard', DashboardView.as_view()),
    url(r'^logout', LogoutView.as_view()),
    url(r'^twitter', TwitterView.as_view()),
    url(r'^facebook', FacebookView.as_view()),
    url(r'^linkedin', LinkedInView.as_view()),
    url(r'^$', IndexView.as_view())

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
