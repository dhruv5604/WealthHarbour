from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('',views.index,name="liabilities"),
    path('add-liabilities',views.add_liabilities,name="add-liabilities"), 
    path('edit-liabilities/<int:id>',views.liabilities_edit,name="liabilities-edit"),    
    path('liabilities-delete/<int:id>',views.delete_liabilities,name="liabilities-delete"),
    path('search-liabilities',csrf_exempt(views.search_liabilities),name="search_liabilities"),
    path('export_csv',csrf_exempt(views.export_csv),name="export-csv"),
    path('export_excel',csrf_exempt(views.export_excel),name="export-excel"),
    path('statL',views.stat_view,name="statL"),
    path('liabilities_category_summary',views.liabilities_category_summary,name="liabilities_category_summary"),
]
