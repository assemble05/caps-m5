from rest_framework.test import APITestCase
from services.models import Service
from users.models import User


class ServiceCreateModelTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user_data1 = {
            "first_name": "Gordon",
            "last_name": "Charlie",
            "email": "gordoncharlie@mail.com",
            "phone": 123432321,
            "password": "123",
            "description": "sou legal",
        }

        cls.user = User.objects.create_user(**cls.user_data1)

        cls.service_info = {
            "title": "limpar calha",
            "description": "tem que limpar a calha muito bem ",
            "price": 200,
            "contractor": cls.user,
        }
        cls.service = Service.objects.create(**cls.service_info)

    def test_is_delete(self):
        account = Service.objects.get(title="limpar calha")
        is_delete = account._meta.get_field("is_delete").default
        self.assertEquals(is_delete, False)

    def test_description(self):
        account = Service.objects.get(title="limpar calha")
        description = account._meta.get_field("description").max_length
        self.assertEquals(description, 255)

    def test_price(self):
        account = Service.objects.get(title="limpar calha")
        price = account._meta.get_field("price").max_digits
        self.assertEquals(price, 10)
    
    def test_title(self):
        account = Service.objects.get(title="limpar calha")
        title = account._meta.get_field("title").max_length
        self.assertEquals(title, 45)
    
    def test_is_active(self):
        account = Service.objects.get(title="limpar calha")
        is_active = account._meta.get_field("is_active").default
        self.assertEquals(is_active, True)