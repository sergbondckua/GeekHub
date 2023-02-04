"""Views the Cart"""
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_POST

from rozetka.models import Product
from .cart import Cart
from .forms import CartAddProductForm


@require_POST
def cart_add(request):
    """Add a new product in the cart"""
    product_id = request.POST.get('pid')
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
    return JsonResponse(
        {
            "status": "product add to cart success",
            "qty": cart.__len__(),
        }
    )


def cart_remove(request):
    """Remove a product from the cart"""
    product_id = request.GET['product_id']
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return JsonResponse(
        {
            "status": "product remove from cart success",
            "qty": cart.__len__(),
            "total_price": cart.get_total_price()
        }
    )


def cart_clear(request):
    """Clear the cart"""
    cart = Cart(request)
    cart.clear()
    return JsonResponse(
        {
            "status": "Clear cart success",
            "qty": cart.__len__(),
            "total_price": 0
        }
    )


def cart_detail(request):
    """Cart status detail"""
    context = {"title": "Cart", "cart": Cart(request)}
    return render(request, "cart/cart_detail.html", context=context)
