from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('motifsearch/', include('motifsearch.urls')),
    path('admin/', admin.site.urls),
]
