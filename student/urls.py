from django.urls import path

from . import views

urlpatterns = [
    path('studentregistration/', views.studentregistration_view, name='studentregistration'),
]