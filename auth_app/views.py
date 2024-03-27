from django.http import HttpRequest
from django.shortcuts import redirect
from jwt_geocoding_project.common import response_sender
from http import HTTPStatus
from .forms import UserModel,LoginModel
import json
from jwt_geocoding_project.common import Responses,gethashpwd,get_random_id,JWT,checkpwd,put_session_cache
from .models import User,Activity
from datetime import datetime
from django.conf import settings
import requests


def user_signup(request:HttpRequest):
  
  if request.method == 'POST':
    try:
      user_json = json.loads(request.body)
      user_model = UserModel(user_json)
      existing_data = User.objects.filter(email = user_model.data['email']).first()
      if existing_data is not None:
        return response_sender(message=Responses.DUPLICATE_DATA,data=None,http=HTTPStatus.CONFLICT)
      
      
      user = User()
      user.email = user_model.data['email']
      user.name = user_model.data['name']
      user.password = gethashpwd(user_model.data['password'])
      user.save()
      
      return response_sender(message=Responses.CREATE_RESPONSE,data=None,http=HTTPStatus.CREATED)
      
    except json.JSONDecodeError :
      return response_sender(message=Responses.INVALID_DATA,data=None,http=HTTPStatus.BAD_REQUEST)
    
    except Exception as e:
      return response_sender(message=Responses.SERVER_ERROR,data=None,http=HTTPStatus.INTERNAL_SERVER_ERROR)
    
  else:
    return response_sender(message=Responses.INVALID_REQUEST,data=None,http=HTTPStatus.BAD_GATEWAY)

def login(request:HttpRequest):

  if request.method == 'POST':
    try:
      user_json = json.loads(request.body)
      login_model = LoginModel(user_json)
      user = User.objects.filter(email = login_model.data['email']).first()
      if user is None:
        return response_sender(message=Responses.NOT_FOUND,data=None,http=HTTPStatus.NOT_FOUND)
      pwd_state = checkpwd(user.password,login_model.data['password'])
      if pwd_state == False:
        return response_sender(message=Responses.INVALID_CREDENTIALS,data=None,http=HTTPStatus.FORBIDDEN)
      activity = Activity()
      activity.session_id = get_random_id()
      activity.user = user
      activity.save()
      
      token = JWT.get_jwt(activity.session_id)
      ref_token = JWT.get_jwt_refresh(activity.session_id)
      
      token_response = {
        'token':token,
        'refresh_token':ref_token
      }
      put_session_cache(activity.session_id,activity)
      
      return response_sender(message=Responses.SUCCESS_RESPONSE,data=token_response,http=HTTPStatus.OK)
      
    except json.JSONDecodeError :
      return response_sender(message=Responses.INVALID_DATA,data=None,http=HTTPStatus.BAD_REQUEST)
    
    except Exception as e:
      print(e)
      return response_sender(message=Responses.SERVER_ERROR,data=None,http=HTTPStatus.INTERNAL_SERVER_ERROR)
    
    
  
  else:
    return response_sender(message=Responses.INVALID_REQUEST,data=None,http=HTTPStatus.BAD_GATEWAY)
  
  
def logout(request:HttpRequest):
  
  if request.method == 'GET':
    try:
      session_id = JWT.verify_jwt_token(request.headers['Authorization'])['sub']
      session = Activity.objects.filter(session_id = session_id).first()
      if session == None or session.logout_at != None:
        return response_sender(message=Responses.INVALID_CREDENTIALS,data=None,http=HTTPStatus.FORBIDDEN)
      session.logout_at = datetime.now()
      session.save()
      return response_sender(message=Responses.SUCCESS_RESPONSE,data=None,http=HTTPStatus.OK)
    except Exception as e:
      return response_sender(message=Responses.SERVER_ERROR,data=None,http=HTTPStatus.INTERNAL_SERVER_ERROR)
  else:
    return response_sender(message=Responses.INVALID_REQUEST,data=None,http=HTTPStatus.BAD_GATEWAY)
  
def refresh(request:HttpRequest):
  
  if request.method == 'GET':
    try:
      claim = {
        'is_extended':'True'
      }
      session_id  = JWT.verify_jwt_token(request.headers['Authorization'])['sub']
      token = JWT.get_jwt(session_id,claim)
      ref_token = JWT.get_jwt_refresh(session_id,claim)
      
      token_response = {
        'token':token ,
        'refresh_token':ref_token
      }
      return response_sender(message=Responses.SUCCESS_RESPONSE,data=token_response,http=HTTPStatus.OK)
      
    except Exception as e:
      print(e)
      return response_sender(message=Responses.SERVER_ERROR,data=None,http=HTTPStatus.INTERNAL_SERVER_ERROR)
  else:
    return response_sender(message=Responses.INVALID_REQUEST,data=None,http=HTTPStatus.BAD_GATEWAY)
  

def oauth_login(request:HttpRequest):
  
  if request.method == 'GET':
    try:
      redirect_uri = 'http://localhost:8000/auth/google/login'
      client_id = settings.GOOGLE_CLIENT_ID
      authorization_url = f'https://accounts.google.com/o/oauth2/v2/auth?response_type=code&client_id={client_id}&redirect_uri={redirect_uri}&scope=email%20profile%20openid'
      return redirect(authorization_url)
    except Exception as e:
      return response_sender(message=Responses.SERVER_ERROR,data=None,http=HTTPStatus.INTERNAL_SERVER_ERROR)
    
  else:
    return response_sender(message=Responses.INVALID_REQUEST,data=None,http=HTTPStatus.BAD_GATEWAY)
  

def callback_google(request:HttpRequest):
  
  if request.method == 'GET':
    try:
      code = request.GET.get('code')

      token_url = 'https://oauth2.googleapis.com/token'
      client_id = settings.GOOGLE_CLIENT_ID
      client_secret = settings.GOOGLE_CLIENT_SECRET
      redirect_uri = 'http://localhost:8000/auth/google/login'
      payload = {
          'code': code,
          'client_id': client_id,
          'client_secret': client_secret,
          'redirect_uri': redirect_uri,
          'grant_type': 'authorization_code'
      }
      token_response = requests.post(token_url, data=payload)
      token_data = token_response.json()
      access_token = token_data['access_token']

      userinfo_url = 'https://www.googleapis.com/oauth2/v3/userinfo'
      headers = {'Authorization': f'Bearer {access_token}'}
      userinfo_response = requests.get(userinfo_url, headers=headers)
      userinfo_data = userinfo_response.json()
      email = userinfo_data['email']
      user = User.objects.filter(email = email).first()
      if user is None:
        return response_sender(message=Responses.NOT_FOUND,data=None,http=HTTPStatus.NOT_FOUND)
      activity = Activity()
      activity.session_id = get_random_id()
      activity.user = user
      activity.save()
      
      token = JWT.get_jwt(activity.session_id)
      ref_token = JWT.get_jwt_refresh(activity.session_id)
      
      token_response = {
        'token':token,
        'refresh_token':ref_token
      }
      put_session_cache(activity.session_id,activity)
      
      return response_sender(message=Responses.SUCCESS_RESPONSE,data=token_response,http=HTTPStatus.OK)
    except Exception as e:
      return response_sender(message=Responses.SERVER_ERROR,data=None,http=HTTPStatus.INTERNAL_SERVER_ERROR)
  else:
    return response_sender(message=Responses.INVALID_REQUEST,data=None,http=HTTPStatus.BAD_GATEWAY)