from django.contrib import admin
from django.urls import path
from . import views
from .views import register
from rest_framework_simplejwt.views import TokenObtainPairView

urlpatterns = [
    path('', views.index),
    path('products', views.myProducts),
    path('products/<int:id>', views.product_detail),
    path('login', TokenObtainPairView.as_view()),    
    path('test', views.test),
    path('staff', views.staff_only),
    path('superusers', views.superuser_only),
    path('register', register, name='register'),
]
