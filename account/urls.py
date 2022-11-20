from django.urls import path

from . import views

urlpatterns = [
    path('createexpense/', views.createexpense_view, name='createexpense'),
    path('stockinvestment/', views.stockinvestment_view, name='stockinvestment'),
    path('fundinvestment/', views.fundinvestment_view, name='fundinvestment'),
    path('depoinvestment/', views.depoinvestment_view, name='depoinvestment'),
]