from django.urls import path
from users.views import ListCreateAccount, LoginView


urlpatterns = [
    path('accounts/', ListCreateAccount.as_view()),
    path('login/', LoginView.as_view()),
]