from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from reviews.models import Review
from users.models import User


class ReviewCreateViewTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user_critic = User.objects.create_user(
            email="goleiro_cassio@mail.com",
            password="123546",
            first_name="Goleiro",
            last_name="Cassioo",
            is_provider=False,
            phone="1140028922",
        )

        cls.critic_token = Token.objects.create(user=cls.user_critic)

        cls.user_criticized = User.objects.create(
            email="roni_calma@mail.com",
            password="123546",
            first_name="Roni",
            last_name="Calma",
            is_provider=True,
            phone="1189224002",
        )

    def test_create_review(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.critic_token.key}")

        request_body = {
            "stars": 5,
            "description": """Lorem ipsum dolor sit amet, 
        consectetur adipiscing elit, sed do eiusmod tempor 
        incididunt ut labore et dolore magna aliqua.""",
        }

        response = self.client.post(
            f"/api/accounts/{self.user_criticized.id}/reviews/",
            request_body,
            format="json",
        )

        self.assertEqual(response.status_code, 201)
        # self.assertIn(response.data, CreateReviewSerializer(Review.objects.all(), many=True).data)
