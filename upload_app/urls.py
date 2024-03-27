from django.urls import path
from . import views

urlpatterns = [
  path('fileupload',view=views.file_upload,name='files_upload'),
  path('async/fileupload',view=views.async_file_upload,name='async_file_upload')
]
