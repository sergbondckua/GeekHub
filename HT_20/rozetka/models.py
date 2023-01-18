"""Models"""
from django.db import models


class Product(models.Model):
    """Fields model for product"""

    product_id = models.BigIntegerField("ID")
    title = models.CharField(max_length=255)
    old_price = models.DecimalField(max_digits=20, decimal_places=2,
                                    blank=True, default=0.00, null=True)
    price = models.DecimalField(max_digits=20, decimal_places=2, default=0.00)
    href = models.URLField("URL")
    brand = models.CharField(max_length=255, blank=True, default="Unknown",
                             null=True)
    category = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(blank=True, default="", null=True)

    class Meta:  #pylint: disable=too-few-public-methods
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
