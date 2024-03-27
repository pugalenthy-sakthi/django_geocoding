from django.contrib.gis.db import models


class Base(models.Model):
  
  id = models.AutoField(primary_key=True)
  created_at = models.DateTimeField(auto_now_add = True)
  updated_at = models.DateTimeField(auto_now = True)
  
  class Meta:
    abstract = True
    
class Restaurant(Base):
  
  name = models.CharField(max_length = 40,unique = True)
  point = models.PointField(srid=4326)


class ServiceProvider(Base):
  
  name = models.CharField(max_length = 40,unique = True)
  restaurants = models.ManyToManyField(Restaurant,related_name='service_providers')
    
class Region(Base):
  
  name = models.CharField(max_length= 80,unique = True)
  service_provider = models.ForeignKey(ServiceProvider,on_delete = models.CASCADE,related_name = 'regions')
  geometry = models.PolygonField(srid=4326) 
  
  
    

  
  

  