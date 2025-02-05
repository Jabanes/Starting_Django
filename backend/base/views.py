from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Product, Cart
from .serializer import ProductSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .serializer import RegisterSerializer, CartSerializer
from rest_framework import status
from .permissions import IsSuperUser  # Import the custom permission


@api_view(['GET'])
@permission_classes([IsSuperUser])  
def superuser_only(req):
    return Response({"message": "Superuser Access Granted"})

@api_view(['GET'])
@permission_classes([IsAdminUser])
def staff_only(req):
    return Response({"message": "Staff Access Granted"})

@api_view(['POST'])
def register(req):
    serializer = RegisterSerializer(data=req.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def test(req):
    return Response("WELCOME USER")

@api_view(['GET'])
def index(req):
    return Response('Welcom To home page')

@api_view(['GET', 'POST'])
def myProducts(req):
    if req.method == 'GET':
        return Response(ProductSerializer(Product.objects.all(), many=True).data)

    serializer = ProductSerializer(data=req.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def product_detail(req, id):
    product = get_object_or_404(Product, id=id)

    if req.method == 'GET':
        return Response(ProductSerializer(product).data)

    elif req.method == 'PUT':
        serializer = ProductSerializer(product, data=req.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    product.delete()
    return Response({'message': 'Deleted'}, status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def cart(request):
    user = request.user

    if request.method == 'GET':
        # Retrieve all cart items for the logged-in user
        cart_items = Cart.objects.filter(user=user)
        serialized_cart = CartSerializer(cart_items, many=True).data  # Serialize the cart items
        return Response(serialized_cart)

    elif request.method == 'POST':
        product_id = request.data.get("product_id")
        quantity = request.data.get("quantity", 1)  # Default quantity is 1

        if not product_id:
            return Response({"error": "Product ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

        # Check if the product is already in the cart
        cart_item, created = Cart.objects.get_or_create(user=user, product=product)

        if not created:
            cart_item.quantity += int(quantity)  # Increment quantity if already exists
            cart_item.save()

        return Response(CartSerializer(cart_item).data, status=status.HTTP_201_CREATED)
