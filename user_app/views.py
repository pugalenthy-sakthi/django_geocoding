from django.http import HttpRequest
from jwt_geocoding_project.common import Responses,response_sender,JWT
from http import HTTPStatus
from auth_app.models import Activity
from jwt_geocoding_project.common import cache_with_request


@cache_with_request(timeout=3600)
def userprofile(request:HttpRequest):

  if request.method == 'GET':
    try:
      session_id = JWT.verify_jwt_token(request.headers['Authorization'])['sub']
      session = Activity.objects.filter(session_id = session_id).first()
      user = session.user
      user_details = {
        'user_name' : user.name,
        'email_id' : user.email
      }
      return response_sender(message=Responses.SUCCESS_RESPONSE,data=user_details,http=HTTPStatus.OK)
    except Exception:
      return response_sender(message=Responses.SERVER_ERROR,data=None,http=HTTPStatus.INTERNAL_SERVER_ERROR)
  else:
    return response_sender(message=Responses.INVALID_REQUEST,data=None,http=HTTPStatus.BAD_GATEWAY)
