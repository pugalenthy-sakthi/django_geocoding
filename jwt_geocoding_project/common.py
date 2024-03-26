from http import HTTPStatus
from django.http import JsonResponse
import bcrypt
import jwt
from .settings import JWT_TOKEN_TIME,JWT_REFRESH_TIME,JWT_ALGO,JWT_SECRET
from datetime import datetime,timedelta
import uuid
from django.conf import settings
from django.views.decorators.cache import cache_page
from django.core.cache import cache
from auth_app.models import Activity
import json

class Responses:
  
  INVALID_DATA = 'Invalid Data'
  DUPLICATE_DATA = 'Data Already Exist'
  CREATE_RESPONSE = 'Data Created Successfully'
  SERVER_ERROR = 'OOPS!'
  INVALID_REQUEST = 'Invalid Request'
  NOT_FOUND = 'The Given Data Not Found'
  SUCCESS_RESPONSE = 'Success'
  INVALID_CREDENTIALS = 'Invalid Credentials'
  FORBIDDEN = 'Forbidden'
  API_NOT_FOUND = 'Api Not Found'
  UPDATED_RESPONSE = 'Updated'
  DELETED_RESPONSE = 'Deleted'

def response_sender(message,data,http:HTTPStatus):
  
  body = {
    'http_status':http.phrase,
    'message':message,
    'data':data
  }
  
  return JsonResponse(data = body,status = http.value)


def gethashpwd(pwd):
  
  return (bcrypt.hashpw(bytes(pwd,'utf-8'),bcrypt.gensalt())).decode('utf-8')


def checkpwd(pwd:str,hpwd:str):
  
  return bcrypt.checkpw(hpwd.encode('utf-8'),pwd.encode('utf-8'))
  
  
class JWT:
  
  
  def get_jwt(subject,payload = None):
    
    jwt_claims = {
      'exp' : datetime.utcnow() + timedelta(seconds=float(JWT_TOKEN_TIME)),
      'sub' : subject,
      'iat' : datetime.utcnow()
    }
    
    if payload is None : 
      payload = jwt_claims
    
    payload.update(jwt_claims)
    
    return jwt.encode(payload,JWT_SECRET,algorithm=JWT_ALGO)
  
  
  def get_jwt_refresh(subject,payload = None):
    
    jwt_claims = {
      'exp' : datetime.utcnow() + timedelta(seconds=float(JWT_REFRESH_TIME)),
      'sub' : subject,
      'iat' : datetime.utcnow()
    }
    
    if payload is None : 
      payload = jwt_claims
      
    payload.update(jwt_claims)
    
    return jwt.encode(payload,JWT_SECRET,algorithm=JWT_ALGO)
  
  def verify_jwt_token(token):
    try:
      payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGO],verify=True)
      return payload  
    except jwt.ExpiredSignatureError as e:
      return None
    except jwt.InvalidTokenError as e:
      return None
    except Exception as e:
      return None
    
def get_random_id():
    return uuid.uuid4().hex
  
  
def cache_with_request(timeout=settings.REDIS_TIMEOUT):
    def wrapper(func):
        def wrapper_func(request, *args, **kwargs):
            cache_key = get_key(request)
            return cache_page(timeout=timeout, key_prefix=cache_key)(func)(request, *args, **kwargs)
        return wrapper_func
    return wrapper
  
  
def get_key(request):
  session_id = JWT.verify_jwt_token(request.headers['Authorization'])['sub']
  return request.path+'/'+session_id
  
  
def put_session_cache(session_id,session):
  
  data = {
    'session_id' : session_id,
    'user_email' : session.user.email,
    'logout_at' : session.logout_at
  }
  
  data_String = json.dumps(data)
  
  cache.set(key = session_id,value=data_String,timeout=60*60)
  
def get_session_cache(session_id):
  caches = cache.get(default=None,key=session_id)
  if caches is None :
    return None
  data = json.loads(caches)
  return data
  