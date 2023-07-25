"""household_site URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', include('dashboard.urls')),
    path('billing/', include('billing.urls')),
    path('product/', include('product.urls')),
    path('student/', include('student.urls')),
    path('account/', include('account.urls')),
    path('trading/', include('tradingstock.urls')),
    path('login', views.login_page, name='login_page'),
    path('login_process', views.login_process, name='login_process'),
    path('logout', views.logout_process, name='logout_process'),
]

# handler404 = 'dashboard.views.error_404_view'