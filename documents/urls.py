from django.urls import path

from . import views

urlpatterns = [
    path("accounts/<id_user>/documents/", views.DocumentsView.as_view()),
]
