from django.test import TestCase,Client
from .models import CarDealer, CarMake, CarModel,DealerReview
# Create your tests here.


class FunctionalTestCase(TestCase):
   
    def setUp(self):
        CarDealer.objects.create(address="1234", city="city", full_name="name", id=1, lat=1, long=1, short_name="short", st="st", zip="zip")
        CarMake.objects.create(name="name", description="description")
        CarModel.objects.create(car_make=CarMake.objects.get(id=1), name="name", type_c="type", dealer_id=1, year="2020")
        DealerReview.objects.create(dealership=CarDealer.objects.get(id=1), name="name", purchase="purchase", review="review", purchase_date="2020-01-01", car_make="make", car_model="model", car_year="2020", sentiment="sentiment", id=1)

    def assert_has_attr(self, obj, attr):
        self.assertTrue(hasattr(obj, attr), msg="Object {} doesn't have attribute {}".format(obj, attr))

        
    
    def main(self):
        self.assert_has_attr(CarDealer.objects.get(id=1), "address")

        


if __name__ == "__main__":
    functTest = FunctionalTestCase()
    functTest.main()