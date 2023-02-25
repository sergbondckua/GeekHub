"""URLs"""
from django.urls import path, include
from . import views
from rest_framework import routers

# Routers
router = routers.DefaultRouter()
router.register("products", views.ApiProductViewSet)
router.register("category", views.ApiCategoryViewSet)

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("products/add", views.add_id, name="products-add"),
    path("products/", views.ProductsListView.as_view(), name="products-list"),
    path(
        "product/<int:pk>/", views.ProductsDetailView.as_view(), name="product-detail"
    ),
    path(
        "product/<int:pk>/update/",
        views.ProductsUpdateView.as_view(),
        name="product-update",
    ),
    path(
        "product/<int:pk>/delete/",
        views.ProductsDeleteView.as_view(),
        name="product-delete",
    ),
    path(
        "products/category/<int:category_id>/",
        views.DetailsByCategory.as_view(),
        name="product-category",
    ),
    # API URLs
    path(
        "api/products/<int:pk>/",
        views.ApiProductViewSet.as_view(
            {
                "get": "retrieve",
                "put": "update",
                "patch": "partial_update",
                "delete": "destroy",
            }
        ),
        name="api-product-detail",
    ),
    path(
        "api/products/",
        views.ApiProductViewSet.as_view(
            {
                "get": "list",
                "post": "create",
            }
        ),
        name="api-products",
    ),
    path(
        "api/category/",
        views.ApiCategoryViewSet.as_view({"get": "list"}),
        name="api-categories",
    ),
    path(
        "api/category/<int:pk>",
        views.ApiCategoryViewSet.as_view({"get": "retrieve"}),
        name="api-category-detail",
    ),
    # path("", include(router.urls)),  # Routers include
]

app_name = "rozetka"
