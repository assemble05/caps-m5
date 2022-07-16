from django.urls import path

from . import views

urlpatterns = [
    path("services/<id_service>/reviews/", views.CreateReviewView.as_view()),
    path("accounts/<id_user>/reviews/", views.ReviewView.as_view()),
    path("reviews/<id_user>/", views.ReviewParamsView.as_view()),
]
