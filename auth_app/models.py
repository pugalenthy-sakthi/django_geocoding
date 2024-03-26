from django.db import models

class Base(models.Model):
  
  id = models.AutoField(primary_key=True)
  create_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now = True)
  
  class Meta:
    abstract = True


class User(Base):
  
  name = models.CharField(max_length = 60)
  email = models.EmailField(max_length = 80)
  password = models.TextField()


class Activity(Base):
  
  user = models.ForeignKey(User,on_delete = models.CASCADE,related_name = 'activities')
  
  login_at  = models.DateTimeField(auto_now_add = True)
  logout_at = models.DateTimeField(null = True,blank = True)
  session_id = models.CharField(max_length = 50)
  

  
  
