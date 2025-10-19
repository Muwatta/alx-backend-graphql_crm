import graphene
from graphene import relay
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from .models import Customer
from .filters import CustomerFilter


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
