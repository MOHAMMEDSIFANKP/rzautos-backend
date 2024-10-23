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
        fields = ['id','car','name','number','email','message','car_name','date_added']

    def get_car_name(self,obj):
        car_model =''
        if obj.car:
            car_model = obj.car.model if obj.car.model else ''
            return f'{obj.car.make.company_name} - {car_model}'
        else:
            return None
        
class ResaleEnquirySerializers(serializers.ModelSerializer):
    class Meta:
        model = ResaleEnquiry
        fields = ['id','name','number','email','registration','mileage','transmission','body_type','fuel_type','color','date_added','make','model']

class ResaleEnquiryImagesSerializers(serializers.ModelSerializer):
    class Meta:
        model = ResaleEnquiryImages
        fields = ['id','resale','image']

class HomePageCarouselSerializers(serializers.ModelSerializer):
    class Meta:
        model = HomePageCarousel
        fields = ['id', 'image', 'title_1', 'title_2']
class SeoSerializer(serializers.ModelSerializer):
    class Meta:
        model = SEO
        fields = ['id', 'page', 'path', 'meta_title','meta_description']


class PopularServicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = PopularServices
        fields = ['id','icon','title','description']


class HeadOfficeSerializer(serializers.ModelSerializer):
    class Meta:
        model = HeadOffice
        fields = ['id','address','phone','email','office_hours','footer_content','instagram','facebook','linked_in','twitter']
