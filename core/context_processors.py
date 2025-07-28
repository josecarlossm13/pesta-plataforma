# core/context_processors.py
from .models import Area

# para filtar na navbar por area
# garantir que todas as views que usam o base.html enviem as áreas no contexto
def areas_dropdown(request):
    return {
        'all_areas': Area.objects.all().order_by('id')
    }
