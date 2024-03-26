import datetime
from django.core import mail
from auth_app.models import User
from django.conf import settings

def send_email():
  
  users = User.objects.all()
  user_list = []
  
  for user in users:
    user_list.append(user.email)
    
  mail.send_mail('Temp',"Hello",settings.EMAIL_HOST_USER,user_list)