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
    path('updateprice/', views.updateprice, name='updateprice'),
    path('saving_goal_tracker/', views.saving_goal_tracker_view, name='saving_goal_tracker'),
    path('get_final_goal/'+'<str:inflation_rate>/'+'<int:period_in_year>/'+'<int:current_value>/', views.get_final_goal, name='get_final_goal'),
]