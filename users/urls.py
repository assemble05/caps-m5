from django.urls import path
from users.views import ListCreateAccount, LoginView, ListAccountDetail



urlpatterns = [
    path('accounts/', ListCreateAccount.as_view(), name="list_create_user"),
    path('login/', LoginView.as_view()),
    path("accounts/<pk>/", ListAccountDetail.as_view(), name="list_account_view")
]