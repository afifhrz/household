from django.shortcuts import render
from django.urls import reverse
from .engine_trading import trading_engine, get_data_prev
from tradingstock.models import trd_mst_stock, trd_filtered_stock, trd_trx_stock
from django.http import HttpResponse, HttpResponseRedirect
import json
import time as tm
from datetime import datetime, date, time
from django.forms.models import model_to_dict
from dateutil.relativedelta import relativedelta
from django.views.decorators.csrf import csrf_protect

# Create your views here.
def run_filter(request):
    datamst = trd_mst_stock.objects.filter(valid_status=1).order_by('stock_code')
    # response_data = trd_filtered_stock.objects.filter(mst_id=datamst[0]).order_by('-date_modified')[0]
    # dict_obj = model_to_dict( response_data )
    # dict_obj['date_modified'] = dict_obj['date_modified'].strftime("%Y-%m-%d %H:%M:%S")
    # return HttpResponse(json.dumps(dict_obj), content_type="application/json")
    response_data = {}
    pub_date = date.today()
    min_pub_date_time = datetime.combine(pub_date, time.min) 
    
    for data in datamst:
        response_data[data.stock_code] = {}
        
        prev_data = trd_filtered_stock.objects.filter(mst_id=data, date_modified__lt=min_pub_date_time).order_by('-date_modified')
        
        if not prev_data:
            public_date = date.today()
            public_date = datetime.combine(public_date, time.min) - relativedelta(hours=7)
            epoch = int(tm.mktime(public_date.timetuple()))
            prev_data = get_data_prev(data.stock_code, epoch)
        else:
            prev_data = prev_data[0]
            prev_data = model_to_dict(prev_data)
        
        response_data[data.stock_code]['status'],response_data[data.stock_code]['summary'] = trading_engine(data.stock_code, prev_data)
        new_data = trd_filtered_stock.objects.create(
            mst_id = data,
            date_modified = datetime.today(),
            last_price = response_data[data.stock_code]['summary']['last_price'],
            last_open = response_data[data.stock_code]['summary']['last_open'],
            ma_d_3 = response_data[data.stock_code]['summary']['ma_d_3'],
            ma_d_5 = response_data[data.stock_code]['summary']['ma_d_5'],
            ma_d_7 = response_data[data.stock_code]['summary']['ma_d_7'],
            ma_d_10 = response_data[data.stock_code]['summary']['ma_d_10'],
            ma_d_14 = response_data[data.stock_code]['summary']['ma_d_14'],
            ma_d_18 = response_data[data.stock_code]['summary']['ma_d_18'],
            ma_d_50 = response_data[data.stock_code]['summary']['ma_d_50'],
            ma_d_100 = response_data[data.stock_code]['summary']['ma_d_100'],
            ma_d_200 = response_data[data.stock_code]['summary']['ma_d_200'],
            status = response_data[data.stock_code]['status'],
        )
        new_data.save()
        
        tm.sleep(0.5)
    return HttpResponse(json.dumps(response_data), content_type="application/json")

def last_filter(request):
    public_date = date.today()
    public_date = datetime.combine(public_date, time.min) - relativedelta(days=1)
    datafilter = trd_filtered_stock.objects.filter(date_modified__gt=public_date)
    
    if not datafilter:
        public_date = date.today()
        public_date = datetime.combine(public_date, time.min) - relativedelta(days=2)
        datafilter = trd_filtered_stock.objects.filter(date_modified__gt=public_date)
    
    if not datafilter:
        public_date = date.today()
        public_date = datetime.combine(public_date, time.min) - relativedelta(days=3)
        datafilter = trd_filtered_stock.objects.filter(date_modified__gt=public_date)
    
    datafilter = datafilter.order_by('-status')
    
    response_data = {}
    for data in datafilter:
        response_data[data.mst_id.stock_code] =  model_to_dict(data)
        response_data[data.mst_id.stock_code]['date_modified'] = response_data[data.mst_id.stock_code]['date_modified'].strftime("%Y-%m-%d %H:%M:%S")

    return HttpResponse(json.dumps(response_data), content_type="application/json")

@csrf_protect
def createtransactionstock(request):
    if request.method == "POST":
        if request.POST['InputConditionTransaction'] == "sell":
            amount = float(request.POST['inputAmount'])*0.9971
        else:
            amount = float(request.POST['inputAmount'])*-1*1.0019
            
        mst = trd_mst_stock(id=request.POST['inputStockId'])
        trx =trd_trx_stock(
            mst_id = mst,
            lot = request.POST['inputLot'],
            price = request.POST['inputPrice'],
            amount = amount,
        )
        trx.save()
        return HttpResponseRedirect(reverse('createtransactionstock'))
    datamst = trd_mst_stock.objects.all()
    datatrading = trd_trx_stock.objects.all()
    summary = 0
    for data in datatrading:
        summary+=data.amount
    summary = int(summary)    
    
    context = {
        'title':'H - Trading Info',
        'dashboard_active':'Trading',
        'datamst':datamst,
        'datatrading':datatrading,
        'summary':summary
        }
    return render(request, 'tradingstock/createtransactionstock_view.html', context)