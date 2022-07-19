from rest_framework.test import APITestCase
from rest_framework.views import status
from rest_framework.authtoken.models import Token
import ipdb
from adresses.models import Address
from adresses.serializers import AddressSerializer
from users.models import User


class AccountViewsTest(APITestCase):
    @classmethod
    def setUpTestData(cls):

        cls.user_data1 = {
            "first_name": "Gordon",
            "last_name": "Charlie",
            "email": "gordoncharlie@mail.com",
            "phone": 123432321,
            "password": "123",
            "description": "sou legal"
        }
        cls.adrr = {
                "country" : "brasil",
                "state" : "sp",
                "city" : "sp",
                "street" : "casa do pardal2",
                "number" : 32,
                "complement" : "house",
                "zip_code" : 1245234534
            }
 
        cls.login = {"password": "123", "email": "gordoncharlie@mail.com"}
        cls.service_info = {
            "title": "limpar calha",
            "description": "tem que limpar a calha muito bem ",
            "price": 200
        }

    def test_create_service(self):
        
        adrr_create = Address.objects.create(**self.adrr)

        usert_create = User.objects.create_user(**self.user_data1)

        user_login = Token.objects.create(user=usert_create)

        self.client.credentials(HTTP_AUTHORIZATION="Token" + " " + user_login.key)
        seri  = AddressSerializer(instance=adrr_create)
        self.service_info["address"] = seri.data
        
        res_user = self.client.post(
            f'/api/accounts/{usert_create.__dict__["id"]}/service/',
            data=self.service_info,
        )

        self.assertEqual(res_user.status_code, status.HTTP_201_CREATED)
