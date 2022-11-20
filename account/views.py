from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from datetime import datetime
from account.models import acc_income_expense, acc_investment_stock, acc_investment_fund, acc_investment_deposit
from billing.models import bll_mst_bill_item
import urllib
import requests
import json
import numpy_financial as npf

# Create your views here.
@csrf_protect
def createexpense_view(request):
    if request.method == 'POST':
        data_bill = bll_mst_bill_item.objects.filter(id=request.POST['inputNameBilling'])
        amount_in = 0
        amount_out= 0
        datalatest = acc_income_expense.objects.latest('id')
        data_bill = bll_mst_bill_item.objects.filter(id=request.POST['inputNameBilling'])

        if data_bill[0].debet_credit == 0:
            amount_in = int(request.POST['inputAmount'])
            acc_income_expense.objects.create(
                description=data_bill[0].item_name,
                # category=request.POST['inputCategory'],
                amount_in=amount_in,
                amount_out=amount_out,
                overall_balance=datalatest.overall_balance+amount_in,
                account_type=request.POST['inputType'],
                account_date=request.POST['inputDate'],
                bll_mst_item_id=data_bill[0]
            )
        else:
            amount_out = int(request.POST['inputAmount'])
            acc_income_expense.objects.create(
                description=data_bill[0].item_name,
                # category=request.POST['inputCategory'],
                amount_in=amount_in,
                amount_out=amount_out,
                overall_balance=datalatest.overall_balance-amount_out,
                account_type=request.POST['inputType'],
                account_date=request.POST['inputDate'],
                bll_mst_item_id=data_bill[0]
            )
        
        return HttpResponseRedirect(reverse('createexpense'))
    date= str(datetime.today().year) +"-"+ str(datetime.today().month)+"-01"
    dataexpense = acc_income_expense.objects.filter(account_date__gte=date).order_by('-pk')
    data_bill = bll_mst_bill_item.objects.filter(validstatus=1)
    context = {
        'title':'H - Expense',
        'dashboard_active':'Account',
        'dataexpense':dataexpense,
        'databill':data_bill
        }
    return render(request, 'account/createexpense_view.html', context)

@csrf_protect
def stockinvestment_view(request):
    if request.method == 'POST':
        data_stock = acc_investment_stock.objects.filter(stock_code=request.POST['inputNameStock'])
        if data_stock:
            new_amount = data_stock[0].lot + int(request.POST['inputLot'])
            if new_amount == 0:
                data_stock.delete()
            else:
                data_stock.update(lot=new_amount, average = request.POST['inputAverage'])
        else:
            new = acc_investment_stock(
                stock_code = request.POST['inputNameStock'],
                lot = request.POST['inputLot'],
                average = request.POST['inputAverage'],
                der_annual = 0,
                bv_5 = 1,
                bv_annual = 1,
                dividend = 0
                )
            new.save()
        return HttpResponseRedirect(reverse('stockinvestment'))
    datastock = acc_investment_stock.objects.all()
    current_price = []
    growth_rate = []
    fut_val = []
    pbv = []
    porto = []
    
    for data in datastock:
        
        #current price
        url = f'https://query1.finance.yahoo.com/v8/finance/chart/{data.stock_code}.JK'

        req = urllib.request.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7')
        response = urllib.request.urlopen(req)
        res = response.read()      # a `bytes` object
        html = res.decode('utf-8') # a `str`; this step can't be used if data is binary
        html = json.loads(html)
        current_price.append(html['chart']['result'][0]['meta']['regularMarketPrice'])
        
        #growth rate
        temp_gr = (float(data.bv_annual) / float(data.bv_5)) ** (1 / (6 - 1)) - 1
        growth_rate.append(round(temp_gr*100,2))
        
        #fv
        fut_val.append(round((npf.fv(temp_gr,5,0,-1*float(data.bv_annual))+(float(data.dividend)*5)),2))
        
        #pbv
        pbv.append(round((1-(float(data.bv_annual)-html['chart']['result'][0]['meta']['previousClose'])/float(data.bv_annual)),2))
        
        #myporto 
        res_porto = '{:20,.2f}'.format((html['chart']['result'][0]['meta']['previousClose']*data.lot*100))
        porto.append(res_porto)
    
    datastock = zip(datastock, current_price, growth_rate, fut_val, pbv, porto)
    
    # data_bill = bll_mst_bill_item.objects.filter(validstatus=1)
    context = {
        'title':'H - Expense',
        'dashboard_active':'Account',
        'datastock':list(datastock),
        # 'databill':data_bill
        }
    return render(request, 'account/stockinvestment_view.html', context)

@csrf_protect
def fundinvestment_view(request):
    if request.method == 'POST':
        data_fund = acc_investment_fund.objects.filter(fund_code=request.POST['inputNameFund'])
        if data_fund:
            data_fund.update(
                unit=request.POST['inputUnit'], 
                average_nav = request.POST['inputAverageNav'],
                current_nav = request.POST['inputCurrentNav'])
        else:
            new = acc_investment_fund(
                fund_code = request.POST['inputNameFund'],
                unit = request.POST['inputUnit'],
                average_nav = request.POST['inputAverageNav'],
                current_nav = request.POST['inputCurrentNav'])
            new.save()
        return HttpResponseRedirect(reverse('fundinvestment'))
    datafund = acc_investment_fund.objects.all()
    m_value = []
    gain_loss = []
    
    for data in datafund:
                
        #m_value
        if data.pk == 2:
            temp_val = float(data.unit) * float(data.current_nav)
            titipan_bune = 20000000+((float(data.current_nav)-1224.21)*16337.0663)
            m_value.append(round(temp_val-titipan_bune,2))
            gain_loss.append(
                round(
                    (temp_val-titipan_bune)-(float(data.average_nav)*(float(data.unit)-16337.0663)),2
                        )
                             )
        else:
            temp_val = float(data.unit) * float(data.current_nav)
            m_value.append(round(temp_val,2))
            gain_loss.append(round(temp_val-(float(data.average_nav)*float(data.unit)),2))
    
    data_fund = zip(datafund, m_value, gain_loss)
    
    # data_bill = bll_mst_bill_item.objects.filter(validstatus=1)
    context = {
        'title':'H - Expense',
        'dashboard_active':'Account',
        'datafund':list(data_fund),
        'datareksa_ibu':[16337.0663,round(titipan_bune,2),round(titipan_bune-20000000,2)],
        }
    return render(request, 'account/fundinvestment_view.html', context)

@csrf_protect
def depoinvestment_view(request):
    if request.method == 'POST':
        new = acc_investment_deposit(
            date_created = request.POST['inputDate'],
            description = request.POST['inputDesc'],
            amount = request.POST['inputNominal'])
        new.save()
        return HttpResponseRedirect(reverse('depoinvestment'))
    datadepo = acc_investment_deposit.objects.all()
    
    context = {
        'title':'H - Expense',
        'dashboard_active':'Account',
        'datadepo':datadepo,
        }
    return render(request, 'account/depoinvestment_view.html', context)