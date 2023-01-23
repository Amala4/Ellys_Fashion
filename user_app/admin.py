from django.contrib import admin
from .models import  UserOrder, CustomerWish




class CustomerWishAdmin (admin.ModelAdmin):
    list_display = ('id', 'user', 'product')
    list_display_links = ('id',)
    list_filter = ('user', 'product')
    list_per_page = 25


admin.site.register(CustomerWish, CustomerWishAdmin)



class UserOrderAdmin (admin.ModelAdmin):
    list_display = ('id', 'customer', 'customer_phone_no',  'item_ordered', 'quantity', 'order_status', 'payment_status', 'order_reference_id')
    readonly_fields = ('order_reference_id', 'delivery_address', 'item_total_price', 'order_total_price', 'quantity', 'customer_phone_no')
    list_display_links = ('id', 'item_ordered')
    list_filter = ('customer', 'item_ordered', 'order_reference_id')
    list_editable = ('order_status', 'payment_status')
    list_select_related = ('customer', 'item_ordered')
    search_fields = ('customer', 'item_ordered', 'order_reference_id')
    list_per_page = 100


admin.site.register(UserOrder, UserOrderAdmin)





