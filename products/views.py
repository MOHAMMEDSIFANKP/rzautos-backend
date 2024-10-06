import models as product_models

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

    def create_response(self, data, message, status_code=6000, detail="Success", page=None, total_count=None):
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
        