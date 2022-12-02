from django.urls import path

from . import views

urlpatterns = [
    path('createexpense/', views.createexpense_view, name='createexpense'),
    path('stockinvestment/', views.stockinvestment_view, name='stockinvestment'),
    path('fundinvestment/', views.fundinvestment_view, name='fundinvestment'),
    path('depoinvestment/', views.depoinvestment_view, name='depoinvestment'),
    path('arliability/', views.arliability_view, name='arliability'),
    path('arliability_paid/'+'<int:id>/', views.arliability_paid, name='arliability_paid'),
    path('cancel_ar/'+'<int:id>/', views.cancel_ar, name='cancel_ar'),
]