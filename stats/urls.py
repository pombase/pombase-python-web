from django.urls import path

from . import views

urlpatterns = [
    path('cumulative_curated_by_year/',
         views.cumulative_curated_by_year,
         name='cumulative_curated_by_year'),
    path('curated_by_year/',
         views.curated_by_year,
         name='curated_by_year'),
    path('curatable_by_year/',
         views.curatable_by_year,
         name='curatable_by_year')
]
