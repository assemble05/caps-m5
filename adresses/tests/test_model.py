from django.test import TestCase
from adresses.models import Address
import ipdb

class AddressModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):

        cls.address_data =  {
            "country" : "brasil",
            "state" : "sp",
            "city" : "sp",
            "street" : "casa do pardal2",
            "number" : 32,
            "complement" : "house",
            "zip_code" : 1245234534
        }

        cls.address = Address.objects.create(**cls.address_data)

    def test_coutry_name_max_length(self):
        address = Address.objects.get(country="brasil")
        max_length = address._meta.get_field("country").max_length
        self.assertEqual(max_length,25)
    
    def test_state_name_max_length(self):
        address = Address.objects.get(country="brasil")
        max_length = address._meta.get_field("state").max_length
        self.assertEqual(max_length,35)
    
    def test_street_name_max_length(self):
        address = Address.objects.get(country="brasil")
        max_length = address._meta.get_field("street").max_length
        self.assertEqual(max_length,105)

    def test_city_name_max_length(self):
        address = Address.objects.get(country="brasil")
        max_length = address._meta.get_field("city").max_length
        self.assertEqual(max_length,35)
    

    
    def test_address_has_information_fields(self):              
        self.assertIsNotNone(self.address.country)
        self.assertIsNotNone(self.address.city)
        self.assertIsNotNone(self.address.complement)
        self.assertIsNotNone(self.address.street)
        self.assertIsNotNone(self.address.state)
        self.assertIsNotNone(self.address.zip_code)

