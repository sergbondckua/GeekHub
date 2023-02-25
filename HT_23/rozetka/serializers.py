from rest_framework import serializers

from .models import Category, Product


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for category"""

    class Meta:  # pylint: disable=too-few-public-methods
        """Class Meta"""

        model = Category
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    """Serializer for product"""

    class Meta:  # pylint: disable=too-few-public-methods
        """Class Meta"""

        model = Product
        fields = "__all__"
