from django.urls import path

from . import views

urlpatterns = [
    path('query/', views.query, name='query'),
    path('ping/', views.ping, name='ping'),
]
