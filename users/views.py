from rest_framework import generics
from rest_framework.views import APIView, Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from users.models import User
from users.serializers import UserLoginSerializer, UserRegisterSerializer


class LoginView(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(
            username=serializer.validated_data["email"],
            password=serializer.validated_data["password"],
        )

        if user:
            token, _ = Token.objects.get_or_create(user=user)

            return Response({"token": token.key})

        return Response(
            {"detail": "invalid username or password"},
            status=status.HTTP_401_UNAUTHORIZED,
        )


class ListCreateAccount(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
