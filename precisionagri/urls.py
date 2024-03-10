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
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('',views.home,name= 'home'),
    path('form/',views.crop,name= 'form'),
    path('result/<crop>/<n>/<p>/<k>/<t>/<h>/<phv>/<r>/',views.result,name='prediction'),
    path('search/',views.user_search,name='search'),
    path('signup/',views.signup,name = 'signup'),
    path('signin/',views.signin,name = 'signin'),
    path('userimg/',views.img_change,name = 'img'),
    path('userpasswordmsg/',views.pwd_change_message,name = 'pwdchange'),
    path('userpassword/<str:value>/<str:time>/',views.password_change,name = 'pwd'),
    path('userprofile/',views.profile,name = 'profile'),
    path('useredit/',views.user_edit,name = 'edit'),
    path('logout/',auth_views.LogoutView.as_view(),name = 'logout'),
    path('useractivity/',views.user_Activity,name = 'activity'),
    path('otp/<str:enc_email>/', views.otp, name='otp'),
    path('getotp/', views.getotp, name='latergetotp'),
    path('getapikey/', views.getapi, name='getapikey'),
    path('forgotapikey/', views.forgotapi, name='forgotapikey'),
    path('deleteapikey/', views.deleteapi, name='deleteapikey'),
    path('bookreviews/', views.getbooks, name='bookreviews'),
    path('play/<int:id>/',views.playaudio,name = "playaudio"),
    path('mergeaccount/',views.mergeaccountverify,name = "merge"),
    path('mergeaccountsuccess/',views.mergeaccount,name = "mergeaccount"),
]
