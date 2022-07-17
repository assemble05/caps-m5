from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from reviews.models import Review
from reviews.serializers import ReviewSerializer
from services.models import Service
from users.models import User


class ReviewCreateViewTest(APITestCase):
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

        cls.provider = User.objects.create_user(
            email="roni_calma@mail.com",
            password="123546",
            first_name="Roni",
            last_name="Calma",
            is_provider=True,
            phone="1189224002",
        )
        cls.provider_token = Token.objects.create(user=cls.provider)

        cls.service = Service.objects.create(
            title="Concerto de pia",
            description="Preciso de concerto na pia da cozinha da minha casa.",
            price=80.00,
            contractor=cls.contractor,
            provider=cls.provider,
        )

    def test_contractor_can_create_review(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.contractor_token.key}")

        request_body = {"stars": 5, "description": "Lorem ipsum dolor sit amet"}

        response = self.client.post(
            f"/api/services/{self.service.id}/reviews/",
            request_body,
            format="json",
        )

        self.assertEqual(response.status_code, 201)
        self.assertIn(
            response.data, ReviewSerializer(Review.objects.all(), many=True).data
        )

    def test_provider_can_create_review(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.provider_token.key}")

        request_body = {"stars": 5, "description": "Lorem ipsum dolor sit amet"}

        response = self.client.post(
            f"/api/services/{self.service.id}/reviews/",
            request_body,
            format="json",
        )

        self.assertEqual(response.status_code, 201)
        self.assertIn(
            response.data, ReviewSerializer(Review.objects.all(), many=True).data
        )

    def test_incorret_create_review_fields(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.contractor_token.key}")

        incorrect_data = {"stars": -5, "description": False}

        serializer = ReviewSerializer(data=incorrect_data)

        self.assertEqual(serializer.is_valid(), False)

        response = self.client.post(
            f"/api/services/{self.service.id}/reviews/",
            incorrect_data,
            format="json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(serializer._errors, response.data)

    def test_not_authenticated_error(self):
        request_body = {"stars": 5, "description": "Lorem ipsum dolor sit amet"}

        response = self.client.post(
            f"/api/services/{self.service.id}/reviews/",
            request_body,
            format="json",
        )

        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            response.data, {"detail": "Authentication credentials were not provided."}
        )

    def test_not_related_user_cannot_create(self):
        new_user = User.objects.create_user(
            email="mano_magica@mail.com",
            password="123546",
            first_name="Mano",
            last_name="Magica",
            is_provider=False,
            phone="1189224002",
        )
        new_user_token = Token.objects.create(user=new_user)

        self.client.credentials(HTTP_AUTHORIZATION=f"Token {new_user_token.key}")

        request_body = {"stars": 5, "description": "Lorem ipsum dolor sit amet"}

        response = self.client.post(
            f"/api/services/{self.service.id}/reviews/",
            request_body,
            format="json",
        )

        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.data,
            {"detail": "You do not have permission to perform this action."},
        )


class ReviewViewsTests(APITestCase):
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

        cls.provider = User.objects.create_user(
            email="roni_calma@mail.com",
            password="123546",
            first_name="Roni",
            last_name="Calma",
            is_provider=True,
            phone="1189224002",
        )
        cls.provider_token = Token.objects.create(user=cls.provider)

        cls.service = Service.objects.create(
            title="Concerto de pia",
            description="Preciso de concerto na pia da cozinha da minha casa.",
            price=80.00,
            contractor=cls.contractor,
            provider=cls.provider,
        )

        cls.first_review = Review.objects.create(
            description="Poderia ter trabalhado melhor!",
            user_critic=cls.contractor,
            user_criticized=cls.provider,
            service=cls.service,
        )

        cls.second_review = Review.objects.create(
            stars=5,
            description="Muito bom, sem reclamações!",
            user_critic=cls.provider,
            user_criticized=cls.contractor,
            service=cls.service,
        )

    def test_anyone_can_list_one_user_received_reviews(self):
        response = self.client.get(
            f"/api/accounts/{self.provider.id}/received_reviews/"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            [ReviewSerializer(instance=self.first_review).data], response.data
        )

    def test_anyone_can_list_one_user_created_reviews(self):
        response = self.client.get(
            f"/api/accounts/{self.contractor.id}/created_reviews/"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            [ReviewSerializer(instance=self.first_review).data], response.data
        )

    def test_auth_user_can_filter(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.provider_token.key}")

        response = self.client.get(f"/api/reviews/{self.first_review.id}/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            ReviewSerializer(instance=self.first_review).data, response.data
        )

    def test_not_authenticated_user_cannot_filter(self):
        response = self.client.get(f"/api/reviews/{self.first_review.id}/")

        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            response.data, {"detail": "Authentication credentials were not provided."}
        )

    def test_review_owner_can_delete(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.contractor_token.key}")

        response = self.client.delete(f"/api/reviews/{self.first_review.id}/")

        self.assertEqual(response.status_code, 204)
        self.assertEqual(Review.objects.all().count(), 1)
        self.assertNotIn(self.first_review, Review.objects.all())

    def test_not_owner_cannot_delete_review(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.provider_token.key}")

        response = self.client.delete(f"/api/reviews/{self.first_review.id}/")

        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.data,
            {"detail": "You do not have permission to perform this action."},
        )
        self.assertIn(self.first_review, Review.objects.all())

    def test_owner_can_update_review(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.contractor_token.key}")

        update_data = {"stars": 4, "description": "Mandou bem!"}

        response = self.client.patch(
            f"/api/reviews/{self.first_review.id}/", update_data, format="json"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["stars"], 4)
        self.assertEqual(response.json()["description"], "Mandou bem!")
        self.assertEqual(
            ReviewSerializer(instance=Review.objects.get(id=self.first_review.id)).data,
            response.data,
        )

    def test_not_owner_cannot_update_review(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.provider_token.key}")

        update_data = {"stars": 5, "description": "O melhor de todos!"}

        response = self.client.patch(
            f"/api/reviews/{self.first_review.id}/", update_data, format="json"
        )

        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.data,
            {"detail": "You do not have permission to perform this action."},
        )
