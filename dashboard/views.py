import datetime
import calendar
import urllib
import json

from django.shortcuts import render
from account.models import acc_income_expense, acc_investment_stock, acc_investment_fund, acc_ar_debt, acc_investment_deposit
from django.db import connection
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required(login_url='/login')
def index(request):

    month_of_emergency = 3
    data = {}
    year = datetime.datetime.today().year
    month = datetime.datetime.today().month
    total_day = calendar.monthrange(year, month)[1]
    if len(str(month)) < 2:
        date = str(year)+"-"+'0'+str(month)+"-"+"01"
        enddate = str(year)+"-"+'0'+str(month)+"-"+ str(total_day)
    else:
        date = str(year)+"-"+str(month)+"-"+"01"
        enddate = str(year)+"-"+str(month)+"-"+ str(total_day)
    
    
    # data balance
    data['month_sale']=acc_income_expense.objects.raw(f'''SELECT id, SUM(AMOUNT_IN) MONTH_SALE FROM ACC_INC_EXP WHERE BLL_MST_BILL_ITEM_ID = 1 AND ACCOUNT_DATE >= "{date}"''')[0]
    data['profit_investment']=0
    data['month_expense']=acc_income_expense.objects.raw(f'''SELECT id, SUM(AMOUNT_OUT) MONTH_EXPENSE FROM ACC_INC_EXP WHERE BLL_MST_BILL_ITEM_ID NOT IN  (1,6) AND ACCOUNT_DATE >= "{date}" AND ACCOUNT_DATE <= "{enddate} 23:59:59"''')[0]
    data['overall_balance']=acc_income_expense.objects.raw(f'''SELECT id, OVERALL_BALANCE FROM ACC_INC_EXP ORDER BY id desc LIMIT 1''')[0]

    # data expense chart
    cursor = connection.cursor()
    cursor.execute("""select DISTINCT case
		when BLL_MST_BILL_ITEM_ID in (7,8,11) then 'FIXED-EXPENSE'
		when BLL_MST_BILL_ITEM_ID in (2, 16, 17) then 'MONTHLY-EXPENSE'
		when BLL_MST_BILL_ITEM_ID in (9) then 'LAUNDRY'
		when BLL_MST_BILL_ITEM_ID in (4) then 'EMERGENCY EXPENSE'
		when BLL_MST_BILL_ITEM_ID in (5) then 'SECONDARY NEED'
		when BLL_MST_BILL_ITEM_ID in (12, 20) then 'DINING OUT - VACATION'
		when BLL_MST_BILL_ITEM_ID in (10) then 'CHARITY'
		when BLL_MST_BILL_ITEM_ID in (14, 19) then 'INVESTMENT'
	end as category from ACC_INC_EXP aie order by category""")
    category = list(cursor.fetchall())
    category = category[1:]
    
    data_chart = []
    counter = 0
    for row in category:
        cursor.execute(
            f"""SELECT * FROM
            (select
                case
                    when BLL_MST_BILL_ITEM_ID in (7,8,11) then 'FIXED-EXPENSE'
                    when BLL_MST_BILL_ITEM_ID in (2, 16, 17) then 'MONTHLY-EXPENSE'
                    when BLL_MST_BILL_ITEM_ID in (9) then 'LAUNDRY'
                    when BLL_MST_BILL_ITEM_ID in (4) then 'EMERGENCY EXPENSE'
                    when BLL_MST_BILL_ITEM_ID in (5) then 'SECONDARY NEED'
                    when BLL_MST_BILL_ITEM_ID in (12, 20) then 'DINING OUT - VACATION'
                    when BLL_MST_BILL_ITEM_ID in (10) then 'CHARITY'
                    when BLL_MST_BILL_ITEM_ID in (14, 19) then 'INVESTMENT'
                end as category,
                IFNULL(SUM(AMOUNT_OUT),0) as AMOUNT,
                DATE_FORMAT(ACCOUNT_DATE, "%m-%Y") as 'month_year' 
                FROM ACC_INC_EXP
                group by DATE_FORMAT(ACCOUNT_DATE, "%m-%Y"), category
                order by ACCOUNT_DATE)
            as tabel1
            where category = '{row[0]}';""")
        result = list(cursor.fetchall())
        
        if counter==6:
            data_chart.append(result[len_temp:len(data_chart[3])+1])   
        elif counter==3:
            len_temp = len(result) - len(result[-12:])
            data_chart.append(result[-12:])
        else:
            data_chart.append(result[-12:])
            
        counter+=1
    cursor.execute("""select DISTINCT DATE_FORMAT(ACCOUNT_DATE, "%m-%Y") as 'month_year' from ACC_INC_EXP order by ACCOUNT_DATE""")
    date = list(cursor.fetchall())[len_temp:len(data_chart[3])+1]
    
    final_data = []
    for cat in data_chart:
        temp_data_chart = []
        for tanggal in date:
            status = False
            for item in cat:
                if item[2] == tanggal[0]:
                    temp_data_chart.append(float(item[1]))
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
        (214, 78, 18),
        (300, 300, 100)
    ]
    color = color[:len(category)]
    final_data = zip(category, final_data, color)    
    
    expense_chart = {
        'label': date,
        'data':final_data
    }
    
    # data sales chart
    dateIn = ""
    for item in date:
        dateIn+="'"+item[0]+"',"
    dateIn = dateIn[:-1]
    cursor.execute(
        f"""SELECT * FROM 
        (select id,
            SUM(AMOUNT_IN) REVENUE,
            IFNULL(SUM(AMOUNT_OUT),0) EXPENSE,
            IFNULL((SUM(AMOUNT_IN) - SUM(AMOUNT_OUT)),0) as NET_PROFIT,
            DATE_FORMAT(ACCOUNT_DATE, "%m-%Y") as 'month_year' 
            from ACC_INC_EXP 
            group by DATE_FORMAT(ACCOUNT_DATE, "%m-%Y")
            order by ACCOUNT_DATE)
        as tabel1
        where month_year IN ({dateIn});""")
    sales_chart = cursor.fetchall()

    cursor.execute(
        f"""SELECT * FROM 
            (
                select 	id,
                SUM(AMOUNT_OUT) EXPENSE,
                DATE_FORMAT(ACCOUNT_DATE, "%m-%Y") as 'month_year' 
                from ACC_INC_EXP 
                WHERE BLL_MST_BILL_ITEM_ID IN (7,8,11,2,16,17)
                group by DATE_FORMAT(ACCOUNT_DATE, "%m-%Y")
                order by ACCOUNT_DATE
            )
        as tabel1
        where month_year IN ({dateIn});"""
        )
    data_average = cursor.fetchall()
    data_average_expense = []
    sum_data = 0
    for data_amount_out in data_average:
        sum_data += float(data_amount_out[1])
    avg = sum_data//len(data_average)
    for data_amount_out in data_average:
        data_average_expense.append(avg) 

    # liabilities, ar, short_inv
    ar_data = {}
    ar_data['liabilities'] = float(acc_ar_debt.objects.raw("SELECT id, IFNULL(SUM(AMOUNT),0) total_amount FROM ACC_AR_DEBT WHERE ACCOUNT_STATUS = 'UNPAID' AND ACCOUNT_TYPE='LIABILITY' ")[0].total_amount)
    ar_data['ar'] = float(acc_ar_debt.objects.raw("SELECT id, IFNULL(SUM(AMOUNT),0) total_amount FROM ACC_AR_DEBT WHERE ACCOUNT_STATUS = 'UNPAID' AND ACCOUNT_TYPE='AR' AND VALID_STATUS = 'VALID' ")[0].total_amount)
    total_cash = float(data['overall_balance'].overall_balance) - ar_data['liabilities'] + ar_data['ar']
    ar_data['emergency_fund'] = total_cash
    ar_data['short'] = total_cash-(month_of_emergency*avg)
	
    
    # data asset
    asset = {}
    
    datastock = acc_investment_stock.objects.all()
    total_price = 0
    avg_price = 0
    for item in datastock:
        total_price += item.last_price*item.lot*100
        avg_price += item.lot*item.average*100
    asset['stock_inv'] = total_price
    asset['stock_percentage'] = (asset['stock_inv']-float(avg_price))/float(avg_price)*100

    asset['fund_inv'] = acc_investment_fund.objects.raw("SELECT id, round(SUM(CURRENT_NAV*UNIT)-(select (20000000 + (CURRENT_NAV-1224.21) * 16337.0663) from ACC_INVESTMENT_FUND aif where id = 2),2) total_fund from ACC_INVESTMENT_FUND aif")[0]
    
    url = "https://data-asg.goldprice.org/dbXRates/IDR"
    req = urllib.request.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7')
    
    try:    
        response = urllib.request.urlopen(req)
        res = response.read()      # a `bytes` object
        html = json.loads(res)
    except UnicodeDecodeError:
        response = urllib.request.urlopen(req)
        res = response.read()      # a `bytes` object
        html = json.loads(res)
    
    gold_price = html['items'][0]['xauPrice']    
    asset['gold_inv'] = round(gold_price/31.06778927*5,2)

    asset['gold_percentage'] = round((asset['gold_inv']-5*800000)/(5*800000)*100,2)    
    asset['total_asset'] = float(total_cash) + float(asset['fund_inv'].total_fund) + asset['stock_inv'] + asset['gold_inv']
    
    modal = acc_investment_deposit.objects.raw("select id, sum(amount) as total_modal from ACC_INVESTMENT_DEPOSIT")[0]
    data['profit_investment'] = round(-float(modal.total_modal) + (float(asset['fund_inv'].total_fund) + asset['stock_inv']),2)
    data['profit_percentage'] = round(data['profit_investment']/float(modal.total_modal)*100,2)
    
    context = {
        'title':'Dashboard Edumin',
        'dashboard_active':'Dashboard',
        'data':data,
        'ar_data':ar_data,
        'asset':asset,
        'sales':sales_chart,
        'expense':expense_chart,
        'data_avg_expense':data_average_expense
    }
    return render(request, 'dashboard/index.html', context)