from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('',views.cal_networth,name="cal_networth"),
    path('get_networth/',views.get_networth,name="get_networth"),
    path('export_csv_networth/',views.export_csv_networth,name="export_csv_networth")
]
