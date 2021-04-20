from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('motifsearch/', include('motifsearch.urls')),
    path('gene_ex/', include('gene_ex.urls')),
    path('admin/', admin.site.urls),
]
