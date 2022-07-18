from django.db import IntegrityError
from django.test import TestCase
from reviews.models import Review
from services.models import Service
from users.models import User


class ReviewModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.stars = 5
        cls.description = """Lorem ipsum dolor sit amet, 
        consectetur adipiscing elit, sed do eiusmod tempor 
        incididunt ut labore et dolore magna aliqua."""

        cls.contractor = User.objects.create_user(
            email="goleiro_cassio@mail.com",
            password="123546",
            first_name="Goleiro",
            last_name="Cassioo",
            is_provider=False,
            phone="1140028922",
        )

        cls.provider = User.objects.create_user(
            email="roni_calma@mail.com",
            password="123546",
            first_name="Roni",
            last_name="Calma",
            is_provider=True,
            phone="1189224002",
        )

        cls.service = Service.objects.create(
            title="Concerto de pia",
            description="Preciso de concerto na pia da cozinha da minha casa.",
            price=80.00,
            contractor=cls.contractor,
            provider=cls.provider,
        )

    def test_description_max_length_and_stars_default(self):
        review = Review.objects.create(
            description=self.description,
            user_critic=self.contractor,
            user_criticized=self.provider,
            service=self.service,
        )

        max_length = review._meta.get_field("description").max_length

        self.assertEqual(max_length, 255)
        self.assertEqual(review.stars, 3)

    def test_stars_negative_value_error(self):
        with self.assertRaises(IntegrityError):
            Review.objects.create(
                stars=-2,
                description=self.description,
                user_critic=self.contractor,
                user_criticized=self.provider,
                service=self.service,
            )

    def test_review_fields_values(self):
        review = Review.objects.create(
            stars=self.stars,
            description=self.description,
            user_critic=self.contractor,
            user_criticized=self.provider,
            service=self.service,
        )

        self.assertEqual(review.user_critic, self.contractor)
        self.assertEqual(review.user_criticized, self.provider)
        self.assertEqual(review.stars, self.stars)
        self.assertEqual(review.description, self.description)
        self.assertEqual(review.service, self.service)

    def test_review_cannot_have_more_than_one_user_critic(self):
        review = Review.objects.create(
            stars=self.stars,
            description=self.description,
            user_critic=self.contractor,
            user_criticized=self.provider,
            service=self.service,
        )

        contractor_two = User.objects.create_user(
            email="mano_magica@mail.com",
            password="123546",
            first_name="Mano",
            last_name="Magica",
            is_provider=False,
            phone="1140028922",
        )

        review.user_critic = contractor_two
        review.save()

        self.assertNotIn(review, self.contractor.created_reviews.all())
        self.assertIn(review, contractor_two.created_reviews.all())

    def test_review_cannot_have_more_than_one_user_criticized(self):
        review = Review.objects.create(
            stars=self.stars,
            description=self.description,
            user_critic=self.contractor,
            user_criticized=self.provider,
            service=self.service,
        )

        provider_two = User.objects.create_user(
            email="lofi_girl@mail.com",
            password="123546",
            first_name="Lofi",
            last_name="Girl",
            is_provider=True,
            phone="1189224002",
        )

        review.user_criticized = provider_two
        review.save()

        self.assertNotIn(review, self.provider.critics.all())
        self.assertIn(review, provider_two.critics.all())

    def test_review_cannot_pertence_to_more_than_one_service(self):
        review = Review.objects.create(
            stars=self.stars,
            description=self.description,
            user_critic=self.contractor,
            user_criticized=self.provider,
            service=self.service,
        )

        service_two = Service.objects.create(
            title="Limpeza de Garage,",
            description="Preciso de alguem para limpar minha garagem empoeirada.",
            price=50.00,
            contractor=self.contractor,
            provider=self.provider,
        )

        review.service = service_two
        review.save()

        self.assertNotIn(review, self.service.reviews.all())
        self.assertIn(review, service_two.reviews.all())
