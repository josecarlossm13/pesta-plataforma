from django.shortcuts import render

# Create your views here.

# accounts/views.py
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView

#creating a new class called SignUpView that extends CreateView, sets the form as UserCreationForm,
# and uses the template signup.html

class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'