from django.urls import path

from . import views

urlpatterns = [
    path('generatebillcourse/', views.generatebillcourse_view, name='generatebillcourse'),
    path('liststatusbill/', views.liststatusbill_view, name='liststatusbill'),
    path('send_invoice/'+'<int:id>/', views.send_invoice, name='sendinvoice'),
    path('paid_invoice/'+'<int:id>/', views.paid_invoice, name='paidinvoice'),
    path('cancel_invoice/'+'<int:id>/', views.cancel_invoice, name='cancelinvoice'),
    path('createmstbill/', views.createmstbill_view, name='createmstbill'),
]