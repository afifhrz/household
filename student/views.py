from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect

from student.models import std_mst, std_trx, std_trx_course
from product.models import prd_mst

# Create your views here.
@csrf_protect
def studentregistration_view(request):
    if request.method=="POST":
        # dosomething
        member = std_mst(
            name=request.POST['inputName'],
            email=request.POST['inputEmail'],
            phone=request.POST['inputPhone'],
            address=request.POST['inputAddress'],
            gender=request.POST['inputGender'],
        )
        member.save()
        return HttpResponseRedirect(reverse('studentregistration'))

    datamst = std_mst.objects.filter(validuntil__isnull=True)
    context = {
        'title':'H - Student Registration',
        'dashboard_active':'Student',
        'datamst':datamst
        }

    return render(request, 'student/studentregistration_view.html', context)

@csrf_protect
def courseregistration_view(request):
    if request.method=="POST":
        # dosomething

        datastd = std_mst.objects.filter(id=request.POST['inputNameStudent'])
        dataprd = prd_mst.objects.filter(id=request.POST['inputNameCourse'])
        
        member = std_trx(
            std_mst_id=datastd[0],
            prd_mst_id=dataprd[0],
            email=request.POST['inputEmail'],
            phone=request.POST['inputPhone'],
            amount=request.POST['inputAmount'],
        )
        member.save()
        return HttpResponseRedirect(reverse('courseregistration'))
    
    data_std = std_mst.objects.filter(validuntil__isnull=True)
    data_prd = prd_mst.objects.filter(validuntil__isnull=True)
    data_trx = std_trx.objects.raw('''SELECT st.ID, sm.NAME, st.AMOUNT FROM STD_TRX st
	JOIN STD_MST sm ON sm.ID = st.STD_MST_ID 
	WHERE st.VALID_UNTIL ISNULL''')

    context = {
        'title':'H - Course Registration',
        'dashboard_active':'Student',
        'data_std':data_std,
        'data_prd':data_prd,
        'data_trx':data_trx
        }

    return render(request, 'student/courseregistration_view.html', context)

def completedcourse_view(request):
    if request.method=="POST":
        # dosomething

        datastd = std_trx.objects.filter(std_mst_id=request.POST['inputNameStudent'])
        
        member = std_trx_course(
            std_trx_id=datastd[0],
            amount_hour=request.POST['inputAmountHour'],
            date_time=request.POST['inputDate']
        )
        member.save()
        return HttpResponseRedirect(reverse('completedcourse'))
    
    datastd = std_mst.objects.raw('SELECT * FROM STD_MST sm where id in (SELECT STD_MST_ID from STD_TRX st where VALID_UNTIL ISNULL)')
    data_trx = std_trx_course.objects.raw('''SELECT stc.ID, sm.NAME, stc.DATETIME, stc.AMOUNT_HOUR FROM STD_TRX_COURSE stc
	left join STD_TRX st on stc.STD_TRX_ID = st.id
	left join STD_MST sm on st.STD_MST_ID =sm.ID
	WHERE stc.VALID_UNTIL ISNULL''')

    context = {
        'title':'H - Completed Course',
        'dashboard_active':'Student',
        'data_std':datastd,
        'data_trxcourse':data_trx
        }

    return render(request, 'student/completedcourse_view.html', context)