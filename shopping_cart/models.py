from django.db import models
from decimal import Decimal
from django.contrib.auth.models import User
from shop.models import Profile, Product


class cartItem(models.Model):
    cart_id = models.AutoField
    product = models.ForeignKey(Product, on_delete = models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    user_name = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)
    is_ordered =  models.BooleanField(default=False)

    def __str__(self):
        return self.product.name
