from django.contrib import admin
from django.urls import include, path

import os

urlpatterns = [
    path('gocam_viz/', include('gocam_viz.urls')),
    path('gocam_view/', include('gocam_view.urls')),
    path('gocam_connections/', include('gocam_connections.urls')),
]

if len(os.environ["WEBSITE_CONFIG_JSON_PATH"]) > 0:
    urlpatterns.append(path('motifsearch/', include('motifsearch.urls')))
    urlpatterns.append(path('gene_ex/', include('gene_ex.urls')))
    urlpatterns.append(path('structure_view/', include('structure_view.urls')))
    urlpatterns.append(path('rna_2d_structure/', include('rna_2d_structure.urls')))
    urlpatterns.append(path('protein_feature_view/', include('protein_feature_view.urls')))
    urlpatterns.append(path('rhea_widget/', include('rhea_widget.urls')))
    urlpatterns.append(path('stats/', include('stats.urls')))
    urlpatterns.append(path('admin/', admin.site.urls))
