import csv
from django.http import HttpResponse
from django.contrib import admin
from .models import *
from utils.helper import generate_pdf
from django.forms.widgets import FileInput
from django import forms
from django.utils.html import format_html
from django.core.exceptions import ValidationError
import imghdr

# Register your models here.

@admin.register(Transmission)
class TransmissionAdmin(admin.ModelAdmin):
    search_fields = ('transmission',)
    list_filter = ('date_added', 'is_hide')

@admin.register(FuelType)
class FuelTypeAdmin(admin.ModelAdmin):
    search_fields = ('fuel_type',)
    list_filter = ('date_added', 'is_hide')

@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    search_fields = ('color',)
    list_filter = ('date_added', 'is_hide')

@admin.register(Make)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('company_name',)
    list_filter = ('date_added', 'is_hide')
    search_fields = ('company_name',)

class MultipleFileInput(FileInput):
    allow_multiple_selected = True

class MultipleImageField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def validate_image_file(self, file):
        valid_image_types = ['jpeg', 'jpg', 'png', 'gif']
        file_type = imghdr.what(file)
        
        if file_type not in valid_image_types:
            raise ValidationError(
                f'Unsupported image format. Please use one of: {", ".join(valid_image_types)}',
                code='invalid_image'
            )

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = []
            for d in data:
                cleaned_file = single_file_clean(d, initial)
                if cleaned_file:
                    self.validate_image_file(cleaned_file)
                    result.append(cleaned_file)
            return result
        else:
            result = single_file_clean(data, initial)
            if result:
                self.validate_image_file(result)
            return result

class CarImagesInline(admin.TabularInline):
    model = CarImages
    extra = 0
    fields = ('image', 'image_alt', 'get_image_preview')
    readonly_fields = ('get_image_preview',)
    
    def get_image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 100px;"/>', obj.image.url)
        return "No Image"
    get_image_preview.short_description = 'Preview'

class CarsAdminForm(forms.ModelForm):
    multiple_images = MultipleImageField(
        required=False, 
        help_text="Hold Ctrl/Cmd to select multiple images at once. Supported formats: JPG, JPEG, PNG, GIF"
    )

    class Meta:
        model = Cars
        fields = '__all__'

@admin.register(Cars)
class CarsAdmin(admin.ModelAdmin):
    form = CarsAdminForm
    inlines = [CarImagesInline]
    
    list_display = ('vehicle_registration', 'make', 'model', 'engine_size', 
                   'transmission', 'fuel_type', 'selling_price', 'get_thumbnail_preview')
    list_filter = ('make__company_name', 'transmission__transmission', 
                  'fuel_type__fuel_type', 'color__color', 'date_added', 'is_hide')
    search_fields = ('vehicle_registration', 'model')
    prepopulated_fields = {"slug": ("vehicle_registration",)}

    fieldsets = (
        ('Basic Information', {
            'fields': ('make', 'model', 'vehicle_type', 'vehicle_registration', 'thumbnail')
        }),
        ('Vehicle Details', {
            'fields': ('transmission', 'fuel_type', 'engine_size', 'color', 'body_type',
                      'number_of_doors', 'number_of_keys', 'number_of_owners')
        }),
        ('Technical Information', {
            'fields': ('chassis_number', 'mileage', 'co2_emissions')
        }),
        ('Sales Information', {
            'fields': ('selling_price', 'sale_price', 'vat_type', 'sale_date')
        }),
        ('Documentation', {
            'fields': ('log_book', 'purchase_invoice_number', 'registration_date')
        }),
        ('Description and SEO', {
            'fields': ('description', 'slug')
        }),
        ('Additional Images', {
            'fields': ('multiple_images',),
            'description': 'Upload multiple images at once. These will be added to the existing images below.'
        }),
    )

    def get_thumbnail_preview(self, obj):
        if obj.thumbnail:
            return format_html('<img src="{}" style="max-height: 50px;"/>', obj.thumbnail.url)
        return "No Thumbnail"
    get_thumbnail_preview.short_description = 'Thumbnail'

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        
        if 'multiple_images' in request.FILES:
            files = request.FILES.getlist('multiple_images')
            for image in files:
                CarImages.objects.create(
                    car=obj,
                    image=image,
                    image_alt=f"{obj.make} {obj.model} - Additional Image"
                )

@admin.register(CarImages)
class CarImagesAdmin(admin.ModelAdmin):
    list_display = ('get_car_info', 'get_image_preview', 'image_alt')
    list_filter = ('car__vehicle_registration', 'car__make__company_name', 
                  'date_added', 'is_hide')
    search_fields = ('car__model', 'car__make__company_name', 'image_alt')
    
    def get_car_info(self, obj):
        return f"{obj.car.make} {obj.car.model} ({obj.car.vehicle_registration})"
    get_car_info.short_description = 'Car'
    
    def get_image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 50px;"/>', obj.image.url)
        return "No Image"
    get_image_preview.short_description = 'Preview'
    
@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('car','car_expense_amount','company_expense_amount')
    list_filter = ('car','date', 'is_hide')
    search_fields = ('car__model','car__make__company_name')


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('car','sold_price','cost_price','additional_expenses')
    list_filter = ('car','car__model','car__make__company_name', 'car__transmission', 'car__fuel_type', 'is_hide','date_added')
    search_fields = ('car__vehicle_registration','car__model')
    date_hierarchy = 'date_added'
    actions = ['export_as_csv','export_as_pdf']  

    def export_as_csv(self, request, queryset):
        # Create the HttpResponse object with CSV headers.
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="reports.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['Car','Transmission', 'Fuel Type' ,'Sold Price', 'Cost Price', 'Additional Expenses', 'Total Expenses', 'Date Added'])
        
        # Write data from queryset
        for report in queryset:
            writer.writerow([
                report.car,
                report.car.transmission.transmission,
                report.car.fuel_type.fuel_type,
                report.sold_price,
                report.cost_price,
                report.additional_expenses,
                report.total_expenses(),
                report.date_added.strftime("%d/%m/%Y")
            ])
        
        return response
    
    # PDF Export Function

    def export_as_pdf(self, request, queryset):
        context = {'reports': queryset}
        return generate_pdf('reports.html', context)

    export_as_csv.short_description = "Export Selected Reports as CSV"
    export_as_pdf.short_description = "Export Selected as PDF"
