from django import forms 
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm,PasswordChangeForm,UserChangeForm
from django.contrib.auth.models import User
from .models import Contact




class Registerform(UserCreationForm):
    password1 = forms.CharField(label='Password',widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2 = forms.CharField(label='Confirm Password',widget=forms.PasswordInput(attrs={'class':'form-control'}))
    mobile_number = forms.CharField(
        label='Mobile Number',
        max_length=15,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''})
    )



    class Meta:
        model = User
        fields = ['username','mobile_number','email','password1','password2']
        labels = {'email':'Email'}
        widgets= {'username':forms.TextInput(attrs={'class':'form-control'}),
                  'email':forms.TextInput(attrs={'class':'form-control'}),
                  }
        
class AuthenticateForm(AuthenticationForm):
    username = forms.CharField(widget = forms.TextInput(attrs={'class':'form-control'}))
    password = forms.CharField(label = 'Password',widget=forms.PasswordInput(attrs={'class':'form-control'}))


class ChangePasswordForm(PasswordChangeForm):
    old_password = forms.CharField(label='Old Password', widget = forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password1 = forms.CharField(label='New Password', widget = forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password2 = forms.CharField(label='Confirm Password', widget = forms.PasswordInput(attrs={'class': 'form-control'}))




class UserProfileForm(UserChangeForm):
    password =None


    class Meta:
        model = User
        fields =['username','email']
        widgets= {'username':forms.TextInput(attrs={'class':'form-control'}),
                  'email':forms.TextInput(attrs={'class':'form-control'}),
                  }



class AdminProfileForm(UserChangeForm):
    password =None


    class Meta:
        model = User
        fields = '__all__'
        widgets= {'username':forms.TextInput(attrs={'class':'form-control'}),
                  'email':forms.TextInput(attrs={'class':'form-control'}),
                  'first_name':forms.TextInput(attrs={'class':'form-control'}),
                  'last_name':forms.TextInput(attrs={'class':'form-control'}),
                  }
        


class ContactForm(forms.ModelForm):

    class Meta:
        model = Contact
        fields = ['name', 'email', 'message']
        widgets = {
            'name' : forms.TextInput(attrs={'class': 'form-control'}),
            'email' : forms.EmailInput(attrs={'class': 'form-control'}),
            'message' : forms.Textarea(attrs={'class': 'form-control'})
        } 




