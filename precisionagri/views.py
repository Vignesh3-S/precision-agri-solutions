from django.shortcuts import render,redirect
from .models import Agriculture,NPK,User,Search,ApiUser
from .form import (CropRecommendform,Queryform,Searchform,Loginform,Signupform,
                    Userimgform,Userupdateform,PasswordChangeForm,Emailform,ForgotApiForm,FeedbackForm)
from django.contrib import messages
from .prediction import cropprediction
from django.core.mail import send_mail
from django.contrib.auth import authenticate,login
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
import requests
import random
import string
from datetime import datetime
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.hashers import check_password


# mobile number validate
def mobile_validate(request,mobile):
    if (mobile[0] not in ['6','7','8','9']) or (not mobile.isdigit()):
        messages.error(request,'Enter a valid mobile number.')
        return False
    else:
        return mobile
# home part
def home(request):
    if request.method == 'POST':
       form = Queryform(request.POST)
       name = request.POST['Name']
       email = request.POST['email']
       mess = request.POST['message']
       if form.is_valid():
            form.save()
            message = "Hi this is "+name+" .My query is "+mess+" .Please solve this query and share the solution via "+email+" ."
            send_mail('Query Message',message,'brsapp33@gmail.com',['sasiguruvignesh@gmail.com',],fail_silently=False)
            return redirect(reverse('home',messages.success(request,'Message sent successfully.')),permanent=True)
       else:
            return redirect(reverse('home',messages.error(request,'Oops an error occured! Please try again.')),premanent=True)
    try:
        user = User.objects.get(email= request.user.email)
        userimg = user.userimg
        return render(request,'precisionagri/home.html',{'query':Queryform,'userimg':userimg})
    except:
        return render(request,'precisionagri/home.html',{'query':Queryform})

# Registration part
def signup(request):
    if request.method == 'POST':
        form = Signupform(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            #recv_mobile_0 = request.POST['mobile_0']
            recv_mobile_1 = request.POST['mobile_1']
            recv_password = form.cleaned_data['password']
            recv_confirm_password = form.cleaned_data['confirm_password']

            check_mobile = mobile_validate(request,recv_mobile_1)
             
            if not check_mobile:
                return redirect('signup',permanent=True)
            
            if recv_password != recv_confirm_password:
                return redirect(reverse('signup',messages.error(request,'Password and Confirm Password mismatched.')),permanent=True)
            
            user = form.save(commit=False)
            user.set_password(recv_password)
            user.is_PAS_account = True
            user.save()
            encode_email = urlsafe_base64_encode(force_bytes(email))
            return redirect('otp',encode_email,permanent=True)
        else:
            error = form.errors 
            return redirect(reverse('signup',messages.error(request,error)),permanent=True)
    return render(request,'precisionagri/signup.html',{'form':Signupform})

# Generate otp
def otp(request,enc_email):
    decrypt_email =  urlsafe_base64_decode(force_str(enc_email))
    email = decrypt_email.decode()
    if request.method == "GET":
        otp = str(random.randint(100000, 999999))
        try:
            user = User.objects.get(email=email)
            user.otp = otp
            user.save()
            message =f'Hello this is from Precision Agriculture Solutions. This is your otp {otp}.'
            send_mail('One Time Password',message,'brsapp33@gmail.com',[email],fail_silently=False)
            messages.success(request,'Enter the OTP sent to your email.')
            return render(request,'precisionagri/otp.html')
        except:
            return redirect(reverse('signup',messages.error(request,'OTP generate error')),permanent=True)
    if request.method == "POST":
        otp = request.POST['otp']
        #type(otp)
        user = User.objects.get(email=email)
        if user.otp == otp:
            user.is_account_verified = True
            user.save()
            return redirect(reverse('signin',messages.success(request,'Verifiction Successful')),permanent=True)
        else:
            return redirect(reverse('signup',messages.error(request,'Invalid OTP')),permanent=True)
# Verify Account
def getotp(request):
    if request.method=='POST':
        form=Emailform(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = User.objects.get(email = email)
            except:
                return redirect(reverse('signup',messages.error(request,"Account not Registered. Please signup first.")))
            if not user.is_PAS_account:
                return redirect(reverse('signup',messages.info(request,"Third party accounts not need to be verify.")))
            if not user.is_account_verified:
                encode_email = urlsafe_base64_encode(force_bytes(email))
                return redirect('otp',encode_email,permanent=True)
            else:
                return redirect(reverse('home',messages.info(request,"This account already verified.")))
        else:
            error = form.errors
            return redirect(reverse('latergetotp',messages.error(request,error)))
    return render(request,'precisionagri/pwdchange.html',{'form2':Emailform})


#login part
def signin(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            return redirect(reverse('home',messages.error(request,"Account already signed in.")),permanent=True)
    if request.method == 'POST':
        form = Loginform(request.POST)
        if form.is_valid():
            useremail = form.cleaned_data['email']
            userpwd = form.cleaned_data['password']
            next = request.POST['next']
            try:
                user = User.objects.get(email = useremail)                    
                if not user.is_account_verified:
                    return redirect(reverse('home',messages.error(request,'Account not verified.')),permanent=True)
                if not user.is_PAS_account:
                    return redirect(reverse('home',messages.error(request,'Invalid Account.')),permanent=True)
                if user.is_active:
                    person = authenticate(request,email = useremail,password = userpwd)
                    if person is not None:
                        login(request,person)
                        if next:
                            return redirect(next,permanent=True)
                        if user.is_superuser:
                            return redirect('/pasadmin/',permanent=True)
                        else:
                            return redirect(reverse('home',messages.success(request,'Login successfully.')),permanent=True)
                    else:
                        return redirect(reverse('signin',messages.error(request,"Enter Valid Credentials.")),permanent=True)
                else:
                    return redirect(reverse('signin',messages.error(request,'Sorry! Your account has been de-activated.')),permanent=True)
            except:
                return redirect(reverse('signin',messages.error(request,'Invalid User.')),permanent=True)
        else:
            error = form.errors
            return redirect(reverse('signin',messages.error(request,error)),permanent=True)
    return render(request,'precisionagri/signin.html',{'form':Loginform})

# view profile
@login_required(login_url = 'signin')
def profile(request):
    if request.method == "GET":
        user = User.objects.get(email = request.user.email)
        if user.userimg:
            data = {'email':user.email,'name':user.username,'state':user.state,'district':user.district,'native':user.native,'mobile':user.mobile,
                    'join':user.date_joined,'update':user.date_updated,'login':user.last_login,'img':user.userimg}
        else:
            data = {'email':user.email,'state':user.state,'district':user.district,'native':user.native,'mobile':user.mobile,
                    'join':user.date_joined,'update':user.date_updated,'login':user.last_login,'name':user.username}
        return render(request,'precisionagri/user_profile.html',data)
    
# Edit profile
@login_required(login_url = 'signin')
def user_edit(request):
    if request.method == 'POST':
        form = Userupdateform(request.POST)
        if form.is_valid():
            recv_mobile_1 = request.POST['mobile_1']
            recv_state = form.cleaned_data['state']
            recv_name = form.cleaned_data['username']
            recv_district = form.cleaned_data['district']
            recv_native = form.cleaned_data['native']
            
            check_mobile = mobile_validate(request,recv_mobile_1)
             
            if not check_mobile:
                return redirect('edit',permanent=True)
            
            mob_number = request.POST['mobile_0']+recv_mobile_1
            user = User.objects.get(email = request.user.email)
            user.state,user.username,user.district,user.native,user.mobile = recv_state,recv_name,recv_district,recv_native,mob_number 
            user.save()
            return redirect(reverse('profile',messages.success(request,'Updated Successfully.')),permanent=True)
        else:
            error = form.errors 
            return redirect(reverse('edit',messages.error(request,error)),permanent=True)
    return render(request,'precisionagri/useredit.html',{'form':Userupdateform})

# User activity
@login_required(login_url='signin')
def user_Activity(request): 
    if request.method == "GET":
        agriuser = Agriculture.objects.filter(user = request.user.id)
        searchuser = Search.objects.filter(user = request.user.id)
        return render(request,'precisionagri/activity.html',{'data1':agriuser,'data2':searchuser})

# User Image Change
@login_required(login_url = 'signin')
def img_change(request):
    if request.method == 'POST':
        form = Userimgform(request.FILES)
        if form.is_valid():
            user = User.objects.get(email = request.user.email)
            if user.userimg:
                user.userimg.delete()
                user.userimg = request.FILES['image']
                user.save()
            else:
                user.userimg = request.FILES['image']
                user.save()
            return redirect(reverse('profile',messages.success(request,'Profile picture successfully changed.')),permanent=True)
        elif not form.is_valid():
            error = form.errors
            return redirect(reverse('profile',messages.error(request,error)),permanent=True)
    return render(request,'precisionagri/imgupload.html',{'form':Userimgform})

# crop recommend form part
@login_required(login_url = 'signin')
def crop(request):
    context = {'agriform':CropRecommendform}
    if request.method == "POST":
        form = CropRecommendform(request.POST)
        if form.is_valid():
            nit = float(request.POST['Nitrogen'])
            pho = float(request.POST['Phosphorous'])
            pot = float(request.POST['Potassium'])
            temp = float(request.POST['Temperature'])
            humidity = float(request.POST['Humidity'])
            ph = float(request.POST['PH'])
            rain = float(request.POST['Rainfall'])
            if (nit < 0 or pho < 0 or pot < 0 or temp < 0 or humidity < 0 or ph < 0 or rain < 0):
                return redirect(reverse('form',messages.error(request,'Input values must be a positive number.')),permanent=True)
            if (nit == 0 or pho == 0 or pot == 0 or temp == 0 or humidity == 0 or ph == 0 or rain == 0):
                return redirect(reverse('form',messages.error(request,'Input values must be greater than zero.')),permanent=True)
            if (len(str(nit)) > 25 or len(str(pho)) > 25 or len(str(pot)) > 25 or len(str(temp)) > 25 or len(str(humidity)) > 25 or len(str(ph)) > 25 or len(str(rain)) > 25):
                return redirect(reverse('form',messages.error(request,'Input values length must be within or equal to 25.')),permanent=True)
            store = Agriculture.objects.filter(Nitrogen = nit, Phosphorous = pho, Potassium = pot, Temperature = temp, Humidity = humidity, PH = ph, Rainfall = rain)
            n=urlsafe_base64_encode(force_bytes(nit))
            p=urlsafe_base64_encode(force_bytes(pho))
            k=urlsafe_base64_encode(force_bytes(pot))
            t=urlsafe_base64_encode(force_bytes(temp))
            h=urlsafe_base64_encode(force_bytes(humidity))
            phv=urlsafe_base64_encode(force_bytes(ph))
            r=urlsafe_base64_encode(force_bytes(rain))
            if store:
                stored_crop = store.first()
                crop = stored_crop.Crop_Label
                enc_crop=urlsafe_base64_encode(force_bytes(crop))
                return redirect('prediction',enc_crop,n,p,k,t,h,phv,r,permanent=True)
            else:
                results = cropprediction([nit,pho,pot,temp,humidity,ph,rain])
                a = Agriculture.objects.create(user = User.objects.get(id = request.user.id),Nitrogen = nit, Phosphorous = pho, Potassium = pot, Temperature = temp, Humidity = humidity, PH = ph, Rainfall = rain, Crop_Label = results)
                a.save()
                enc_result=urlsafe_base64_encode(force_bytes(results))
                return redirect('prediction',enc_result,n,p,k,t,h,phv,r,permanent=True)
    return render(request,'precisionagri/crop.html',context)

# Crop Recommend Result Part
@login_required(login_url = 'signin')
def result(request,crop,n,p,k,t,h,phv,r):
    crop=urlsafe_base64_decode(force_str(crop))
    crop_decode=crop.decode()
    n=float(urlsafe_base64_decode(force_str(n)))
    p=float(urlsafe_base64_decode(force_str(p)))
    k=float(urlsafe_base64_decode(force_str(k)))
    t=float(urlsafe_base64_decode(force_str(t)))
    h=float(urlsafe_base64_decode(force_str(h)))
    ph=float(urlsafe_base64_decode(force_str(phv)))
    r=float(urlsafe_base64_decode(force_str(r)))
    crop_dict = {'crop':crop_decode,'n':n,'p':p,'k':k,'t':t,'h':h,'ph':ph,'r':r}
    return render(request,'precisionagri/result.html',crop_dict) 

# Crop NPK Search
@login_required(login_url = 'signin')
def user_search(request):
    if request.method == 'POST':
        query = request.POST['search']
        querylower = query.lower()
        try:
            cropname = NPK.objects.get(Crop_Name = query)
            n = cropname.Std_nitrogen
            p = cropname.Std_phosphorus
            k = cropname.Std_potassium
            user = User.objects.get(email = request.user.email)
            Search.objects.create(user = user, Crop_Name = cropname)
            return render(request,'precisionagri/searchtl.html',{'nitrogen' : n,'phosphorous':p,'potassium':k, 'crop': querylower})
        except ObjectDoesNotExist:
            return redirect(reverse('search',messages.error(request,'Select a valid crop')),permanent=True)
    return render(request,'precisionagri/search.html',{'forms':Searchform})

# Password handling part -- Message sending
def pwd_change_message(request):
    if request.method == "POST":
        time = datetime.now()
        time_str = time.strftime("%Y")+time.strftime("%m")+time.strftime("%d")+time.strftime("%H")+time.strftime("%M")+time.strftime("%S")
        timestamp = urlsafe_base64_encode(force_bytes(time_str))
        site = get_current_site(request)
        form = Emailform(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = User.objects.get(email = email)
            except:
                return redirect(reverse('pwdchange',messages.error(request,'There is no account with this email. Please give your registered email')),permanent=True)
            if user.is_active == True:
                if user.is_PAS_account == True:
                    encrypted_email = urlsafe_base64_encode(force_bytes(email)) 
                    message =f'''Hello this is from Precision Agriculture Solutions. Your can use the below link to change the password of your PAS account. link : '{request.scheme}://{site.domain}/userpassword/{encrypted_email}/{timestamp}/'. Don"t reply to this email.'''
                    send_mail('Email changing link',message,'brsapp33@gmail.com',[email],fail_silently=False)
                    return redirect(reverse('pwdchange',messages.info(request,'Check email and follow the link for changing your password.')),permanent=True)
                else:
                    return redirect(reverse('pwdchange',messages.error(request,'Invalid Email. This email registered using third party.')),permanent=True)
            else:
                return redirect(reverse('pwdchange',messages.error(request,'De-active Account.')),permanent=True)
    return render(request,'precisionagri/emailmsg.html',{'form':Emailform})

#Password handing part -- change password 
def password_change(request,value,time):
    decrypt_email =  urlsafe_base64_decode(force_str(value)) 
    times = datetime.now()
    time_str = times.strftime("%Y")+times.strftime("%m")+times.strftime("%d")+times.strftime("%H")+times.strftime("%M")+times.strftime("%S")
    decrypt_time = urlsafe_base64_decode(force_str(time))
    
    if(int(time_str)-int(decrypt_time)) > 300:
        return redirect(reverse('home',messages.error(request,'Link expired.')),permanent=True)
    
    try:
        str_decrypt_email = str(decrypt_email,encoding='utf-8')
    except:
        return redirect(reverse('home',messages.error(request,'Invalid Link.')),permanent=True)
    
    try:
        user = User.objects.get(email = str_decrypt_email)
    except:
        return redirect(reverse('home',messages.error(request,'Invalid User.')),permanent=True)
    
    if request.method == "POST":    
        form = PasswordChangeForm(request.POST)
        if form.is_valid():
            pwd = form.cleaned_data['password']
            confirm_pwd = form.cleaned_data['confirm_password']
            if pwd != confirm_pwd:
                messages.error(request,'Password and Confirm Password mismatched.')
            user = User.objects.get(email = str_decrypt_email)
            user.set_password(pwd)
            user.save()
            return redirect(reverse('signin',messages.success(request,'password changed successfully.')),permanent=True)
        else:
            error = form.errors
            return messages.error(request,error)
    return render(request,'precisionagri/pwdchange.html',{'form':PasswordChangeForm})


@login_required(login_url = 'signin')
def getapi(request):
    if request.method == "POST":
        encode_email = urlsafe_base64_encode(force_bytes(request.user.email))
        key = ''.join(random.choices(string.ascii_lowercase +string.digits, k=35))
        apikey = f'{request.scheme}://{request.get_host()}/getapicrop/{encode_email}/'
        try:
            usercreate = ApiUser.objects.create(user=request.user,apikey=key,app_name=request.POST['app_name'],app_type=request.POST['app_type'],token_valid=True)
            usercreate.save()
            return render(request,'precisionagri/showapi.html',{'url':apikey,'token':key,'name':request.user})
        except:
            return redirect(reverse('home',messages.info(request,"Already got Apikey")))
    if request.method == "GET":
        user = User.objects.get(email = request.user.email)
        #print(user.count)
        if user.count < 2:
            return render(request,'precisionagri/apiform.html')
        else:
            return redirect(reverse('home',messages.info(request,"Sorry!, Maximum count reached")))
    
@login_required(login_url="signin")
def forgotapi(request):
    if request.method == "GET":
        return render(request,'precisionagri/forgotapi.html',{'form':ForgotApiForm})
    if request.method == "POST":
        form = ForgotApiForm(request.POST)
        try:
            user = User.objects.get(email=request.user.email)
            apiuser = ApiUser.objects.get(user = user.id)
        except:
            return redirect(reverse('forgotapi',messages.error(request,'Invalid user')),permanent=True)
        if form.is_valid():
            password = form.cleaned_data['password']
            name = form.cleaned_data['app_name']
            type = form.cleaned_data['app_type']
            if (check_password(password,user.password)) and (apiuser.app_type == type) and (apiuser.app_name == name):
                encode_email = urlsafe_base64_encode(force_bytes(request.user.email))
                apiurl = f'{request.scheme}://{request.get_host()}/getbookreviews/{encode_email}/'
                return render(request,'precisionagri/showapi.html',{'value':apiuser.apikey,'url':apiurl,'username':user.username})
            else:
                return redirect(reverse('forgotapi',messages.error(request,'Invalid credentials')),permanent=True)
        else:
            return redirect(reverse('forgotapi',messages.error(request,form.errors)),permanent=True)

@login_required(login_url="signin")
def deleteapi(request):
    if request.method == "GET":
        return render(request,'precisionagri/deleteapi.html',{'form':ForgotApiForm})
    if request.method == "POST":
        form = ForgotApiForm(request.POST)
        try:
            user = User.objects.get(email=request.user.email)
            apiuser = ApiUser.objects.get(user = user.id)
        except:
            return redirect(reverse('forgotapi',messages.error(request,'Invalid user')),permanent=True)
        if form.is_valid():
            password = form.cleaned_data['password']
            name = form.cleaned_data['app_name']
            type = form.cleaned_data['app_type']
            if (check_password(password,user.password)) and (apiuser.app_type == type) and (apiuser.app_name == name):
                ApiUser.objects.get(user=user.id,app_name=name,app_type=type).delete()
                user.count += 1
                user.save()
                return redirect(reverse('home',messages.success(request,'API token deleted successfully.')),permanent=True)
            else:
                return redirect(reverse('deleteapi',messages.error(request,'Invalid user')),permanent=True)
        else:
            return redirect(reverse('deleteapi',messages.error(request,form.errors)),permanent=True)

@login_required(login_url="signin")
def getbooks(request,id):
    if request.method == "GET":
        books = requests.get(f" https://book-reviews-app-ca75.onrender.com/getbookreviews/c2FzaWd1cnV2aWduZXNoQGdtYWlsLmNvbQ/pz6kx2341p8nac3cjtlzb5ffa7esu1zki6m/?page={id}")
        if books.status_code == 404:
            return redirect(reverse('home',messages.error(request,'Invalid User')),permanent=True)
        else:
            res_data = books.json()
            book_data = res_data['results']
            next_number = None
            pre_number = None
            next_page = str(res_data['next'])
            pre_page = str(res_data['previous'])
            if next_page != None:
                try:
                    next_page_split = next_page.split("=")
                    next_number = int(next_page_split[-1])
                except:
                    pass
            if pre_page != None:
                try:
                    pre_page_split = pre_page.split("=")
                    pre_number = int(pre_page_split[-1])
                except:
                    if next_number == None:
                        pre_number = 1
                    else:
                        pre_number = next_number - 2
            return render(request,'precisionagri/book_collection.html',{"data":book_data,'pag':res_data,'next_no':next_number,'pre_no':pre_number})
    if request.method == "POST":
        payload = {'search':request.POST.get("search")}
        books = requests.post("https://book-reviews-app-ca75.onrender.com/getbookreviews/c2FzaWd1cnV2aWduZXNoQGdtYWlsLmNvbQ/pz6kx2341p8nac3cjtlzb5ffa7esu1zki6m/",data=payload)
        if books.status_code == 200:
            book_data = books.json()
            return render(request,'precisionagri/book_collection.html',{"data":book_data})
        else:
            messages.error(request,'Invalid search value')
            return redirect(reverse('bookreviews',args=(1,)))

@login_required(login_url="signin")
def playaudio(request,id):
    if request.method == "GET":
        books = requests.get(f"https://book-reviews-app-ca75.onrender.com/getbookreviews/c2FzaWd1cnV2aWduZXNoQGdtYWlsLmNvbQ/pz6kx2341p8nac3cjtlzb5ffa7esu1zki6m/{id}/")
        if books.status_code == 200:
            book_data = books.json()
            return render(request,'precisionagri/bookplay.html',{"data":book_data,'form':FeedbackForm})
        elif books.status_code == 404:
            messages.error(request,'Invalid User')
            return redirect(reverse('bookreviews',args=(1,)))
        else:
           messages.error(request,'Invalid Token')
           return redirect(reverse('bookreviews',args=(1,)))
    if request.method ==  "POST":
        payload = {'username':request.POST.get("name"),'feedback':request.POST.get("feedback")}
        books = requests.post(f"https://book-reviews-app-ca75.onrender.com/getbookreviews/c2FzaWd1cnV2aWduZXNoQGdtYWlsLmNvbQ/pz6kx2341p8nac3cjtlzb5ffa7esu1zki6m/{id}/",data=payload)
        if books.status_code == 201:
            messages.success(request,'Feedback submitted successfully')
            return redirect(reverse('bookreviews',args=(1,)))
        else:
            messages.error(request,'Invalid data')
            return redirect(reverse('bookreviews',args=(1,)))
# merge account verify
def mergeaccountverify(request):
    if request.method == "GET":
        return render(request,'precisionagri/emailmsg.html',{'form':Emailform})
    elif request.method == "POST":
        form = Emailform(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = User.objects.get(email = email)
            except:
                return redirect(reverse('merge',messages.error(request,'There is no account with this email. Please give your registered third party email')),permanent=True)
            if user.is_active == True:
                if (user.is_PAS_account != True) and (user.is_account_verified != True):
                    return render(request,'precisionagri/pwdchange.html',{'mform':PasswordChangeForm,'email':email})
                else:
                    return redirect(reverse('merge',messages.error(request,'Not a third party account')),permanent=True)
            else:
                return redirect(reverse('merge',messages.error(request,'Account deactive. Please contact admin via contact form')),permanent=True)

# merge account success
def mergeaccount(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            pwd = form.cleaned_data['password']
            confirm_pwd = form.cleaned_data['confirm_password']
            if pwd != confirm_pwd:
                return redirect(reverse('merge',messages.error(request,'Password and Confirm Password mismatched.')),permanent=True)
            try:
                user = User.objects.get(email = email)
            except:
                return redirect(reverse('merge',messages.error(request,'There is no account with this email. Please give your registered third party email')),permanent=True)
            if user.is_active == True:
                if user.is_PAS_account != True:
                    user.is_PAS_account = True
                    user.is_account_verified = True
                    user.set_password(pwd)
                    user.save()
                    return redirect(reverse('home',messages.success(request,'successfully merged')),permanent=True)
                else:
                    return redirect(reverse('merge',messages.error(request,'Not a third party account')),permanent=True)
            else:
                return redirect(reverse('merge',messages.error(request,'Account deactive. Please contact admin via contact form')),permanent=True)
  