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
         name='curatable_by_year'),
    path('ltp_genes_per_pub_per_year_range',
         views.ltp_genes_per_pub_per_year_range,
         name='ltp_genes_per_pub_per_year_range')
    path('ltp_annotations_per_pub_per_year_range',
         views.ltp_annotations_per_pub_per_year_range,
         name='ltp_annotations_per_pub_per_year_range'),
    path('htp_annotations_per_pub_per_year_range',
         views.htp_annotations_per_pub_per_year_range,
         name='htp_annotations_per_pub_per_year_range')
]
