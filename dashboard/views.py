import datetime
import calendar
import urllib
import json

from django.shortcuts import render
from account.models import acc_income_expense, acc_investment_stock, acc_investment_fund, acc_ar_debt, acc_investment_deposit
from django.db import connection
from django.contrib.auth.decorators import login_required

def get_query_date(month, year):
    total_day = calendar.monthrange(year, month)[1]
    if len(str(month)) < 2:
        startDate = str(year)+"-"+'0'+str(month)+"-"+"01"
        endDate = str(year)+"-"+'0'+str(month)+"-"+ str(total_day)
    else:
        startDate = str(year)+"-"+str(month)+"-"+"01"
        endDate = str(year)+"-"+str(month)+"-"+ str(total_day)
    return startDate, endDate

def get_gold_info():
    url = "https://data-asg.goldprice.org/dbXRates/IDR"
    req = urllib.request.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36')
    
    try:    
        response = urllib.request.urlopen(req)
        res = response.read()      # a `bytes` object
        html = json.loads(res)
    except UnicodeDecodeError:
        response = urllib.request.urlopen(req)
        res = response.read()      # a `bytes` object
        html = json.loads(res)
    return html

def get_fund_inv():
    total_fund = acc_investment_fund.objects.raw(
        """SELECT id, round(SUM(CURRENT_NAV*UNIT),2) total_fund 
            FROM ACC_INVESTMENT_FUND aif""")[0]
    mother_first_fund = acc_investment_fund.objects.raw(
        """SELECT id, round(SUM(CURRENT_NAV * 8937.0663),2) mother_first_fund
            FROM ACC_INVESTMENT_FUND aif WHERE id = 2""")[0]
    mother_second_fund = acc_investment_fund.objects.raw(
        """SELECT id, round(SUM(CURRENT_NAV * 2116.3145),2) mother_second_fund
            FROM ACC_INVESTMENT_FUND aif WHERE id = 7""")[0] 
    total_fund.total_fund = total_fund.total_fund - mother_first_fund.mother_first_fund - mother_second_fund.mother_second_fund
    return total_fund

# Create your views here.
@login_required(login_url='/login')
def index(request):
    month_of_emergency = 3
    data = {}
    year = datetime.datetime.today().year
    month = datetime.datetime.today().month
    startDate, endDate = get_query_date(month, year)
    
    # data balance
    data['month_sale']=acc_income_expense.objects.raw(
        f'''SELECT id, IFNULL(SUM(AMOUNT_IN),0) - IFNULL(SUM(AMOUNT_OUT),0) MONTH_SALE 
                FROM ACC_INC_EXP 
                WHERE BLL_MST_BILL_ITEM_ID IN (1,19) 
                AND ACCOUNT_DATE >= "{startDate}"'''
                )[0]
    data['profit_investment']=0
    data['month_expense']=acc_income_expense.objects.raw(
        f'''SELECT aie.id, SUM(AMOUNT_OUT) MONTH_EXPENSE 
                FROM ACC_INC_EXP aie
	            LEFT JOIN BLL_MST_BILL_ITEM bmbi ON bmbi .id = aie.BLL_MST_BILL_ITEM_ID 
                WHERE bmbi.DEBET_CREDIT = 1
                AND bmbi.VALID_STATUS = 1
                AND bmbi.id NOT IN (19,21) 
                AND ACCOUNT_DATE >= "{startDate}" 
                AND ACCOUNT_DATE <= "{endDate} 23:59:59"'''
                )[0]
    data['overall_balance']=acc_income_expense.objects.raw(
        f'''SELECT id, OVERALL_BALANCE 
                FROM ACC_INC_EXP 
                ORDER BY id DESC LIMIT 1'''
                )[0]

    # data expense chart
    cursor = connection.cursor()
    cursor.execute(
        """SELECT DISTINCT bmbi.CATEGORY AS category 
            FROM ACC_INC_EXP aie
	        LEFT JOIN BLL_MST_BILL_ITEM bmbi ON bmbi.ID = aie.BLL_MST_BILL_ITEM_ID 
            WHERE bmbi.DEBET_CREDIT = 1
            ORDER BY category """)
    category = list(cursor.fetchall())
    
    data_chart = []
    counter = 0
    for row in category:
        # if category got monthly-expense 
        if row[0]=="MONTHLY-EXPENSE":
            cursor.execute(
            f"""SELECT * FROM
            (SELECT DISTINCT bmbi.CATEGORY as category,
                IFNULL(SUM(AMOUNT_OUT),0) as AMOUNT,
                DATE_FORMAT(ACCOUNT_DATE, "%m-%Y") as 'month_year' 
                FROM ACC_INC_EXP aie
                left join BLL_MST_BILL_ITEM bmbi ON bmbi.ID = aie.BLL_MST_BILL_ITEM_ID 
				where bmbi.DEBET_CREDIT = 1
                and ACCOUNT_DATE >= '{date_filter}'
                group by DATE_FORMAT(ACCOUNT_DATE, "%m-%Y"), category
                order by ACCOUNT_DATE)
            as tabel1
            where category = '{row[0]}';""")
            result = list(cursor.fetchall())
            data_chart.append(result[:12])   
        elif row[0]=="FIXED-EXPENSE":
            cursor.execute(
            f"""SELECT * FROM
            (select DISTINCT bmbi.CATEGORY as category,
                IFNULL(SUM(AMOUNT_OUT),0) as AMOUNT,
                DATE_FORMAT(ACCOUNT_DATE, "%m-%Y") as 'month_year' 
                FROM ACC_INC_EXP aie
                left join BLL_MST_BILL_ITEM bmbi ON bmbi.ID = aie.BLL_MST_BILL_ITEM_ID 
				where bmbi.DEBET_CREDIT = 1
                group by DATE_FORMAT(ACCOUNT_DATE, "%m-%Y"), category
                order by ACCOUNT_DATE)
            as tabel1
            where category = '{row[0]}';""")
            result = list(cursor.fetchall())
            data_chart.append(result[-12:])
            date_filter = result[-12][2].split("-")
            date_filter = date_filter[1] + "-" + date_filter[0] + "-01"
        else:
            cursor.execute(
            f"""SELECT * FROM
            (select DISTINCT bmbi.CATEGORY as category,
                IFNULL(SUM(AMOUNT_OUT),0) as AMOUNT,
                DATE_FORMAT(ACCOUNT_DATE, "%m-%Y") as 'month_year' 
                FROM ACC_INC_EXP aie
                left join BLL_MST_BILL_ITEM bmbi ON bmbi.ID = aie.BLL_MST_BILL_ITEM_ID 
				where bmbi.DEBET_CREDIT = 1
                group by DATE_FORMAT(ACCOUNT_DATE, "%m-%Y"), category
                order by ACCOUNT_DATE)
            as tabel1
            where category = '{row[0]}';""")
            result = list(cursor.fetchall())
            data_chart.append(result[-12:])
            
        counter+=1
    cursor.execute(f"""select DISTINCT DATE_FORMAT(ACCOUNT_DATE, "%m-%Y") as 'month_year' from ACC_INC_EXP WHERE ACCOUNT_DATE >= '{date_filter}' order by ACCOUNT_DATE""")
    date = list(cursor.fetchall())[:12]
    
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
        (300, 300, 100),
        (50, 30, 100),
        (30, 150, 100),
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
    # print(dateIn)
    cursor.execute(
        f"""SELECT * FROM 
        (SELECT 
            SUM(AMOUNT_IN) REVENUE,
            IFNULL(SUM(AMOUNT_OUT),0) EXPENSE, 
            IFNULL((SUM(AMOUNT_IN) - SUM(AMOUNT_OUT)),0) as NET_PROFIT,
            DATE_FORMAT(ACCOUNT_DATE, "%m-%Y") as 'month_year' 
            from 
            (select aie.* from ACC_INC_EXP aie
                left join BLL_MST_BILL_ITEM bmbi ON bmbi .id = aie.BLL_MST_BILL_ITEM_ID 
                AND bmbi.VALID_STATUS = 1
                WHERE aie.BLL_MST_BILL_ITEM_ID not in (21, 18)) as t1 
            group by DATE_FORMAT(ACCOUNT_DATE, "%m-%Y")
            order by ACCOUNT_DATE)
        as tabel1
        where month_year IN ({dateIn});""")
    sales_chart = cursor.fetchall()

    cursor.execute(
        f"""SELECT * FROM 
            (
                select 	aie.id,
                    SUM(AMOUNT_OUT) EXPENSE,
                    DATE_FORMAT(ACCOUNT_DATE, "%m-%Y") as 'month_year' 
                    from ACC_INC_EXP aie
                    left join BLL_MST_BILL_ITEM bmbi on bmbi.id = aie.BLL_MST_BILL_ITEM_ID 
                    WHERE bmbi.DEBET_CREDIT = 1
                    and bmbi.VALID_STATUS = 1
                    and bmbi.CATEGORY = 'MONTHLY-EXPENSE'
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

    asset['fund_inv'] = get_fund_inv()
    html = get_gold_info()
    gold_gram_owned = 7
    gold_avg_price = 995142
    gold_asset_owned_base_price = gold_gram_owned*gold_avg_price
    gold_price = html['items'][0]['xauPrice']    
    asset['gold_inv'] = round(gold_price/31.06778927*gold_gram_owned,2)
    asset['gold_percentage'] = round((asset['gold_inv']-gold_asset_owned_base_price)/(gold_asset_owned_base_price)*100,2)    
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
