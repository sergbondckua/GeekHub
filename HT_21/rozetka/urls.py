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
        "product/<int:pk>/",
        views.ProductsDetailView.as_view(),
        name="product-detail"
    ),
    path(
        "product/<int:pk>/update/",
        views.ProductsUpdateView.as_view(),
        name="product-update"
    ),
    path(
        "product/<int:pk>/delete/",
        views.ProductsDeleteView.as_view(),
        name="product-delete"
    ),
    path(
        "products/category/<int:category_id>",
        views.DetailsByCategory.as_view(),
        name="product-category"
    ),
]

app_name = "rozetka"
