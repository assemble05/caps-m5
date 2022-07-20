from django.urls import path

from . import views

urlpatterns = [
    path("accounts/<id_user>/service/", views.ServiceView.as_view()),
    path("services/<pk>/", views.ServiceRetrieveUpdateDeleteView.as_view()),
    path("services/<pk>/candidates/", views.CandidateToServiceView.as_view()),
    path("services/", views.ListServiceView.as_view()),
]
