from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
import urllib.parse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect

import calendar
from datetime import datetime
from account.models import acc_income_expense
from student.models import std_mst, std_trx, std_trx_course
from billing.models import bll_trx_billing, bll_trx_bill_item, bll_mst_bill_item

# Create your views here.
@csrf_protect
def generatebillcourse_view(request):
    BLL_MST_ITEM_ID = 1
    if request.method=="POST":
        # dosomething
        datastd = std_trx.objects.filter(std_mst_id=request.POST['inputNameStudent'])
        datamstitem = bll_mst_bill_item.objects.filter(id=BLL_MST_ITEM_ID)
        
        data_bill = bll_trx_billing.objects.create(
            invoice_status=1,
            total_amount=0, 
            tobe_paid=0, 
            month=datetime.now().month,
            year=datetime.now().year,
            periode=int(str(datetime.now().year)+str(datetime.now().month)),
            std_trx_id=datastd[0])

        datacourse = std_trx_course.objects.raw(f"""
        SELECT * FROM STD_TRX_COURSE WHERE STD_TRX_ID = {datastd[0].id} AND
        VALID_UNTIL ISNULL AND
        DATETIME >= '{request.POST['inputStartDate']}' AND
        DATETIME <= '{request.POST['inputEndDate']} 23:59:59'
        """)

        amount = 0
        for course in datacourse:
            amount += datastd[0].amount * course.amount_hour
            bll_trx_bill_item.objects.create(
                description=datamstitem[0].item_name,
                value=datastd[0].amount * course.amount_hour,
                bll_mst_id=datamstitem[0],
                btb_id=data_bill,
                std_trx_id=datastd[0],
                std_trx_course_id=course
            )

        bll_trx_billing.objects.filter(pk=data_bill.pk).update(
            invoice_status=8,
            total_amount=amount,
            tobe_paid=amount
        )        

        return HttpResponseRedirect(reverse('generatebillcourse'))

    datastd = std_mst.objects.raw('''SELECT * FROM STD_MST where ID in (SELECT st.STD_MST_ID FROM STD_TRX st
	JOIN STD_MST sm ON sm.ID = st.STD_MST_ID 
	WHERE sm.VALID_UNTIL ISNULL)''')

    context = {
        'title':'H - Invoice Generator',
        'dashboard_active':'Billing',
        'data_std':datastd,
        }

    return render(request, 'billing/generatebillcourse_view.html', context)

def liststatusbill_view(request):
    
    year = datetime.today().year
    month = datetime.today().month-1
    if len(str(month))==1:
        date = str(year)+"-0"+str(month)+"-"+"01"
    else:
        date = str(year)+"-"+str(month)+"-"+"01"
    total_day = calendar.monthrange(year, month)[1]
    enddate = str(year)+"-"+str(month)+"-"+ str(total_day)
    
    data_unpaid_bill = bll_trx_billing.objects.raw("""SELECT btb.ID, btb.INVOICE_DATE, btb.TOBE_PAID, btb.MONTH, btb.YEAR , sm.NAME, sm.BOOKED_PHONE  FROM BLL_TRX_BILLING btb 
	JOIN STD_TRX st ON st.id = btb.STD_TRX_ID 
	JOIN STD_MST sm ON sm.id = st.STD_MST_ID 
	WHERE INVOICE_STATUS = 8
    ORDER BY TOBE_PAID DESC""")
    data_paid_bill = bll_trx_billing.objects.raw(f"""SELECT btb.ID, btb.INVOICE_DATE, btb.TOTAL_AMOUNT, btb.MONTH, btb.YEAR , sm.NAME, sm.BOOKED_PHONE  FROM BLL_TRX_BILLING btb 
	JOIN STD_TRX st ON st.id = btb.STD_TRX_ID 
	JOIN STD_MST sm ON sm.id = st.STD_MST_ID 
	WHERE INVOICE_STATUS = 1 AND INVOICE_DATE >= '{date}'""")
    print(f"""SELECT btb.ID, btb.INVOICE_DATE, btb.TOTAL_AMOUNT, btb.MONTH, btb.YEAR , sm.NAME, sm.BOOKED_PHONE  FROM BLL_TRX_BILLING btb 
	JOIN STD_TRX st ON st.id = btb.STD_TRX_ID 
	JOIN STD_MST sm ON sm.id = st.STD_MST_ID 
	WHERE INVOICE_STATUS = 1 AND INVOICE_DATE >= '{date}'""")
    context = {
        'title':'H - Status Bill',
        'dashboard_active':'Billing',
        'datapaid':data_paid_bill,
        'dataunpaid':data_unpaid_bill
        }
    return render(request, 'billing/liststatusbill_view.html', context)

def send_invoice(request, id):
    data = std_trx_course.objects.raw(f"""SELECT stc.ID, SUM(stc .AMOUNT_HOUR) as TOTAL_HOUR, st.AMOUNT as AMOUNT_PERHOUR, sm.NAME, sm.GENDER, sm.BOOKED_PHONE, SUM(stc .AMOUNT_HOUR)*st.AMOUNT as TOTAL_AMOUNT
FROM STD_TRX_COURSE stc 
	JOIN STD_TRX st ON stc.STD_TRX_ID = st.ID
	JOIN STD_MST sm on st.STD_MST_ID = sm.ID 
	WHERE stc.ID IN 
		(SELECT STD_TRX_COURSE_ID FROM BLL_TRX_BILL_ITEM btbi
			WHERE btbi.BLL_TRX_BILLING_ID = {id})""")

    total_hour = data[0].TOTAL_HOUR
    amount_perhour = '{:0,.0f}'.format(data[0].AMOUNT_PERHOUR)
    total_amount = '{:0,.0f}'.format(data[0].TOTAL_AMOUNT)
    name = data[0].NAME.split(" ")[0]
    phone_number = data[0].BOOKED_PHONE

    if data[0].GENDER == "mr":
        gender = "Pak"
    elif data[0].GENDER == "mrs":
        gender = "Bu"
    elif data[0].GENDER == "bro":
        gender = "Mas"
    elif data[0].GENDER == "sist":
        gender = "Mbak"

    message = f"""Selamat Pagi {gender} {name}, mohon maaf mengganggu waktunya.

Izin menginfokan lesnya total {total_hour} jam ya {gender}
Totalnya Rp. {amount_perhour} * {total_hour} = Rp. {total_amount}

Rekening tersedia a/n Ahmad Afif Aulia Hariz

Bank Permata 4159142766
Bank BRI 627301023198538
Bank Sinarmas 0055573158

Terimakasih"""
    message = urllib.parse.quote(message)
    return HttpResponse(f"https://wa.me/{phone_number}?text={message}")

def paid_invoice(request, id):
    data_bill = bll_trx_billing.objects.filter(id=id)
    data_bill_item = bll_trx_bill_item.objects.filter(btb_id=data_bill[0])
    # print(data_bill_item.values()[0][""])
    data_mst = bll_mst_bill_item.objects.filter(id=data_bill_item[0].bll_mst_id_id)
    data_last_acc = acc_income_expense.objects.latest('id')
    acc_income_expense.objects.create(
        description=data_mst[0].item_name,  
        amount_in=data_bill[0].tobe_paid, 
        overall_balance=data_last_acc.overall_balance+data_bill[0].tobe_paid,
        account_type='Cash',
        account_date=data_bill[0].invoice_date,
        bll_mst_item_id=data_mst[0])
    data_bill.update(invoice_status=1, tobe_paid=0)
    return HttpResponse(None)

def cancel_invoice(request, id):
    data_bill = bll_trx_billing.objects.filter(id=id)
    data_bill.update(invoice_status=0)
    return HttpResponse(None)

@csrf_protect
def createmstbill_view(request):
    if request.method=="POST":
        # dosomething
        member = bll_mst_bill_item(
            item_name=request.POST['inputItemName'],
            debet_credit=request.POST['inputDebet'],
        )
        member.save()
        return HttpResponseRedirect(reverse('createmstbill'))

    datamst = bll_mst_bill_item.objects.filter(validstatus=1)
    context = {
        'title':'H - Master Billing',
        'dashboard_active':'Billing',
        'datamst':datamst
        }

    return render(request, 'billing/createmstbill_view.html', context)