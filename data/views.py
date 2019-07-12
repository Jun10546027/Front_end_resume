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
        return render(request,'homepage3.html',context)

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
                           year_mvg7_day)

class LineChartData(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self,request,format=None):

        title = ["本年比特幣趨勢","移動平均線"]
        labels = [year_day,year_mvg7_day]

        data = {
            'labels':labels,
            "sales":100,
            "customers":10,
            "item":[year_data,year_mvg7_data],
            "title":title
        }
        return Response(data)

class BarChartData(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self,request,format=None):
        UserCount=User.objects.all().count()
        title = "長條圖測試"
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

class PieChartData(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self,request,format=None):
        UserCount=User.objects.all().count()
        title = "長條圖測試"
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
