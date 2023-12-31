from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.urls import reverse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.core import serializers
import json

from datetime import timedelta
from .models import *

# Create your views here.
@csrf_protect
@login_required(login_url='/login')
def mastervehicle_view(request):
    if request.method=="POST":
        # dosomething
        member = auto_mst_vehicle(
            name=request.POST['inputName'],
            year=request.POST['inputYear'],
            current_kilometer=request.POST['inputKilometer'],
        )
        member.save()
        return HttpResponseRedirect(reverse('mastervehicle'))

    datamst = auto_mst_vehicle.objects.filter(validstatus=1)
    dataterminated = auto_mst_vehicle.objects.filter(validstatus=0).order_by('-validstatus')
    context = {
        'title':'H - Master Vehicle',
        'dashboard_active':'Automotive',
        'datamst':datamst,
        'dataterminated':dataterminated
        }

    return render(request, 'automotive/mastervehicle_view.html', context)

def calculateNext(repeating_month, repeating_kilometer, last_date, last_kilometer):
    ok = datetime.strptime(last_date,"%Y-%m-%d")
    next_date = ok + timedelta(days=int(repeating_month)*30)
    next_km = int(last_kilometer)+int(repeating_kilometer)
    return next_date, next_km

@csrf_protect
@login_required(login_url='/login')
def serviceitem_view(request):
    if request.method=="POST":
        datavehicle = auto_mst_vehicle.objects.get(pk=request.POST['inputVehicle'])
        member = auto_mst_service_item(
            service_name = request.POST['inputServiceName'],
            repeating_kilometer = request.POST['inputRepeatingKilometer'],
            repeating_months =request.POST['inputRepeatingMonths'],
            service_type = request.POST['inputType'],
            vehicle_id = datavehicle,
            validstatus = 1
        )
        next_date, next_km = calculateNext(
            repeating_month=request.POST['inputRepeatingMonths'],
            repeating_kilometer=request.POST['inputRepeatingKilometer'],
            last_date=request.POST['inputDate'],
            last_kilometer=request.POST['inputLastKilometer']
            )
        sec_member = auto_service_history(
            auto_mst_service_item_id = member,
            price = request.POST['inputPrice'],
            last_service_kilometer = request.POST['inputLastKilometer'],
            last_service_date = request.POST['inputDate'],
            next_service_kilometer = next_km,
            next_service_date = next_date,
            note = "First Input",
            validstatus = 1
        )
        member.save()
        sec_member.save()
        return HttpResponseRedirect(reverse('serviceitem'))
    
    data_vehicle = auto_mst_vehicle.objects.filter(validstatus=1)
    data_maintain = auto_mst_service_item.objects.filter(validstatus=1)

    context = {
        'title':'H - Maintainance Item Registration',
        'dashboard_active':'Auto',
        'data_vehicle':data_vehicle,
        'data_maintain':data_maintain,
        }

    return render(request, 'automotive/maintainanceitem_view.html', context)

@csrf_protect
@login_required(login_url='/login')
def servicehistory_view(request):
    if request.method=="POST":
        data_vehicle = auto_mst_vehicle.objects.get(pk=request.POST['inputVehicle'])
        datamaintain = auto_mst_service_item.objects.get(pk=request.POST['inputServiceName'])
        last_service = auto_service_history.objects.filter(auto_mst_service_item_id=datamaintain).order_by('-pk')[0]

        next_date, next_km = calculateNext(
            repeating_month=datamaintain.repeating_months,
            repeating_kilometer=datamaintain.repeating_kilometer,
            last_date=request.POST['inputDate'],
            last_kilometer=request.POST['inputLastKilometer']
            )
        sec_member = auto_service_history(
            auto_mst_service_item_id = datamaintain,
            price = request.POST['inputPrice'],
            last_service_kilometer = request.POST['inputLastKilometer'],
            last_service_date = request.POST['inputDate'],
            next_service_kilometer = next_km,
            next_service_date = next_date,
            note = request.POST['inputNote'],
            validstatus = 1
        )
        data_vehicle.current_kilometer = request.POST['inputLastKilometer']
        data_vehicle.save()
        last_service.validstatus = 0
        last_service.save()
        sec_member.save()
        return HttpResponseRedirect(reverse('history'))
    
    # update last kilometer of current vehicle
    data_vehicle = auto_mst_vehicle.objects.filter(validstatus=1)
    data_history = auto_service_history.objects.filter(validstatus=1)

    warning_kilometer = 750
    today = datetime.today()
    status = []
    for data in data_history:
        if data.auto_mst_service_item_id.vehicle_id.current_kilometer + warning_kilometer > data.next_service_kilometer or (today + timedelta(days=10)).date() > data.next_service_date:
            status.append(True)
        else:
            status.append(False)
    data_history = zip(data_history,status)

    context = {
        'title':'H - History Service Registration',
        'dashboard_active':'Auto',
        'data_vehicle':data_vehicle,
        'data_history':data_history,
        }

    return render(request, 'automotive/history_view.html', context)

def get_maintainance_item(request, vehicle_id):
    if request.user.is_authenticated:
        if request.method == "GET":
            vehicle = auto_mst_vehicle.objects.get(pk = vehicle_id)
            data = auto_mst_service_item.objects.filter(vehicle_id=vehicle).filter(validstatus=1)
            json_model = serializers.serialize("json", data)
            data = json.loads(json_model)
            return JsonResponse(data, safe=False)
        else:
            return JsonResponse({"message":"Wrong Method"}, status=400)
    else:
        return JsonResponse({"message":"Unauthenticated"}, status=401)