from django.urls import path
from . import apiviews as views

urlpatterns = [
path('fetch/<str:type>/', views.PropertyView.as_view(), name='fetch'),
path('param/', views.ParamView.as_view(), name='param'),
path('search/', views.SearchView.as_view(), name='asearch'),
]
