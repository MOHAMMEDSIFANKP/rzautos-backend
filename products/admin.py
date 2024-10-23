import csv
from django.http import HttpResponse
from django.contrib import admin
from .models import *
from utils.helper import generate_pdf
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

@admin.register(Cars)
class CarsAdmin(admin.ModelAdmin):
    list_display = ('vehicle_registration','make','model','engine_size','transmission','fuel_type','selling_price')
    list_filter = ('make__company_name','transmission__transmission','fuel_type__fuel_type','color__color','date_added', 'is_hide')
    search_fields = ('vehicle_registration','model')
    prepopulated_fields = {"slug": ("vehicle_registration",)}

@admin.register(CarImages)
class CarImagesAdmin(admin.ModelAdmin):
    list_display = ('image_alt',)
    list_filter = ('car__vehicle_registration','car__make__company_name','date_added', 'is_hide')
    search_fields = ('car__model','car__make__company_name')

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
