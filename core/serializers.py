from rest_framework import serializers
from .models import Food, CustomUser, Promokod, Order, OrderItem
from rest_framework.response import Response
from django.utils import timezone
from rest_framework.exceptions import ValidationError

class FoodInputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Food
        fields = '__all__'


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id','name', 'phone', 'username', 'role', 'created_at']


class PromokodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promokod
        fields = '__all__'



class OrderItemSerializer(serializers.Serializer):
    food_id = serializers.IntegerField()
    count = serializers.IntegerField()


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id','items','manzil', 'promokod', 'created_at', 'status', 'total_price']
        read_only_fields = ['created_at', 'status', 'total_price', 'id']
    def create(self, validated_data):
        items = validated_data.pop('items')
        total_price=0
        for item in items:
            try:
                food = Food.objects.get(pk=item['food_id'])
                print(food)
            except Food.DoesNotExist:
                raise ValidationError({'items': "Mavjud bo'lmagan taom kiritilgan!"})
            total_price+=food.price*item['count']
        promokod = validated_data['promokod']
        user = validated_data.get('user')
        manzil = validated_data.get('manzil')
    
        if promokod.amount > 0 and promokod.end_date.date()>timezone.now().date():
            total_price = total_price-promokod.amount
            if total_price<0:
                total_price=0
        order = Order.objects.create(user=user, manzil=manzil, total_price=total_price, promokod=promokod)
        for item in items:
            food = Food.objects.get(pk=item['food_id'])
            OrderItem.objects.create(food=food, count=item['count'], total_price = item['count']*food.price, order=order, )
        return order

   
class RegisterRequestSerializer(serializers.Serializer):
    phone = serializers.CharField()
    name = serializers.CharField()
    username = serializers.CharField()
    password = serializers.CharField()
 
class OrderCreateRequestSerializer(serializers.Serializer):
    manzil = serializers.CharField()
    promokod = serializers.CharField(required=False, allow_null=True)
    items = OrderItemSerializer(many=True)
