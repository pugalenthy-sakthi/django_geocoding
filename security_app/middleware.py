from typing import Any
from jwt_geocoding_project.common import JWT,response_sender,Responses,put_session_cache,get_session_cache
from django.http import HttpRequest
from http import HTTPStatus
from auth_app.models import Activity
import traceback

open_paths = [
  '/auth/login',
  '/auth/signup'
]

class token_required:
  
  def __init__(self,get_response) :
    
    self.get_response = get_response
    
  def __call__(self, request:HttpRequest) :
    
    if request.path in open_paths :
      return self.get_response(request)
    if 'Authorization' not in request.headers:
      return response_sender(Responses.INVALID_CREDENTIALS,data=None,http=HTTPStatus.FORBIDDEN)
    token = request.headers['Authorization']
    try:
      data = JWT.verify_jwt_token(token)
      if data == None :
        return response_sender(Responses.INVALID_CREDENTIALS,data=None,http=HTTPStatus.FORBIDDEN)
      session_id = data['sub']
      cache_data = get_session_cache(session_id)
      if cache_data is None:
        activity = Activity.objects.filter(session_id = session_id).first()
        put_session_cache(activity.session_id,activity)
        cache_data = get_session_cache(session_id)
      if cache_data['logout_at'] != None:
        return response_sender(Responses.INVALID_CREDENTIALS,data=None,http=HTTPStatus.FORBIDDEN)
      return self.get_response(request)
    except Exception as e:
      traceback.print_exception(e)
      return response_sender(Responses.INVALID_CREDENTIALS,data=None,http=HTTPStatus.FORBIDDEN)

  
  def process_exception(self,request,exception):
    
    print(exception)
    
    return response_sender(Responses.INVALID_DATA,data=None,http=HTTPStatus.BAD_REQUEST)
    