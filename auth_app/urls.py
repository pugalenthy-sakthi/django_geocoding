from django.urls import path
from . import views

urlpatterns = [
    path('signup',view=views.user_signup,name='user_signup'),
    path('login',view=views.login,name='user_login'),
    path('logout',view=views.logout,name='user_logout'),
    path('refresh',view=views.refresh,name='user_refresh'),
    path('oauth/google',view=views.oauth_login,name='google_login'),
    path('google/login',view=views.callback_google,name='google_callback')
]
