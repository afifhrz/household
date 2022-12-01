import datetime
import calendar
from django.shortcuts import render
from dashboard.models import admin_mst_module
from account.models import acc_income_expense, acc_investment_stock, acc_investment_fund, acc_ar_debt, acc_investment_deposit
from django.db import connection
import requests
import urllib
import json

# Create your views here.
def index(request):

    data = {}
    year = datetime.datetime.today().year
    month = datetime.datetime.today().month
    date = str(year)+"-"+str(month)+"-"+"01"
    total_day = calendar.monthrange(year, month)[1]
    enddate = str(year)+"-"+str(month)+"-"+ str(total_day)
    
    # data balance
    data['month_sale']=acc_income_expense.objects.raw(f'''SELECT ID, SUM(AMOUNT_IN) MONTH_SALE FROM ACC_INC_EXP WHERE BLL_MST_BILL_ITEM_ID = 1 AND ACCOUNT_DATE >= "{date}"''')[0]
    data['profit_investment']=0
    data['month_expense']=acc_income_expense.objects.raw(f'''SELECT ID, SUM(AMOUNT_OUT) MONTH_EXPENSE FROM ACC_INC_EXP WHERE BLL_MST_BILL_ITEM_ID NOT IN  (1,3,6) AND ACCOUNT_DATE >= "{date}" AND ACCOUNT_DATE <= "{enddate} 23:59:59"''')[0]
    data['overall_balance']=acc_income_expense.objects.raw(f'''SELECT ID, OVERALL_BALANCE FROM ACC_INC_EXP ORDER BY id desc LIMIT 1''')[0]

    # data expense chart
    
    cursor = connection.cursor()
    category = list(cursor.execute("""select DISTINCT case
		when BLL_MST_BILL_ITEM_ID in (1,6) then 'INCOME'
		when BLL_MST_BILL_ITEM_ID in (3,18) then 'OPS-INCOME'
		when BLL_MST_BILL_ITEM_ID in (2,7,8,9,11,17) then 'MONTHLY-EXPENSE'
		when BLL_MST_BILL_ITEM_ID in (4) then 'EMERGENCY FUND'
		when BLL_MST_BILL_ITEM_ID in (5,12,13) then 'SECONDARY NEED'
		when BLL_MST_BILL_ITEM_ID in (10) then 'CHARITY'
		else 'UNDEFINED'
	end as category from ACC_INC_EXP aie"""))
    
    data_chart = []
    for row in category:
        data_chart.append(list(cursor.execute(f"""select
	case
		when BLL_MST_BILL_ITEM_ID in (1,6) then 'INCOME'
		when BLL_MST_BILL_ITEM_ID in (3,18) then 'OPS-INCOME'
		when BLL_MST_BILL_ITEM_ID in (2,7,8,9,11,17) then 'MONTHLY-EXPENSE'
		when BLL_MST_BILL_ITEM_ID in (4) then 'EMERGENCY FUND'
		when BLL_MST_BILL_ITEM_ID in (5,12,13) then 'SECONDARY NEED'
		when BLL_MST_BILL_ITEM_ID in (10) then 'CHARITY'
		else 'UNDEFINED'
	end as category,
	IFNULL(SUM(AMOUNT_IN),0) + IFNULL(SUM(AMOUNT_OUT),0) as AMOUNT,
       strftime("%m-%Y", ACCOUNT_DATE) as 'month_year' 
       from ACC_INC_EXP
    where category = '{row[0]}'
    group by strftime("%m-%Y", ACCOUNT_DATE), category ;""")))   
        
    date = list(cursor.execute("""select DISTINCT strftime("%m-%Y", ACCOUNT_DATE) as 'month_year' from ACC_INC_EXP"""))
    
    final_data = []
    for cat in data_chart:
        temp_data_chart = []
        for tanggal in date:
            status = False
            for item in cat:
                if item[2] == tanggal[0]:
                    temp_data_chart.append(item[1])
                    status = True
                    break
            if status == False:
                temp_data_chart.append(0)
        final_data.append(temp_data_chart)    
    
    color =[
        (155, 95, 224),
        (22, 164, 216),
        (96, 219, 232),
        (139, 211, 70),
        (239, 223, 72),
        (249, 165, 44),
        (214, 78, 18)
    ]
    color = color[:len(category)]
    final_data = zip(category, final_data, color)    
    
    expense_chart = {
        'label': date,
        'data':final_data
    }
    
    # data sales chart
    sales_chart = acc_income_expense.objects.raw("""select ID,
	SUM(AMOUNT_IN) REVENUE,
	IFNULL(SUM(AMOUNT_OUT),0) EXPENSE,
	IFNULL((SUM(AMOUNT_IN) - SUM(AMOUNT_OUT)),0) as NET_PROFIT,
       strftime("%m-%Y", ACCOUNT_DATE) as 'month_year' 
       from ACC_INC_EXP group by strftime("%m-%Y", ACCOUNT_DATE);""")

    # liabilities, ar, short_inv
    ar_data = {}
    ar_data['liabilities'] = float(acc_ar_debt.objects.raw("SELECT ID, IFNULL(SUM(AMOUNT),0) total_amount FROM ACC_AR_DEBT WHERE ACCOUNT_STATUS = 'UNPAID' AND ACCOUNT_TYPE='LIABILITY' ")[0].total_amount)
    ar_data['ar'] = float(acc_ar_debt.objects.raw("SELECT ID, IFNULL(SUM(AMOUNT),0) total_amount FROM ACC_AR_DEBT WHERE ACCOUNT_STATUS = 'UNPAID' AND ACCOUNT_TYPE='AR' ")[0].total_amount)
    total_cash = float(data['overall_balance'].overall_balance) - ar_data['liabilities'] + ar_data['ar']
    ar_data['emergency_fund'] = total_cash
    ar_data['short'] = total_cash-(3*6541666.67)
	
    
    # data asset
    asset = {}
    
    datastock = acc_investment_stock.objects.all()
    total_price = 0
    avg_price = 0
    for item in datastock:
        #current price
        url = f'https://query1.finance.yahoo.com/v8/finance/chart/{item.stock_code}.JK'

        req = urllib.request.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7')
        response = urllib.request.urlopen(req)
        res = response.read()      # a `bytes` object
        html = res.decode('utf-8') # a `str`; this step can't be used if data is binary
        html = json.loads(html)
        total_price += html['chart']['result'][0]['meta']['regularMarketPrice']*item.lot*100
        avg_price += item.lot*item.average*100
    asset['stock_inv'] = total_price
    asset['stock_percentage'] = (asset['stock_inv']-float(avg_price))/float(avg_price)*100

    asset['fund_inv'] = acc_investment_fund.objects.raw("SELECT ID, round(SUM(CURRENT_NAV*UNIT)-(select (20000000 + (CURRENT_NAV-1224.21) * 16337.0663) from ACC_INVESTMENT_FUND aif where id = 2),2) total_fund from ACC_INVESTMENT_FUND aif")[0]
    
    url = "https://data-asg.goldprice.org/dbXRates/IDR"
    req = urllib.request.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7')
    response = urllib.request.urlopen(req)
    res = response.read()      # a `bytes` object
    html = json.loads(res)
    gold_price = html['items'][0]['xauPrice']    
    asset['gold_inv'] = round(gold_price/31.06778927*5,2)

    asset['gold_percentage'] = round((asset['gold_inv']-5*800000)/(5*800000)*100,2)    
    asset['total_asset'] = float(total_cash) + float(asset['fund_inv'].total_fund) + asset['stock_inv'] + asset['gold_inv']
    
    modal = acc_investment_deposit.objects.raw("select id, sum(amount) as total_modal from acc_investment_deposit")[0]
    data['profit_investment'] = round(-float(modal.total_modal) + (float(asset['fund_inv'].total_fund) + asset['stock_inv']),2)
    data['profit_percentage'] = round(data['profit_investment']/modal.total_modal*100,2)
    
    context = {
        'title':'Dashboard Edumin',
        'dashboard_active':'Dashboard',
        'data':data,
        'ar_data':ar_data,
        'asset':asset,
        'sales':sales_chart,
        'expense':expense_chart
    }
    return render(request, 'dashboard/index.html', context)

# from django.conf import settings
# from django.shortcuts import redirect
 
# def error_404_view(request, exception):
#     context = {}
#     # we add the path to the the 404.html file
#     # here. The name of our HTML file is 404.html
#     return render(request, '404.html', context)