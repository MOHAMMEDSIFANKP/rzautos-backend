from django.db import models
from web.models import BaseModel
from ckeditor.fields import RichTextField
# Create your models here.

class Transmission(BaseModel):
    transmission = models.CharField(max_length=200, help_text="eg: automatic or manual")

    class Meta:
        db_table = 'products.transmission'
        verbose_name = 'Transmission'
        verbose_name_plural = 'Transmissions'
        ordering = ('-date_added',)

    def __str__(self) -> str:
        return self.transmission if self.transmission else str(self.id)
    
class FuelType(BaseModel):
    fuel_type = models.CharField(max_length=250, help_text="eg: petrol or diesel")

    class Meta:
        db_table = 'products.fuel_type'
        verbose_name = 'Fuel Type'
        verbose_name_plural = 'Fuel Types'
        ordering = ('-date_added',)

    def __str__(self) -> str:
        return self.fuel_type if self.fuel_type else str(self.id)
    
class Color(BaseModel):
    color = models.CharField(max_length=200, help_text="eg: red or black")

    class Meta:
        db_table = 'products.color'
        verbose_name = 'color'
        verbose_name_plural = 'colors'
        ordering = ('-date_added',)

    def __str__(self) -> str:
        return self.color if self.color else str(self.id)
    
class Company(BaseModel):
    logo = models.FileField(upload_to='company_logo', blank=True,null=True)
    company_name = models.CharField(max_length=255)
    description = models.TextField(blank=True,null=True)

    class Meta:
        db_table = 'products.company'
        verbose_name = 'Company'
        verbose_name_plural = 'Companys'
        ordering = ('-date_added',)

    def __str__(self) -> str:
        return self.company_name if self.company_name else str(self.id)

class Cars(BaseModel): 
    vehicle_registration = models.CharField(max_length=15, unique=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    model = models.CharField(max_length=50)
    engine_size = models.DecimalField(max_digits=4, decimal_places=1, help_text="Enter engine size in liters (e.g., 2.0)")
    transmission = models.ForeignKey(Transmission, on_delete=models.CASCADE)
    fuel_type = models.ForeignKey(FuelType, on_delete=models.CASCADE)
    color = models.ForeignKey(Color, on_delete=models.CASCADE)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2,null=True, blank=True)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    description = RichTextField(blank=True,null=True)
    slug = models.SlugField(default="", unique=True)
    
    class Meta:
        db_table = 'products.cars'
        verbose_name = 'cars'
        verbose_name_plural = 'cars'
        ordering = ('-date_added',)


    def __str__(self):
        return f"{self.company} {self.model} ({self.vehicle_registration})"
        
    
class CarImages(BaseModel):
    car = models.ForeignKey(Cars, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='car_ihotos')
    image_alt = models.CharField(max_length=255,blank=True,null=True)

    class Meta:
        db_table = 'products.car_images'
        verbose_name = 'Car Image'
        verbose_name_plural = 'Car Images'
        ordering = ('-date_added',)

    def __str__(self) -> str:
        return str(self.id)


class Expense(BaseModel):
    car = models.ForeignKey(Cars, on_delete=models.CASCADE, related_name='expenses', null=True, blank=True)
    car_expense_amount = models.DecimalField(max_digits=10, decimal_places=2)
    company_expense_amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    date = models.DateField()

    class Meta:
        db_table = 'products.expense'
        verbose_name = 'Expense'
        verbose_name_plural = 'Expenses'
        ordering = ('-date_added',)

    def __str__(self):
        return f"{self.car}"


class Report(BaseModel):
    car = models.OneToOneField(Cars, on_delete=models.CASCADE)
    sold_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    cost_price = models.DecimalField(max_digits=10, decimal_places=2)
    additional_expenses = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def total_expenses(self):
        return self.cost_price + (self.additional_expenses or 0)

    class Meta:
        db_table = 'products.report'
        verbose_name = 'Report'
        verbose_name_plural = 'Reports'
        ordering = ('-date_added',)

    def __str__(self):
        return f"Report for {self.car.company} {self.car.model} ({self.car.vehicle_registration})"
