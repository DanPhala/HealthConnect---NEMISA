from datetime import datetime, time
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.urls import reverse
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from .form import PatientCreateForm, DoctorCreateForm
from ..utils import utils
import requests, logging, json, os

MESSAGE = "Some Error Occured, Please Try Again."
CONSULTATION_TEMPLATE = 'patient/consult_a_doctor/consult_a_doctor.html'
JSON_DATA = 'application/json'


def signup_patient(request):
    
    stored_messages = messages.get_messages(request)
    for message in stored_messages:
        pass
    
    if request.method == 'POST':
        
        try:
            temp_form = PatientCreateForm(request.POST)
            
            if temp_form.is_valid():
                request_data = {
                    'email': temp_form.cleaned_data['email'],
                    'password': temp_form.cleaned_data['password'],
                    'name': temp_form.cleaned_data['name'],
                    'surname': temp_form.cleaned_data['surname'],
                    'dob': datetime.combine(temp_form.cleaned_data['dob'], time(10, 0)).strftime('%Y-%m-%dT%H:%M'),
                    'address': temp_form.cleaned_data['address'],
                    'mobile_no': temp_form.clean_mobile_no(),
                    'gender': temp_form.cleaned_data['gender'],
                }
                
                request_data = json.dumps(request_data, indent=4, ensure_ascii=False)
                headers = { 'Content-Type': JSON_DATA, }
                
                api_url = os.getenv("API_ENDPOINT") + '/users/signup_patient'
                response = requests.post(api_url, data=request_data, headers=headers)
                response.raise_for_status()
                
                if response.status_code == 201:
                    api_response = response.json()
                    if api_response.get('status') == "success":
                        messages.info(request, "Account created Successfully")
                        return redirect(reverse('login'))
                    
                    else:
                        messages.info(request, api_response.get('data'))
                        return render(request,'pages-register.html')
            
            messages.info(request, MESSAGE)
            return render(request,'pages-register.html')
    
        except requests.RequestException as e:
            temp_message = ""
            try:
                api_response = response.json()
                temp_message = api_response.get('data')
            except Exception as e:
                temp_message = "Please Make Sure All Required Fields are Filled Out Correctly"
                
            messages.info(request, temp_message)
            return render(request,'pages-register.html')

    else:
        return render(request,'pages-register.html')


def signup_doctor(request):
    
    stored_messages = messages.get_messages(request)
    for message in stored_messages:
        pass
    
    if request.method == 'POST':
        
        try:
            temp_form = DoctorCreateForm(request.POST)
            
            if temp_form.is_valid():
                request_data = {
                    'email': temp_form.cleaned_data['email'],
                    'password': temp_form.cleaned_data['password'],
                    'name': temp_form.cleaned_data['name'],
                    'surname': temp_form.cleaned_data['surname'],
                    'dob': datetime.combine(temp_form.cleaned_data['dob'], time(10, 0)).strftime('%Y-%m-%dT%H:%M'),
                    'address': temp_form.cleaned_data['address'],
                    'mobile_no': temp_form.clean_mobile_no(),
                    'gender': temp_form.cleaned_data['gender'],
                    'qualification': temp_form.cleaned_data['qualification'],
                    'registration_no': temp_form.cleaned_data['registration_no'],
                    'year_of_registration': datetime.combine(temp_form.cleaned_data['year_of_registration'], time(10, 0)).strftime('%Y-%m-%dT%H:%M'),
                    'state_medical_council': temp_form.cleaned_data['state_medical_council'],
                    'specialization': temp_form.cleaned_data['specialization'],
                }
                
                api_url = os.getenv("API_ENDPOINT") + '/users/signup_doctor'
                
                request_data = json.dumps(request_data, indent=4, ensure_ascii=False)
                headers = {
                    'Content-Type': JSON_DATA,
                }
                
                response = requests.post(api_url, data=request_data, headers=headers)
                response.raise_for_status()
                
                if response.status_code == 201:
                    api_response = response.json()
                    if api_response.get('status') == "success":
                        messages.info(request, "Account created Successfully")
                        return redirect(reverse('login'))
                    
                    else:
                        messages.info(request, api_response.get('data'))
                        return render(request,'pages-register.html')
            
            messages.info(request, MESSAGE)
            return render(request,'pages-register.html')
            
        except requests.RequestException as e:
            temp_message = ""
            try:
                api_response = response.json()
                temp_message = api_response.get('data')
            except Exception as e:
                temp_message = "Please Make Sure All Required Fields are Filled Out Correctly"
                
            messages.info(request, temp_message)
            return render(request,'pages-register.html')
        
    else:
        return render(request,'pages-register.html')


def get_user(request):

    stored_messages = messages.get_messages(request)
    for message in stored_messages:
        pass
    
    if (request.method == 'GET' or request.method == 'POST') and not request.session.get('is_admin'):
        
        try:
            user_id = request.session.get('user_id')
                
            jwt_token = request.session.get('access_token')
            token_type = request.session.get('token_type')

            api_url = os.getenv("API_ENDPOINT") + f'/users/{user_id}'

            headers = { "Content-Type": JSON_DATA, "Authorization": f"{token_type} {jwt_token}",}

            response = requests.post(api_url, headers=headers)
            response.raise_for_status()
            
            if response.status_code == 200:
                api_response = response.json()
                if api_response.get('status') == "success":

                    response_data = api_response.get('data')
                    
                    response_data["user"]["created_at"] = utils.format_date(response_data["user"]["created_at"])
                    response_data["details"]["dob"] = utils.format_date(response_data["details"]["dob"])
                    mobile = response_data["details"]["mobile_no"] 
                    response_data["details"]["mobile_no"] = f'0{mobile}'
                    
                    return render(request, 'users-profile.html', { 'profile_data': response_data })

            
            messages.error(request, f"Error Occured When Requesting for Doctors Data, User Id: {user_id}")
                
        except requests.RequestException as e:
            temp_message = ""
            try:
                api_response = response.json()
                temp_message = api_response.get('data')
            except Exception as e:
                temp_message = f"Error Occured When Requesting User Data, User Id: {user_id}"
                
            messages.info(request, temp_message)

    messages.error(request, "Could not retrieve user information.")
    return render(request, 'users-profile.html', { 'profile_data': utils.get_random_user() })


def savedata(request, user_id):
    
    stored_messages = messages.get_messages(request)
    for message in stored_messages:
        pass
    
    if request.method == 'POST':
        
        try:
            param_id = user_id
            user_id = request.session.get('user_id')
            
            if param_id == user_id:

                jwt_token = request.session.get('access_token')
                token_type = request.session.get('token_type')
                
                api_url = os.getenv("API_ENDPOINT") + f'/users/savedata/{user_id}'
                
                headers = {
                    'Content-Type': JSON_DATA,
                    "Authorization": f"{token_type} {jwt_token}",
                }
                
                request_data = {
                    "name": request.POST['name'],
                    "surname": request.POST['surname'],
                    "address": request.POST['address'],
                    "mobile_no": request.POST['mobile_no']
                }
                
                response = requests.put(api_url, json=request_data, headers=headers)
                response.raise_for_status()
                
                if response.status_code == 200:
                    api_response = response.json()
                    
                    if api_response.get('status') == "success":

                        if api_response.get('name')[:2].lower() == 'dr':
                            return reverse('doctor_profile', args=[user_id])
                        else:
                            return redirect(reverse('patient_profile', args=[user_id]))

                messages.info(request, MESSAGE)
                return redirect(reverse('patient_profile', args=[user_id]))            
            
            else:
                messages.error(request, "Incorrect User Id used.")

        except requests.RequestException as e:
            temp_message = ""
            try:
                api_response = response.json()
                temp_message = api_response.get('data')
            except Exception as e:
                temp_message = f"Error Occured When Updating User Data, User Id: {user_id}"
                
            messages.error(request, temp_message)
            return None
        
    else:
        return redirect(reverse('doctor_profile', args=[user_id]))
    
