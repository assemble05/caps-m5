from django.urls import path
from users.views import ListCreateAccount, LoginView


urlpatterns = [
    path('accounts/', ListCreateAccount.as_view(), name="list_create_user"),
    path('login/', LoginView.as_view()),
]