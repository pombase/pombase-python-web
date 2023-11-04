from django.urls import path

from . import views

urlpatterns = [
    path('cumulative_curated_by_year/',
         views.cumulative_curated_by_year,
         name='cumulative_curated_by_year')
]
