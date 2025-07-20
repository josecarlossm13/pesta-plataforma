# accounts/urls.py
from django.urls import path
from .views import TermListView, TermDetailView, AreaListView, SubAreaListView, area_detail

urlpatterns = [
    path('terms/', TermListView.as_view(), name='term-list'),
    path('terms/<str:ref>/', TermDetailView.as_view(), name='term_detail'),
    path('areas/', AreaListView.as_view(), name='area_list'),
    path('subareas/', SubAreaListView.as_view(), name='subareas_list'),
    path('areas/<int:area_id>/', area_detail, name='area_detail'),

]