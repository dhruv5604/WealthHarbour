from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .models import Category,Liabilities
from django.contrib import messages
from django.core.paginator import Paginator
import json
from django.http import JsonResponse,HttpResponse
import datetime
import csv
import xlwt
# Create your views here.

def search_liabilities(request):
    if request.method == 'POST':
        search_str = json.loads(request.body).get('searchText')
        liabilities = Liabilities.objects.filter(
            amount__istartswith=search_str, owner=request.user) | Liabilities.objects.filter(
            date__istartswith=search_str, owner=request.user) | Liabilities.objects.filter(
            description__icontains=search_str,owner=request.user) | Liabilities.objects.filter(
            category=search_str,owner=request.user)  
        data = liabilities.values() 
        return JsonResponse(list(data),safe=False)
   

@login_required(login_url='/authentication/login')
def index(request):
    categories=Category.objects.all()
    liabilities = Liabilities.objects.filter(owner=request.user)
    paginator =Paginator(liabilities,4)
    page_number = request.GET.get('page')
    page_obj=Paginator.get_page(paginator,page_number)
    # currency = UserPreference.objects.get(user=request.user).currency
    context={
        'liabilities':liabilities,
        'page_obj':page_obj,
        # 'currency':currency
    }

    return render(request,'liabilities/index.html',context)

def add_liabilities(request):
    category=Category.objects.all()
    context={
        'category': category,
        'values':request.POST
    }

    if request.method=='GET':
        return render(request,'liabilities/add_liabilities.html',context)

    if request.method == 'POST':
        amount = request.POST['amount']

        if not amount:
            messages.error(request,'Amount is required')
            return render(request,'liabilities/add_liabilities.html',context)
        description = request.POST['description']
        date = request.POST['liabilities_date']
        category = request.POST['category']

        if not description:
            messages.error(request,'description is required')
            return render(request,'liabilities/add_liabilities.html',context)

        Liabilities.objects.create(owner=request.user,amount=amount,date=date,category=category,description=description)
        messages.success(request,'Liability saved successfully')

        return redirect('liabilities')
    

def liabilities_edit(request,id):
    liabilities = Liabilities.objects.get(pk=id)
    category=Category.objects.all()
    context={
        'liabilities':liabilities,
        'values':liabilities,
        'category':category
    }

    if request.method=='GET':
        return render(request,'liabilities/edit-liabilities.html',context)
    if request.method=='POST':
        amount = request.POST['amount']

        if not amount:
            messages.error(request,'Amount is required')
            return render(request,'liabilities/edit-liabilities.html',context)
        description = request.POST['description']
        date = request.POST['liabilities_date']
        category = request.POST['category']

        if not description:
            messages.error(request,'description is required')
            return render(request,'liabilities/edit-liabilities.html',context)

        liabilities.owner=request.user
        liabilities.amount=amount
        liabilities.amount=amount
        liabilities.category=category
        liabilities.description=description

        liabilities.save()
        messages.success(request,'liabilities updated successfully')

        return redirect('liabilities')
    
def delete_liabilities(request,id):
    liabilities = Liabilities.objects.get(pk=id)
    liabilities.delete()
    messages.success(request,'liabilities removed')
    return redirect('liabilities')    

def liabilities_category_summary(request):
    today_date=datetime.date.today()
    six_month_ago=today_date-datetime.timedelta(30*6)
    liabilities=Liabilities.objects.filter(owner=request.user,date__gte=six_month_ago,date__lte=today_date)
    finalrep={}

    def get_category(liabilities):
        return liabilities.category
    source_list=list(set(map(get_category,liabilities)))

    def get_liabilities_category_amount(category):
        amount=0
        filtered_by_category= liabilities.filter(category=category)

        for item in filtered_by_category:
            amount+=item.amount
        return amount
    
    for x in liabilities:
        for y in source_list:
            finalrep[y]=get_liabilities_category_amount(y)

    return JsonResponse({'liabilities_category_data':finalrep},safe=False)        

def stat_view(request):
    return render(request,'liabilities/stat.html')

def export_csv(request):

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=liabilities'+\
        str(datetime.datetime.now())+'.csv'
    
    writer = csv.writer(response)
    writer.writerow(['Amount','Description','Category','Date'])

    liabilities = Liabilities.objects.filter(owner=request.user)

    for liabilities in liabilities:
        writer.writerow([liabilities.amount,liabilities.description,liabilities.category,liabilities.date])

    return response   

def export_excel(request):
    response = HttpResponse(content_type='application/ms-excel') 
    response['Content-Disposition'] = 'attachment; filename=liabilities'+\
        str(datetime.datetime.now())+'.xls'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Liabilities')
    row_num=0
    font_style= xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Amount','Description','Category','Date']

    for col_num in range(len(columns)):
        ws.write(row_num,col_num,columns[col_num],font_style)
    
    font_style=xlwt.XFStyle()

    rows = Liabilities.objects.filter(owner=request.user).values_list(
        'amount','description','category','date')
    
    for row in rows:
        row_num+=1

        for col_num in range(len(row)):
            ws.write(row_num,col_num,str(row[col_num]),font_style)
    wb.save(response)

    return response