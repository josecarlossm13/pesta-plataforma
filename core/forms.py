from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

class UserRegistrationForm(UserCreationForm):
     email = forms.EmailField(required=True, label="Email")

     class Meta:
         model = User
         fields = ("username", "email", "password1", "password2")


# class SearchForm(forms.Form):
#     query = forms.CharField(label='Pesquisar', max_length=100)  # Campo de texto para a pesquisa.
#     language = forms.ChoiceField(  # Campo de seleção para escolher o idioma.
#         choices=[
#             ('all', 'Todos'),  # Opção para pesquisar em todos os idiomas.
#             ('pt', 'Português'),
#             ('en', 'Inglês'),
#             ('es', 'Espanhol'),
#
#         ],
#         required=False,  # Este campo não é obrigatório.
#         label='Idioma'
#     )


# class UserRegistrationForm(forms.ModelForm):
#     primeiro_nome = forms.CharField(max_length=30, required=True, label='Primeiro Nome')
#     ultimo_nome = forms.CharField(max_length=30, required=True, label='Último Nome')
#     email = forms.EmailField(required=True, label='E-mail')
#     password = forms.CharField(widget=forms.PasswordInput, required=True, label='Senha')
#
#     class Meta:
#         model = User  # Define o modelo que será utilizado.
#         fields = ['primeiro_nome', 'ultimo_nome', 'email', 'password']  # Campos a serem incluídos no formulário.
#
#     def save(self, commit=True):
#         user = super().save(commit=False)  # Cria uma instância do utilizador sem salvar ainda.
#         user.set_password(self.cleaned_data['password'])  # Define a senha do utilizador.
#         if commit:
#             user.save()  # Salva o utilizador na base de dados.
#         return user