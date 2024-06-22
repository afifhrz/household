# engine trading
import json
import http.client
import logging

logger = logging.getLogger(__name__)

def connection_builder(url_link):
    conn = http.client.HTTPSConnection("query1.finance.yahoo.com")
    payload = ''
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:75.0) Gecko/20100101 Firefox/75.0'}
    conn.request("GET", url_link, payload, headers)
    return conn

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

def summary1(daily, previousOpen = None, test = False):
    result = {}

    if not test:
        closing_all_daily = daily['chart']['result'][0]['indicators']['quote'][0]['close']
        result['last_open'] = daily['chart']['result'][0]['indicators']['quote'][0]['open'][-1]
    else:
        closing_all_daily = daily
        result['last_open'] = previousOpen[-1]

    
    result['last_price'] = closing_all_daily[-1] 
    daily_len = [3,5,8,13,18,50,100,200]
    
    for i in daily_len:
        result["ma_d_"+str(i)] = int(sum(closing_all_daily[-1*i:])/len(closing_all_daily[-1*i:]))
    
    return result

def check_signal_buy(data, prev_data, owned=False, buy_price = 1):
    CLOSE_PERCENTAGE_MA100_200_CONSTANT = 0.025
    CLOSE_PERCENTAGE_CONSTANT = 0.05
    PRICE_ADMIN_BUY = 0.0019
    PRICE_ADMIN_SELL = 0.0029
    TAKE_PROFIT_PERCENTAGE = PRICE_ADMIN_BUY + PRICE_ADMIN_SELL
    CUTLOSS_PERCENTAGE = 0.075

    if owned:
        if abs(data['last_price'] - buy_price)/buy_price >= TAKE_PROFIT_PERCENTAGE and data['last_price'] > buy_price:
            if prev_data['ma_d_18'] < prev_data['ma_d_5'] and data['ma_d_18'] > data['ma_d_5']:
                return "SELL_TAKEPROFIT_CROSS"
            elif abs(data['last_price'] - buy_price)/buy_price >= CUTLOSS_PERCENTAGE and data['last_price'] > buy_price:
                return "SELL_TAKEPROFIT"
            else:
                return "HOLD"
        elif abs(data['last_price'] - buy_price)/buy_price >= CUTLOSS_PERCENTAGE and data['last_price'] < buy_price:
            return "SELL_CUTLOSS"
        else:
            return "HOLD"
    
    if \
        abs(data['ma_d_200'] - data['last_price'])/data['last_price'] <= CLOSE_PERCENTAGE_MA100_200_CONSTANT and \
        abs(data['ma_d_100'] - data['last_price'])/data['last_price'] <= CLOSE_PERCENTAGE_MA100_200_CONSTANT and \
        abs(data['ma_d_50'] - data['last_price'])/data['last_price'] <= CLOSE_PERCENTAGE_CONSTANT and \
        abs(data['ma_d_18'] - data['last_price'])/data['last_price'] <= CLOSE_PERCENTAGE_CONSTANT and \
        abs(data['ma_d_8'] - data['last_price'])/data['last_price'] <= CLOSE_PERCENTAGE_CONSTANT and \
        abs(data['ma_d_3'] - data['last_price'])/data['last_price'] <= CLOSE_PERCENTAGE_CONSTANT and \
        \
        data['ma_d_3'] >= data['ma_d_18'] and \
        \
        data['last_price'] >= data['ma_d_200'] and \
        data['last_price'] >= data['ma_d_100'] and \
        data['last_price'] >= data['ma_d_50'] and \
        data['last_price'] >= data['ma_d_18'] and \
        data['last_price'] >= data['ma_d_8'] and \
        data['last_price'] >= data['ma_d_3']:
        return "THEONE"
    # SIGNAL BUY_FAST -> BUY IF PRICE UPPER THAN MA 200 AND WHEN MA D 3 CROSS MA_D 18,UPPER ALL OTHER MA W and MA M
    # elif prev_data['ma_d_50'] > prev_data['ma_d_3'] and \
    #     data['ma_d_50'] < data['ma_d_3'] and \
    #     data['last_price'] > data['ma_d_200'] and \
    #     data['last_price'] > data['ma_d_100'] and \
    #     data['last_price'] > data['ma_d_50']:
    #     return "BUY_FAST"
    # SIGNAL WATCHLIST -> PRICE LOWER THAN MA 18
    elif abs(data['ma_d_18'] - data['last_price'])/data['last_price'] <= .0275:
        if abs(data['ma_d_3'] - data['ma_d_200'])/data['ma_d_3'] <= .0275:
            return "WATCHLIST_KETAT"
        elif abs(data['ma_d_18'] - data['ma_d_3'])/data['ma_d_18'] <= .0275:
            return "WATCHLIST_WEEKLY"
        else:
            return "WATCHLIST"
    elif data['last_price'] >= prev_data['last_open']:
        return "UPTREND"
    elif data['last_price'] < prev_data['last_open']:
        return "DOWNTREND"
    
    if owned:
        pass  
    # SIGNAL SELL_TAKEPROFIT_14 -> SELL IF GAIN 14%
    # SIGNAL SELL_CUTTING_LOSS -> SELL IF LOSS 3%

def trading_engine(code, prev_data):
    conn = connection_builder(f"/v8/finance/chart/{code}.JK?interval=1d&range=1y")
    res = conn.getresponse()
    data = res.read()
    logger.debug(f"trading_engine response data: {data}")
    data = json.loads(data.decode("utf-8"))
    summary_data = summary1(data)
    return check_signal_buy(summary_data, prev_data), summary_data

def get_data_prev(code, epoch):
    conn = connection_builder(f"/v8/finance/chart/{code}.JK?interval=1d&period2={epoch}")
    res = conn.getresponse()
    data = res.read()
    data = json.loads(data.decode("utf-8"))
    summary_data = summary1(data)
    return summary_data

def get2ydata(code):
    conn = connection_builder(f"/v8/finance/chart/{code}.JK?interval=1d&range=2y")
    res = conn.getresponse()
    data = res.read()
    data = json.loads(data.decode("utf-8"))
    return data