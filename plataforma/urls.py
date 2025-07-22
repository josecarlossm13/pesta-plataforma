"""
URL configuration for plataforma project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin            # Importa o módulo de administração do Django.
from django.urls import include, path       # Importa as funções para incluir URLs e definir caminhos.
from django.conf import settings            # Importa as configurações do Django.
#from plataforma.core.views import TermDetailView, area_list, area_detail, subareas_list #, UserLoginView, logout_view, HomeView,
from django.conf.urls.static import static
#from ..core import views
from django.views.generic.base import TemplateView
from django.contrib.auth import views as auth_views
from core.views import home

urlpatterns = [
    path('admin/', admin.site.urls),                        # Define a URL para aceder à interface de administração do Django.
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/', include('accounts.urls')),
    path('core/', include('core.urls')),
    path("i18n/", include("django.conf.urls.i18n")),

   # path('', TemplateView.as_view(template_name="home.html"), name='home'),
    path('', home, name='home'),

    path('ckeditor/', include('ckeditor_uploader.urls')),   # Inclui as URLs do CKEditor para permitir uploads e outras funcionalidades.
]

# Package Rosetta (tal como no tutorial)
if 'rosetta' in settings.INSTALLED_APPS:                      # Verifica se a app 'rosetta' está instalada nas configurações do Django.
    urlpatterns += [                                          # Adiciona novas URLs à lista existente de urlpatterns.
        path('rosetta/', include('rosetta.urls'))       # Inclui as URLs da app 'rosetta' para acesso à interface de tradução.
    ]

# Permite que o Django sirva arquivos de media durante o desenvolvimento, facilitando o acesso a esses arquivos através de URLs específicas.
# Num ambiente de produção, é comum usar um servidor web (como Nginx ou Apache) para servir arquivos de media, em vez de depender do Django para isso.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Adiciona as URLs relacionadas com áreas e termos dentro de i18n_patterns
# URLs com prefixo de idioma
# urlpatterns += i18n_patterns(
#     path('home/', HomeView.as_view(), name='home'),
#     path('areas/', area_list, name='area_list'),
#     path('areas/<str:area_id>/', area_detail, name='area_detail'),
#     path('terms/', TermListView.as_view(), name='term_list'),
#     path('terms/<str:ref>/', TermDetailView.as_view(), name='term_detail'),
    # path('register/', UserRegistrationView.as_view(), name='register'),
    # path('login/', UserLoginView.as_view(), name='login'),
    # path('logout/', logout_view, name='logout'),
#)


