from django.http import HttpRequest
from jwt_geocoding_project.common import response_sender
from http import HTTPStatus
import json
from jwt_geocoding_project.common import Responses,gethashpwd,get_random_id,JWT,checkpwd,put_session_cache

def file_upload(request):
  
  if request.method == 'POST':
    try:
      pass
      
    except json.JSONDecodeError :
      return response_sender(message=Responses.INVALID_DATA,data=None,http=HTTPStatus.BAD_REQUEST)
    
    except Exception as e:
      return response_sender(message=Responses.SERVER_ERROR,data=None,http=HTTPStatus.INTERNAL_SERVER_ERROR)
    
  else:
    return response_sender(message=Responses.INVALID_REQUEST,data=None,http=HTTPStatus.BAD_GATEWAY)