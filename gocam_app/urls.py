from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('lookup_ids', views.index, name='lookup_ids'),
]
