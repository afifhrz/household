from django.urls import path

from . import views

urlpatterns = [
    path('studentregistration/', views.studentregistration_view, name='studentregistration'),
    path('courseregistration/', views.courseregistration_view, name='courseregistration'),
    path('completedcourse/', views.completedcourse_view, name='completedcourse'),
]