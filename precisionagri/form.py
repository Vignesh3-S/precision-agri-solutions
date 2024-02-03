from django import forms
from django.forms import TextInput,NumberInput,Textarea
from .models import Contact,User,Agriculture
from django.utils.translation import gettext_lazy as _
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV2Checkbox
from phonenumber_field.widgets import PhoneNumberPrefixWidget

#Crop form -- Recommend
class CropRecommendform(forms.ModelForm):
    class Meta:
        model = Agriculture
        exclude = ('user','Crop_Label','date',)
        labels = {"Nitrogen":"","Phosphorous":"","Potassium": "","Temperature":"","Humidity":"","PH":"","Rainfall":""}
        widgets = {
            "Nitrogen": NumberInput(attrs={'placeholder':_('Nitrogen Value')}),
            "Phosphorous": NumberInput(attrs={'placeholder':_('Phosphorus Value')}),
            "Potassium": NumberInput(attrs={'placeholder':_('Potassium Value')}),
            "Temperature": NumberInput(attrs={'placeholder':_('Temperature Value')}),
            "Humidity": NumberInput(attrs={'placeholder':_('Humidity Value')}),
            "PH": NumberInput(attrs={'placeholder':_('PH Value')}),
            "Rainfall": NumberInput(attrs={'placeholder':_('Rainfall Value')}),}

# Crop form -- NPK
class Searchform(forms.Form):
    Choices = (('. . . select the crop . . .','. . . select any crop . . .'),('Apple','Apple'),('Banana','Banana'),('Blackgram','Blackgram'),('Coffee','Coffee'),('Chickpea','Chickpea'),('Coconut','Coconut')
               ,('Cotton','Cotton'),('Grapes','Grapes'),('Jute','Jute'),('Kidneybeans','Kidneybeans'),('Mango','Mango'),('Maize','Maize'),
              ('Mothbeans','Mothbeans'),('Mungbean','Mungbean'),('Muskmelon','Muskmelon'),('Lentil','Lentil'),('Orange','Orange'),('Papaya','Papaya'),
              ('Pomegranate','Pomegranate'),('Pigeonpeas','Pigeonpeas'),('Rice','Rice'),('Watermelon','Watermelon'))   
    search = forms.ChoiceField(label="",choices=Choices,widget=forms.Select(attrs={'class':'form-control'}))

# User query form
class Queryform(forms.ModelForm):
    email = forms.EmailField(label='',widget=forms.EmailInput(attrs={'placeholder':_('Email'),'class':'form-control'}))       
    class Meta:
        model = Contact
        fields = ('Name','message',)
        labels = {"Name":"","message":"",}
        widgets = {
            "Name": TextInput(attrs={'placeholder':_('Name')}),
            "message": Textarea(attrs={'placeholder':_('Message')}),
        }
    field_order = ['email','Name','message']

#Signup form
class Signupform(forms.ModelForm):
    email = forms.EmailField(label='',widget=forms.EmailInput(attrs={'placeholder':_('Email'),'class':'form-control'}))       
    password = forms.CharField(label = '',max_length=15,min_length=8,help_text=_("Password must be atleast 8 characters."),
                              widget=forms.PasswordInput(attrs={'placeholder':_('password'),'class':'form-control'}))
    confirm_password = forms.CharField(label = '',max_length=15,min_length=8,help_text=_("Password and confirm password must be same."),
                                     widget=forms.PasswordInput(attrs={'placeholder':_('confirm password'),'class':'form-control'}))
    class Meta():
        model = User
        fields = ('state','district','native','username','email','mobile',)
        labels = {"state":"","mobile":"","district": "","native":"","username":"","email":"",}
        widgets = {
            "district": TextInput(attrs={'placeholder':_('District')}),
            "native": TextInput(attrs={'placeholder':_('Native')}),
            "username": TextInput(attrs={'placeholder':_('Name')}),
            "mobile": PhoneNumberPrefixWidget(attrs={'placeholder': _('MobileNumber'), 'class': "form-control"},country_choices=[("IN", "+91 INDIA"),]),
        }

#login form
class Loginform(forms.Form):
    email = forms.EmailField(label = '',widget=forms.EmailInput(attrs={'placeholder': _('Email'),'class':'form-control'}),)
    password = forms.CharField(label = '',max_length=15,widget=forms.PasswordInput(attrs={'placeholder':_('password'),'class':'form-control'}))
    captcha = ReCaptchaField(label = '',widget=ReCaptchaV2Checkbox)

# User_update form
class Userupdateform(forms.ModelForm):
    class Meta():
        model = User
        fields = ('state','district','native','username','mobile',)
        labels = {"state":"","mobile":"","district": "","native":"","username":"",}
        widgets = {
            "district": TextInput(attrs={'placeholder':_('District')}),
            "native": TextInput(attrs={'placeholder':_('Native')}),
            "username": TextInput(attrs={'placeholder':_('Name')}),
            "mobile": PhoneNumberPrefixWidget(attrs={'placeholder': _('MobileNumber'), 'class': "form-control"},country_choices=[("IN", "+91 INDIA"),]),
        } 

# Email form for password change
class Emailform(forms.Form):
    email = forms.EmailField(label='',widget=forms.EmailInput(attrs={'placeholder':'Enter the email','class':'form-control'}))       

# User image upload form
class Userimgform(forms.Form):
    image = forms.ImageField(label = "",required=False)

#Password change form
class PasswordChangeForm(forms.Form):
    password = forms.CharField(label='', help_text="Password must be atleast 8 characters, should contain alphnumeric and special characters.",
                                max_length=15,min_length=8,widget=forms.PasswordInput(attrs={'placeholder':'Password', 'class':"form-control"}))
    confirm_password = forms.CharField(label='',help_text="Password and confirm password must be same.",
                                max_length=15,min_length=8,widget=forms.PasswordInput(attrs={'placeholder':'Confirm Password', 'class':"form-control"}))