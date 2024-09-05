"""epidemicShiXun URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path
from mindashixun import views

urlpatterns = [
    path('admin/', admin.site.urls),  # 参数有两个:前者:是前端的请求接口(接受请求),后者:对接收到的请求进行实现(调用方法(views.py),处理请求)
    path('index/', views.index),
    path('index/getConfirmedAndCured/', views.getConfirmedAndCured),
    path('index/getConfirmedTopSeven/', views.getConfirmedTopSeven),
    path('index/getSCConfirmedTopFive/', views.getSCConfirmedTopFive),
    path('index/getMap/', views.getMap),
    path('index/getConfirmedCuredDead/', views.getConfirmedCuredDead),
]
