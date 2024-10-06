from rest_framework import serializers
from .models import *

class TransmissionSerializers(serializers.ModelSerializer):
    class Meta:
        model = Transmission
        fields = ['id','transmission']

class FuelTypeSerializers(serializers.ModelSerializer):
    class Meta:
        model = FuelType
        fields = ['id','fuel_type']

class ColorSerializers(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = ['id','color']

class CompanySerializers(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['id','logo','company_name','description']

class CarsSerializers(serializers.ModelSerializer):
    company = CompanySerializers()
    transmission = TransmissionSerializers()
    fuel_type = FuelTypeSerializers()
    color = ColorSerializers()
    class Meta:
        model = Cars
        fields = ['id','vehicle_registration','company','model','engine_size','transmission',
                  'fuel_type','color','selling_price','sale_price','description','slug']


class CarImagesSerializers(serializers.ModelSerializer):
    class Meta:
        model = CarImages
        fields = ['id','car','image','image_alt']
