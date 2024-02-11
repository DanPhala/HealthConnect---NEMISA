from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.urls import reverse


MESSAGE = "Some Error Occured, Please Try Again."
FORM_DATA = 'application/x-www-form-urlencoded'
JSON_DATA = 'application/json'
HOME_TEMPLATE = 'index.html'


def home(request):
    if request.method == 'GET':
        if request.session.get('is_authenticated') is not None and request.session.get('is_authenticated') == True and request.session.get('user_type') is not None and request.session.get('name') is not None:
            if request.session.get('user_type') == 'Admin User' and request.session.get('name') == 'Admin User':
                return redirect('admin-dashboard.html')
            else:
                return render(request, 'posts.html')
        else:
            return render(request, 'index.html')
    else:
        return redirect('')


def home_id(request, fragment):
    if request.method == 'GET':
        url = reverse('home') + f'#{fragment}'
        return redirect(url)
    else:
        return redirect('')
#@Tebogo please help,move this as needed
def consultation_home(request):

    if request.method == 'GET':
    
            return render(request, 'consultations/consultation.html')

    else:
        return redirect('home')
    
def self_diagnose(request):

    if request.method == 'GET':
    
            return render(request, 'consultations/selfdiagnose.html')

    else:
        return redirect('home')
    

    
#--------------------------------------------#
# TEMPORARY ROUTES FOR TESTING PURPOSES ONLY
#--------------------------------------------#

def sendmail(request):

    return home_id(request, 'contact')
 

def calendar(request):

    if request.method == 'GET':
    
            return render(request, 'schedule.html')

    else:
        return redirect('home')

def page(request):

    if request.method == 'GET':
    
            return render(request, 'consultation-chats.html')

    else:
        return redirect('home')

def help(request):

    if request.method == 'GET':

        return render(request, 'help.html')

    else:
        return redirect('home')

    
def contact(request):

    if request.method == 'GET':

        return render(request, 'contact.html')

    else:
        return redirect('home')
    
    
def admin_page(request):

    if request.method == 'GET':

        return render(request, 'admin-dashboard.html')

    else:
        return redirect('home')

 
def register(request):

    if request.method == 'GET':

        return render(request, 'pages-register.html')

    else:
        return redirect('home')
    
    
def login(request):

    if request.method == 'GET':

        return render(request, 'pages-login.html')

    else:
        return redirect('home')

    
def login_temp(request):

    print("Form Submists Successfully")
    return redirect('home')