from django.shortcuts import render
from .engine_trading import trading_engine, get_data_prev
from tradingstock.models import trd_mst_stock, trd_filtered_stock
from django.http import HttpResponse
import json
import time as tm
from datetime import datetime, date, time
from django.forms.models import model_to_dict
from dateutil.relativedelta import relativedelta

# assuming obj is your model instance


# Create your views here.
def run_filter(request):
    datamst = trd_mst_stock.objects.filter(valid_status=1)
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