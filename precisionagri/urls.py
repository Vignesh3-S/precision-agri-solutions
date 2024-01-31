"""agriproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from precisionagri import views

urlpatterns = [
    path('',views.Home,name= 'home'),
    path('form/',views.Crop,name= 'form'),
    path('result/<crop>/<n>/<p>/<k>/<t>/<h>/<phv>/<r>/',views.Result,name='prediction'),
    path('search/',views.User_search,name='search'),
    path('signup/',views.Signup,name = 'signup'),
    path('signin/',views.Signin,name = 'signin'),
    path('userimg/',views.Img_change,name = 'img'),
    path('userpasswordmsg/',views.Pwd_change_message,name = 'pwdchange'),
    path('userpassword/<str:value>/<str:time>/',views.Password_change,name = 'pwd'),
    path('userprofile/',views.Profile,name = 'profile'),
    path('useredit/',views.User_edit,name = 'edit'),
    path('userlogout/',views.User_logout,name = 'logout'),
    path('useractivity/',views.user_Activity,name = 'activity'),
    path('otp/<str:enc_email>/', views.otp, name='otp'),
    path('getotp/', views.Getotp, name='latergetotp'),
    path('getapikey/', views.Getapi, name='getapikey'),
]
