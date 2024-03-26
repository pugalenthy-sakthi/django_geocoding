from typing import Any
from djongo import models


class Base(models.Model):
  
  id = models.ObjectIdField(primary_key = True)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now = True)
  
  
  class Meta:
    abstract = True
    
    
class Department(Base):
  
  department_name  = models.CharField(max_length = 20,unique = True)

class Student(Base):
  
  name = models.CharField(max_length = 60)
  department = models.ForeignKey(Department,on_delete = models.SET_NULL,related_name = 'students',null = True)
  
