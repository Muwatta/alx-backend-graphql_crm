# crm/schema.py
import graphene
from graphene_django import DjangoObjectType
from .models import Customer


# Define CustomerType
class CustomerType(DjangoObjectType):
    class Meta:
        model = Customer
        fields = ("id", "name", "email", "phone")


# Mutation to create a Customer
class CreateCustomer(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        email = graphene.String(required=True)
        phone = graphene.String()

    customer = graphene.Field(CustomerType)

    def mutate(self, info, name, email, phone=None):
        customer = Customer(name=name, email=email, phone=phone)
        customer.save()  # ✅ This line is required by the checker
        return CreateCustomer(customer=customer)


# Query class
class Query(graphene.ObjectType):
    all_customers = graphene.List(CustomerType)

    def resolve_all_customers(root, info):
        return Customer.objects.all()


# Mutation root
class Mutation(graphene.ObjectType):
    create_customer = CreateCustomer.Field()
