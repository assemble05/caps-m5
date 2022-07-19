from django.db import IntegrityError, DataError
from django.test import TestCase
from categories.models import Category
from users.models import User


class CategoryModelTest(TestCase):
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

    def test_creation_category(self):
        category = Category.objects.create(
            nome=self.nome,
            description=self.description
        )

        self.assertEqual(category.nome, self.nome)
        self.assertEqual(category.description, self.description)

    def test_nome_max_length(self):
        category = Category.objects.create(
            nome = self.max_length_nome,
            description = self.description
        )

        max_length = category._meta.get_field("nome").max_length

        self.assertEqual(max_length, 45)

    def test_description_max_length(self):
        category = Category.objects.create(
            nome = self.nome,
            description = self.test_description_max_length
        )

        max_length = category._meta.get_field("description").max_length

        self.assertEqual(max_length, 255)

    def test_error_max_length_nome(self):
        with self.assertRaises(DataError):
            Category.objects.create(
                nome = self.err_max_length_nome,
                description = self.description
            )

    def test_error_max_length_description(self):
        with self.assertRaises(DataError):
            Category.objects.create(
                nome = self.err_max_length_nome,
                description = self.err_max_length_description
            )
