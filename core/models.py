from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
    phone = models.CharField(max_length=30, unique=True)
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    role = models.CharField(max_length=20,choices=[
        ("user","User"),
        ("admin","Admin")
    ],default="user")


class Food(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(choices=[
        ('ichimlik', 'Ichimlik'),
        ('shirinlik', 'Shirinlik'),
        ('ovqat', 'Ovqat')
    ], max_length=50)
    status = models.CharField(choices=[
        ('mavjud', "Mavjud"),
        ('tugagan', "Tugagan")
    ], default='mavjud')
    image = models.ImageField(upload_to="media/",null=True,blank=True)


class Promokod(models.Model):
    name = models.CharField(max_length=30)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateField(default=timezone.now().date())
    end_date = models.DateField()


class Order(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    manzil = models.TextField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(choices=[
        ('tayyorlanmoqda', 'Tayyorlanmoqda'),
        ('yetkazilmoqda', 'Yetkazilmoqda'),
        ('yetkazilgan', 'Yetkazilgan')
    ], default='tayyorlanmoqda', max_length=50)
    promokod = models.ForeignKey(Promokod, on_delete=models.CASCADE, default=0)


class OrderItem(models.Model):
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    count = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    order = models.ForeignKey(Order, related_name='items',on_delete=models.CASCADE)

