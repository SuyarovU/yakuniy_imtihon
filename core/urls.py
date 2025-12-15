from . import views
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from drf_spectacular.views import SpectacularAPIView,SpectacularSwaggerView


urlpatterns = [
    path('restaurant/foods/', views.FoodView.as_view()),
    path('restaurant/foods/create/', views.FoodCreateView.as_view()),
    path('restaurant/foods/create/<int:pk>', views.FoodDetailView.as_view()),
    path('restaurant/order/create', views.OrderCreateView.as_view()),
    path('restaurant/order/', views.GetOrderView.as_view()),
    path('restaurant/promokod/', views.PromokodView.as_view()),
    path('restaurant/token/', TokenObtainPairView.as_view()),
    path('restaurant/refresh/', TokenRefreshView.as_view()),
    path('restaurant/register/', views.RegisterView.as_view()),
    path("auth/schema/",SpectacularAPIView.as_view(),name="schema"),
    path("auth/docs/",SpectacularSwaggerView.as_view(),name='swagger-ui'),
]