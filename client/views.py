from products import models as product_models
from web import models as web_models

from products import serializers as project_serializers
from web import serializers as web_serializers

from utils.filters import custom_filter
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import get_template
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
# Create your views here.


class BaseAPIView(APIView):
    """
    Base API view class providing common methods for handling queries and responses.
    """
    model = None
    serializer_class = None

    def get_queryset(self):
        return self.model.objects.filter(is_deleted=False)

    def get_object(self, id):
        return get_object_or_404(self.get_queryset(), id=id)

    def create_response(self, data, message, status_code=6000, detail="Success", page=None, total_count=None,images=None):
        response = {
            "StatusCode": status_code,
            "detail": detail,
            "data": data,
            "message": message
        }
        if page is not None:
            response['page'] = page
        if total_count is not None:
            response['total_count'] = total_count
        if images is not None:
            response['images'] = images
        return Response(response, status=status.HTTP_200_OK)

    def validate_pagination(self, request):
        """
        Validates pagination parameters. if params is all return all datas
        """
        try:
            page = int(request.GET.get('page', 1))
            page_limit_param = request.GET.get('page_limit', '10')
        
            if page_limit_param == 'all':
                page_limit = self.get_queryset().count()
            else:
                page_limit = int(page_limit_param)
            if page < 1 or page_limit < 1:
                raise ValueError("Page and page_limit must be positive integers.")
            return page, page_limit
        except ValueError:
            return None, None
        

class HomePageCarouselApi(BaseAPIView):
    """
    API view to retrieve Home Page Carousel.
    """
    model = web_models.HomePageCarousel
    serializer_class = web_serializers.HomePageCarouselSerializers

    def get(self, request):
        try:
            queryset = self.get_queryset()
            serializer = self.serializer_class(queryset.order_by('-date_added'), many=True, context={'request': request})
            return self.create_response(
                data=serializer.data,
                message="Home Page Carousel data fetched successfully",
            )
        except Exception as e:
            return Response({
                "StatusCode": 6004,
                "detail": "Error fetching Home Page Carousel data",
                "message": str(e)
            }, status=status.HTTP_200_OK)


class CarsApi(BaseAPIView):
    """
    API view to retrieve Home Page Carousel.
    """
    model = product_models.Cars
    serializer_class = project_serializers.CarsSerializers

    def get(self, request):
        try:
            price_order_type = request.GET.get('price_order_type', 'low')
            page, page_limit = self.validate_pagination(request)
            if page is None or page_limit is None:
                return self.create_response(data=[], message="Invalid pagination parameters", status_code=6004, detail="Bad Request")
            
            queryset = self.get_queryset()
            if price_order_type:
                if price_order_type == 'low':
                    queryset = queryset.order_by('selling_price')
                elif price_order_type == 'high':  
                    queryset = queryset.order_by('-selling_price')
            filter_params = request.GET.dict()
            search_fields = ['model','company__company_name','body_type','fuel_type__fuel_type','vehicle_registration','chassis_number','transmission__transmission']
            paginated_queryset = custom_filter(
                queryset,
                filter_params,
                search_fields,
                page,
                page_limit
            )
            serializer = self.serializer_class(paginated_queryset, many=True, context={'request': request})
            return self.create_response(
                data=serializer.data,
                message="Cars data fetched successfully",
                page=paginated_queryset.number,
                total_count=paginated_queryset.paginator.count
            )
        except Exception as e:
            return self.create_response(
                data=serializer.data,
                message=str(e),
                status_code=6004,
                detail="Error fetching Cars data"
            )
        
class CarsSingleApi(BaseAPIView):
    """
    API view to retrieve Cars and related images.
    """
    model = product_models.Cars
    serializer_class = project_serializers.CarsSerializers

    def get(self, request, id=None):
        try:
            if id:
                # Get the specific car object by ID
                queryset = self.get_object(id)
                serializer = self.serializer_class(queryset, context={'request': request})

                # Get the related car images
                car_images_queryset = product_models.CarImages.objects.filter(car=id, is_deleted=False)
                car_image_serializer = project_serializers.CarImagesSerializer(
                    car_images_queryset, many=True, context={'request': request}
                )

                return self.create_response(
                    data={
                        'car_data': serializer.data,
                        'car_images': car_image_serializer.data
                    },
                    message=f'{queryset.model} data fetched successfully',
                )
            else:
                queryset = self.get_queryset()
                serializer = self.serializer_class(queryset, many=True, context={'request': request})

                return self.create_response(
                    data=serializer.data,
                    message="Cars data fetched successfully",
                )
        except Exception as e:
            return self.create_response(
                data=[],
                message=str(e),
                status_code=6004,
                detail="Error fetching Cars data"
            )


class TestimonialsApi(BaseAPIView):
    """
    API view to retrieve Testimonials.
    """
    model = web_models.Testimonials
    serializer_class = web_serializers.TestimonialsSerializers

    def get(self, request):
        try:
            queryset = self.get_queryset()
            serializer = self.serializer_class(queryset, many=True, context={'request': request})
            return self.create_response(
                data=serializer.data,
                message="Testimonials data fetched successfully",
            )
        except Exception as e:
            return self.create_response(
                data=serializer.data,
                message=str(e),
                status_code=6004,
                detail="Error fetching Testimonials data"
            )

class FaqApi(BaseAPIView):
    """
    API view to retrieve Faq.
    """
    model = web_models.Faq
    serializer_class = web_serializers.Faqserializers

    def get(self, request):
        try:
            queryset = self.get_queryset()
            serializer = self.serializer_class(queryset, many=True, context={'request': request})
            return self.create_response(
                data=serializer.data,
                message="Faq data fetched successfully",
            )
        except Exception as e:
            return self.create_response(
                data=serializer.data,
                message=str(e),
                status_code=6004,
                detail="Error fetching Faq data"
            )

class SeoAPIView(BaseAPIView):
    """
    API view to retrieve Seo.
    """
    model = web_models.SEO
    serializer_class = web_serializers.SeoSerializer

    def get(self, request):
        page, page_limit = self.validate_pagination(request)
        if page is None or page_limit is None:
            return self.create_response(data=[], message="Invalid pagination parameters", status_code=6004, detail="Bad Request")

        filter_params = request.GET.dict()
        search_fields = ['page','path']
        paginated_queryset = custom_filter(
            self.get_queryset(),
            filter_params,
            search_fields,
            page,
            page_limit
        )

        serializer = self.serializer_class(paginated_queryset, many=True, context={'request': request})
        return self.create_response(
            data=serializer.data,
            message="Seo Choice data fetched successfully",
            page=paginated_queryset.number,
            total_count=paginated_queryset.paginator.count
        )

from datetime import datetime

class EnquiryApi(BaseAPIView):
    """
    API view to retrieve Faq.
    """
    model = web_models.Enquiry
    serializer_class = web_serializers.Enquiryserializers

    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                serializer.save()

                context = {
                    'name': serializer.data['name'],
                    'email': serializer.data['email'],
                    'number': serializer.data['number'],
                    'message': serializer.data['message'],
                    'car_name': serializer.data['car_name'],
                    'date_added': datetime.strptime(serializer.data['date_added'], '%Y-%m-%dT%H:%M:%S.%fZ').strftime('%d-%m-%y')
                }
                template = get_template('enquiry-email.html').render(context)
                e=settings.EMAIL_HOST_USER
                send_mail(
                    'Enquiry Data',
                    None, 
                    settings.EMAIL_HOST_USER,
                    ['muhammadsifan.accolades@gmail.com'],
                    fail_silently=False,
                    html_message = template,
                    )
                return self.create_response(
                    data=serializer.data,
                    message="Enquiry successfully",
                    status_code=6001,
                )
            else:
                return self.create_response(
                    data="",
                    detail="Erro",
                    status_code=6004,
                    message='Invalid data'
                )
            
        except Exception as e:
            return self.create_response(
                data=serializer.data,
                message= f'Something went wrong {e}',
                status_code=6004,
                detail="Error fetching Faq data"
            )
        

# Filter Suggestions
class TransmissionAPIView(BaseAPIView):
    """
    API view to retrieve Transmission Suggestion.
    """
    model = product_models.Transmission
    serializer_class = project_serializers.TransmissionSerializers

    def get(self, request):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True, context={'request': request})
        return self.create_response(
            data=serializer.data,
            message="Transmission data fetched successfully",
        )
    
class FuelTypeAPIView(BaseAPIView):
    """
    API view to retrieve Transmission Suggestion.
    """
    model = product_models.FuelType
    serializer_class = project_serializers.FuelTypeSerializers

    def get(self, request):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True, context={'request': request})
        return self.create_response(
            data=serializer.data,
            message="Fuel Type data fetched successfully",
        )