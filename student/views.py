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
        )
        member.save()
        return HttpResponseRedirect(reverse('studentregistration'))

    context = {
        'title':'H - Student Registration',
        'dashboard_active':'Student',
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

    context = {
        'title':'H - Course Registration',
        'dashboard_active':'Student',
        'data_std':data_std,
        'data_prd':data_prd,
        }

    return render(request, 'student/courseregistration_view.html', context)

def completedcourse_view(request):
    if request.method=="POST":
        # dosomething

        datastd = std_trx.objects.filter(id=request.POST['inputNameStudent'])
        
        member = std_trx_course(
            std_trx_id=datastd[0],
            amount_hour=request.POST['inputAmountHour'],
            date_time=request.POST['inputDate']
        )
        member.save()
        return HttpResponseRedirect(reverse('completedcourse'))
    
    datastd = std_mst.objects.raw('SELECT * FROM STD_MST sm where id in (SELECT ID from STD_TRX st where VALID_UNTIL ISNULL)')

    context = {
        'title':'H - Completed Course',
        'dashboard_active':'Student',
        'data_std':datastd,
        }

    return render(request, 'student/completedcourse_view.html', context)