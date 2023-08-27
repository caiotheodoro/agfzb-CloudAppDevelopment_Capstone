from django.db import models
from django.utils.timezone import now
from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _

# Create your models here.

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object
class CarMake(models.Model):
    name = models.CharField(null=False, max_length=35,primary_key=True)
    description = models.CharField(null=False, max_length=200)

    def __str__(self):
        return 'Name:' + self.name + ',' + \
            'Description:' + self.description

# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
# - Name
# - Dealer id, used to refer a dealer created in cloudant database
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
# - Year (DateField)
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object
class CarModel(models.Model):
    #class CarType(models.TextChoices):
    #    COUPE = 'CPE', _('Coupe')
    #    PICKUP = 'PKU', _('Pickup')
    #    SEDAN = 'SDN', _('Sedan')
    #    SUV = 'SUV'
    #    WAGON = 'WGN', _('wagon')

    CarType = (
        ('CPE', 'COUPE'),
        ('PKU', 'PICKUP'),
        ('SDN', 'SEDAN'),
        ('SUV', 'SUV'),
        ('WGN', 'WAGON')
    )

    
    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    name = models.CharField(null=False, max_length=60,primary_key=True)
    dealer_id = models.IntegerField(null=False)
    car_type = models.CharField(null=False, choices=CarType, max_length=25)
    #car_type = models.CharField(null=False, choices=CarType.choices, max_length=25)
    year = models.PositiveSmallIntegerField(null=False, validators=[MinValueValidator(1900)])
    
    def __str__(self):
        #return (str(self.year) + " " + self.name + " " + self.car_type)
        return 'Name ' + self.name

# <HINT> Create a plain Python class `CarDealer` to hold dealer data
class CarDealer:
    def __init__(self, address, city, full_name, id, lat, long, short_name, st, zip, state):
        self.address = address
        self.city = city
        self.full_name = full_name
        self.id = id
        self.lat = lat
        self.long = long
        self.short_name = short_name
        self.st = st
        self.zip = zip
        self.state = state

    def __str__(self):
        return "Dealer name: " + self.full_name

# <HINT> Create a plain Python class `DealerReview` to hold review data
class DealerReview:
    def __init__(self, dealership, name, purchase, review, purchase_date,
        car_make, car_model, car_year, sentiment, id):
        self.dealership = dealership
        self.name = name
        self.purchase = purchase
        self.review = review
        self.purchase_date = purchase_date
        self.car_make = car_make
        self.car_model = car_model
        self.car_year = car_year
        self.sentiment = sentiment
        self.id = id
    
    def __str__(self):
        return "Review: " + self.review