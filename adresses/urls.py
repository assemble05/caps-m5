from django.urls import path




urlpatterns = [
    path('adresses/<pk>', ListCreateAccount.as_view(), name="list_create_user"),
]