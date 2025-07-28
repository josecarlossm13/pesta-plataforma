from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, DetailView, ListView       # Importa classes de visualização genéricas do Django.
from django.views import View                                   # Base para CBV simples
from django.shortcuts import render, redirect, get_object_or_404                             # Importa funções para renderizar templates e redirecionar.
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView                           # Importa a visualização de login do Django.
from django.urls import reverse_lazy
from django.utils.translation import get_language               # Para obter idioma da interface
from core.models import Term, Area, SubArea, News                                # Importa o modelo Term,  que contém os dados dos termos.
from core.forms import UserRegistrationForm #, SearchForm                       # Importa o formulário de registro de utilizador que será criado e o de pesquisa
from django.db.models import Q
from django.contrib.auth.forms import UserCreationForm              # Importa o formulário de criação de utilizador padrão do Django.
from django.utils import translation
from django.db import models
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.urls import reverse                                     # usado para gerar URLs com base no nome dos caminhos

# funções para gerar uma stack para usar no botão "voltar"
def update_navigation_stack(request):
    stack = request.session.get('navigation_stack', [])
    current_url = request.get_full_path()

    # Se a pilha estiver vazia ou o topo for diferente da URL atual, adiciona
    if not stack or stack[-1] != current_url:
        # Se o URL atual existir na stack (loop), remove-o antes de re-adicionar
        if current_url in stack:
            stack.remove(current_url)
        stack.append(current_url)

    # Mantém apenas os últimos 10 itens
    request.session['navigation_stack'] = stack[-10:]

def get_back_url(request, fallback_url):
    stack = request.session.get('navigation_stack', [])

    # Remover a página atual do topo
    current_url = request.get_full_path()
    if stack and stack[-1] == current_url:
        stack.pop()

    # Atualizar a stack no request.session
    request.session['navigation_stack'] = stack

    if stack:
        return stack[-1]  # página anterior real
    return fallback_url



class AreaListView(LoginRequiredMixin, ListView):
    model = Area
    template_name = 'area_list.html'
    context_object_name = 'areas'
    ordering = ['id']
    login_url = "/accounts/account/"

    def get(self, request, *args, **kwargs):
        update_navigation_stack(request)
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['back_url'] = get_back_url(self.request, fallback_url=reverse('home'))

        return context



# View para listar subareas. [pode receber uma (area_id)]
class SubAreaListView(LoginRequiredMixin, ListView):
    model = SubArea
    template_name = 'subarea_list.html'
    context_object_name = 'subareas'
    login_url = "/accounts/account/"

    # # para o botão voltar. armazenar manualmente o caminho anterior desejado em request.session, uma vez que o HTTP_REFERER usava apenas o histórico e não resultava sempre
    # def get(self, request, *args, **kwargs):
    #     request.session['previous_url'] = request.get_full_path()
    #     return super().get(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        update_navigation_stack(request)
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        area_id = self.kwargs.get('area_id')
        qs = SubArea.objects.select_related('area').order_by('area__id', 'id')
        if area_id:
            qs = qs.filter(area__id=area_id)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        area_id = self.kwargs.get('area_id')
        if area_id:
            context['area'] = Area.objects.filter(id=area_id).first()

        # Botão voltar
        context['back_url'] = get_back_url(self.request, fallback_url=reverse('area-list'))

        return context


# função para detalhes de um termo
@login_required(login_url='/accounts/account/')
def term_detail(request, ref):
    term = get_object_or_404(Term, ref=ref)                     # vai buscar o termo pela ref
    return render(request, 'core/term_detail.html', {'term': term})  # aqui podemos escolher o idioma dos conteúdos se necessário


class TermListView(LoginRequiredMixin, ListView):
    model = Term
    context_object_name = 'terms'
    login_url = "/accounts/account/"

    # # para o botão voltar. armazenar manualmente o caminho anterior desejado em request.session, uma vez que o HTTP_REFERER usava apenas o histórico e não resultava sempre
    # def get(self, request, *args, **kwargs):
    #     request.session['previous_url'] = request.get_full_path()
    #     return super().get(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        update_navigation_stack(request)
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        q = self.request.GET.get("q")
        subarea_ref = self.kwargs.get('ref')  # vem da URL
        object_list = self.model.objects.all()

        # Filtra pelo termo de busca, se existir
        if q:
            object_list = object_list.filter(
                Q(name__icontains=q) | Q(name_pt__icontains=q) | Q(name_pt_br__icontains=q) | Q(name_es__icontains=q) |
                Q(description__icontains=q) | Q(description_pt__icontains=q) | Q(description_pt_br__icontains=q) | Q(
                    description_es__icontains=q) |
                Q(subarea__name__icontains=q) | Q(subarea__name_pt__icontains=q) | Q(
                    subarea__name_pt_br__icontains=q) | Q(subarea__name_es__icontains=q)
            )

        # Filtra pela subárea guardada na sessão, se existir
        if subarea_ref:
            object_list = object_list.filter(subarea__ref=subarea_ref)

        return object_list.order_by('ref')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        subarea_ref = self.kwargs.get('ref')
        if subarea_ref:
            context['subarea'] = SubArea.objects.filter(ref=subarea_ref).first()
            context['subarea_ref'] = subarea_ref
        else:
            # Se não há subarea, evita usar esses campos no template
            context['subarea_ref'] = None
            context['subarea'] = None

        # # Adiciona botão de voltar com fallback (técnica http_referer)
        # referer = self.request.META.get('HTTP_REFERER')
        # if referer and self.request.get_host() in referer:
        #     context['back_url'] = referer
        # elif subarea_ref:
        #     context['back_url'] = reverse('subarea-list')
        # else:
        #     context['back_url'] = reverse('area-list')  # fallback mais genérico

        # Botão voltar
        context['back_url'] = get_back_url(self.request, fallback_url=reverse('subarea-list'))

        return context


class TermDetailView(LoginRequiredMixin, DetailView):
    model = Term
    context_object_name = 'term'
    login_url = "/accounts/account/"

    def get(self, request, *args, **kwargs):
        update_navigation_stack(request)
        return super().get(request, *args, **kwargs)

    def get_object(self, queryset=None):
        ref = self.kwargs.get('ref')
        return get_object_or_404(Term, ref=ref)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # # botão para voltar atrás com fallback caso seja acedido diretamente pelo link (técnica http_referer)
        # referer = self.request.META.get('HTTP_REFERER')
        # if referer and self.request.get_host() in referer:
        #     context['back_url'] = referer
        # else:
        #     context['back_url'] = reverse('term-list')  # fallback seguro

        # # Fallback robusto para back_url
        # back_url = self.request.session.get('previous_url')
        # if back_url and self.request.get_host() in back_url:
        #     context['back_url'] = back_url
        # else:
        #     context['back_url'] = reverse('term-list')  # Ou algum outro valor seguro

        # Usar a função para obter o back_url (botão "voltar")
        context['back_url'] = get_back_url(self.request, fallback_url=reverse('term-list'))

        # Define o idioma do conteúdo a partir da query string ou da interface
        content_language = self.request.GET.get('language') or get_language()
        query = self.request.GET.get('query', '')

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

        return context

#  para mostrar mensagens de avisos/notícias na homepage
def home(request):
    now = timezone.now()
    news = News.objects.filter(
        active=True
    ).filter(
        models.Q(start_date__lte=now) | models.Q(start_date__isnull=True),
        models.Q(end_date__gte=now) | models.Q(end_date__isnull=True)
    ).order_by('-created_at').first()

    return render(request, 'home.html', {'news': news})

