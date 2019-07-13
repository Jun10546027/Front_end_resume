from django.contrib.auth import get_user_model
from django.shortcuts import render
from django.views.generic import View
from django.http import JsonResponse


from rest_framework.response import Response
from rest_framework.views import APIView

User = get_user_model()

class DemoView(View):
    def get(self,request,*arg,**kwargs):
        context = {"title":"Django & Chart.js Visualization"}
        return render(request,'homepage4.html',context)

class HomeView(View):
    def get(self,request,*arg,**kwargs):
        context = {"title":"Django & Chart.js Visualization"}
        return render(request,'Resume.html',context)

def get_data(request,*arg,**kwargs):
    data = {
        "test":100,
        "test2":"222"
    }
    return JsonResponse(data)


from .bitcoin_data import (year_data,
                           year_day,
                           year_mvg7_data,
                           year_mvg7_day,
                           bar_time,
                           bar_data)

class LineChartData(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self,request,format=None):

        title = ["本年比特幣趨勢","移動平均線"]
        labels = [year_day,year_mvg7_day]
        data = [year_data,year_mvg7_data]
        background = ['rgba(0, 0, 0, 0.4)','rgba(229, 25, 25, 0.8)']

        data = {
            'labels':labels,
            "sales":100,
            "customers":10,
            "item":data,
            "title":title,
            "background":background,
        }
        return Response(data)

class BarChartData(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self,request,format=None):
        title = ["長條圖測試"]
        labels = [bar_time]
        data = [bar_data]
        background = [background_color(12)]

        data = {
            'labels':labels,
            "sales":100,
            "customers":10,
            "item":data,
            "title":title,
            "background": background,
        }
        return Response(data)

class PieChartData(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self,request,format=None):
        UserCount=User.objects.all().count()
        title = "月份平均圖"
        labels = ["yellow","black","red","green","blue","pink"]
        default_items = [UserCount,1,2,3,4,5]
        data = {
            'labels':labels,
            "sales":100,
            "customers":10,
            "item":default_items,
            "title":title
        }
        return Response(data)


import random
def background_color(num):
    background = []
    x = ["rgba(255, 99, 132, 0.4)","rgba(54, 162, 235, 0.4)","rgba(255, 206, 86, 0.4)","rgba(75, 192, 192, 0.4)","rgba(153, 102, 255, 0.4)","rgba(255, 159, 64, 0.4)"]
    # randint(a,b)  a<= x <= 5
    index = x[random.randint(0, 5)]
    for i in range(0,num):
        background.append(index)
    return background
