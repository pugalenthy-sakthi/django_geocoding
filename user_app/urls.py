from django.urls import path
from . import views
urlpatterns = [
    path('profile',view=views.userprofile,name='user_profile')
]
