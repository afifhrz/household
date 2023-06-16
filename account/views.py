from django.http import HttpResponseRedirect, HttpResponse
from django.http import JsonResponse
from django.urls import reverse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from datetime import datetime
import calendar
from account.models import acc_income_expense, acc_investment_stock, acc_investment_fund, acc_investment_deposit, acc_ar_debt, acc_saving_goal_tracker
from billing.models import bll_mst_bill_item, bll_trx_bill_item
import urllib
import requests
import json
import numpy_financial as npf
from dateutil.relativedelta import relativedelta

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
                amount_in=amount_in,
                amount_out=amount_out,
                overall_balance=datalatest.overall_balance+amount_in,
                account_type=request.POST['inputType'],
                account_date=request.POST['inputDate'],
                bll_mst_item_id=data_bill[0],
                remarks=request.POST['inputRemarks']
            )
        else:
            if request.POST['inputNameBilling'] == "16":
                dateContract = request.POST['inputStartDateContract']
                date_time_obj = datetime.strptime(dateContract, '%Y-%m-%d')
                month_length = int(request.POST['periodContract'])*12
                amountPaid = int(request.POST['inputAmount'])/month_length
                overall_balance_latest = float(datalatest.overall_balance)
                for i in range(month_length):
                    overall_balance_latest = overall_balance_latest - amountPaid
                    acc_income_expense.objects.create(
                        description=data_bill[0].item_name,
                        amount_in=amount_in,
                        amount_out=amountPaid,
                        overall_balance=overall_balance_latest,
                        account_type=request.POST['inputType'],
                        bll_mst_item_id=data_bill[0],
                        remarks=request.POST['inputRemarks'],
                        account_date=date_time_obj
                    )
                    date_time_obj = date_time_obj + relativedelta(months=1)
            
            elif request.POST['inputNameBilling'] == "21":
                amount_out = int(request.POST['inputAmount'])
                acc_income_expense.objects.create(
                    description=data_bill[0].item_name,
                    amount_in=amount_in,
                    amount_out=amount_out,
                    overall_balance=datalatest.overall_balance-amount_out,
                    account_type=request.POST['inputType'],
                    account_date=request.POST['inputDate'],
                    bll_mst_item_id=data_bill[0],
                    remarks=request.POST['inputRemarks']
                )
                acc_ar_debt.objects.create(
                    amount = amount_out,
                    description = request.POST['inputRemarks'],
                    account_status = "UNPAID",
                    account_type = "AR",
                    bll_mst_item_id = data_bill[0],
                    valid_status = "VALID"
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
                    bll_mst_item_id=data_bill[0],
                    remarks=request.POST['inputRemarks']
                )
        
        return HttpResponseRedirect(reverse('createexpense'))
    date= str(datetime.today().year) +"-"+ str(datetime.today().month)+"-01"
    res = calendar.monthrange(datetime.today().year, datetime.today().month)
    day = str(res[1])
    date_2= str(datetime.today().year) +"-"+ str(datetime.today().month)+"-"+day
    dataexpense = acc_income_expense.objects.filter(account_date__gte=date, account_date__lte=date_2).order_by('-account_date')
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
    wbiv = []
    bi_rate = 0.035
    selisih_tp = []
    g_l = []
    
    for data in datastock:
        temp_cp = data.last_price
        current_price.append(temp_cp)
        #growth rate
        temp_gr = (float(data.bv_annual) / float(data.bv_5)) ** (1 / (6 - 1)) - 1
        growth_rate.append(round(temp_gr*100,2))
        
        #fv
        temp_fv = round((npf.fv(temp_gr,5,0,-1*float(data.bv_annual))+(float(data.dividend)*5)),2)
        fut_val.append(temp_fv)
        
        #pbv
        pbv.append(round((1-(float(data.bv_annual)-temp_cp)/float(data.bv_annual)),2))
        
        #myporto 
        res_porto = '{:20,.2f}'.format((temp_cp*data.lot*100))
        porto.append(res_porto)
        
        # wbiv / targetprice
        temp_wbiv = -1*npf.pv(bi_rate, 5,0,temp_fv)
        wbiv.append(round(temp_wbiv,2))
        
        # selisih tp dan cp
        if data.average > temp_wbiv:
            selisih_tp.append((temp_cp - float(data.average))/float(data.average)*100)
        else:
            selisih_tp.append((temp_cp - temp_wbiv)/temp_wbiv*100)
            
        # g/l
        g_l.append('{:20,.2f}'.format(round((temp_cp-float(data.average))*data.lot*100,2)))
        
    datastock = zip(datastock, current_price, growth_rate, fut_val, pbv, porto, wbiv, selisih_tp,g_l)
    
    # data_bill = bll_mst_bill_item.objects.filter(validstatus=1)
    context = {
        'title':'H - Expense',
        'dashboard_active':'Account',
        'datastock':list(datastock),
        # 'databill':data_bill
        }
    return render(request, 'account/stockinvestment_view.html', context)

@csrf_protect
def updateprice(request):
    datastock = acc_investment_stock.objects.all()
    for data in datastock:        
        url = f'https://query1.finance.yahoo.com/v8/finance/chart/{data.stock_code}.JK'
        req = urllib.request.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7')
        response = urllib.request.urlopen(req)
        res = response.read()      # a `bytes` object
        html = res.decode('utf-8') # a `str`; this step can't be used if data is binary
        html = json.loads(html)
        temp_cp = html['chart']['result'][0]['meta']['regularMarketPrice']
        data.last_price = temp_cp
        data.last_price_date = datetime.now()
        data.date_modified = data.date_modified
        data.save()
        
    return HttpResponse("Ok")

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

def arliability_view(request):
    
    year = datetime.today().year
    month = datetime.today().month-1
    date = str(year)+"-"+str(month)+"-"+"01"
    total_day = calendar.monthrange(year, month)[1]
    
    data_ar = acc_ar_debt.objects.filter(account_type='AR', account_status='UNPAID', valid_status='VALID')
    data_li = acc_ar_debt.objects.filter(account_type='LIABILITY', account_status='UNPAID', valid_status='VALID')
    data_paid = acc_ar_debt.objects.filter(account_status='PAID', valid_status='VALID')

    context = {
        'title':'H - Account Receivable & Liability',
        'dashboard_active':'Account',
        'dataar':data_ar,
        'datali':data_li,
        'data_paid':data_paid
        }
    return render(request, 'account/arliability_view.html', context)

def arliability_paid(request, id):
    data_debt = acc_ar_debt.objects.filter(id=id).values()
    data_mst = bll_mst_bill_item.objects.filter(id=data_debt[0]['bll_mst_item_id_id'])
    data_last_acc = acc_income_expense.objects.latest('id')
    acc_income_expense.objects.create(
        description=data_mst[0].item_name,  
        amount_out=float(data_debt[0]['amount']), 
        overall_balance=data_last_acc.overall_balance-data_debt[0]['amount'],
        account_type='Cash',
        account_date=datetime.today(),
        bll_mst_item_id=data_mst[0])
    data_debt.update(account_status="PAID")
    return HttpResponse(None)

def cancel_ar(request, id):
    data_bill = acc_ar_debt.objects.filter(id=id)
    data_bill.update(valid_status='INVALID')
    return HttpResponse(None)

@csrf_protect
def saving_goal_tracker_view(request):
    if request.method == 'POST':
        acc_saving_goal_tracker.objects.create(
            goal_name = request.POST['inputGoalName'],
            final_saving_goal = request.POST['inputFinalValue'],
            inflation_rate = request.POST['inputInflationRate'],
            curr_value = request.POST['inputCurrentValue'],
            period_in_year = request.POST['inputPeriod'],
            fund_id = request.POST['inputFundSource']
        )
        return HttpResponseRedirect(reverse('saving_goal_tracker'))

    data_fund = acc_investment_fund.objects.all()
    data_saving = acc_saving_goal_tracker.objects.all()
    fund_val = []
    process_percentage = []
    expected_return = []
    yearly_saving = []
    monthly_saving = []
    
    for data in data_saving:
        fund_data = acc_investment_fund.objects.filter(id=data.fund_id)
        
        if fund_data:
            fund_name = fund_data[0].fund_code
            curr_saving = fund_data[0].average_nav*fund_data[0].unit
            exp_rtn = fund_data[0].exp_return
        else:
            fund_name = "Stock Investment"
            curr_saving = acc_investment_stock.objects.raw("SELECT ID, SUM(LAST_PRICE*LOT) as FUND_VALUE FROM ACC_INVESTMENT_STOCK")[0].FUND_VALUE*100
            exp_rtn = 0.15
        yearly_save = -1*npf.pmt(exp_rtn,data.period_in_year,0,int(data.final_saving_goal))
        
        expected_return.append('{:20,.2f} %'.format(exp_rtn*100))
        yearly_saving.append('Rp. {:20,.2f}'.format(yearly_save))
        monthly_saving.append('Rp. {:20,.2f}'.format(yearly_save/12))
        fund_val.append('Rp. {:20,.2f}'.format(curr_saving))
        process_percentage.append(int(curr_saving/data.final_saving_goal*100))
        data.fund_id = fund_name
        data.inflation_rate = '{:20,.2f} %'.format(data.inflation_rate*100)
        data.final_saving_goal = 'Rp. {:20,.2f}'.format(data.final_saving_goal)
        data.curr_value = 'Rp. {:20,.2f}'.format(data.curr_value)
    
    from copy import deepcopy
    data_target_monthly = zip(data_saving, expected_return, yearly_saving, monthly_saving)
    data_saving = zip(data_saving, fund_val, process_percentage)
    
    context = {
        'title':'H - Fund Tracker',
        'dashboard_active':'Account',
        'data_fund':data_fund,
        'data_saving':data_saving,
        'data_target_monthly':data_target_monthly,
        }
    return render(request, 'account/saving_goal_tracker_view.html', context)

def get_final_goal(request, inflation_rate, period_in_year, current_value):
    final_value = int(-1*npf.fv(rate=float(inflation_rate),pmt=0,nper=period_in_year,pv=current_value))
    return JsonResponse({"final_value":final_value})