from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    path('',views.index,name="incomes"),
    path('add-income',views.add_income,name="add-incomes"), 
    path('edit-income/<int:id>',views.income_edit,name="income-edit"),    
    path('income-delete/<int:id>',views.delete_income,name="income-delete"),
    path('search-incomes',csrf_exempt(views.search_incomes),name="search_incomes"),
    path('export_csv',csrf_exempt(views.export_csv),name="income-export-csv"),
    path('export_excel',csrf_exempt(views.export_excel),name="income-export-excel"),
    path('stat1',views.stat_view,name="stat1"),
    path('income_source_summary',views.income_source_summary,name="income_source_summary"),
]