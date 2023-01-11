"""Models"""
from django.db import models


class Product(models.Model):
    """Fields model for product"""
    product_id = models.BigIntegerField("ID")
    title = models.CharField(max_length=255)
    old_price = models.DecimalField(max_digits=20, decimal_places=2, blank=True)
    price = models.DecimalField(max_digits=20, decimal_places=2)
    href = models.URLField("URL")
    brand = models.CharField(max_length=255, blank=True)
    category = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    class Meta:
        """Meta object for Product"""
        ordering = ["title"]
        verbose_name = "Product"
        verbose_name_plural = "Products"

    def __str__(self):
        """String representation of Product"""
        return f"{self.title} (id:{self.product_id})"


class ScrapingTask(models.Model):
    """Fields model for scraping"""
    products_id = models.TextField()
