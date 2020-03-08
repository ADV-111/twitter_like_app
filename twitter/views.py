# from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView, logout_then_login
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView

from twitter.forms import UserRegistrationForm, AuthenticationFormExtended
from twitter.models import User, Tweet


def success_registration(request):
    return render(request, 'success_registration.html', {})


class BaseView(View):
    def get(self, request):
        tweets = Tweet.objects.all()
        return render(request, 'base.html', context={'tweets': tweets})


class UserCreationView(CreateView):
    template_name = 'create_user.html'
    form_class = UserRegistrationForm

    def form_valid(self, form):
        # save the new user first
        form.save()
        # get the username and password
        username = self.request.POST['email']
        password = self.request.POST['password1']
        # authenticate user then login
        user = authenticate(username=username, password=password)
        login(self.request, user)
        return redirect(reverse_lazy('base'))


class UserLoginView(LoginView):
    template_name = 'login_user.html'
    authentication_form = AuthenticationFormExtended
    # success_url = reverse_lazy('base') # nie trzeba tego bo jest ustawiony w settings na sztywno LOGIN_REDIRECT_URL bo wykorzystuje AuthenticationForm


def logout_and_home(request):
    return logout_then_login(request, login_url='base')


class CreateTweet(CreateView):
    template_name = 'create_tweet.html'
    model = Tweet
    fields = '__all__'
    success_url = reverse_lazy('base')
