from django.urls import path

from . import views

urlpatterns = [
    path('createexpense/', views.createexpense_view, name='createexpense'),
]