"""URLs"""
from django.urls import path
from . import views

urlpatterns = [
    path("", views.add_id, name="index"),
    path("my-products/", views.my_products, name="my-products"),
    path("product-view/<int:slug>/", views.product_detail,
         name="product-detail"),
]
