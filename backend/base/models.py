from django.db import models
from django.contrib.auth.models import User  # Import User model

class Product(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  
    desc = models.CharField(max_length=50, null=True, blank=True)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    image = models.ImageField(null=True,blank=True,default='/placeholder.png')
    stock = models.PositiveIntegerField(default=0)  # Add stock field to keep track of product inventory

    def __str__(self):
        return self.desc if self.desc else "Unnamed Product"


class Purchase(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    purchase_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Purchase by {self.user.username} on {self.purchase_date} for {self.total_amount} USD"
    

class PurchaseItem(models.Model):
    purchase = models.ForeignKey(Purchase, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product.desc} (x{self.quantity}) in {self.purchase.user.username}'s purchase"