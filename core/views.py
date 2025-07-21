from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, DetailView, ListView       # Importa classes de visualização genéricas do Django.
from django.views import View                                   # Base para CBV simples
from django.shortcuts import render, redirect, get_object_or_404                             # Importa funções para renderizar templates e redirecionar.
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView                           # Importa a visualização de login do Django.
from django.urls import reverse_lazy
from django.utils.translation import get_language               # Para obter idioma da interface
from core.models import Term, Area, SubArea                                                  # Importa o modelo Term,  que contém os dados dos termos.
from core.forms import UserRegistrationForm #, SearchForm                       # Importa o formulário de registro de utilizador que será criado e o de pesquisa
from django.db.models import Q
from django.contrib.auth.forms import UserCreationForm              # Importa o formulário de criação de utilizador padrão do Django.
from django.utils import translation
from django.db import models
from django.conf import settings

# Classe para a página inicial
# class HomeView(TemplateView):
#     template_name = 'home.html'                                         # Define o template a ser utilizado para esta View.

# view para listar todas as areas
# def area_list(request):
#     areas = Area.objects.all().order_by('id')  # vai buscar todas as áreas e ordena pelo ID
#     return render(request, 'area_list.html', {'areas': areas})

class AreaListView(LoginRequiredMixin, ListView):
    model = Area
    template_name = 'area_list.html'
    context_object_name = 'areas'
    ordering = ['id']

    login_url = "/accounts/login/"

    # view para listar todas as subareas
# def subareas_list(request):
#     subareas = SubArea.objects.all().order_by('ref')    # vai buscar todas as subareas e ordena pela ref (ex: 301-01)
#     return render(request, 'subareas_list.html', {'subareas': subareas})

class SubAreaListView(LoginRequiredMixin, ListView):
    model = SubArea
    template_name = 'subareas_list.html'
    context_object_name = 'subareas'

    login_url = "/accounts/login/"

    def get_queryset(self):
        return SubArea.objects.select_related('area').order_by('ref')

# def subareas_list(request):
#     subareas = SubArea.objects.all().select_related('area').order_by('ref')         # vai buscar todas as subareas ordenadas pela ref (ex: 301-01), e associa a respectiva area com o .select_related('area')
#
#     # for subarea in subareas:                                                                    # Formata o id de cada subarea
#     #     #subarea.subarea_id_0x = subarea.id if int(subarea.id) >= 10 else f"0{subarea.id}"       # Verifica se o id da subarea é menor que 10 e, caso seja, formata com um zero à esquerda
#     #     subarea.subarea_id_0x = f"{int(subarea.id):02d}"
#
#     return render(request, 'subareas_list.html', {'subareas': subareas})   # Passa as subáreas para o template


#view para detalhes de uma area (ou seja as subareas de uma area)
# def area_detail(request, area_id):                              #request fornece informações sobre o request do user. area_id é um identificador que permite à função localizar a área específica na base de dados
#     area = get_object_or_404(Area, id=area_id)                  # vai buscar a área pelo id
#     subareas = SubArea.objects.filter(area=area).order_by('ref')
#     return render(request, 'area_detail.html', {'area': area, 'subareas': subareas})

def area_detail(request, area_id):                              #request fornece informações sobre o request do user. area_id é um identificador que permite à função localizar a área específica na base de dados
    area = get_object_or_404(Area, id=area_id)                  # vai buscar a área pelo id
    subareas = SubArea.objects.filter(area=area).order_by('ref')
#é preciso fazer verificação se subarea.id é um int ????????????????????????????
    # for subarea in subareas:                                                                    # Formata o id de cada subarea
    #     subarea.subarea_id_0x = subarea.id if int(subarea.id) >= 10 else f"0{subarea.id}"       # Verifica se o id da subarea é menor que 10 e, caso seja, formata com um zero à esquerda

    return render(request, 'area_detail.html', {'area': area, 'subareas': subareas})

# view para detalhes de um termo
def term_detail(request, ref):
    term = get_object_or_404(Term, ref=ref)                     # vai buscar o termo pela ref
    return render(request, 'core/term_detail.html', {'term': term})  # aqui podemos escolher o idioma dos conteúdos se necessário

# class UserRegistrationView(TemplateView):
#     template_name = 'registration/signup.html'  # Define o template a ser utilizado para o registo.
#
#     def get(self, request, *args, **kwargs):
#         form = UserRegistrationForm()                               # Cria uma instância do formulário de registo.
#         return render(request, self.template_name, {'form': form})  # Renderiza o template com o formulário.
#
#     def post(self, request, *args, **kwargs):
#         form = UserRegistrationForm(request.POST)  # Cria uma instância do formulário com os dados enviados.
#
#         if form.is_valid():  # Verifica se o formulário é válido.
#             user = form.save()  # Salva o novo utilizador no banco de dados.
#             login(request, user)  # Faz login automático do utilizador após o registo.
#             return redirect('home')  # Redireciona para a página inicial após o registo.
#         return render(request, self.template_name, {'form': form})  # Se o formulário não for válido, faz novamente render do template com o formulário.
#

# view para listar os termos com filtro de idioma
# def term_list(request):
#     # Recupera idioma selecionado ou usa 'en' por padrão
#     content_language = request.GET.get('language', 'en')
#
#     # Recupera subárea e termo pesquisado (query)
#     subarea_ref = request.GET.get('subarea')
#     query = request.GET.get('query', '')
#
#     terms = Term.objects.all()
#
#     # Filtro de busca textual
#     if query:
#         if content_language != 'all':
#             terms = terms.filter(**{f'name_{content_language}__icontains': query})
#         else:
#             # Busca em todos os idiomas definidos
#             q = Q()                                                 #Q() dinâmico: permite combinar todos os campos traduzidos com OR
#             for lang_code, _ in settings.LANGUAGES:
#                 safe_lang_code = lang_code.replace('-', '_')        # <- Corrige pt-br → pt_br    lang_code.replace('-', '_'): evita o erro de campo inexistente como name_pt-br.
#                 q |= Q(**{f'name_{lang_code}__icontains': query})
#             terms = terms.filter(q)
#
#     # Filtro por subárea (se fornecido)
#     if subarea_ref:
#         terms = terms.filter(subarea__ref=subarea_ref)
#         subarea = SubArea.objects.filter(ref=subarea_ref).first()
#     else:
#         subarea = None
#
#     # Otimização e ordenação
#     terms = terms.select_related('subarea__area').order_by('ref')
#
#     # Envia para template
#     return render(request, 'term_list.html', {
#         'terms': terms,
#         'content_language': content_language,
#         'subarea_ref': subarea_ref,
#         'subarea': subarea,
#         'query': query,
#         'LANGUAGES': settings.LANGUAGES,                #LANGUAGES do settings.py não está automaticamente disponível no template term_list.html, por isso é preciso adicionar
#     })


# def term_list(request):
#     # Recupera o idioma de conteúdo selecionado (se houver) ou usa o padrão 'en'
#     content_language = request.GET.get('language', 'en')  # Padrão para 'en' se não for fornecido
#
#     # Verifica se a subárea está na query string
#     subarea_ref = request.GET.get('subarea', None)
#
#     # Filtra os termos com base no idioma de conteúdo e subárea (se fornecida)
#     query = request.GET.get('query', '')
#     if content_language != 'all':  # Se não for 'all', filtra pelo idioma específico
#         terms = Term.objects.filter(**{f'name_{content_language}__icontains': query}) #A variável query é usada para buscar os termos, usando o operador icontains, que permite buscar termos que contenham o texto inserido, sem considerar o caso das letras.
#     else:
#         terms = Term.objects.all()
#
#     if subarea_ref:
#         # Filtra os termos pela subárea, se a referência da subárea for fornecida
#         terms = terms.filter(subarea__ref=subarea_ref)
#         # Busca a subárea com base no ref
#         subarea = SubArea.objects.filter(ref=subarea_ref).first() #first() retorna o primeiro objeto ou None caso não exista.
#
#         # if subarea:
#         #     #subarea.subarea_id_0x = subarea.id if int(subarea.id) >= 10 else f"0{subarea.id}"
#         #     subarea.subarea_id_0x = f"{int(subarea.id):02d}"
#     else:
#         subarea = None
#
#     # Ordena os termos pelo campo ref do modelo Term
#     terms = terms.order_by('ref')
#     terms = terms.select_related('subarea__area').order_by('ref')
#     # Passa as variáveis para o template
#     return render(request, 'core/term_list.html', {
#         'terms': terms,
#         'content_language': content_language,
#         'subarea_ref': subarea_ref,
#         'subarea': subarea,  # Passa o nome da subárea para o template
#         'query': query,
#     })

class TermListView(LoginRequiredMixin, ListView):
    model = Term
    context_object_name = 'terms'

    login_url = "/accounts/login/"

    def get_queryset(self):
        q = self.request.GET.get("q")
        object_list = self.model.objects.all()
        if q:
            object_list = object_list.filter(
                Q(name__icontains=q) | Q(name_pt__icontains=q) | Q(name_pt_br__icontains=q) | Q(name_es__icontains=q) |
                Q(description__icontains=q) | Q(description_pt__icontains=q) | Q(description_pt_br__icontains=q) | Q(description_es__icontains=q) |
                Q(subarea__name__icontains=q) | Q(subarea__name_pt__icontains=q) | Q(subarea__name_pt_br__icontains=q) | Q(subarea__name_es__icontains=q)
            )
        return object_list


class TermDetailView(DetailView):
    model = Term
    context_object_name = 'term'

    def get_object(self, queryset=None):
        ref = self.kwargs.get('ref')
        return get_object_or_404(Term, ref=ref)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Define o idioma do conteúdo a partir da query string ou da interface
        content_language = self.request.GET.get('language') or get_language()
        query = self.request.GET.get('query', '')
        subarea_ref = self.request.GET.get('subarea', '')

        term = context['term']

        # Campos traduzidos dinamicamente
        name_field = f'name_{content_language}'
        description_field = f'description_{content_language}'
        extra_field = f'extra_{content_language}'

        # Atribui os valores traduzidos ao contexto
        context['term_name'] = getattr(term, name_field, term.name)
        context['term_description'] = getattr(term, description_field, term.description)
        context['term_extra'] = getattr(term, extra_field, term.extra)
        context['content_language'] = content_language
        context['subarea'] = term.subarea

        # Adiciona filtros ao contexto para manter os valores no link de retorno
        context['query'] = query
        context['subarea_ref'] = subarea_ref

        # # Adiciona subarea ao contexto, se existir
        # subarea = term.subarea
        # if subarea:
        #     subarea.subarea_id_0x = f"{int(subarea.id):02d}"
        #     context['subarea'] = subarea

        return context
