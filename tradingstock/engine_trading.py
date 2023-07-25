# engine trading
import json
import http.client

def summary(daily, weekly, monthly):
    closing_all_daily = daily['chart']['result'][0]['indicators']['quote'][0]['close']
    closing_all_weekly = weekly['chart']['result'][0]['indicators']['quote'][0]['close']
    closing_all_monthly = monthly['chart']['result'][0]['indicators']['quote'][0]['close']
    
    result = {}
    result['last_price'] = closing_all_daily[-1]
    daily_len = [3,5,7,10,14,18,50,100,200]
    weekly_len = {50,100,200}
    monthly_len = {50,100}
    
    for i in daily_len:
        result["ma_d_"+str(i)] = int(sum(closing_all_daily[-1*i:])/len(closing_all_daily[-1*i:]))
        
    for i in weekly_len:
        result["ma_w_"+str(i)] = int(sum(closing_all_weekly[-1*i:])/len(closing_all_weekly[-1*i:]))
    
    for i in monthly_len:
        result["ma_m_"+str(i)] = int(sum(closing_all_monthly[-1*i:])/len(closing_all_monthly[-1*i:]))
    
    return result

def summary1(daily):
    closing_all_daily = daily['chart']['result'][0]['indicators']['quote'][0]['close']
    
    result = {}
    result['last_price'] = closing_all_daily[-1]
    result['last_open'] = daily['chart']['result'][0]['indicators']['quote'][0]['open'][-1]
    daily_len = [3,5,7,10,14,18,50,100,200]
    
    for i in daily_len:
        result["ma_d_"+str(i)] = int(sum(closing_all_daily[-1*i:])/len(closing_all_daily[-1*i:]))
    
    return result

def check_signal_buy(data, prev_data, owned=False):
    
    if owned:
        # SIGNAL SELL_TAKEPROFIT_CROSS -> SELL IF MA D 3 cross 18
        if prev_data['ma_d_18'] < prev_data['ma_d_3'] and data['ma_d_18'] >= data['ma_d_3']:
            return "SELL_TAKEPROFIT_CROSS"
    
    # SIGNAL BUY_SLOW -> THEONE -> BUY IF PRICE LOWER THAN MA 18 AND WHEN MA D 3 CROSS MA_D 18 AND LOWER THAN MA D 200
    if prev_data['ma_d_18'] > prev_data['ma_d_3'] and data['ma_d_18'] <= data['ma_d_3'] and data['last_price'] <= data['ma_d_200']:
        return "THEONE"
    # SIGNAL BUY_FAST -> BUY IF PRICE UPPER THAN MA 200 AND WHEN MA D 3 CROSS MA_D 18,UPPER ALL OTHER MA W and MA M
    elif prev_data['ma_d_18'] > prev_data['ma_d_3'] and (data['ma_d_18'] <= data['ma_d_3']) and data['last_price'] > data['ma_d_200']:
        return "BUY_FAST"
    # SIGNAL WATCHLIST -> PRICE LOWER THAN MA 18
    elif abs(data['ma_d_18'] - data['last_price'])/data['last_price'] <= .0275:
        return "WATCHLIST"
    # elif data['last_price'] >= data['ma_d_7'] and data['ma_d_3'] >= data['ma_d_14'] and data['ma_d_18'] >= data['ma_d_50']:
    elif data['last_price'] >= prev_data['last_open']:
        return "UPTREND"
    # elif data['last_price'] <= data['ma_d_7'] and data['ma_d_3'] <= data['ma_d_14']:
    elif data['last_price'] < prev_data['last_open']:
        return "DOWNTREND"
    
    if owned:
        pass  
    # SIGNAL SELL_TAKEPROFIT_14 -> SELL IF GAIN 14%
    # SIGNAL SELL_CUTTING_LOSS -> SELL IF LOSS 3%

def trading_engine(code, prev_data):
    conn = http.client.HTTPSConnection("query1.finance.yahoo.com")
    payload = ''
    headers = {}
    conn.request("GET", f"/v8/finance/chart/{code}.JK?interval=1d&range=1y", payload, headers)
    res = conn.getresponse()
    data = res.read()
    data = json.loads(data.decode("utf-8"))
    summary_data = summary1(data)
    return check_signal_buy(summary_data, prev_data), summary_data

def get_data_prev(code, epoch):
    conn = http.client.HTTPSConnection("query1.finance.yahoo.com")
    payload = ''
    headers = {}
    conn.request("GET", f"/v8/finance/chart/{code}.JK?interval=1d&period2={epoch}", payload, headers)
    res = conn.getresponse()
    data = res.read()
    data = json.loads(data.decode("utf-8"))
    summary_data = summary1(data)
    return summary_data