from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Purchase, Product, PurchaseItem
from .serializer import ProductSerializer, PurchaseSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .serializer import RegisterSerializer
from rest_framework import status
from .permissions import IsSuperUser  # Import the custom permission
from decimal import Decimal
from django.contrib.auth.decorators import login_required

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
    return Response('Welcome To home page')

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


# API view to handle checkout
@api_view(['POST'])
@permission_classes([IsAuthenticated])  # Ensure only authenticated users can checkout
def checkout(request):
    user = request.user
    cart = request.data.get('cart', [])

    if not cart:
        return Response({"detail": "Your cart is empty."}, status=status.HTTP_400_BAD_REQUEST)

    # Calculate the total price of the purchase
    total_price = sum(
        float(item['price']) * int(item['quantity'])  # Explicitly convert to float and int
        for item in cart
    )


    # Create the Purchase record
    purchase = Purchase.objects.create(user=user, total_amount=total_price)

    # Loop through the cart items and create PurchaseItem records
    for item in cart:
        product = get_object_or_404(Product, id=item['id'])  # Get the product from the database
        quantity = item['quantity']
        price = item['price']

        # Create the purchase item for each product in the cart
        PurchaseItem.objects.create(
            purchase=purchase,
            product=product,
            quantity=quantity,
            price=price
        )

        # Optionally, you can update the product stock here if needed
        product.stock -= quantity  # Decrease stock based on the quantity purchased
        product.save()

    return Response({"detail": "Checkout successful!"}, status=status.HTTP_201_CREATED)
