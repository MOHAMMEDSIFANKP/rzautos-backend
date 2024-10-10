from rest_framework import serializers
from .models import *

class TestimonialsSerializers(serializers.ModelSerializer):
    class Meta:
        model = Testimonials
        fields = ['id','name','location','review_text','profile_picture']

class Faqserializers(serializers.ModelSerializer):
    class Meta:
        model = Faq
        fields = ['id','question','answer']

class Enquiryserializers(serializers.ModelSerializer):
    car_name = serializers.SerializerMethodField()
    class Meta:
        model = Enquiry
        fields = ['id','car','name','number','email','message','car_name']

    def get_car_name(self,obj):
        car_model = obj.car.model if obj.car.model else ''
        return f'{obj.car.company.company_name} - {car_model}'

class HomePageCarouselSerializers(serializers.ModelSerializer):
    class Meta:
        model = HomePageCarousel
        fields = ['id', 'image', 'title_1', 'title_2']
class SeoSerializer(serializers.ModelSerializer):
    class Meta:
        model = SEO
        fields = ['id', 'page', 'path', 'meta_title','meta_description']
