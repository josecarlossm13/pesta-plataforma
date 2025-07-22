# accounts/urls.py
from django.urls import path
from .views import TermListView, TermDetailView, AreaListView, SubAreaListView, home
from . import views


urlpatterns = [
    path('terms/', TermListView.as_view(), name='term-list'),
    path('terms/subarea/<str:ref>/', TermListView.as_view(), name='term-list-by-subarea'),  # termos filtrados por subarea
    path('terms/<str:ref>/', TermDetailView.as_view(), name='term_detail'),

    path('areas/', AreaListView.as_view(), name='area-list'),

    path('subareas/', SubAreaListView.as_view(), name='subarea-list'),                         # todas as subareas
    path('subareas/<int:area_id>/', SubAreaListView.as_view(), name='subarea-list-by-area'),
]