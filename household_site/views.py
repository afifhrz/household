from django.contrib.auth.models import User
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.urls import reverse

def login_page(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect("home/")
    context = {
        'title' : 'Household',
        'path':request.GET.get("next",'')

    }
    return render(request, 'signin.html', context)

@csrf_protect
def login_process(request):
    user = authenticate(username=request.POST['username'], password = request.POST['password'])
    if user is not None:
        login(request, user)
        if request.GET.get("next",'') == "":
            path = 'home/'
        else:
            path = request.GET.get("next")
        return HttpResponseRedirect(path)
    else:
        return HttpResponseRedirect(reverse('login_page'))
    
def logout_process(request):
    logout(request)
    return HttpResponseRedirect(reverse('login_page'))