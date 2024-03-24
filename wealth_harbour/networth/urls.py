from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('',views.cal_networth,name="cal_networth"),
    path('get_networth/',views.get_networth,name="get_networth"),
    path('export_csv_networth/',views.export_csv_networth,name="export_csv_networth"),
    path('export_excel_networth/',views.export_csv_networth,name="export_excel_networth"),
    path('stat_networth/',views.stat_view_networth,name="stat_view_networth"),
    path('detail_networth/',views.detail_networth,name="detail_networth"),
    path('interest_form_view/',views.interest_form_view,name="interest_form_view"),
]
