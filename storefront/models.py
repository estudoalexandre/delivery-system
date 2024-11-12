from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField('delivery_store.Product', through='CartProduct')
    completed = models.BooleanField(default=False)
    
    def add_product(self, product, quantity):
        cart_product, created = CartProduct.objects.get_or_create(
            cart=self,
            product=product,
            defaults={'quantity': quantity}
        )
        if not created:
            cart_product.quantity += quantity
            cart_product.save()
    
    def get_total_price(self):
        return sum([cp.product.price * cp.quantity for cp in self.cartproduct_set.all()])
        


class CartProduct(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey('delivery_store.Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)