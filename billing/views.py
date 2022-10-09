from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect

# Create your views here.
@csrf_protect
def generatebillcourse_view(request):
    if request.method=="POST":
        # dosomething
        member = std_mst(
            name=request.POST['inputName'],
            email=request.POST['inputEmail'],
            phone=request.POST['inputPhone'],
            address=request.POST['inputAddress'],
        )
        member.save()
        return HttpResponseRedirect(reverse('generatebillcourse'))

    context = {
        'title':'H - Invoice Generator',
        'dashboard_active':'Billing',
        }

    return render(request, 'billing/generatebillcourse_view.html', context)