# from django.shortcuts import render,redirect
# from django.views import View
# from django.contrib.auth.models import User
# from django.contrib import messages
# from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
# from django.utils.encoding import force_bytes,force_str,DjangoUnicodeDecodeError
# from django.contrib.sites.shortcuts import get_current_site
# from .utils import token_generator
# from django.contrib import auth
# from django.core.mail import send_mail
# from wealth_harbour import settings
# from django.urls import reverse
# # Create your views here.

# class login(View):
#     def get(self, request):
#         return render(request, 'authentication/login.html')

#     def post(self, request):
#         username = request.POST.get('username')
#         password = request.POST.get('password')

#         if username and password:
#             user = auth.authenticate(username=username, password=password)

#             if user:
#                 auth.login(request, user)
#                 return redirect('/')
#             else:
#                 error_message = "Invalid username or password."
#                 return render(request, 'authentication/login.html', {'error_message': error_message})
#         else:
#             error_message = "Both username and password are required."
#             return render(request, 'authentication/login.html', {'error_message': error_message})    

# class register(View):
#     def get(self,request):
#         return render(request,'authentication/register.html')
    
#     def post(self,request):
#         username = request.POST['username']
#         email = request.POST['email']
#         password = request.POST['password']

#         context={
#             'fieldValues':request.POST
#         }

#         if not User.objects.filter(username=username).exists():
#             #if not User.objects.filter(email=email).exists():
#                 if len(password)<6:
#                     messages.error(request,'password too short')
#                     return render(request,'authentication/register.html',context)

#                 user = User.objects.create_user(username=username,email=email)
#                 user.set_password(password)
#                 # user.set_active = False
#                 user.save()
#                 # email_subject='Activate your account'
#                 # email_body='Test Body'
#                 # email = EmailMessage(
#                 #     email_subject,
#                 #     email_body,
#                 #     'dhruvsolanki5604@gmail.com',
#                 #     [email],
#                 #     )
#                 # email.send(fail_silently=False)

#                 # uidb64= urlsafe_base64_encode(force_bytes(user.pk))

#                 # domain = get_current_site(request).domain
#                 # link= reverse('activate',kwargs={
#                 #     'uidb64':uidb64,'token':token_generator.make_token(user)
#                 # })

#                 # activate_url = 'http://'+domain+link

#                 # subject = "Actiavate your account"
#                 # message = "Hi "+ user.username+" Please use this link to verify your accout\n"+activate_url
#                 # from_email = settings.EMAIL_HOST_USER
#                 # to_list = [email]
#                 # send_mail(subject, message, from_email, to_list, fail_silently=True)


#                 messages.success(request,"account successsfully Created ")
#                 return render(request,'authentication/login.html')    

#         return render(request,'authentication/register.html') 
    
# class LogoutView(View):
#     def post(self,request):
#         auth.logout(request)
#         messages.success(request,"you have been logged out")
#         return redirect('login')    

from django.shortcuts import render,redirect
from django.views import View
import json
from django.http import JsonResponse
from django.contrib.auth.models import User
from validate_email import validate_email
from django.contrib import messages
from wealth_harbour import settings
from django.urls import reverse
from django.core.mail import send_mail
from django.utils.encoding import force_bytes,force_str,DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from .utils import token_generator
from django.contrib import auth
from urllib.parse import urlparse
from django.template import RequestContext

# Create your views here.
class EmailValidationView(View):
    def post(self,request): 
        data=json.loads(request.body)
        email=data['email']

        if not validate_email(email):
            return JsonResponse({'email_error' : 'Email is invalid'},status=400)
        # if User.objects.filter(email=email).exists():
        #     return JsonResponse({'email_error' : 'Email is already taken'},status=409)
        
        return JsonResponse({'email_valid':True})
    
class UsernameValidationView(View):
    def post(self,request): 
        data=json.loads(request.body)
        username=data['username']

        if not str(username).isalnum():
            return JsonResponse({'username_error' : 'username should only contains alphanumeric characters'},status=400)
        if User.objects.filter(username=username).exists():
            return JsonResponse({'username_error' : 'username is already taken'},status=409)
        
        return JsonResponse({'username_valid':True})    

class RegistrationView(View):
    def get(self,request):
        return render(request,'authentication/register.html')

    def post(self,request):
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        context={
            'fieldValues':request.POST
        }

        if not User.objects.filter(username=username).exists():
            #if not User.objects.filter(email=email).exists():
                if len(password)<6:
                    messages.error(request,'password too short')
                    return render(request,'authentication/register.html',context)

                user = User.objects.create_user(username=username,email=email)
                user.set_password(password)
                user.set_active = False
                user.save()
                # email_subject='Activate your account'
                # email_body='Test Body'
                # email = EmailMessage(
                #     email_subject,
                #     email_body,
                #     'dhruvsolanki5604@gmail.com',
                #     [email],
                #     )
                # email.send(fail_silently=False)

                uidb64= urlsafe_base64_encode(force_bytes(user.pk))

                domain = get_current_site(request).domain
                link= reverse('activate',kwargs={
                    'uidb64':uidb64,'token':token_generator.make_token(user)
                })

                activate_url = 'http://'+domain+link

                subject = "Actiavate your account"
                message = "Hi "+ user.username+" Please use this link to verify your accout\n"+activate_url
                from_email = settings.EMAIL_HOST_USER
                to_list = [email]
                send_mail(subject, message, from_email, to_list, fail_silently=True)


                messages.success(request,"account successsfully Created ")
                return render(request,'authentication/login.html')
        else:
            messages.success(request,"Username already taken! ")
            return render(request,'authentication/register.html')    

        return render(request,'authentication/register.html')

class VerificationView(View):
    def get(self,request,uidb64,token):
        try:
            id =  force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=id)

            if token_generator.check_token(user,token):
                return redirect('login'+'?message'+'User already activated')

            if user.is_active:
                return redirect('login')
            user.is_active =True
            user.save()

            messages.success('Account activated successfully')    
            return redirect('login')
        
        except Exception as ex:
            pass

        return redirect('login')    
    
class LoginView(View):

    def __init__(self, **kwargs: json) -> None:
        super().__init__(**kwargs)
        

    def get(self,request):
        return render(request,'authentication/login.html')
    
    def post(self,request):
        username = request.POST['username']
        password = request.POST['password']
        

        if username and password:
            user = auth.authenticate(username=username,password=password)

            if user:
                if user.is_active:
                    auth.login(request,user)
                    # messages.success(request, 'Welcome ' + user.username + ' You are logged in.')
                    next_url = request.GET.get('next')
                    current_url = request.build_absolute_uri()
                    if 'wealthchat' in current_url:
                        return redirect('homeWealth')
                    else:
                        return redirect('indexHome')

                messages.error(
                    request,'Account is not activate,please check your email')
                return render(request,'authentication/login.html')    

            messages.error(
                request,'Invalid credentials,try again')
            return render(request,'authentication/login.html')
        
        messages.error(
                request,'please fill all fields')
        return render(request,'authentication/login.html')
    
class LogoutView(View):
    def get(self,request):
        auth.logout(request)
        messages.success(request,"you have been logged out")
        return redirect('login')
    
    def post(self,request):
        auth.logout(request)
        messages.success(request,"you have been logged out")
        return redirect('login')