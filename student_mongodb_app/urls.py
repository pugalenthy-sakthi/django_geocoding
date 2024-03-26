from django.urls import path
from . import views

urlpatterns = [
    path('department/create',view = views.create_department,name = 'create_department'),
    path('student/create',view = views.create_student,name='create_student'),
    path('student/update',view=views.update_student,name='update_student'),
    path('student/delete/<int:student_id>',view=views.delete_student,name='delete_student'),
]
