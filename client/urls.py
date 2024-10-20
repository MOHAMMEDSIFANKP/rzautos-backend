from django.urls import path
from . import views

urlpatterns = [
    path('home-page-carousel/', views.HomePageCarouselApi.as_view(), name='home-page-carousel'),
    path('cars/', views.CarsApi.as_view(), name='cars-list'),
    path('cars/<uuid:id>/', views.CarsSingleApi.as_view(), name='cars-detail'),
    path('testimonials/', views.TestimonialsApi.as_view(), name='testimonials-list'),
    path('faq/', views.FaqApi.as_view(), name='faq-list'),
    path('seo/', views.SeoAPIView.as_view(), name='seo-list'),
    path('enquiry/', views.EnquiryApi.as_view(), name='enquiry'),
    path('resale-enquiry/', views.ResaleEnquiryApi.as_view(), name='resale-enquiry'),
    path('popular-services/', views.PopularServicesAPIView.as_view(), name='popular-services-get'),
    path('head-office/', views.HeadOfficeAPIView.as_view(), name='head-office-get'),

# Suggestion
    path('transmission/', views.TransmissionAPIView.as_view(), name='transmission-list'),
    path('fuel-types/', views.FuelTypeAPIView.as_view(), name='fuel-types-list'),



]