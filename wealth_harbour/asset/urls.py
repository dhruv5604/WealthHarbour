from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('',views.index,name='asset'),
    path('add-asset',views.add_asset,name="add-asset"),
    path('edit-asset/<int:id>',views.asset_edit,name="asset-edit"), 
    path('asset-delete/<int:id>',views.delete_asset,name="asset-delete"),
    path('search_assets',csrf_exempt(views.search_assets),name="search_assets"),
    path('export_csv',csrf_exempt(views.export_csv),name="asset-export-csv"),
    path('export_excel',csrf_exempt(views.export_excel),name="asset-export-excel"),
    path('statA',views.stat_view,name="statA"),
    path('asset_category_summary',views.asset_category_summary,name="asset_category_summary"),

]