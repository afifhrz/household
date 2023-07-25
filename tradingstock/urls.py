from django.urls import path

from . import views

urlpatterns = [
    path('runfilter/', views.run_filter, name='run_filter'),
]