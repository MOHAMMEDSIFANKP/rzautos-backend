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

class MakeSerializers(serializers.ModelSerializer):
    class Meta:
        model = Make
        fields = ['id','logo','company_name','description']

class CarsSerializers(serializers.ModelSerializer):
    make = MakeSerializers()
    transmission = TransmissionSerializers()
    fuel_type = FuelTypeSerializers()
    color = ColorSerializers()

    class Meta:
        model = Cars
        fields = [
            'id',
            'thumbnail',
            'vehicle_registration',
            'make',
            'model',
            'engine_size',
            'transmission',
            'fuel_type',
            'color',
            'mileage',  
            'body_type', 
            'co2_emissions',
            'number_of_doors',
            'number_of_keys',
            'number_of_owners',
            'vat_type',
            'log_book',
            'sale_date',
            'registration_date',
            'selling_price',
            'sale_price',
            'description',
            'slug'
        ]

class CarImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarImages
        fields = ['id','car','image','image_alt']
