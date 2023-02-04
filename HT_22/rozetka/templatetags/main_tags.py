from django import template
from rozetka.models import Category, Product


register = template.Library()


@register.simple_tag
def get_categories():
    """Returns a list of categories"""
    return Category.objects.all()

@register.simple_tag
def get_count_products_in_category(category_id):
    """Returns a count products in category"""
    cat = Category.objects.get(id=category_id)
    return cat.product.count()
