"""URLs"""
from django.urls import path
from . import views

urlpatterns = [
    path("", views.add_id, name="index"),
    path(
        "products/",
         views.ProductsListView.as_view(),
         name="products-list"
         ),
    path(
        "products/<int:pk>/",
         views.ProductsDetailView.as_view(),
         name="product-detail"
         ),
]

app_name = "rozetka"
