from django.urls import path

from . import views

urlpatterns = [
    path('generatebillcourse/', views.generatebillcourse_view, name='generatebillcourse'),
]