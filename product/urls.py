from django.urls import path

from . import views

urlpatterns = [
    path('createproduct/', views.createproduct_view, name='createproduct'),
]