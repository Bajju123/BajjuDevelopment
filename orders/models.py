from django.db import models
from shop.models import Product, Profile


class Order(models.Model):
    user_name = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)
    fullname = models.CharField(max_length=50)
    email = models.EmailField()
    address = models.CharField(max_length=250)
    postal_code = models.CharField(max_length=20, null=True)
    city = models.CharField(max_length=100, null=True)
    state = models.CharField(max_length=100, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return 'Order {}'.format(self.id)

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    user_name = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, related_name='items', on_delete=False)
    product = models.ForeignKey(Product, related_name='order_items', on_delete=False)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return '{}'.format(self.id)

    def get_cost(self):
        return self.price * self.quantity
