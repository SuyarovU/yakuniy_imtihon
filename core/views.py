from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import CustomUserSerializer, FoodInputSerializer, OrderItemSerializer, PromokodSerializer, OrderSerializer
from rest_framework.response import Response
from rest_framework.request import Request
from .models import CustomUser, Food, Promokod, Order
from rest_framework.permissions import BasePermission, IsAuthenticated
from drf_spectacular.utils import extend_schema


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return (request.user.is_authenticated and request.user.role == 'admin')
    


class RegisterView(APIView):
    @extend_schema(
    tags=['Auth'],
    summary="Royxatdan o'tish uchun",
    description="Foydalanuvchi ro'yxatdan o'tish uchun ma'lumotlarini kiritadi, va to'g'ri ma'lumot kiritsa bazaga saqlanadi")
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
    @extend_schema(
    tags=['Foods'],
    summary="Ovqatlarni ko'rish",
    description="Foydalanuvchi bu yerda barcha ovqatlarni ko'rishi mumkin, buning uchun authenticatsiya talab qilinmaydi")
    def get(self, request:Request):
        foods = Food.objects.all()
        category = request.query_params.get('category')
        if category:
            foods = foods.filter(category=category)
        serializer = FoodInputSerializer(foods, many=True)
        return Response(serializer.data)
    


class FoodCreateView(APIView):
    permission_classes=[IsAdmin]
    @extend_schema(
    tags=['Foods'],
    summary="Ovqat qo'shish",
    description="Bu yerda ovqat nomi, narxi va kategoriyasini kiritib bazaga ovqat qo'shiladi buning uchun admin bo'lish kerak")
    def post(self, request):
        serializer = FoodInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    

class FoodDetailView(APIView):
    permission_classes=[IsAdmin]
    @extend_schema(
    tags=['Foods'],
    summary="Yangilash",
    description="pk orqali mavjud ovqat ma'lumotlarini yangilash mumkin buning uchun admin bo'lish kerak.")
    def put(self, request, pk):
        try: 
            food = Food.objects.get(pk=pk)
        except Food.DoesNotExist:
            return Response({'error':"Ma'lumot topilmadi!"})
        serializer = FoodInputSerializer(food, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    @extend_schema(
    tags=['Foods'],
    summary="O'chirish",
    description="pk ga mos ovqatni o'chirish uchun ishlatilinadi, buning uchun admin bo'lish kerak")
    def delete(self, request, pk):
        try: 
            food = Food.objects.get(pk=pk)
        except Food.DoesNotExist:
            return Response({'error':"Ma'lumot topilmadi!"})
        food.delete()
        return Response({'error':'Deleted'})


class OrderCreateView(APIView):
    permission_classes=[IsAuthenticated]
    @extend_schema(
    tags=['Order'],
    summary="Buyurtma yaratish",
    description="Kerakli ma'lumotlarni kiritib buyurtma yaratish uchun ishlatilinadi")
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
    permission_classes=[IsAdmin]
    @extend_schema(
    tags=['Promokod'],
    summary="Promokod yaratish",
    description="Promokod uchun kerakli ma'lumotlarni kiritib yaratiladi, buning uchun admin bo'lish kerak")
    def post(self, request:Request):
        serializer = PromokodSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
class GetOrderView(APIView):
    permission_classes=[IsAuthenticated]
    @extend_schema(
    tags=['Order'],
    summary="Buyurtma ko'rish",
    description="Foydalanuvchi o'ziga tegishli bo'lgan buyurtmalarni ko'ra oladi")
    def get(self, request):
        orders = Order.objects.filter(user=request.user)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)
    


