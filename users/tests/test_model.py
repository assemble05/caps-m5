from django.test import TestCase
from users.models import User
import ipdb

class UserModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.userdata = {
            "first_name": "Gordon",
            "last_name": "Charlie",
            "email": "charlie2233343d3dsasade33@mail.com",
            "phone": 123432321,
            "password": 123,
            "description": "sou legal",
        }

        cls.user = User.objects.create(**cls.userdata)

    def test_first_name_max_length(self):
        user = User.objects.get(first_name="Gordon")
        max_length = user._meta.get_field("first_name").max_length
        self.assertEqual(max_length,20)
    
    def test_last_name_max_length(self):
        user = User.objects.get(first_name="Gordon")
        max_length = user._meta.get_field('last_name').max_length
        self.assertEquals(max_length, 20)

    
    def test_user_has_information_fields(self):              
        self.assertEqual(self.user.first_name, self.userdata.get("first_name"))
        self.assertEqual(self.user.last_name, self.userdata.get("last_name"))
        self.assertIsNotNone(self.user.description)
        self.assertIsNotNone(self.user.phone)
