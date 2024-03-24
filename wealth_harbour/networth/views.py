import csv
import datetime
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render,redirect
from liabilities.models import Liabilities
from django.contrib.auth.decorators import login_required
from asset.models import Asset
import json
import xlwt
from .forms import InterestForm

def get_assets(request):
    requested_user = request.user
    user_assets = Asset.objects.filter(owner=requested_user)

    assets_data = []
    for asset in user_assets:
        assets_data.append({
            'type': asset.category,
            'amt': asset.amount
        })
    return assets_data


def get_liabilities(request):
    requested_user = request.user
    user_liabilities = Liabilities.objects.filter(owner=requested_user)

    liabilities_data = []
    for liability in user_liabilities:
        liabilities_data.append({
            'type': liability.category,
            'amt': liability.amount
        })
    return liabilities_data

def interest_form_view(request):
    if request.method == 'POST':
        form = InterestForm(request.POST)
        if form.is_valid():
            # Save form data in session
            request.session['interest_form_data'] = form.cleaned_data
            return redirect('cal_networth')
    else:
        form = InterestForm()
    return render(request, 'networth/details.html', {'form': form})


def detail_networth(request):
    return render(request,'networth/details.html')

@login_required(login_url="/authentication/login")
def cal_networth(request):
    
    form_data = request.session.get('interest_form_data')

    if form_data:
        value_l = get_liabilities(request)
        value_a = get_assets(request)
     

        Rate_a_c = form_data.get('cashRate')
        Rate_a_Rs = form_data.get('reRate')
        Rate_a_in = form_data.get('iaRate')
        Rate_a_o = form_data.get('otherRate')

        Rate_l_sl = form_data.get('slRate')
        Rate_l_m = form_data.get('mdRate')
        Rate_l_PL_CD = form_data.get('plRate')
        Rate_l_o = form_data.get('otherRateL')
        Years_l = form_data.get('yearLib')

        def calc_a(value_a, r1,r2,r3,r4):
            value_a_sum = 0
            for (idx,i) in  enumerate(value_a):
                if i["type"] == "cash":
                    value_a[idx]["amt"] += r1 * i["amt"]
                    value_a_sum += value_a[idx]["amt"]
                elif i["type"] == "Real-Estate":
                    value_a[idx]["amt"] += r2 * i["amt"]
                    value_a_sum += value_a[idx]["amt"]
                elif i["type"] == "Investment Accounts":
                    value_a[idx]["amt"] += r3 * i["amt"]
                    value_a_sum += value_a[idx]["amt"]
                else:
                    value_a[idx]["amt"] += r4 * i["amt"]
                    value_a_sum += value_a[idx]["amt"]
            return value_a_sum

        def calc_l(value_l, r1,r2,r3,r4):
            value_l_sum = 0
            for (idx,i) in  enumerate(value_l):
                if i["type"] == "Student-Loan":
                    value_l[idx]["amt"] += r1 * i["amt"]
                    value_l_sum += value_l[idx]["amt"]
                elif i["type"] == "Mortage-debt":
                    value_l[idx]["amt"] += r2 * i["amt"]
                    value_l_sum += value_l[idx]["amt"]
                elif i["type"] == "Credit card/Personal Loan":
                    value_l[idx]["amt"] += r3 * i["amt"]
                    value_l_sum += value_l[idx]["amt"]
                else:
                    value_l[idx]["amt"] += r4 * i["amt"]
                    value_l_sum += value_l[idx]["amt"]
            return value_l_sum
        
        n = 10
        networths = list()
        value_a_sum = 0
        value_l_sum = 0
        assets = list()
        liabilities = list()

        for i in range(0,n,1):
            value_a_sum = calc_a(value_a,Rate_a_c,Rate_a_Rs,Rate_a_in,Rate_a_o)
            assets.append(value_a_sum)
            # print(value_a_sum)
            # print(i)
            if i < Years_l:
                # print(Years_l)
                value_l_sum = calc_l(value_l,Rate_l_sl,Rate_l_m,Rate_l_PL_CD,Rate_l_o)
                liabilities.append(value_l_sum)
                # print(value_l_sum)
                networths.append(value_a_sum - value_l_sum)
                # print(value_a_sum - value_l_sum)
            else :
                networths.append(value_a_sum)
                # print(value_a_sum)
            
        print(" ")
        # print(networths)
        remaining_years = n - Years_l
        liabilities += ["NA"] * remaining_years
        zipped_data = list(zip(networths, assets, liabilities))

        return render(request, 'networth/index.html', {"zipped_data":zipped_data})
    else:
        return redirect('interest_form_view')

def get_networth(request):

    form_data = request.session.get('interest_form_data')

    if form_data:

        value_l = get_liabilities(request)
        value_a = get_assets(request)

        Rate_a_c = form_data.get('cashRate')
        Rate_a_Rs = form_data.get('reRate')
        Rate_a_in = form_data.get('iaRate')
        Rate_a_o = form_data.get('otherRate')

        Rate_l_sl = form_data.get('slRate')
        Rate_l_m = form_data.get('mdRate')
        Rate_l_PL_CD = form_data.get('plRate')
        Rate_l_o = form_data.get('otherRateL')
        Years_l = form_data.get('yearLib')

        def calc_a(value_a, r1,r2,r3,r4):
            value_a_sum = 0
            for (idx,i) in  enumerate(value_a):
                if i["type"] == "cash":
                    value_a[idx]["amt"] += r1 * i["amt"]
                    value_a_sum += value_a[idx]["amt"]
                elif i["type"] == "Real-Estate":
                    value_a[idx]["amt"] += r2 * i["amt"]
                    value_a_sum += value_a[idx]["amt"]
                elif i["type"] == "Investment Accounts":
                    value_a[idx]["amt"] += r3 * i["amt"]
                    value_a_sum += value_a[idx]["amt"]
                else:
                    value_a[idx]["amt"] += r4 * i["amt"]
                    value_a_sum += value_a[idx]["amt"]
            return value_a_sum

        def calc_l(value_l, r1,r2,r3,r4):
            value_l_sum = 0
            for (idx,i) in  enumerate(value_l):
                if i["type"] == "Student-Loan":
                    value_l[idx]["amt"] += r1 * i["amt"]
                    value_l_sum += value_l[idx]["amt"]
                elif i["type"] == "Mortage-debt":
                    value_l[idx]["amt"] += r2 * i["amt"]
                    value_l_sum += value_l[idx]["amt"]
                elif i["type"] == "Credit card/Personal Loan":
                    value_l[idx]["amt"] += r3 * i["amt"]
                    value_l_sum += value_l[idx]["amt"]
                else:
                    value_l[idx]["amt"] += r4 * i["amt"]
                    value_l_sum += value_l[idx]["amt"]
            return value_l_sum
            
        n = 10

        networths = list()
        value_a_sum = 0
        value_l_sum = 0

        for i in range(0,n,1):
            value_a_sum = calc_a(value_a,Rate_a_c,Rate_a_Rs,Rate_a_in,Rate_a_o)
            if Years_l > i:
                value_l_sum = calc_l(value_l,Rate_l_sl,Rate_l_m,Rate_l_PL_CD,Rate_l_o)
                networths.append(value_a_sum - value_l_sum)
            else :
                networths.append(value_a_sum)

        return JsonResponse({'networth_of_10_years':networths},safe=False)

def export_csv_networth(request):
    form_data = request.session.get('interest_form_data')
    if form_data:

        value_l = get_liabilities(request)
        value_a = get_assets(request)
        Rate_a_c = form_data.get('cashRate')
        Rate_a_Rs = form_data.get('reRate')
        Rate_a_in = form_data.get('iaRate')
        Rate_a_o = form_data.get('otherRate')

        Rate_l_sl = form_data.get('slRate')
        Rate_l_m = form_data.get('mdRate')
        Rate_l_PL_CD = form_data.get('plRate')
        Rate_l_o = form_data.get('otherRateL')
        Years_l = form_data.get('yearLib')
    
        def calc_a(value_a, r1,r2,r3,r4):
            value_a_sum = 0
            for (idx,i) in  enumerate(value_a):
                if i["type"] == "cash":
                    value_a[idx]["amt"] += r1 * i["amt"]
                    value_a_sum += value_a[idx]["amt"]
                elif i["type"] == "Real-Estate":
                    value_a[idx]["amt"] += r2 * i["amt"]
                    value_a_sum += value_a[idx]["amt"]
                elif i["type"] == "Investment Accounts":
                    value_a[idx]["amt"] += r3 * i["amt"]
                    value_a_sum += value_a[idx]["amt"]
                else:
                    value_a[idx]["amt"] += r4 * i["amt"]
                    value_a_sum += value_a[idx]["amt"]
            return value_a_sum

        def calc_l(value_l, r1,r2,r3,r4):
            value_l_sum = 0
            for (idx,i) in  enumerate(value_l):
                if i["type"] == "Student-Loan":
                    value_l[idx]["amt"] += r1 * i["amt"]
                    value_l_sum += value_l[idx]["amt"]
                elif i["type"] == "Mortage-debt":
                    value_l[idx]["amt"] += r2 * i["amt"]
                    value_l_sum += value_l[idx]["amt"]
                elif i["type"] == "Credit card/Personal Loan":
                    value_l[idx]["amt"] += r3 * i["amt"]
                    value_l_sum += value_l[idx]["amt"]
                else:
                    value_l[idx]["amt"] += r4 * i["amt"]
                    value_l_sum += value_l[idx]["amt"]
            return value_l_sum

        n = 10
        

        networths = list()
        value_a_sum = 0
        value_l_sum = 0
        assets = list()
        liabilities = list()

        for i in range(0,n,1):
            value_a_sum = calc_a(value_a,Rate_a_c,Rate_a_Rs,Rate_a_in,Rate_a_o)
            assets.append(value_a_sum)
            # print(value_a_sum)
            # print(i)
            if i < Years_l:
                # print(Years_l)
                value_l_sum = calc_l(value_l,Rate_l_sl,Rate_l_m,Rate_l_PL_CD,Rate_l_o)
                liabilities.append(value_l_sum)
                # print(value_l_sum)
                networths.append(value_a_sum - value_l_sum)
                # print(value_a_sum - value_l_sum)
            else :
                networths.append(value_a_sum)
                # print(value_a_sum)
            
        # print(networths)
        liabilities.append("NA")
        liabilities.append("NA")
        liabilities.append("NA")
        liabilities.append("NA")
        zipped_data = list(zip(networths, assets, liabilities))

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=Networths'+\
            str(datetime.datetime.now())+'.csv'
        
        writer = csv.writer(response)
        writer.writerow(['Year','Networth','Asset','Liabilities'])
        row_number=1
        for data in zipped_data:
            writer.writerow([row_number,data[0],data[1],data[2]])
            row_number+=1
        return response   

def stat_view_networth(request):
    return render(request,'networth/statNetworth.html')

def export_excel_networth(request):
    response = HttpResponse(content_type='application/ms-excel') 
    response['Content-Disposition'] = 'attachment; filename=Networth'+\
        str(datetime.datetime.now())+'.xls'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Networth')
    row_num=0
    font_style= xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Year','Networth','Asset','Liabilities']

    for col_num in range(len(columns)):
        ws.write(row_num,col_num,columns[col_num],font_style)
    
    font_style=xlwt.XFStyle()

    form_data = request.session.get('interest_form_data')
    if form_data:

        value_l = get_liabilities(request)
        value_a = get_assets(request)
        Rate_a_c = form_data.get('cashRate')
        Rate_a_Rs = form_data.get('reRate')
        Rate_a_in = form_data.get('iaRate')
        Rate_a_o = form_data.get('otherRate')

        Rate_l_sl = form_data.get('slRate')
        Rate_l_m = form_data.get('mdRate')
        Rate_l_PL_CD = form_data.get('plRate')
        Rate_l_o = form_data.get('otherRateL')
        Years_l = form_data.get('yearLib')

        def calc_a(value_a, r1,r2,r3,r4):
            value_a_sum = 0
            for (idx,i) in  enumerate(value_a):
                if i["type"] == "cash":
                    value_a[idx]["amt"] += r1 * i["amt"]
                    value_a_sum += value_a[idx]["amt"]
                elif i["type"] == "Real-Estate":
                    value_a[idx]["amt"] += r2 * i["amt"]
                    value_a_sum += value_a[idx]["amt"]
                elif i["type"] == "Investment Accounts":
                    value_a[idx]["amt"] += r3 * i["amt"]
                    value_a_sum += value_a[idx]["amt"]
                else:
                    value_a[idx]["amt"] += r4 * i["amt"]
                    value_a_sum += value_a[idx]["amt"]
            return value_a_sum

        def calc_l(value_l, r1,r2,r3,r4):
            value_l_sum = 0
            for (idx,i) in  enumerate(value_l):
                if i["type"] == "Student-Loan":
                    value_l[idx]["amt"] += r1 * i["amt"]
                    value_l_sum += value_l[idx]["amt"]
                elif i["type"] == "Mortage-debt":
                    value_l[idx]["amt"] += r2 * i["amt"]
                    value_l_sum += value_l[idx]["amt"]
                elif i["type"] == "Credit card/Personal Loan":
                    value_l[idx]["amt"] += r3 * i["amt"]
                    value_l_sum += value_l[idx]["amt"]
                else:
                    value_l[idx]["amt"] += r4 * i["amt"]
                    value_l_sum += value_l[idx]["amt"]
            return value_l_sum
        
        n = 10
        Years_l = float(request.GET.get('yearLib'))

        networths = list()
        value_a_sum = 0
        value_l_sum = 0
        assets = list()
        liabilities = list()

        for i in range(0,n,1):
            value_a_sum = calc_a(value_a,Rate_a_c,Rate_a_Rs,Rate_a_in,Rate_a_o)
            assets.append(value_a_sum)
            # print(value_a_sum)
            # print(i)
            if i < Years_l:
                # print(Years_l)
                value_l_sum = calc_l(value_l,Rate_l_sl,Rate_l_m,Rate_l_PL_CD,Rate_l_o)
                liabilities.append(value_l_sum)
                # print(value_l_sum)
                networths.append(value_a_sum - value_l_sum)
                # print(value_a_sum - value_l_sum)
            else :
                networths.append(value_a_sum)
                # print(value_a_sum)
            
        print(" ")
        # print(networths)
        liabilities.append("NA")
        liabilities.append("NA")
        liabilities.append("NA")
        liabilities.append("NA")
        zipped_data = list(zip(networths, assets, liabilities))
        
        
        for row in zipped_data:
            row_num+=1

            for col_num in range(len(row)):
                ws.write(row_num,col_num,str(row[col_num]),font_style)
        wb.save(response)

        return response
            