# from rest_framework.authtoken.models import Token
# from rest_framework.test import APITestCase
# from reviews.models import Review
# from reviews.serializers import ReviewSerializer, UpdateReviewSerializer
# from users.models import User
# from users.serializers import UserRegisterSerializer


# class ReviewCreateViewTest(APITestCase):
#     @classmethod
#     def setUpTestData(cls):
#         cls.user_critic = User.objects.create_user(
#             email="goleiro_cassio@mail.com",
#             password="123546",
#             first_name="Goleiro",
#             last_name="Cassioo",
#             is_provider=False,
#             phone="1140028922",
#         )

#         cls.critic_token = Token.objects.create(user=cls.user_critic)

#         cls.user_criticized = User.objects.create_user(
#             email="roni_calma@mail.com",
#             password="123546",
#             first_name="Roni",
#             last_name="Calma",
#             is_provider=True,
#             phone="1189224002",
#         )

#     def test_create_review(self):
#         self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.critic_token.key}")

#         request_body = {"stars": 5, "description": "Lorem ipsum dolor sit amet"}

#         response = self.client.post(
#             f"/api/accounts/{self.user_criticized.id}/reviews/",
#             request_body,
#             format="json",
#         )

#         self.assertEqual(response.status_code, 201)
#         self.assertIn(
#             response.data, ReviewSerializer(Review.objects.all(), many=True).data
#         )

#     def test_incorret_create_review_fields(self):
#         self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.critic_token.key}")

#         incorrect_data = {"stars": -5, "description": False}

#         serializer = ReviewSerializer(data=incorrect_data)

#         self.assertEqual(serializer.is_valid(), False)

#         response = self.client.post(
#             f"/api/accounts/{self.user_criticized.id}/reviews/",
#             incorrect_data,
#             format="json",
#         )

#         self.assertEqual(response.status_code, 400)
#         self.assertEqual(serializer._errors, response.data)

#     def test_not_authenticated_error(self):
#         request_body = {"stars": 5, "description": "Lorem ipsum dolor sit amet"}

#         response = self.client.post(
#             f"/api/accounts/{self.user_criticized.id}/reviews/",
#             request_body,
#             format="json",
#         )

#         self.assertEqual(response.status_code, 401)
#         self.assertEqual(
#             response.data, {"detail": "Authentication credentials were not provided."}
#         )


# class ReviewViewsTests(APITestCase):
#     @classmethod
#     def setUpTestData(cls):
#         cls.user_critic = User.objects.create_user(
#             email="goleiro_cassio@mail.com",
#             password="123546",
#             first_name="Goleiro",
#             last_name="Cassioo",
#             is_provider=False,
#             phone="1140028922",
#         )
#         cls.critic_token = Token.objects.create(user=cls.user_critic)

#         cls.user_criticized = User.objects.create_user(
#             email="roni_calma@mail.com",
#             password="123546",
#             first_name="Roni",
#             last_name="Calma",
#             is_provider=True,
#             phone="1189224002",
#         )
#         cls.criticized_token = Token.objects.create(user=cls.user_criticized)

#         cls.first_review = Review.objects.create(
#             description="Poderia ter trabalhado melhor!",
#             user_critic=cls.user_critic,
#             user_criticized=cls.user_criticized,
#         )

#         Review.objects.create(
#             stars=5,
#             description="Muito bom, sem reclamações!",
#             user_critic=cls.user_critic,
#             user_criticized=cls.user_criticized,
#         )

#     def test_anyone_can_list_one_user_critics_received(self):
#         response = self.client.get(f"/api/accounts/{self.user_criticized.id}/reviews/")

#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(
#             ReviewSerializer(Review.objects.all(), many=True).data, response.data
#         )

#     def test_auth_user_can_filter(self):
#         self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.criticized_token.key}")

#         response = self.client.get(f"/api/reviews/{self.first_review.id}/")

#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(
#             ReviewSerializer(instance=self.first_review).data, response.data
#         )

#     def test_not_authenticated_user_cannot_filter(self):
#         response = self.client.get(f"/api/reviews/{self.first_review.id}/")

#         self.assertEqual(response.status_code, 401)
#         self.assertEqual(
#             response.data, {"detail": "Authentication credentials were not provided."}
#         )

#     def test_review_owner_can_delete(self):
#         self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.critic_token.key}")

#         response = self.client.delete(f"/api/reviews/{self.first_review.id}/")

#         self.assertEqual(response.status_code, 204)
#         self.assertEqual(Review.objects.all().count(), 1)
#         self.assertNotIn(self.first_review, Review.objects.all())

#     def test_not_owner_cannot_delete_review(self):
#         self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.criticized_token.key}")

#         response = self.client.delete(f"/api/reviews/{self.first_review.id}/")

#         self.assertEqual(response.status_code, 403)
#         self.assertEqual(
#             response.data,
#             {"detail": "You do not have permission to perform this action."},
#         )
#         self.assertIn(self.first_review, Review.objects.all())

#     def test_owner_can_update_review(self):
#         self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.critic_token.key}")

#         update_data = {"stars": 4, "description": "Mandou bem!"}

#         response = self.client.patch(
#             f"/api/reviews/{self.first_review.id}/", update_data, format="json"
#         )

#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(response.json()["stars"], 4)
#         self.assertEqual(response.json()["description"], "Mandou bem!")
#         self.assertEqual(
#             UpdateReviewSerializer(
#                 instance=Review.objects.get(id=self.first_review.id)
#             ).data,
#             response.data,
#         )

#     def test_not_owner_cannot_update_review(self):
#         self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.criticized_token.key}")

#         update_data = {"stars": 5, "description": "O melhor de todos!"}

#         response = self.client.patch(
#             f"/api/reviews/{self.first_review.id}/", update_data, format="json"
#         )

#         self.assertEqual(response.status_code, 403)
#         self.assertEqual(
#             response.data,
#             {"detail": "You do not have permission to perform this action."},
#         )

#     def test_owner_can_change_the_review_criticized_user(self):
#         self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.critic_token.key}")

#         another_user = User.objects.create_user(
#             email="mano_magica@mail.com",
#             password="123546",
#             first_name="Mano",
#             last_name="Magica",
#             is_provider=True,
#             phone="1189224002",
#         )
#         id = UserRegisterSerializer(instance=another_user).data["id"]

#         update_data = {"user_criticized_id": id}

#         response = self.client.patch(
#             f"/api/reviews/{self.first_review.id}/", update_data, format="json"
#         )

#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(
#             Review.objects.get(id=self.first_review.id).user_criticized, another_user
#         )
#         self.assertNotIn(self.first_review, self.user_criticized.critics.all())
#         self.assertIn(self.first_review, another_user.critics.all())
#         self.assertEqual(
#             UpdateReviewSerializer(
#                 instance=Review.objects.get(id=self.first_review.id)
#             ).data,
#             response.data,
#         )
