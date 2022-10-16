from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect

from product.models import prd_mst

# Create your views here.
@csrf_protect
def createproduct_view(request):
    if request.method=="POST":
        # dosomething
        member = prd_mst.objects(
            course_name=request.POST['inputNameCourse'],
            description=request.POST['inputDescription'],
            remarks=request.POST['inputRemarks'],
        )
        member.save()
        return HttpResponseRedirect(reverse('createproduct'))

    datamst = prd_mst.objects.filter(validuntil__isnull=True)
    context = {
        'title':'H - Product Record',
        'dashboard_active':'Product',
        'datamst':datamst
        }

    return render(request, 'product/createproduct_view.html', context)