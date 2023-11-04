from django.urls import path

from . import views

urlpatterns = [
    path('cumulative_pub_stats_by_month/',
         views.cumulative_pub_stats_by_month,
         name='cumulative_pub_stats_by_month')
]
