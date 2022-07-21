from django.urls import path

from . import views

urlpatterns = [
    path("service/", views.ServiceView.as_view()),
    path("services/<pk>/", views.ServiceRetrieveUpdateDeleteView.as_view()),
    path("services/<pk>/candidates/", views.CandidateToServiceView.as_view()),
    path("services/", views.ListServiceView.as_view()),
    path(
        "contractors/<contractor_id>/services/",
        views.ListContractorServicesView.as_view(),
    ),
    path("providers/<provider_id>/services/", views.ListProviderServicesView.as_view()),
]
