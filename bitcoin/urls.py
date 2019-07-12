
from django.contrib import admin
from django.urls import path
from data import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/data/',views.get_data,name='api-data'),
    path('api/Linechart/data',views.LineChartData.as_view()),
    path('api/Barchart/data',views.BarChartData.as_view()),
    path('api/PieData/data',views.PieChartData.as_view()),
    path('',views.HomeView.as_view(),name='home'),
    path('demo',views.DemoView.as_view(),name='demo'),
]
