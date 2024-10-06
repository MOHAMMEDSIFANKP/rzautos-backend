from django.db import models
import uuid
from django.utils import timezone
from ckeditor.fields import RichTextField

class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date_added = models.DateTimeField(db_index=True, default=timezone.now, editable=True)
    date_updated = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False, db_index=True)

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
    profile_picture = models.ImageField(upload_to='testimonials/', null=True, blank=True)

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
    