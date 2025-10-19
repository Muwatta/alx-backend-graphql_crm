# crm/schema.py
import graphene
from graphene_django import DjangoObjectType
from .models import Customer


# Define the CustomerType with Meta class and correct fields
class CustomerType(DjangoObjectType):
    class Meta:
        model = Customer
        fields = ("id", "name", "email", "phone")


# Define the Query class
class Query(graphene.ObjectType):
    all_customers = graphene.List(CustomerType)

    def resolve_all_customers(root, info):
        return Customer.objects.all()


# Define the Mutation placeholder (needed later)
class Mutation(graphene.ObjectType):
    pass
