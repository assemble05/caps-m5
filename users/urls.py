from django.urls import path
from users.views import ListAccountContractor,ListAccountProvider,ListCreateAccount, LoginView, ListAccountDetail



urlpatterns = [
    path('accounts/', ListCreateAccount.as_view(), name="list_create_user"),
    path('login/', LoginView.as_view(), name="login_view"),
    path("accounts/<pk>/", ListAccountDetail.as_view(), name="list_account_view"),
    path("accounts/users/providers/", ListAccountProvider.as_view(), name="list_account_providers"),
    path("accounts/users/contractors/", ListAccountContractor.as_view(), name="list_account_contractor"),
]