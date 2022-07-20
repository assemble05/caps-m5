from unicodedata import category
from rest_framework.test import APITestCase
from django.urls import reverse
from users.models import User
from rest_framework.authtoken.models import Token
from categories.models import Category
import ipdb


class TestUserViews(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.login_url = reverse("login_view")
        cls.register_url = reverse("list_create_user")

        cls.user_data1 = {
            "first_name": "Gordon",
            "last_name": "Charlie",
            "email": "charlie2233343d3dsasade33@mail.com",
            "phone": 123432321,
            "password": "123",
            "description": "sou legal",
        }

        cls.userlogin = {
            "email": "charlie2233343d3dsasade33@mail.com",
            "password": "123",
        }

        cls.user = User.objects.create_user(**cls.user_data1)
        cls.token = Token.objects.create(user=cls.user)
        cls.user_token = f"Token {cls.token.key}"
        cls.get_user_id = f"{cls.register_url}{cls.user.id}/"

        cls.category_data = {
            "nome": "Pintura",
            "description": "Pintura em casas e apartamentos",
        }
        cls.category = Category.objects.create(**cls.category_data)

    def setUp(self) -> None:
        self.user_data2 = {
            "first_name": "Gordon",
            "last_name": "Charlie",
            "email": "gordoncharlie@mail.com",
            "phone": 123432321,
            "password": "123",
            "description": "sou legal",
            "address": {
                "country": "brasil",
                "state": "sp",
                "city": "sp",
                "street": "casa do pardal2",
                "number": 32,
                "complement": "house",
                "zip_code": 1245234534,
            },
            "categories": [f'{self.category.id}'],
        }
        self.user_login = {
            "email": "gordoncharlie@mail.com",
            "password": "123",
        }

    def test_list_user_id_no_auth(self):
        res = self.client.get(self.get_user_id)
        response = res.json()
        self.assertEqual(res.status_code, 401)
        self.assertEqual(
            response.get("detail"), "Authentication credentials were not provided."
        )

    def test_list_user_id_auth(self):
        res = self.client.get(self.get_user_id, HTTP_AUTHORIZATION=self.user_token)
        response = res.json()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(bool(response.get("id")), True)

    def test_user_register_fail(self):
        res = self.client.post(self.register_url)
        response = res.json()
        self.assertEqual(response["email"], ["This field is required."])
        self.assertEqual(response["first_name"], ["This field is required."])
        self.assertEqual(response["last_name"], ["This field is required."])
        self.assertEqual(res.status_code, 400)

    def test_user_register_success(self):
        res = self.client.post(self.register_url, self.user_data2)
        response = res.json()
        self.assertEqual(res.status_code, 201)
        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(bool(response["id"]), True)

    def test_login_success(self):
        res = self.client.post(
            self.login_url,
            {
                "email": self.user_data1.get("email"),
                "password": self.user_data1.get("password"),
            },
        )
        response = res.json()
        self.assertEqual(response.get("token"), self.token.key)

    def test_login_fail(self):
        res = self.client.post(
            self.login_url, {"email": self.user_data1.get("email"), "password": "abc"}
        )
        response = res.json()
        self.assertEqual(response.get("detail"), "invalid username or password")
