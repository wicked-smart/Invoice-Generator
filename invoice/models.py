from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

# Create your models here.
class User(AbstractUser):
    pass

class Item(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.FloatField(default=0.0)
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.name}"

class BoughtItem(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="sold")
    quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.item.name}"

class Invoice(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    items = models.ManyToManyField(BoughtItem)
   # customer
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.id}"