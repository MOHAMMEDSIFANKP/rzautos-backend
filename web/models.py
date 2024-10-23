from django.db import models
import uuid
from django.utils import timezone
from utils.helper import OptimalImageField

class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date_added = models.DateTimeField(db_index=True, default=timezone.now, editable=True)
    date_updated = models.DateTimeField(auto_now=True)
    is_hide = models.BooleanField(default=False, db_index=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.date_added:
            self.date_added = timezone.now()
        super(BaseModel, self).save(*args, **kwargs)


class Testimonials(BaseModel):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255, null=True, blank=True)
    review_text = models.TextField()
    profile_picture = OptimalImageField(
        upload_to='testimonials/',
        size_threshold_kb=700,  
        max_dimensions=(1920, 1080)  
    )
    
    class Meta:
        db_table = 'web.testimonials'
        verbose_name = 'Testimonial'
        verbose_name_plural = 'Testimonials'
        ordering = ('-date_added',)


    def __str__(self):
        return f"Testimonial by {self.name} from {self.location}"


class Faq(BaseModel):
    question = models.CharField(max_length=300)
    answer = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'web.faq'
        verbose_name = 'Faq'
        verbose_name_plural = 'Faqs'
        ordering = ('-date_added',)


    def __str__(self):
        return self.question
    
class ResaleEnquiry(BaseModel):
    name = models.CharField(max_length=300, blank=True, null=True)
    number = models.PositiveBigIntegerField(blank=True, null=True)
    email = models.EmailField(null=True, blank=True)
    make = models.CharField(max_length=300,blank=True,null=True)
    model = models.CharField(max_length=500,blank=True,null=True)
    registration = models.CharField(max_length=300,blank=True,null=True)
    mileage = models.CharField(max_length=100,blank=True,null=True)
    transmission = models.CharField(max_length=255,blank=True,null=True)
    body_type = models.CharField(max_length=255,blank=True,null=True)
    fuel_type = models.CharField(max_length=255,blank=True,null=True)
    color = models.CharField(max_length=255,blank=True,null=True)

    class Meta:
        db_table = 'web.resaleenquiry'
        verbose_name = 'Resale Enquiry'
        verbose_name_plural = 'Resale Enquirys'
        ordering = ('-date_added',)

    def __str__(self):
        return self.name if self.name else str(self.id)
    
class ResaleEnquiryImages(BaseModel):
    resale = models.ForeignKey(ResaleEnquiry, on_delete=models.CASCADE)
    image =  OptimalImageField(
        upload_to='resale_enquiry/',
        size_threshold_kb=700,  
        max_dimensions=(1920, 1080)  
    )
    
    class Meta:
        db_table = 'web.resaleenquiryimages'
        verbose_name = 'Resale Enquiry Images'
        verbose_name_plural = 'Resale Enquiry Images'
        ordering = ('-date_added',)

    def __str__(self):
        return str(self.id)
    

class Enquiry(BaseModel):
    car = models.ForeignKey('products.Cars',on_delete=models.CASCADE,blank=True,null=True)
    name = models.CharField(max_length=300, blank=True, null=True)
    number = models.PositiveBigIntegerField(blank=True, null=True)
    email = models.EmailField(null=True, blank=True)
    message = models.TextField(null=True, blank=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        db_table = 'web.enquiry'
        verbose_name = 'Enquiry'
        verbose_name_plural = 'Enquirys'
        ordering = ('-date_added',)


    def __str__(self):
        return self.name if self.name else str(self.id)

class HomePageCarousel(BaseModel):
    image = OptimalImageField(
        upload_to='carousel/',
        size_threshold_kb=700,  
        max_dimensions=(1920, 1080)  
    )    
    title_1 = models.CharField(max_length=300,null=True,blank=True)
    title_2 = models.CharField(max_length=300)

    class Meta:
        db_table='web.homepagecarousel'
        verbose_name = ('HomePage Carousels')
        verbose_name_plural = ('HomePage Carousel')
        ordering = ('date_added',)

    def __str__(self):
        return self.title_2 if self.title_2 else str(self.id)

class PopularServices(BaseModel):
    title = models.CharField(max_length=300)
    icon = models.FileField(upload_to='popular_service',null=True,blank=True)
    description = models.TextField(null=True,blank=True)

    class Meta:
        db_table='web.popularservices'
        verbose_name = ('PopularServices')
        verbose_name_plural = ('PopularServices')
        ordering = ('date_added',)

    def __str__(self) -> str:
        return self.title


from django.core.exceptions import ValidationError

class HeadOffice(models.Model):
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    office_hours = models.CharField(max_length=100)
    footer_content = models.TextField()
    instagram = models.TextField()
    facebook = models.TextField()
    linked_in = models.TextField()
    twitter = models.TextField()


    def save(self, *args, **kwargs):
        if HeadOffice.objects.exists() and not self.pk:
            raise ValidationError("Only one HeadOffice instance is allowed.")
        super().save(*args, **kwargs)

    def __str__(self):
        return "Web Site Information"

class SEO(BaseModel):
    page=models.CharField(max_length=200,blank=True,null=True)
    path=models.CharField(max_length=200)
    meta_title=models.TextField(blank=True,null=True)
    meta_description=models.TextField(blank=True,null=True)
    class Meta:
        db_table='web.seo'
        verbose_name = ('SEO')
        verbose_name_plural = ('SEO')
        ordering = ('date_added',)

    def __str__(self):
        return self.path if self.path else str(self.id)
    