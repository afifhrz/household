from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from student.models import std_mst

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