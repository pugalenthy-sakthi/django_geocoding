from django.urls import path
from . import views

urlpatterns = [
    path('serviceprovider/create',view=views.create_service_provider,name='create_service_provider'),
    path('restaurant/create',view=views.create_restaurant,name='create_restaurant'),
    path('region/create',view=views.create_region,name='create_region'),
    path('restaurant/near',view=views.get_nearest_restaurants,name='get_nearest_reataurant')
]
