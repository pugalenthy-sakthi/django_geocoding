from django import forms
from rest_framework import serializers

class ServiceProviderModel(forms.Form):
  
  name = forms.CharField(max_length=40)

class LatLongModel(serializers.Serializer):
  
  lat = serializers.FloatField()
  lon = serializers.FloatField()
  

class RestaurantModel(serializers.Serializer):
  
  name = serializers.CharField(max_length = 40)
  lat = serializers.FloatField()
  lon = serializers.FloatField()
  
  service_providers = serializers.ListField(child = serializers.CharField())
  
  
class RegionModel(serializers.Serializer):
  
  name = serializers.CharField(max_length = 80)
  service_provider = serializers.CharField(max_length = 40)
  
  geometry = serializers.ListField(child = LatLongModel())