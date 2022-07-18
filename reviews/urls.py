from django.urls import path

from . import views

urlpatterns = [
    path("services/<id_service>/reviews/", views.CreateReviewView.as_view()),
    path("accounts/<id_user>/created_reviews/", views.ListCreatedReviewView.as_view()),
    path(
        "accounts/<id_user>/received_reviews/", views.ListReceivedReviewView.as_view()
    ),
    path("reviews/<id_review>/", views.ReviewParamsView.as_view()),
]
