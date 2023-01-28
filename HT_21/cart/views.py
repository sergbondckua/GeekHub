from django.core.checks import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from rozetka.models import Product
from .cart import Cart
from .forms import CartAddProductForm


@require_POST
def cart_add(request, product_id):
    """Add a new product in the cart"""
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cleaned_data = form.cleaned_data
        cart.add(
            product=product,
            quantity=cleaned_data["quantity"],
            update_quantity=cleaned_data["update"],
        )
    return redirect("rozetka:products-list")

def cart_remove(request, product_id):
    """Remove a product from the cart"""
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect("cart:cart_detail")


def cart_clear(request):
    """Clear the cart"""
    cart = Cart(request)
    cart.clear()
    return redirect("cart:cart_detail")


def cart_detail(request):
    """Cart status detail"""
    context = {"title": "Cart", "cart": Cart(request)}
    return render(request, "cart/cart_detail.html", context=context)
