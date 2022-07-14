import uuid

from django.db import models


class ReviewStars(models.IntegerChoices):
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5


# Create your models here.
class Review(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_critic = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="created_reviews"
    )
    user_criticized = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="critics"
    )
    stars = models.PositiveIntegerField(
        choices=ReviewStars.choices, default=ReviewStars.THREE
    )
    description = models.CharField(max_length=255, null=True)
