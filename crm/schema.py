import graphene
from graphene_django.types import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from django.core.validators import validate_email
from django.db import transaction
from .models import Customer, Product, Order
from .filters import CustomerFilter, ProductFilter, OrderFilter

# Define GraphQL types with Node interface for relay
class CustomerType(DjangoObjectType):
    class Meta:
        model = Customer
        filterset_class = CustomerFilter
        interfaces = (graphene.relay.Node,)  # Add Node for relay support

class ProductType(DjangoObjectType):
    class Meta:
        model = Product
        filterset_class = ProductFilter
        interfaces = (graphene.relay.Node,)  # Add Node for relay support

class OrderType(DjangoObjectType):
    class Meta:
        model = Order
        filterset_class = OrderFilter
        interfaces = (graphene.relay.Node,)  # Add Node for relay support

# Query class with filtering support
class Query(graphene.ObjectType):
    hello = graphene.String()
    all_customers = DjangoFilterConnectionField(CustomerType)
    all_products = DjangoFilterConnectionField(ProductType)
    all_orders = DjangoFilterConnectionField(OrderType)

    def resolve_hello(self, info):
        return "Hello, GraphQL!"

# Mutation classes (unchanged from your setup)
class CustomerInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    email = graphene.String(required=True)
    phone = graphene.String()

class CreateCustomer(graphene.Mutation):
    customer = graphene.Field(CustomerType)
    message = graphene.String()

    class Arguments:
        input = CustomerInput(required=True)

    def mutate(self, info, input):
        try:
            validate_email(input.email)
            if Customer.objects.filter(email=input.email).exists():
                raise Exception("Email already exists")
            if input.phone and not (input.phone.startswith('+') or input.phone.replace('-', '').isdigit()):
                raise Exception("Invalid phone format")
            customer = Customer.objects.create(
                name=input.name, email=input.email, phone=input.phone
            )
            return CreateCustomer(customer=customer, message="Customer created successfully")
        except Exception as e:
            raise Exception(str(e))

class BulkCreateCustomers(graphene.Mutation):
    customers = graphene.List(CustomerType)
    errors = graphene.List(graphene.String)

    class Arguments:
        input = graphene.List(CustomerInput, required=True)

    def mutate(self, info, input):
        customers = []
        errors = []
        with transaction.atomic():
            for item in input:
                try:
                    validate_email(item.email)
                    if Customer.objects.filter(email=item.email).exists():
                        raise Exception(f"Email {item.email} already exists")
                    customer = Customer.objects.create(
                        name=item.name, email=item.email, phone=item.phone
                    )
                    customers.append(customer)
                except Exception as e:
                    errors.append(str(e))
        return BulkCreateCustomers(customers=customers, errors=errors)

class ProductInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    price = graphene.Float(required=True)
    stock = graphene.Int(default_value=0)

class CreateProduct(graphene.Mutation):
    product = graphene.Field(ProductType)

    class Arguments:
        input = ProductInput(required=True)

    def mutate(self, info, input):
        if input.price <= 0:
            raise Exception("Price must be positive")
        if input.stock < 0:
            raise Exception("Stock cannot be negative")
        product = Product.objects.create(
            name=input.name, price=input.price, stock=input.stock
        )
        return CreateProduct(product=product)

class OrderInput(graphene.InputObjectType):
    customer_id = graphene.ID(required=True)
    product_ids = graphene.List(graphene.ID, required=True)
    order_date = graphene.DateTime()

class CreateOrder(graphene.Mutation):
    order = graphene.Field(OrderType)

    class Arguments:
        input = OrderInput(required=True)

    def mutate(self, info, input):
        customer = Customer.objects.filter(id=input.customer_id).first()
        if not customer:
            raise Exception("Invalid customer ID")
        products = Product.objects.filter(id__in=input.product_ids)
        if not products:
            raise Exception("At least one valid product ID is required")
        total_amount = sum(product.price for product in products)
        order = Order.objects.create(
            customer=customer,
            total_amount=total_amount,
            order_date=input.order_date or None
        )
        order.products.set(products)
        return CreateOrder(order=order)

class Mutation(graphene.ObjectType):
    create_customer = CreateCustomer.Field()
    bulk_create_customers = BulkCreateCustomers.Field()
    create_product = CreateProduct.Field()
    create_order = CreateOrder.Field()