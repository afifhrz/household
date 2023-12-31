from django.urls import path

from . import views

urlpatterns = [
    path('vehicle/', views.mastervehicle_view, name='mastervehicle'),
    path('maintainance/', views.serviceitem_view, name='serviceitem'),
    path('history/', views.servicehistory_view, name='history'),
    path('get_maintainance_item/<int:vehicle_id>', views.get_maintainance_item, name='get_maintainance_item'),
]