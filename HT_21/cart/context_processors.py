from .cart import Cart


def cart(request):
    """Returns dict of Cart objects"""
    return {"cart": Cart(request)}
