from django.urls import path

from . import views

urlpatterns = [
    path('runfilter/', views.run_filter, name='run_filter'),
    path('lastfilter/', views.last_filter, name='last_filter'),
    path('testengine/', views.test_engine, name='test_engine'),
    path('testengine-many/', views.test_engine_many, name='test_engine_many'),
    path('create-transaction/', views.createtransactionstock, name='createtransactionstock'),
]