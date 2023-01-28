"""Views"""
from subprocess import Popen

from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import user_passes_test, login_required
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import generic

from .forms import ScrapingTaskForm
from .models import Product, ScrapingTask
from cart.forms import CartAddProductForm


@user_passes_test(lambda u: u.is_superuser)
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

    return render(request, "rozetka/products_add.html", context=context)


class IndexView(generic.TemplateView):
    """View Home Page"""
    template_name = "rozetka/home.html"


class SuperUserRequiredMixin:  # pylint: disable=too-few-public-methods
    """
    View mixin which requires that the authenticated user is a super user
    ('is_superuser' is True).
    """

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        """Check if the super user"""
        if not request.user.is_superuser:
            messages.error(
                request,
                "You do not have the permission required to perform the "
                "requested operation.")
            return redirect("login")
        return super().dispatch(request, *args, **kwargs)


class ProductsListView(generic.ListView):
    """Get product list"""
    model = Product
    paginate_by = 12


class ProductsDetailView(generic.DetailView):
    """Get product detail"""
    model = Product

    def get_context_data(self, **kwargs):
        """Call the base implementation first to get a context"""
        context = super().get_context_data(**kwargs)
        context["cart_product_form"] = CartAddProductForm()
        return context


class ProductsUpdateView(SuperUserRequiredMixin, SuccessMessageMixin,
                         generic.UpdateView):
    """Update product"""
    model = Product
    fields = "__all__"
    template_name = "rozetka/product_form.html"
    success_message = "Product #%(id)s was updated successfully"

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            id=self.object.id,
        )

    def get_success_url(self):
        """Redirect to product page"""
        return reverse_lazy(
            "rozetka:product-detail", kwargs={'pk': self.object.pk})


class ProductsDeleteView(SuperUserRequiredMixin, SuccessMessageMixin,
                         generic.DeleteView):
    """Delete product"""
    model = Product
    template_name = "rozetka/product_delete_confirm.html"
    success_url = reverse_lazy("rozetka:products-list")
    success_message = "%(title)s was deleted successfully"

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            id=self.object.id,
            title=self.object.title)


class DetailsByCategory(generic.ListView):
    """Details by category"""
    paginate_by = 12

    def get_queryset(self):
        return Product.objects.filter(category_id=self.kwargs['category_id'])
