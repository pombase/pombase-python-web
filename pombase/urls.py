from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('motifsearch/', include('motifsearch.urls')),
    path('gene_ex/', include('gene_ex.urls')),
    path('structure_view/', include('structure_view.urls')),
    path('rna_2d_structure/', include('rna_2d_structure.urls')),
    path('protein_feature_view/', include('protein_feature_view.urls')),
    path('gocam_viz/', include('gocam_viz.urls')),
    path('gocam_view/', include('gocam_view.urls')),
    path('gocam_connections/', include('gocam_connections.urls')),
    path('rhea_widget/', include('rhea_widget.urls')),
    path('stats/', include('stats.urls')),
    path('admin/', admin.site.urls),
]
