from django.shortcuts import render
from dashboard.models import admin_mst_module

# Create your views here.
def index(request):

    context = {
        'title':'Dashboard Edumin',
        'dashboard_active':'Dashboard',
    }
    return render(request, 'dashboard/index.html', context)

# from django.conf import settings
# from django.shortcuts import redirect
 
# def error_404_view(request, exception):
#     context = {}
#     # we add the path to the the 404.html file
#     # here. The name of our HTML file is 404.html
#     return render(request, '404.html', context)