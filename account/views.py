from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
import urllib.parse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from datetime import datetime
from account.models import acc_income_expense
from billing.models import bll_mst_bill_item

# Create your views here.
@csrf_protect
def createexpense_view(request):
    if request.method == 'POST':
        data_bill = bll_mst_bill_item.objects.filter(id=request.POST['inputNameBilling'])
        amount_in = 0
        amount_out= 0
        datalatest = acc_income_expense.objects.latest('id')

        if data_bill[0].debet_credit == 0:
            amount_in = int(request.POST['inputAmount'])
            acc_income_expense.objects.create(
                description=data_bill[0].item_name,
                category=request.POST['inputCategory'],
                amount_in=amount_in,
                amount_out=amount_out,
                overall_balance=datalatest.overall_balance+amount_in,
                account_type=request.POST['inputType'],
                account_date=datetime.now()
            )
        else:
            amount_out = int(request.POST['inputAmount'])
            acc_income_expense.objects.create(
                description=data_bill[0].item_name,
                category=request.POST['inputCategory'],
                amount_in=amount_in,
                amount_out=amount_out,
                overall_balance=datalatest.overall_balance-amount_out,
                account_type=request.POST['inputType'],
                account_date=datetime.now()
            )
        
        return HttpResponseRedirect(reverse('createexpense'))
    dataexpense = acc_income_expense.objects.all()
    data_bill = bll_mst_bill_item.objects.filter(validstatus=1)
    context = {
        'title':'H - Expense',
        'dashboard_active':'Account',
        'dataexpense':dataexpense,
        'databill':data_bill
        }
    return render(request, 'account/createexpense_view.html', context)