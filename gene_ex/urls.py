from django.urls import path

from . import views

urlpatterns = [
    path('gene_ex_violin/', views.gene_ex_violin, name='gene_ex_violin'),
]
