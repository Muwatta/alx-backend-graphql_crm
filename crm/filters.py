import django_filters
from .models import Customer, Product, Order

class CustomerFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name="name", lookup_expr="icontains")
    email = django_filters.CharFilter(field_name="email", lookup_expr="icontains")
    created_at = django_filters.DateFromToRangeFilter(field_name="created_at")
    
    class Meta:
        model = Customer
        fields = ['name', 'email', 'created_at']

class ProductFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name="name", lookup_expr="icontains")
    price = django_filters.NumericRangeFilter(field_name="price")
    stock = django_filters.NumericRangeFilter(field_name="stock")

    class Meta:
        model = Product
        fields = ['name', 'price', 'stock']

class OrderFilter(django_filters.FilterSet):
    total_amount = django_filters.NumericRangeFilter(field_name="total_amount")
    order_date = django_filters.DateFromToRangeFilter(field_name="order_date")
    customer_name = django_filters.CharFilter(field_name="customer__name", lookup_expr="icontains")
    product_name = django_filters.CharFilter(field_name="products__name", lookup_expr="icontains")

    class Meta:
        model = Order
        fields = ['total_amount', 'order_date', 'customer_name', 'product_name']
