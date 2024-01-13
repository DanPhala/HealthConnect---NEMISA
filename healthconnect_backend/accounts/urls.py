from django.urls import path
from . import views

urlpatterns = [
    path('signup_patient', views.signup_patient, name="signup_patient"),
    path('signup_doctor', views.signup_doctor , name="signup_doctor"),
    path('doctors', views.get_doctors , name="get_doctors"),
    path('<int:user_id>', views.get_user , name='get_user'),
    path('savedata/<int:user_id>', views.saveddata , name='savedata')
]