"""Forms"""
from django import forms

from .models import ScrapingTask, Product


class ScrapingTaskForm(forms.ModelForm):
    """Form for scraping tasks"""

    class Meta:  # pylint: disable=too-few-public-methods
        """Meta class for ScrapingTask"""

        model = ScrapingTask
        fields = ("products_id",)

        widgets = {
            "products_id": forms.Textarea(
                attrs={
                    "placeholder": "Add id from a new line",
                    "class": "form-control",
                    "name": "products_id",
                    "id": "products",
                    "cols": "30",
                    "rows": "10",
                }
            )
        }


class ProductsUpdateForm(forms.ModelForm):
    """Form for updating products"""

    class Meta:  # pylint: disable=too-few-public-methods
        """Meta class"""
        model = Product
        fields = "__all__"
