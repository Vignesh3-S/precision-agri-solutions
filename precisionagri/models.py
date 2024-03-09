from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin
from django.utils import timezone
from .managers import UsersManager


class User(AbstractBaseUser,PermissionsMixin):
    state_choices = [("Andhra Pradesh","Andhra Pradesh"),("Arunachal Pradesh","Arunachal Pradesh"),
                     ("Assam","Assam"),("Bihar","Bihar"),("Chhattisgarh","Chhattisgarh"),("Goa","Goa"),
                     ("Gujarat","Gujarat"),("Haryana","Haryana"),("Himachal Pradesh","Himachal Pradesh"),
                     ("Jammu and Kashmir ","Jammu and Kashmir "),("Jharkhand","Jharkhand"),("Karnataka","Karnataka"),
                     ("Kerala","Kerala"),("Madhya Pradesh","Madhya Pradesh"),("Maharashtra","Maharashtra"),("Manipur","Manipur"),
                     ("Meghalaya","Meghalaya"),("Mizoram","Mizoram"),("Nagaland","Nagaland"),("Odisha","Odisha"),("Punjab","Punjab"),
                     ("Rajasthan","Rajasthan"),("Sikkim","Sikkim"),("Tamil Nadu","Tamil Nadu"),("Telangana","Telangana"),
                     ("Tripura","Tripura"),("Uttar Pradesh","Uttar Pradesh"),("Uttarakhand","Uttarakhand"),("West Bengal","West Bengal"),
                     ("Andaman and Nicobar Islands","Andaman and Nicobar Islands"),("Chandigarh","Chandigarh"),
                     ("Dadra and Nagar Haveli","Dadra and Nagar Haveli"),("Daman and Diu","Daman and Diu"),("Lakshadweep","Lakshadweep"),
                     ("National Capital Territory of Delhi","National Capital Territory of Delhi"),("Puducherry","Puducherry")]
    state = models.CharField(max_length=70,verbose_name="State Name",choices=state_choices)
    district = models.CharField(verbose_name="District",max_length=50)
    native = models.CharField(verbose_name="Native",max_length=50)
    username = models.CharField(max_length=30,verbose_name="Username")
    email = models.EmailField(unique=True,verbose_name="Email")
    mobile = PhoneNumberField(verbose_name="Mobile",region="IN")
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True,null=True)
    last_login = models.DateTimeField(verbose_name="Last login",null=True)
    userimg = models.ImageField(verbose_name='User Image', upload_to="PASuserimages")
    is_PAS_account = models.BooleanField(default = False)
    is_account_verified = models.BooleanField(default = False)
    is_api_token_obtained = models.BooleanField(default = False)
    otp = models.CharField(verbose_name="OTP",max_length=6)
    
    objects = UsersManager()
    

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['username',]

    def __str__(self):
        return self.username


class Agriculture(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,verbose_name="User",related_name="user")
    Nitrogen = models.FloatField(verbose_name="Nitrogen")
    Phosphorous = models.FloatField(verbose_name="Phosphorus")
    Potassium = models.FloatField(verbose_name="Potassium")
    Temperature = models.FloatField(verbose_name="Temperature")
    Humidity = models.FloatField(verbose_name="Humidity")
    PH = models.FloatField(verbose_name="PH")
    Rainfall = models.FloatField(verbose_name="Rainfall")
    Crop_Label  = models.CharField(max_length=100,verbose_name="Crop")
    date = models.DateTimeField(auto_now_add=True,verbose_name="Date and Time",null = True)

    def __str__(self):
        return f'{self.user} {self.Crop_Label}'

class NPK(models.Model):
    Crop_Name  = models.CharField(max_length=50,verbose_name="Crop Name")
    Std_nitrogen = models.CharField(max_length = 15,verbose_name="Standard Nitrogen")
    Std_phosphorus = models.CharField(max_length = 15,verbose_name="Standard Phosphorus")
    Std_potassium = models.CharField(max_length = 15,verbose_name="Standard Potassium")

    def __str__(self):
        return self.Crop_Name
    
class Search(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,verbose_name="User")
    Crop_Name  = models.ForeignKey(NPK,on_delete=models.CASCADE,verbose_name="Crop Name")
    date = models.DateTimeField(auto_now_add=True,verbose_name="Date and Time",null = True)

    def __str__(self):
        return f'{self.user} {self.Crop_Name}'

class Contact(models.Model):
    Name = models.CharField(max_length=30,verbose_name="Name")
    email = models.EmailField(verbose_name="Email")
    message = models.TextField(verbose_name="Message")


    def __str__(self):
        return f"{self.Name}'s Message"
    
class ApiUser(models.Model):
    user = models.OneToOneField(User,on_delete=models.SET_NULL,verbose_name="User",related_name="apiuser",null=True)
    app_name =  models.CharField(max_length=100,verbose_name="App Name",default="app name")
    app_type =  models.CharField(max_length=100,verbose_name="App Type",default="app type")
    apikey = models.CharField(max_length=100,verbose_name="Apitoken")
    token_valid = models.BooleanField(default=False,verbose_name ="Token validity")
    date = models.DateTimeField(auto_now_add=True,verbose_name="Date and Time",null=True)
    
    def __str__(self):
        return f"{self.user.username}'s token"