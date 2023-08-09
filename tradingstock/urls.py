from django.urls import path

from . import views

urlpatterns = [
    path('runfilter/', views.run_filter, name='run_filter'),
    path('lastfilter/', views.last_filter, name='last_filter'),
    path('createtransactionstock/', views.createtransactionstock, name='createtransactionstock'),
]