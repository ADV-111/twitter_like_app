
from django.contrib import admin
from django.urls import path

from twitter.views import BaseView, UserCreationView, success_registration, UserLoginView, \
    logout_and_home, CreateTweet

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', BaseView.as_view(), name='base'),
    path('user/create/', UserCreationView.as_view(), name='create_user'),
    path('user/login/', UserLoginView.as_view(), name='login'),
    path('user/logout/', logout_and_home, name='logout'),
    path('success_registration/', success_registration, name='success_registration'),
    path('tweet/create/', CreateTweet.as_view(), name='create_tweet'),
]
