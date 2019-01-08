from django.urls import path

from . import views

urlpatterns = [
    path('query/<str:pattern>', views.query, name='query'),
]
