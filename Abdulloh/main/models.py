from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=100)


    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Current price
    old_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # Old price
    sale = models.BooleanField(default=False)  # Indicates if the product is on sale
    description = models.TextField()
    image = models.ImageField(upload_to='products/')
    rating = models.IntegerField(default=0)
    views = models.PositiveIntegerField(default=0)  # Track number of views
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name



class Comment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    rating = models.PositiveIntegerField(default=1)  # Yangi maydon
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user} on {self.product}"



class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/')

    def __str__(self):
        return f"{self.product.name} Image"

