from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .models import Category,Asset
from django.contrib import messages
from django.core.paginator import Paginator
import json
from django.http import JsonResponse,HttpResponse
import datetime
import csv
import xlwt
from django.template.loader import render_to_string
import tempfile
from django.db.models import Sum
# from expensewebsite.userpreferences.models import UserPreference
# Create your views here.

def search_assets(request):
    if request.method == 'POST':
        search_str = json.loads(request.body).get('searchText')
        assets = Asset.objects.filter(
            amount__istartswith=search_str, owner=request.user) | Asset.objects.filter(
            date__istartswith=search_str, owner=request.user) | Asset.objects.filter(
            description__icontains=search_str,owner=request.user) | Asset.objects.filter(
            category__icontains=search_str,owner=request.user)  
        data = assets.values()
        return JsonResponse(list(data),safe=False)
   

@login_required(login_url='/authentication/login')
def index(request):
    categories=Category.objects.all()
    assets = Asset.objects.filter(owner=request.user)
    paginator =Paginator(assets,4)
    page_number = request.GET.get('page')
    page_obj=Paginator.get_page(paginator,page_number)
    # currency = UserPreference.objects.get(user=request.user).currency
    context={
        'assets':assets,
        'page_obj':page_obj,
        # 'currency':currency
    }

    return render(request,'asset/index.html',context)

def add_asset(request):
    categories=Category.objects.all()
    context={
        'categories': categories,
        'values':request.POST
    }

    if request.method=='GET':
        return render(request,'asset/add_asset.html',context)

    if request.method == 'POST':
        amount = request.POST['amount']

        if not amount:
            messages.error(request,'Amount is required')
            return render(request,'asset/add_assets.html',context)
        description = request.POST['description']
        date = request.POST['asset_date']
        category = request.POST['category']

        if not description:
            messages.error(request,'description is required')
            return render(request,'assets/add_asset.html',context)

        Asset.objects.create(owner=request.user,amount=amount,date=date,category=category,description=description)
        messages.success(request,'Asset saved successfully')

        return redirect('asset')
    

def asset_edit(request,id):
    asset = Asset.objects.get(pk=id)
    categories=Category.objects.all()
    context={
        'asset':asset,
        'values':asset,
        'categories':categories
    }

    if request.method=='GET':
        return render(request,'asset/edit-asset.html',context)
    if request.method=='POST':
        amount = request.POST['amount']

        if not amount:
            messages.error(request,'Amount is required')
            return render(request,'asset/edit-asset.html',context)
        description = request.POST['description']
        date = request.POST['asset_date']
        category = request.POST['category']

        if not description:
            messages.error(request,'description is required')
            return render(request,'asset/edit-asset.html',context)

        asset.owner=request.user
        asset.amount=amount
        asset.amount=amount
        asset.category=category
        asset.description=description

        asset.save()
        messages.success(request,'Asset updated successfully')

        return redirect('asset')
    
def delete_asset(request,id):
    asset = Asset.objects.get(pk=id)
    asset.delete()
    messages.success(request,'Asset removed')
    return redirect('asset')    

def asset_category_summary(request):
    todays_date=datetime.date.today()
    six_month_ago = todays_date-datetime.timedelta(30*6)
    assets = Asset.objects.filter(owner=request.user,date__gte=six_month_ago,date__lte=todays_date)
    finalrep={}

    def get_category(asset):
        return asset.category
    category_list=list(set(map(get_category,assets)))

    def get_asset_category_amount(category):
        amount=0
        filtered_by_category = assets.filter(category=category)
        
        for item in filtered_by_category:
            amount+=item.amount
        return amount

    for x in assets:
        for y in category_list:
            finalrep[y]=get_asset_category_amount(y)

    return JsonResponse({'asset_category_data':finalrep},safe=False)

def stat_view(request):
    return render(request,'asset/stat.html')

def export_csv(request):

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=Assets'+\
        str(datetime.datetime.now())+'.csv'
    
    writer = csv.writer(response)
    writer.writerow(['Amount','Description','Category','Date'])

    assets = Asset.objects.filter(owner=request.user)

    for asset in assets:
        writer.writerow([asset.amount,asset.description,asset.category,asset.date])

    return response   

def export_excel(request):
    response = HttpResponse(content_type='application/ms-excel') 
    response['Content-Disposition'] = 'attachment; filename=Assets'+\
        str(datetime.datetime.now())+'.xls'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Assets')
    row_num=0
    font_style= xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Amount','Description','Category','Date']

    for col_num in range(len(columns)):
        ws.write(row_num,col_num,columns[col_num],font_style)
    
    font_style=xlwt.XFStyle()

    rows = Asset.objects.filter(owner=request.user).values_list(
        'amount','description','category','date')
    
    for row in rows:
        row_num+=1

        for col_num in range(len(row)):
                ws.write(row_num,col_num,str(row[col_num]),font_style)
    wb.save(response)

    return response

# def export_pdf(request):
#     response = HttpResponse(content_type='application/pdf') 
#     response['Content-Disposition'] = 'attachment; filename=Expenses'+\
#         str(datetime.datetime.now())+'.pdf'
    
#     response['Content-Transfer-Encoding'] = 'binary'

#     html_string = render_to_string( 'expenses/pdf_output',{'expenses':[],'total':0})
#     html = HTML(string=html_string)

#     result = html.write_pdf()

#     with tempfile.NamedTemporaryFile(delete=True) as output:
#         output.write(result)
#         output.flush()
#         output= open(output.name,"rb")
#         response.write(output.read())

#     return response    


