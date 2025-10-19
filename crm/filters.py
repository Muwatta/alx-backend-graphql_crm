import django_filters
from django_filters import FilterSet
from .models import Customer, Product, Order


class CustomerFilter(FilterSet):
    name = django_filters.CharFilter(field_name="name", lookup_expr="icontains")
    email = django_filters.CharFilter(field_name="email", lookup_expr="icontains")
    created_at = django_filters.DateFromToRangeFilter(field_name="created_at")

    class Meta:
        model = Customer
        fields = ["name", "email", "created_at"]


class ProductFilter(FilterSet):
    name = django_filters.CharFilter(field_name="name", lookup_expr="icontains")
    price = django_filters.RangeFilter(field_name="price")
    stock = django_filters.RangeFilter(field_name="stock")

    class Meta:
        model = Product
        fields = ["name", "price", "stock"]


class OrderFilter(FilterSet):
    total_amount = django_filters.RangeFilter(field_name="total_amount")
    order_date = django_filters.DateFromToRangeFilter(field_name="order_date")
    customer_name = django_filters.CharFilter(field_name="customer__name", lookup_expr="icontains")
    product_name = django_filters.CharFilter(field_name="products__name", lookup_expr="icontains")

    class Meta:
        model = Order
        fields = ["total_amount", "order_date", "customer_name", "product_name"]
