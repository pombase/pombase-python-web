from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('motifsearch/', include('motifsearch.urls')),
    path('gene_ex/', include('gene_ex.urls')),
    path('structure_view/', include('structure_view.urls')),
    path('protein_feature_view/', include('protein_feature_view.urls')),
    path('stats/', include('stats.urls')),
    path('admin/', admin.site.urls),
]
