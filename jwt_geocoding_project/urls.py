
from django.urls import path,include

urlpatterns = [
    path('auth/',include('auth_app.urls')),
    path('user/',include('user_app.urls')),
    path('mongo/',include('student_mongodb_app.urls')),
    path('upload/',include('upload_app.urls'))
]
