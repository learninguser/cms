from django.shortcuts import render, redirect
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.models import User
# from django.contrib.auth.forms import UserCreationForm # Default user Creation form from Django
from django.urls import reverse_lazy
from account import forms
from django.contrib.auth import authenticate, login
from django.conf import settings
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.base import TemplateView
from account import models
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.

class SignUpView(SuccessMessageMixin, CreateView):
    model = settings.AUTH_USER_MODEL
    form_class = forms.SignUpForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        ################## METHOD 1 ##############################################################
        ############# To Login a user after he is successfully registered ########################
        ##########################################################################################

        # valid = super(SignUpView, self).form_valid(form)
        # username, password = form.cleaned_data.get('username'), form.cleaned_data.get('password1')
        # new_user = authenticate(username=username, password=password)
        # login(self.request, new_user)
        
        ################## METHOD 2 ##############################################################
        ############# To Login a user after he is successfully registered ########################
        ##########################################################################################

        # Login the user
        valid = super().form_valid(form)
        login(self.request, self.object,  backend='django.contrib.auth.backends.ModelBackend')
        
        return valid

    def get_success_message(self, cleaned_data):
        username = cleaned_data.get('username')
        return (f"Account for {username}! is created and logged in successfully")

class UserProfileView(LoginRequiredMixin, CreateView):
    model = models.User
    form_class = forms.UserProfileForm
    login_url = reverse_lazy('login')
    template_name = 'registration/profile.html'
    pk_url_kwarg = 'pk'

class UserProfileUpdateView(LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy('login')
    model = models.User
    fields = ('username','first_name','last_name','email')
    template_name = 'registration/profile_update.html'
    pk_url_kwarg = 'pk'