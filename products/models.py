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
    
class Make(BaseModel):
    logo = models.FileField(upload_to='company_logo', blank=True,null=True)
    company_name = models.CharField(max_length=255)
    description = models.TextField(blank=True,null=True)

    class Meta:
        db_table = 'products.company'
        verbose_name = 'Make'
        verbose_name_plural = 'Makes'
        ordering = ('-date_added',)

    def __str__(self) -> str:
        return self.company_name 

class Cars(BaseModel): 
    VEHICLE_TYPE_CHOICES = [
        ('CAR', 'Car'),
        ('BIKE', 'Bike'),
        ('TRUCK', 'Truck'),
        ('BUS', 'Bus'),
        ('VAN', 'Van'),
        ('SUV', 'SUV'),
        ('MOTORCYCLE', 'Motorcycle'),
        ('SCOOTER', 'Scooter'),
        ('TRACTOR', 'Tractor'),
        ('ATV', 'All-Terrain Vehicle (ATV)'),
        ('PICKUP', 'Pickup Truck'),
        ('MINIVAN', 'Minivan'),
        ('CONVERTIBLE', 'Convertible'),
        ('COUPE', 'Coupe'),
        ('WAGON', 'Wagon'),
        ('LIMOUSINE', 'Limousine'),
        ('TRAILER', 'Trailer'),
    ]
    thumbnail = models.ImageField(upload_to='car_images/thumbnail')
    make = models.ForeignKey(
        Make, 
        on_delete=models.CASCADE, 
        help_text="Select the company the vehicle belongs to (e.g., bmw)"
    )
    model = models.CharField(
        max_length=50, 
        help_text="Enter the model of the vehicle (e.g., Polo, Golf)"
    )
    fuel_type = models.ForeignKey(
        FuelType, 
        on_delete=models.CASCADE, 
        help_text="Select the vehicle's fuel type (e.g., Petrol, Diesel)"
    )
    transmission = models.ForeignKey(
        Transmission, 
        on_delete=models.CASCADE, 
        help_text="Select the vehicle's transmission type (e.g., Automatic, Manual)"
    )
    vehicle_type = models.CharField(
        max_length=200,
        choices=VEHICLE_TYPE_CHOICES,
        default='CAR',
        help_text="Select the type of vehicle (Car or Bike)"
    )
    vehicle_registration = models.CharField(
        max_length=15, 
        unique=True, 
        help_text="Enter the vehicle's registration number (e.g., GD08 MDE)"
    )
    color = models.ForeignKey(
        Color, 
        on_delete=models.CASCADE, 
        help_text="Select the color of the vehicle"
    )
    chassis_number = models.CharField(
        max_length=50, 
        unique=True, 
        blank=True, 
        null=True, 
        help_text="Enter the vehicle's chassis number"
    )
    number_of_doors = models.IntegerField(
        null=True, 
        blank=True, 
        help_text="Enter the number of doors"
    )
    number_of_keys = models.IntegerField(
        null=True, 
        blank=True, 
        help_text="Enter the number of keys"
    )
    number_of_owners = models.IntegerField(
        null=True, 
        blank=True, 
        help_text="Enter the number of previous owners"
    )
    engine_size = models.DecimalField(
        max_digits=4, 
        decimal_places=1, 
        help_text="Enter engine size in liters (e.g., 2.0)"
    )
    mileage = models.IntegerField(
        null=True, 
        blank=True, 
        help_text="Enter the vehicle's mileage (in miles or kilometers)"
    )
    body_type = models.CharField(
        max_length=50, 
        blank=True, 
        null=True, 
        help_text="Enter the body type (e.g., Hatchback, Sedan)"
    )
    co2_emissions = models.DecimalField(
        max_digits=5, 
        decimal_places=1, 
        null=True, 
        blank=True, 
        help_text="Enter CO2 emissions (in g/km)"
    )
    vat_type = models.CharField(
        max_length=50, 
        blank=True, 
        null=True, 
        help_text="Enter VAT type (e.g., Marginal)"
    )
    log_book = models.BooleanField(
        default=False, 
        help_text="Check if the log book is available"
    )
    purchase_invoice_number = models.CharField(
        max_length=50, 
        blank=True, 
        null=True, 
        help_text="Enter the purchase invoice number"
    )
    sale_date = models.DateField(
        null=True, 
        blank=True, 
        help_text="Enter the sale date (if applicable)"
    )
    registration_date = models.DateField(
        null=True, 
        blank=True, 
        help_text="Enter the vehicle's registration date"
    )
    selling_price = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        null=True, 
        blank=True, 
        help_text="Enter the vehicle's selling price"
    )
    sale_price = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        null=True, 
        blank=True, 
        help_text="Enter the vehicle's sale price"
    )
    description = RichTextField(
        blank=True, 
        null=True, 
        help_text="Provide a detailed description of the vehicle"
    )
    slug = models.SlugField(
        default="", 
        unique=True, 
        help_text="Unique identifier for the vehicle's URL (auto-generated)"
    )

    class Meta:
        db_table = 'products.cars'
        verbose_name = 'car'
        verbose_name_plural = 'cars'
        ordering = ('-date_added',)

    def __str__(self):
        return f"{self.make} {self.model} ({self.vehicle_registration})"
    
class CarImages(BaseModel):
    car = models.ForeignKey(Cars, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='car_images')
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
        return f"Report for {self.car.make} {self.car.model} ({self.car.vehicle_registration})"
