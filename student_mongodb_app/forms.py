from django import forms
from .models import Student,Department

class DepartmentForm(forms.ModelForm):
    
    class Meta:
        model = Department
        fields = ['department_name']
        
class StudentForm(forms.ModelForm):
  
  department_name = forms.CharField(max_length=20, label='Department Name')
  
  class Meta:
    
    model = Student
    fields = ['name','department_name']

class StudentUpdateForm(forms.Form):
  
  name = forms.CharField(max_length=60)
  id = forms.IntegerField()
  department_name = forms.CharField(max_length=20)
