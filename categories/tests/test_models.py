from django.db import IntegrityError
from django.test import TestCase
from categories.models import Category
from users.models import User


class CategoryModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.nome = "Pintura residencial"
        cls.description = """Lorem ipsum dolor sit amet, 
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

    def test_creation_category(self):
        category = Category.objects.create(
            nome=self.nome
            description=self.description
        )

        self.assertEqual(category.nome, self.description)
        self.assertEqual(category.description, self.description)
