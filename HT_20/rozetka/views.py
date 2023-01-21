"""Views"""
from subprocess import Popen

from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic

from .forms import ScrapingTaskForm
from .models import Product, ScrapingTask
from cart.forms import CartAddProductForm


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
            pid = ScrapingTask.objects.all().first()
            Popen(["python", "scrape.py", f"{pid.id}"])
            return redirect("rozetka:index")
        context["errors"] = form.errors

    return render(request, "rozetka/add.html", context=context)


class ProductsListView(generic.ListView):
    """Get product list"""
    model = Product
    paginate_by = 9


class ProductsDetailView(generic.DetailView):
    """Get product detail"""
    model = Product

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        context['cart_product_form'] = CartAddProductForm()
        return context
