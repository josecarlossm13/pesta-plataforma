# core/context_processors.py
from .models import Area

# para filtar na navbar por area
# garantir que todas as views que usam o base.html enviem as áreas no contexto
def areas_dropdown(request):
    return {
        'all_areas': Area.objects.all().order_by('id')
    }

# verificar se o user é admin, gestor ou superuser. Para exibir certas funcionalidades no site tal como o Painel Admin.
def user_permissions(request):
    is_admin_or_gestor = request.user.groups.filter(name__in=['Admin', 'Gestor']).exists() or request.user.is_superuser
    return {'is_admin_or_gestor': is_admin_or_gestor}