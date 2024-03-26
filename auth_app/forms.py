from django import forms
from .models import User

class UserModel(forms.ModelForm):
  
  class Meta:
    model = User
    
    fields = ['name','email','password']
    
    
class LoginModel(forms.Form):
    username = forms.EmailField(label='Username')
    password = forms.CharField(label='Password')