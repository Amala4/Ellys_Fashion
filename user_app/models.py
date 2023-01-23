from django.db import models
from products.models import ProductList
from django.contrib.auth.models import User



class UserOrder(models.Model):
    status_choices = (
       ('pending', 'pending'),
       ('Received', 'Received'),
       ('Dispatched', 'Dispatched'),
       ('Delivered', 'Delivered')
    )

    payment_choices = (
       ('pending', 'pending'),
       ('Partly Paid', 'Partly Paid'),
       ('Fully Paid', 'Fully Paid'),
    )

    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders", editable = False)
    customer_phone_no = models.CharField(max_length=100, null=True, editable = False)
    delivery_address = models.TextField(blank=True, editable = False)
    item_ordered = models.ForeignKey(ProductList, on_delete=models.PROTECT, null=True, related_name="orders", editable = False)
    order_reference_id = models.CharField(max_length=300, help_text= "When user makes a transfer, they put this ID", editable = False)
    date_ordered = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    payment_status = models.CharField(max_length=100, choices=payment_choices, default='pending')
    order_status = models.CharField(max_length=100, choices=status_choices, default='pending')
    quantity = models.CharField(max_length=100, null=True, editable = False )
    item_total_price = models.CharField(max_length=100, null=True, blank=True, help_text= "The total price for this item", editable = False)
    order_total_price = models.CharField(max_length=100, null=True, blank=True, help_text= "The total price for this order, which may inclde other items", editable = False)


    class Meta:
        verbose_name_plural = "User Orders"

    def __str__(self):
        return self.customer.first_name


class CustomerWish(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, editable=False)
    product = models.ForeignKey(ProductList, on_delete=models.PROTECT, null=True, editable=False)
    date_added = models.DateTimeField(auto_now_add=True)


    class Meta:
        verbose_name_plural = "Customer Wishlists"

    def __str__(self):
        return self.user.first_name
