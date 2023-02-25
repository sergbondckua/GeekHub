from decimal import Decimal

from django.conf import settings
from rozetka.models import Product


class Cart:
    """Cart initalizes"""

    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # save an empty cart in the session
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product, quantity=1, update_quantity=False):
        """Add a product to the cart or update its quantity."""
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {"quantity": 0, "price": str(product.price)}
        if update_quantity:
            self.cart[product_id]["quantity"] = quantity
        else:
            self.cart[product_id]["quantity"] += quantity
        self.save()

    def save(self):
        """Save the cart"""
        # Session update cart
        self.session[settings.CART_SESSION_ID] = self.cart
        # Mark a session as "modified" to make sure it's saved
        self.session.modified = True

    def remove(self, product):
        """Removing an item from the cart."""
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        """
        Iterating through the items in the cart and getting
        the products from the database.
        """
        product_ids = self.cart.keys()
        # getting product objects and adding them to cart
        products = Product.objects.filter(id__in=product_ids)
        for product in products:
            self.cart[str(product.id)]["product"] = product

        for item in self.cart.values():
            item["price"] = Decimal(item["price"])
            item["total_price"] = item["price"] * item["quantity"]
            yield item

    def __len__(self):
        """Counting all items in the cart."""
        return sum(item["quantity"] for item in self.cart.values())

    def get_total_price(self):
        """Calculate the cost of items in the shopping cart."""
        return sum(
            Decimal(item["price"]) * item["quantity"] for item in self.cart.values()
        )

    def clear(self):
        """Clear the shopping cart"""
        # delete cart from session
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True
