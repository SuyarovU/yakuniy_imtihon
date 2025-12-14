from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import CustomUserSerializer, FoodInputSerializer, OrderItemSerializer, PromokodSerializer, OrderSerializer
from rest_framework.response import Response
from rest_framework.request import Request
from .models import CustomUser, Food, Promokod, Order
from rest_framework.permissions import BasePermission, IsAuthenticated


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return (request.user.is_authenticated and request.user.role == 'admin')
    

class RegisterView(APIView):
    def post(self, request:Request):
        phone = request.data.get('phone')
        name = request.data.get('name')
        username = request.data.get('username')
        password = request.data.get('password')
        if CustomUser.objects.filter(username=username).exists():
            return Response({"error":"Username mavjud!"})
        if CustomUser.objects.filter(phone=phone).exists():
            return Response({"error":"Ushbu Phone number ro'yxatdan o'tgan"})
        user = CustomUser.objects.create_user(phone=phone, name=name, username=username, password=password)
        serializer = CustomUserSerializer(user)
        return Response(serializer.data)
    
class FoodView(APIView):
    def get(self, request:Request):
        foods = Food.objects.all()
        category = request.query_params.get('category')
        if category:
            foods = foods.filter(category=category)
        serializer = FoodInputSerializer(foods, many=True)
        return Response(serializer.data)
    

class FoodCreateView(APIView):
    permission_classes=[IsAdmin]
    def post(self, request):
        serializer = FoodInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    

class FoodDetailView(APIView):
    permission_classes=[IsAdmin]
    
    def put(self, request, pk):
        try: 
            food = Food.objects.get(pk=pk)
        except Food.DoesNotExist:
            return Response({'error':"Ma'lumot topilmadi!"})
        serializer = FoodInputSerializer(food, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    def delete(self, request, pk):
        try: 
            food = Food.objects.get(pk=pk)
        except Food.DoesNotExist:
            return Response({'error':"Ma'lumot topilmadi!"})
        food.delete()
        return Response({'error':'Deleted'})


class OrderCreateView(APIView):
    permission_classes=[IsAuthenticated]
    
    def post(self, request:Request):
        data = request.data.copy()
        promokod = data.get('promokod')
        if not promokod is None:
            promokod = Promokod.objects.get(name=promokod)
            print(promokod.amount)
        data['promokod']=promokod.id
        serializer = OrderSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data)
    
class PromokodView(APIView):
    def post(self, request:Request):
        serializer = PromokodSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
class GetOrderView(APIView):
    permission_classes=[IsAuthenticated]
    def get(self, request):
        orders = Order.objects.filter(user=request.user)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)
    


