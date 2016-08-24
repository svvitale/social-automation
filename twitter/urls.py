from django.conf.urls import url
from .views import FollowFromUrlView

urlpatterns = [
    url('follow-from-url/?', FollowFromUrlView.as_view()),
]
