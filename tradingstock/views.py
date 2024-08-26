from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone as tz
from .engine_trading import trading_engine, get_data_prev, get2ydata
from .test_engine import *
from tradingstock.models import trd_mst_stock, trd_filtered_stock, trd_trx_stock
from account.views import inputNewInvestmentStock
from django.http import HttpResponse, HttpResponseRedirect
import json
import time as tm
from datetime import datetime, date, time
from django.forms.models import model_to_dict
from dateutil.relativedelta import relativedelta
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
import logging
import random
import asyncio
from .tele import Tele

logger = logging.getLogger(__name__)

# Create your views here.
def run_filter(request):
    if date.today().strftime("%A") == "Saturday" or date.today().strftime("%A") == "Friday":
        return HttpResponse(json.dumps({}), content_type="application/json")
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
            tm.sleep(0.1)
        else:
            prev_data = prev_data[0]
            prev_data = model_to_dict(prev_data)
        # logger.debug(f"This is prev data: {prev_data}")
        
        response_data[data.stock_code]['status'],response_data[data.stock_code]['summary'] = trading_engine(data.stock_code, prev_data, data.owned, data.buy_price)
        tm.sleep(0.1)
        new_data = trd_filtered_stock.objects.create(
            mst_id = data,
            date_modified = tz.now(),
            last_price = response_data[data.stock_code]['summary']['last_price'],
            last_open = response_data[data.stock_code]['summary']['last_open'],
            ma_d_3 = response_data[data.stock_code]['summary']['ma_d_3'],
            ma_d_5 = response_data[data.stock_code]['summary']['ma_d_5'],
            ma_d_7 = response_data[data.stock_code]['summary']['ma_d_8'],
            ma_d_10 = response_data[data.stock_code]['summary']['ma_d_13'],
            ma_d_14 = response_data[data.stock_code]['summary']['ma_d_13'],
            ma_d_18 = response_data[data.stock_code]['summary']['ma_d_18'],
            ma_d_50 = response_data[data.stock_code]['summary']['ma_d_50'],
            ma_d_100 = response_data[data.stock_code]['summary']['ma_d_100'],
            ma_d_200 = response_data[data.stock_code]['summary']['ma_d_200'],
            status = response_data[data.stock_code]['status'],
        )
        new_data.save()
        
        tm.sleep(0.5)

    teleResponse = {"datetime":str(date.today())}
    for key in response_data:
        if response_data[key]["status"] == "THEONE" or \
            response_data[key]["status"] == "SELL_TAKEPROFIT_CROSS" or \
                response_data[key]["status"] == "SELL_CUTLOSS" or \
                    response_data[key]["status"] == "SELL_TAKEPROFIT":
                        teleResponse[key] = response_data[key]
            
    oke = Tele()
    try:
        asyncio.run(oke.sendMessage(json.dumps(teleResponse, indent=4)))
    except Exception as e:
        print(e)
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
    
    teleResponse = {"datetime":str(date.today())}
    for key in response_data:
        if response_data[key]["status"] == "THEONE" or \
            response_data[key]["status"] == "SELL_TAKEPROFIT_CROSS" or \
                response_data[key]["status"] == "SELL_CUTLOSS" or \
                    response_data[key]["status"] == "SELL_TAKEPROFIT":
                        teleResponse[key] = response_data[key]
            
    oke = Tele()
    try:
        asyncio.run(oke.sendMessage(json.dumps(teleResponse, indent=4)))
    except Exception as e:
        print(e)

    return HttpResponse(json.dumps(response_data), content_type="application/json")

def test_engine(request):
    # get query string
    stock_code = request.GET.get('stockCode',None)
    datamst = trd_mst_stock.objects.filter(valid_status=1).order_by('stock_code')
    if stock_code == None:
        stock = random.choice(datamst)
        stock_code = stock.stock_code
    data = get2ydata(stock_code)
    
    dataCloseRaw = data['chart']['result'][0]['indicators']['quote'][0]['close']
    dataOpenRaw = data['chart']['result'][0]['indicators']['quote'][0]['open']
    timestamp = data['chart']['result'][0]['timestamp']

    result = main_test_engine(stock_code, dataCloseRaw, dataOpenRaw, timestamp)
    return HttpResponse(json.dumps(result), content_type="application/json")

def test_engine_many(request):
    # get query string
    count = int(request.GET.get('count',10))
    details = []
    sum_percentage = 0
    sum_amount = 0

    for i in range(count):
        datamst = trd_mst_stock.objects.filter(valid_status=1).order_by('stock_code')
        stock = random.choice(datamst)
        stock_code = stock.stock_code
        data = get2ydata(stock_code)
        
        dataCloseRaw = data['chart']['result'][0]['indicators']['quote'][0]['close']
        dataOpenRaw = data['chart']['result'][0]['indicators']['quote'][0]['open']
        timestamp = data['chart']['result'][0]['timestamp']

        result = main_test_engine(stock_code, dataCloseRaw, dataOpenRaw, timestamp)
        details.append(result)
        sum_percentage += result['gain/loss']
        sum_amount += result["startbalance"] * result['gain/loss']
        tm.sleep(0.5)
    
    result = {
        "count": count,
        "gain-loss-percentage": sum_percentage,
        "gain-loss-amount": sum_amount,
        "details": details
    }

    return HttpResponse(json.dumps(result), content_type="application/json")

@csrf_protect
@login_required(login_url='/login')
def createtransactionstock(request):
    if request.method == "POST":
        mst = trd_mst_stock(id=request.POST['inputStockId'])

        if request.POST['InputConditionTransaction'] == "sell":
            amount = float(request.POST['inputAmount'])*0.9971
            inputLot = request.POST['inputLot']*-1
            mst.buy_price = 0
            mst.owned = False
        else:
            amount = float(request.POST['inputAmount'])*-1*1.0019
            mst.buy_price = request.POST['inputPrice']
            mst.owned = True
            inputLot = request.POST['inputLot']
        
        trx = trd_trx_stock(
            mst_id = mst,
            lot = request.POST['inputLot'],
            price = request.POST['inputPrice'],
            amount = amount,
            is_last_transaction = mst.owned
        )
        trx.save()
        mst.save(update_fields=["buy_price", "owned"])
        inputNewInvestmentStock(mst.stock_code, inputLot, request.POST['averagePrice'])
        
        return HttpResponseRedirect(reverse('createtransactionstock'))
    datamst = trd_mst_stock.objects.all()
    datatrading = trd_trx_stock.objects.all()
    currenttrading = trd_mst_stock.objects.raw("""
        SELECT tms.id, CODE, trs.LOT, trs.PRICE, trs.AMOUNT, ais.LAST_PRICE
            FROM TRD_MST_STOCK as tms
            LEFT JOIN TRD_TRX_STOCK as trs on trs.TRD_MST_STOCK = tms.id
            LEFT JOIN ACC_INVESTMENT_STOCK ais on ais.STOCKS = tms.CODE
            WHERE tms.OWNED = 1
            AND trs.IS_LAST_TRANSACTION = 1
    """)
    summary = 0
    for data in datatrading:
        summary+=data.amount
    summary = int(summary)

    unrealize_gain_loss = 0
    for data in currenttrading:
        unrealize_gain_loss+=data.LAST_PRICE*data.LOT*100
    unrealize_gain_loss = unrealize_gain_loss + summary
    
    context = {
        'title':'H - Create Trading Transaction',
        'dashboard_active':'Trading',
        'datamst':datamst,
        'datatrading':datatrading,
        'summary':summary,
        'unrealize_gain_loss':unrealize_gain_loss,
        'currenttrading':currenttrading
        }
    return render(request, 'tradingstock/createtransactionstock_view.html', context)