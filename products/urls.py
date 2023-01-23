from django.urls import path
from . import views

urlpatterns = [
    path('product/<int:product_id>/<slug:product_name>',  views.product_detail, name='product_detail'),
    path('products', views.products, name ='products'),
    path('products-filter', views.ajaxproducts, name ='products-filter'),
    path('wishlist', views.Wishlist, name ='wishlist'),
    path('cart', views.Cart, name ='cart'),
    path('search', views.Search, name ='search'),
]
