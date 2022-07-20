from rest_framework.views import APIView, Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404, render
from categories.permissions import CategoryPermission
from categories.models import Category
from categories.serializers import CategorySerializer
from services.models import Service
from services.serializers import ServiceSerializer
from users.models import User
from users.serializers import UserSerializer


class CategoryView(PageNumberPagination, APIView ):
    authentication_classes = [TokenAuthentication]
    permission_classes = [CategoryPermission]
    def post(self, request):
        serializer = CategorySerializer(data = request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
        
        category = serializer.save()
        serializer = CategorySerializer(category)
        return Response(serializer.data, status = 201)

    def get(self, request):
        list_categories = Category.objects.all()
        result_page = self.paginate_queryset(list_categories, request, view = self)
        serializer = CategorySerializer(result_page, many = True)
        return self.get_paginated_response(serializer.data)

class CategoryIdView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [CategoryPermission]

    def get(self, request, category_id):
        category = get_object_or_404(Category, id = category_id)
        serializer = CategorySerializer(category)
        return Response(serializer.data)

    def patch(self, request, category_id):
        category = get_object_or_404(Category, id = category_id)
        serializer = CategorySerializer(category, request.data, partial = True)

        if not serializer.is_valid():
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

        try:
            category_updated = serializer.save()
        except KeyError as err:
            return Response(err.args[0], status = 422)
        serializer = CategorySerializer(category_updated)
        return Response(serializer.data)

    def delete(self, request, category_id):
        category = get_object_or_404(Category, id = category_id)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class CategoryServicesView(APIView, PageNumberPagination):
    authentication_classes = [TokenAuthentication]
    permission_classes = [CategoryPermission]
    def get(self, request, category_id):
        list_services = Service.objects.filter(category_id = category_id)
        result_page = self.paginate_queryset(list_services, request, view = self)
        serializer = ServiceSerializer(result_page, many = True)
        return self.get_paginated_response(serializer.data)

class CategoryUsersView(APIView, PageNumberPagination):
    authentication_classes = [TokenAuthentication]
    permission_classes = [CategoryPermission]
    def get(self, request, category_id):
        list_users = User.objects.filter(categories = category_id)
        result_page = self.paginate_queryset(list_users, request, view = self)
        serializer = UserSerializer(result_page, many = True)
        return self.get_paginated_response(serializer.data)