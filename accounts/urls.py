# accounts/urls.py
from django.urls import path
from .views import SignUpView
from django.views.generic.base import TemplateView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('account/', TemplateView.as_view(template_name="account.html"), name='account')
]