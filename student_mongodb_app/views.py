import json
from jwt_geocoding_project.common import Responses,response_sender,gethashpwd,get_random_id,JWT
from http import HTTPStatus
from .forms import DepartmentForm,StudentForm,StudentUpdateForm
from .models import Student,Department
from django.http import HttpRequest

def create_department(request):
  
  if request.method == 'POST':
    try:
      json_data  = json.loads(request.body)
      department_data = DepartmentForm(json_data)
      deaprtment_exist = Department.objects.using('mongodb').filter(department_name = department_data.data['department_name']).first()
      if deaprtment_exist != None:
        return response_sender(message=Responses.DUPLICATE_DATA,data=None,http=HTTPStatus.CONFLICT)
      department = Department()
      department.department_name = department_data.data['department_name']
      department.save()
      return response_sender(message=Responses.CREATE_RESPONSE,data=None,http=HTTPStatus.CREATED)
      
    except json.JSONDecodeError :
      return response_sender(message=Responses.INVALID_DATA,data=None,http=HTTPStatus.BAD_REQUEST)
    except Exception as e:
      print(e)
      return response_sender(message=Responses.SERVER_ERROR,data=None,http=HTTPStatus.INTERNAL_SERVER_ERROR)
  else:
    return response_sender(message=Responses.INVALID_REQUEST,data=None,http=HTTPStatus.BAD_GATEWAY)
  
  


def create_student(request):
  
  if request.method == 'POST':
    try:
      json_data  = json.loads(request.body)
      student_data = StudentForm(json_data)
      department_name = student_data.data['department_name']
      department = Department.objects.using('mongodb').filter(department_name = department_name).first()
      if department == None:
        return response_sender(message=Responses.NOT_FOUND,data=None,http=HTTPStatus.NOT_FOUND)
      student = Student()
      student.name = student_data.data['name']
      student.department = department
      student.save()
      return response_sender(message=Responses.CREATE_RESPONSE,data=None,http=HTTPStatus.CREATED)
      
    except json.JSONDecodeError :
      return response_sender(message=Responses.INVALID_DATA,data=None,http=HTTPStatus.BAD_REQUEST)
    except Exception as e:
      print(e)
      return response_sender(message=Responses.SERVER_ERROR,data=None,http=HTTPStatus.INTERNAL_SERVER_ERROR)
  else:
    return response_sender(message=Responses.INVALID_REQUEST,data=None,http=HTTPStatus.BAD_GATEWAY)
  
  
def update_student(request):
  
  
  if request.method == 'PUT':
    try:
      json_data  = json.loads(request.body)
      student_data = StudentUpdateForm(json_data)
      print(student_data)
      department = Department.objects.using('mongodb').filter(department_name = student_data.data['department_name']).first()
      if department == None:
        return response_sender(message=Responses.NOT_FOUND,data=None,http=HTTPStatus.NOT_FOUND)
      student = Student.objects.using('mongodb').filter(id = student_data.data['id']).first()
      if student is None:
        return response_sender(message=Responses.NOT_FOUND,data=None,http=HTTPStatus.NOT_FOUND)
      student.name = student_data.data['name']
      student.department = department
      student.save()
      return response_sender(message=Responses.UPDATED_RESPONSE,data=None,http=HTTPStatus.OK)
      
    except json.JSONDecodeError :
      return response_sender(message=Responses.INVALID_DATA,data=None,http=HTTPStatus.BAD_REQUEST)
    except Exception as e:
      return response_sender(message=Responses.SERVER_ERROR,data=None,http=HTTPStatus.INTERNAL_SERVER_ERROR)
  else:
    return response_sender(message=Responses.INVALID_REQUEST,data=None,http=HTTPStatus.BAD_GATEWAY)
  
def delete_student(request:HttpRequest,student_id):
  
  if request.method == 'DELETE':
    try:
      student = Student.objects.using('mongodb').filter(id = student_id).first()
      if student is None:
        return response_sender(message=Responses.NOT_FOUND,data=None,http=HTTPStatus.NOT_FOUND)
      student.delete()
      return response_sender(message=Responses.DELETED_RESPONSE,data=None,http=HTTPStatus.OK)
    except Exception as e:
      return response_sender(message=Responses.SERVER_ERROR,data=None,http=HTTPStatus.INTERNAL_SERVER_ERROR)
  else:
    return response_sender(message=Responses.INVALID_REQUEST,data=None,http=HTTPStatus.BAD_GATEWAY)
  