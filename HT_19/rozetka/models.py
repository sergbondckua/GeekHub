"""Models"""
from django.db import models


class Product(models.Model):
    """Fields model for product"""

    product_id = models.BigIntegerField("ID")
    title = models.CharField(max_length=255)
    old_price = models.DecimalField(max_digits=20, decimal_places=2,
                                    blank=True, default=0.00)
    price = models.DecimalField(max_digits=20, decimal_places=2)
    href = models.URLField("URL")
    brand = models.CharField(max_length=255,blank=True, default="Unknown",
                             null=True)
    category = models.CharField(max_length=255)
    description = models.TextField(blank=True, default="")

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
