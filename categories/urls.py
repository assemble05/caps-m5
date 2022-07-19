from django.urls import path
from . import views



urlpatterns = [
    path('category/', views.CategoryView.as_view()),
    path('category/<category_id>/', views.CategoryIdView.as_view()),
    path('category/<category_id>/services/', views.CategoryServicesView.as_view()),
    path('category/<category_id>/users/', views.View.as_view())
]
