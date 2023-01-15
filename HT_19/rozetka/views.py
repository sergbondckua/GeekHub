"""Views"""
from subprocess import Popen

from django.shortcuts import render, get_object_or_404, redirect

from .forms import ScrapingTaskForm
from .models import Product, ScrapingTask


def add_id(request):
    """Add a new product id"""
    form = ScrapingTaskForm(request.POST if request.POST else None)
    context = {
        "title": "Add Products Ids",
        "form": form,
    }
    if request.method == "POST":
        if form.is_valid():
            form.cleaned_data.get("products_id")
            form.save()
            pid = ScrapingTask.objects.all()[0]
            with Popen(['python', 'scrape.py', f'{pid.id}']):
                ...
            return redirect('index')
        context['errors'] = form.errors

    return render(request, "rozetka/add.html", context=context)


def my_products(request):
    """Get all products"""
    products = Product.objects.all().order_by("id")
    context = {
        "title": "My Products",
        "products": products,
    }
    return render(request, "rozetka/products.html", context=context)


def product_detail(request, slug):
    """Get product detail"""
    product = get_object_or_404(Product, id=slug)
    context = {
        "title": "Product Details",
        "product": product
    }
    return render(request, "rozetka/product_detail.html", context=context)
