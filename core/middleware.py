# from django.utils import translation
#
# class CustomLocaleMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response
#
#     def __call__(self, request):
#         if request.user.is_authenticated:
#             language = request.user.user_profile.language
#             translation.activate(language)
#             request.LANGUAGE_CODE = language
#             request.session['django_language'] = language  # Armazena o idioma na sessão
#         else:
#             request.LANGUAGE_CODE = "en"  # Define o idioma padrão para usuários não autenticados
#
#         response = self.get_response(request)
#         return response