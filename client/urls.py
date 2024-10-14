from django.urls import path
from . import views

urlpatterns = [
    path('home-page-carousel/', views.HomePageCarouselApi.as_view(), name='home-page-carousel'),
    path('cars/', views.CarsApi.as_view(), name='cars-list'),
    path('cars/<uuid:id>/', views.CarsSingleApi.as_view(), name='cars-detail'),
    path('testimonials/', views.TestimonialsApi.as_view(), name='testimonials-list'),
    path('faq/', views.FaqApi.as_view(), name='faq-list'),
    path('seo/', views.SeoAPIView.as_view(), name='seo-list'),
    path('enquiry/', views.EnquiryApi.as_view(), name='fuel-types-list'),

# Suggestion
    path('transmission/', views.TransmissionAPIView.as_view(), name='transmission-list'),
    path('fuel-types/', views.FuelTypeAPIView.as_view(), name='fuel-types-list'),



]
