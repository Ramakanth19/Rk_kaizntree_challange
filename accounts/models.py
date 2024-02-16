from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    # Stores category names for items. Each category can have multiple items associated with it.
    name = models.CharField(max_length=100, unique=True)
    

class Item(models.Model):
    # Defines the stock status choices for items
    IN_STOCK_CHOICES = (
        ('Yes', 'Yes'),
        ('No', 'No'),
    )

    sku = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, related_name='items', on_delete=models.CASCADE)
    tags = models.CharField(max_length=100)
    in_stock = models.CharField(max_length=3, choices=IN_STOCK_CHOICES, default='Yes')
    available_stock = models.IntegerField()
    