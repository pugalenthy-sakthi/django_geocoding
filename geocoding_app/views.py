from django.http import HttpRequest
from http import HTTPStatus
import json
from .forms import ServiceProviderModel,RestaurantModel,RegionModel,LatLongModel
from jwt_geocoding_project.common import Responses,get_random_id,JWT,response_sender
from .models import ServiceProvider,Region,Restaurant
from rest_framework.serializers import ValidationError
from django.contrib.gis.geos import Point,Polygon
from django.db import transaction
from django.contrib.gis.db.models.functions import Distance
from django.core.paginator import Paginator

def create_service_provider(request:HttpRequest):
  
  if request.method == 'POST':
    try:
      json_data = json.loads(request.body)
      service_provider_model = ServiceProviderModel(json_data)
      exists = ServiceProvider.objects.filter(name = service_provider_model.data['name']).first()
      if exists != None:
        return response_sender(message=Responses.DUPLICATE_DATA,data=None,http=HTTPStatus.CONFLICT)
      
      service_provider = ServiceProvider()
      service_provider.name = service_provider_model.data['name']
      service_provider.save()
      return response_sender(message=Responses.CREATE_RESPONSE,data=None,http=HTTPStatus.CREATED)
      
    except json.JSONDecodeError :
      return response_sender(message=Responses.INVALID_DATA,data=None,http=HTTPStatus.BAD_REQUEST)
    except Exception as e:
      print(e)
      return response_sender(message=Responses.SERVER_ERROR,data=None,http=HTTPStatus.INTERNAL_SERVER_ERROR)
  else:
    return response_sender(message=Responses.INVALID_REQUEST,data=None,http=HTTPStatus.BAD_GATEWAY)
    
  
def create_restaurant(request:HttpRequest):
  
  if request.method == 'POST':
    try:
      json_data = json.loads(request.body)
      restaurant_model = RestaurantModel(data = json_data)
      if not restaurant_model.is_valid():
        return response_sender(message=Responses.INVALID_DATA,data=None,http=HTTPStatus.BAD_REQUEST)
      exist = Restaurant.objects.filter(name = restaurant_model.data['name']).first()
      if exist != None:
        return response_sender(message=Responses.DUPLICATE_DATA,data=None,http=HTTPStatus.CONFLICT)
      with transaction.atomic():
        restaurant = Restaurant()
        restaurant.name = restaurant_model.data['name']
        restaurant.point = Point(restaurant_model.data['lon'],restaurant_model.data['lat'],srid=4326)
        restaurant.save()
        service_providers = restaurant_model.data['service_providers']
        for provider in service_providers:
          service_provider = ServiceProvider.objects.filter(name = provider).first()
          if service_provider is None:
            raise ValidationError
          restaurant.service_providers.add(service_provider)
        restaurant.save()
      # transaction.commit()
      return response_sender(message=Responses.CREATE_RESPONSE,data=None,http=HTTPStatus.CREATED)
    except ValidationError:
      transaction.rollback()
      return response_sender(message=Responses.INVALID_DATA,data=None,http=HTTPStatus.BAD_REQUEST)
    except json.JSONDecodeError :
      return response_sender(message=Responses.INVALID_DATA,data=None,http=HTTPStatus.BAD_REQUEST)
    except Exception as e:
      transaction.rollback()
      print(e)
      return response_sender(message=Responses.SERVER_ERROR,data=None,http=HTTPStatus.INTERNAL_SERVER_ERROR)
  else:
    return response_sender(message=Responses.INVALID_REQUEST,data=None,http=HTTPStatus.BAD_GATEWAY)
  
  
def create_region(request:HttpRequest):
  
  if request.method == 'POST':
    try:
      json_data = json.loads(request.body)
      region_model = RegionModel(data = json_data)
      if not region_model.is_valid():
        return response_sender(message=Responses.INVALID_DATA,data=None,http=HTTPStatus.BAD_REQUEST)
      with transaction.atomic():
        if len(region_model.data['geometry']) <3:
          raise ValidationError
        region = Region()
        region.name = region_model.data['name']
        point_list = []
        first_loc = Point(region_model.data['geometry'][0]['lon'],region_model.data['geometry'][0]['lat'],srid=4326)
        for point in region_model.data['geometry']:
          point_list.append(Point(point['lon'],point['lat'],srid=4326))
        point_list.append(first_loc)
        geometry = Polygon(point_list)
        region.geometry = geometry
        service_provider = ServiceProvider.objects.filter(name = region_model.data['service_provider']).first()
        if service_provider is None:
          raise ValidationError
        region.service_provider = service_provider
        region.save()
      transaction.commit()
      return response_sender(message=Responses.CREATE_RESPONSE,data=None,http=HTTPStatus.CREATED)
    except ValidationError:
      transaction.rollback()
      return response_sender(message=Responses.INVALID_DATA,data=None,http=HTTPStatus.BAD_REQUEST)
    except json.JSONDecodeError :
      transaction.rollback()
      return response_sender(message=Responses.INVALID_DATA,data=None,http=HTTPStatus.BAD_REQUEST)
    except Exception as e:
      print(e)
      transaction.rollback()
      return response_sender(message=Responses.SERVER_ERROR,data=None,http=HTTPStatus.INTERNAL_SERVER_ERROR)
  else:
    return response_sender(message=Responses.INVALID_REQUEST,data=None,http=HTTPStatus.BAD_GATEWAY)
  
  
def get_nearest_restaurants(request:HttpRequest):
  
  if request.method == 'POST':
    try:
      json_data = json.loads(request.body)
      latlon_model = LatLongModel(data = json_data)
      if not latlon_model.is_valid():
        return response_sender(message=Responses.INVALID_DATA,data=None,http=HTTPStatus.BAD_REQUEST)
      point = Point(latlon_model.data['lon'],latlon_model.data['lat'],srid=4326)
      restaurant_list = Restaurant.objects.annotate(
        distance = Distance('point',point)
      ).order_by('distance')
      restaurant_data = [
        {
          'restaurant_name':restaurant.name,
          'lat':restaurant.point.y,
          'lon':restaurant.point.x
        }
        for restaurant in restaurant_list
      ]
      return response_sender(message=Responses.SUCCESS_RESPONSE,data=restaurant_data,http=HTTPStatus.OK)
    except json.JSONDecodeError :
      transaction.rollback()
      return response_sender(message=Responses.INVALID_DATA,data=None,http=HTTPStatus.BAD_REQUEST)
    except Exception as e:
      print(e)
      transaction.rollback()
      return response_sender(message=Responses.SERVER_ERROR,data=None,http=HTTPStatus.INTERNAL_SERVER_ERROR)
  else:
    return response_sender(message=Responses.INVALID_REQUEST,data=None,http=HTTPStatus.BAD_GATEWAY)
