from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from categories.serializers import CategorySerializer
from categories.models import Category
from users.models import User


class ReviewCreateViewTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.nome = "Pintura residencial"

        cls.max_length_nome = "Pinturas residenciais para casas apartamentos"

        cls.err_max_length_nome = "Pinturas residenciais para casas apartamentos da cor que você quiser"

        cls.description = """Lorem ipsum dolor sit amet, 
        consectetur adipiscing elit, sed do eiusmod tempor 
        incididunt ut labore et dolore magna aliqua."""

        cls.max_length_description = """Lorem ipsum dolor sit amet, 
        consectetur adipiscing elit, sed do eiusmod tempor 
        incididunt ut labore et dolore magna aliqua. Lorem ipsum dolor sit amet, 
        consectetur adipiscing elit, sed do eiusmod tempor 
        incididunt ut l."""

        cls.err_max_length_description = """Lorem ipsum dolor sit amet, 
        consectetur adipiscing elit, sed do eiusmod tempor 
        incididunt ut labore et dolore magna aliqua. Lorem ipsum dolor sit amet, 
        consectetur adipiscing elit, sed do eiusmod tempor 
        incididunt ut labore et dolore magna aliqua."""

        cls.admin = User.objects.create_superuser(
            email="boss@mail.com",
            password="123546",
            first_name="Cleiton",
            last_name="nevez",
            is_provider=False,
            phone="1140028922",
        )

        cls.admin_token = Token.objects.create(user=cls.admin)

    def test_admin_create_category(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.admin_token.key}")

        request_body = {
            "nome":"Pedriro",
            "description":"Faço obras"
        }

        response = self.client.post(
            f"/api/category/",
            request_body,
            format="json",
        )

        self.assertEqual(response.status_code, 201)
        self.assertIn(
            response.data, CategorySerializer(Category.objects.all(), many=True).data
        )

    def test_update_category(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.admin_token.key}")

        request_body = {
            "nome":"Pedreiro",
            "description":"Faço obras"
        }

        response = self.client.post(
            f"/api/category/",
            request_body,
            format="json",
        )

        category_id = response.data["id"]

        update_data = {
            "nome":"empreiteiro"
        }

        response = self.client.patch(
            f"/api/category/{category_id}/",
            update_data,
            format="json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn(
            response.data, CategorySerializer(Category.objects.all(), many=True).data
        )

    def test_delete_category(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.admin_token.key}")

        request_body = {
            "nome":"Pedreiro",
            "description":"Faço obras"
        }

        response = self.client.post(
            f"/api/category/",
            request_body,
            format="json",
        )

        category_id = response.data["id"]

        response = self.client.delete(
            f"/api/category/{category_id}/",
        )

        self.assertEqual(response.status_code, 204)
