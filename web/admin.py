import csv
from django.http import HttpResponse
from django.contrib import admin
from .models import *
from utils.helper import generate_pdf

# Register your models here.


@admin.register(Testimonials)
class TestimonialAdmin(admin.ModelAdmin):
    search_fields = ('name', 'location', 'review_text')
    list_filter = ('date_added', 'is_deleted')

@admin.register(Faq)
class FaqAdmin(admin.ModelAdmin):
    search_fields = ('question',)
    list_filter = ('date_added', 'is_deleted')

@admin.register(Enquiry)
class EnquiryAdmin(admin.ModelAdmin):
    search_fields = ('name', 'email', 'message')
    list_filter = ('car','date_added', 'is_deleted')
    date_hierarchy = 'date_added'
    actions = ['export_as_csv','export_as_pdf']  

    def export_as_csv(self, request, queryset):
        # Create the HttpResponse object with CSV headers.
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="enquiry.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['Car', 'Name', 'Number', 'Email', 'Message', 'Date Added'])
        
        # Write data from queryset
        for enq in queryset:
            writer.writerow([
                enq.car,
                enq.name,
                enq.number,
                enq.email,
                enq.message,
                enq.date_added
            ])
        
        return response
    
    def export_as_pdf(self, request, queryset):
        context = {'enquiry': queryset}
        return generate_pdf('enquiry.html', context)

    export_as_csv.short_description = "Export Selected Reports as CSV"
    export_as_pdf.short_description = "Export Selected as PDF"

@admin.register(HomePageCarousel)
class SeoAdmin(admin.ModelAdmin):
    search_fields = ('title_1', 'title_2', )
    list_display = ('title_1', 'title_2', )
    list_filter = ('date_added', 'is_deleted')
@admin.register(SEO)
class SeoAdmin(admin.ModelAdmin):
    search_fields = ('page', 'path', )
    list_filter = ('date_added', 'is_deleted')