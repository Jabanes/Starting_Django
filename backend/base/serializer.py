from rest_framework import serializers
from .models import Product, Cart
from django.contrib.auth.models import User


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class CartSerializer(serializers.ModelSerializer):
    product = ProductSerializer()  # Serialize the product details inside cart

    class Meta:
        model = Cart
        fields = ['id', 'product', 'quantity']