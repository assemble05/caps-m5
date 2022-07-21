from adresses.models import Address
from adresses.serializers import AddressSerializer
from categories.models import Category
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from users.models import User


class AccountViewsTest(APITestCase):
    @classmethod
    def setUpTestData(cls):

        cls.contractor = User.objects.create_user(
            email="goleiro_cassio@mail.com",
            password="123546",
            first_name="Goleiro",
            last_name="Cassioo",
            is_provider=False,
            phone="1140028922",
        )
        cls.contractor_token = Token.objects.create(user=cls.contractor)

        cls.address = Address.objects.create(
            country="brasil",
            state="sp",
            city="sp",
            street="casa do pardal2",
            number=32,
            complement="house",
            zip_code=1245234534,
        )

        cls.category = Category.objects.create(
            nome="Limpeza", description="Limpeza de casa e prédios"
        )

        cls.service_info = {
            "title": "limpar calha",
            "description": "tem que limpar a calha muito bem ",
            "price": 200,
            "category_id": cls.category.id,
        }

    def test_create_service(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.contractor_token.key}")
        serializer = AddressSerializer(instance=self.address)
        self.service_info["address"] = serializer.data

        response = self.client.post(
            f"/api/service/",
            self.service_info,
            format="json",
        )

        self.assertEqual(response.status_code, 201)
