"""Forms"""
from django import forms

from .models import ScrapingTask


class ScrapingTaskForm(forms.ModelForm):
    """Form for scraping tasks"""

    class Meta:
        """Meta class for ScrapingTask"""
        model = ScrapingTask
        fields = ('products_id',)

        widgets = {
            "products_id": forms.Textarea(
                attrs={
                    "placeholder": "Add id from a new line", "class": "form-control",
                    "name": "products_id", "id": "products", "cols": "30",
                    "rows": "10",
                })
        }
