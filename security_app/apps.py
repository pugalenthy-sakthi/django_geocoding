from django.apps import AppConfig
from django.conf import settings



class SecurityAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'security_app'
    
    def ready(self):
        if settings.SCHEDULER_DEFAULT:
            from jwt_geocoding_project import operator
            operator.start()

