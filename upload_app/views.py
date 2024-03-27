from django.http import HttpRequest
from jwt_geocoding_project.common import response_sender
from http import HTTPStatus
from jwt_geocoding_project.common import Responses,get_random_id,JWT,get_session_cache
import os
from django.core.files.storage import FileSystemStorage
import aiohttp

def file_upload(request:HttpRequest):
  
  if request.method == 'POST':
    try:
      base_path = 'upload_app'
      if not os.path.exists(os.path.join(base_path,'uploads')):
        os.mkdir(os.path.join(base_path,'uploads'))
      base_path = os.path.join(base_path,'uploads')
      session_id = (JWT.verify_jwt_token(request.headers['Authorization']))['sub']
      user_data = get_session_cache(session_id)
      email = user_data['user_email']
      if not os.path.exists(os.path.join(base_path,email)):
        os.mkdir(os.path.join(base_path,email))
      base_path = os.path.join(base_path,email)
      files = request.FILES.getlist('file')
      fs= FileSystemStorage(base_path)
      for file in files:
        file_name = get_random_id()+file.name
        fs.save(file_name,file)
      return response_sender(message=Responses.CREATE_RESPONSE,data=None,http=HTTPStatus.CREATED)
    except Exception as e:
      return response_sender(message=Responses.SERVER_ERROR,data=None,http=HTTPStatus.INTERNAL_SERVER_ERROR)
    
  else:
    return response_sender(message=Responses.INVALID_REQUEST,data=None,http=HTTPStatus.BAD_GATEWAY)
  
  
async def async_file_upload(request:HttpRequest):
  if request.method == 'POST':
    try:
      files = request.FILES.getlist('file')
      for file in files:
        formdata = aiohttp.FormData()
        formdata.add_field('file',file.file,filename=file.name)
        url = 'http://localhost:8000/upload/fileupload'
        pass
        async with aiohttp.ClientSession() as session:
          async with session.post(url,data = formdata,headers = {'Authorization':request.headers['Authorization']}) as response:
            pass
      return response_sender(message=Responses.CREATE_RESPONSE,data=None,http=HTTPStatus.CREATED)
    except Exception as e:
      print(e)
      return response_sender(message=Responses.SERVER_ERROR,data=None,http=HTTPStatus.INTERNAL_SERVER_ERROR)
  else:
    return response_sender(message=Responses.INVALID_REQUEST,data=None,http=HTTPStatus.BAD_GATEWAY)