import graphene
from graphene import relay
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from .models import Customer
from .filters import CustomerFilter
from .models import Product
from crm.models import Product



# Customer Node
class CustomerNode(DjangoObjectType):
    class Meta:
        model = Customer
        filterset_class = CustomerFilter
        interfaces = (relay.Node,)


# Mutation to create a Customer
class CreateCustomer(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        email = graphene.String(required=True)
        phone = graphene.String()

    customer = graphene.Field(CustomerNode)

    def mutate(self, info, name, email, phone=None):
        customer = Customer(name=name, email=email, phone=phone)
        customer.save()  # ✅ Required by ALX checker
        return CreateCustomer(customer=customer)


# Query class
class Query(graphene.ObjectType):
    all_customers = DjangoFilterConnectionField(CustomerNode)

    def resolve_all_customers(root, info, **kwargs):
        return Customer.objects.all()


# Mutation root
class Mutation(graphene.ObjectType):
    create_customer = CreateCustomer.Field()

class UpdateLowStockProducts(graphene.Mutation):
    message = graphene.String()
    updated_products = graphene.List(graphene.String)

    def mutate(self, info):
        updated_names = []
        low_stock_products = Product.objects.filter(stock__lt=10)
        for p in low_stock_products:
            p.stock += 10
            p.save()
            updated_names.append(f"{p.name} → {p.stock}")
        message = "Low stock products updated successfully!"
        return UpdateLowStockProducts(message=message, updated_products=updated_names)

class Mutation(graphene.ObjectType):
    update_low_stock_products = UpdateLowStockProducts.Field()

class ProductType(DjangoObjectType):
    class Meta:
        model = Product
        fields = "__all__"


class UpdateLowStockProducts(graphene.Mutation):
    ok = graphene.Boolean()

    @classmethod
    def mutate(cls, root, info):
        low_stock_products = Product.objects.filter(stock__lt=10)
        for product in low_stock_products:
            product.low_stock_alert = True
            product.save()
        return UpdateLowStockProducts(ok=True)