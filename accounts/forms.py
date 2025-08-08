from django import forms
from django.contrib.auth.models import Group

class CustomSignupForm(forms.Form):
    def signup(self, request, user):
        # Usa o email como username
        user.username = user.email
        user.save()

        # Adiciona ao grupo "SemAcesso", se existir
        try:
            group = Group.objects.get(name="SemAcesso")
            user.groups.add(group)
        except Group.DoesNotExist:
            pass

        return user
