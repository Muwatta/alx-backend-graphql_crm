# alx_backend_graphql/schema.py
import graphene
from crm.schema import Query as CRMQuery, Mutation as CRMMutation

# Combine your CRM queries into the project-level Query
class Query(CRMQuery, graphene.ObjectType):
    pass

# Combine your CRM mutations into the project-level Mutation
class Mutation(CRMMutation, graphene.ObjectType):
    pass

# Create the main schema that will be exposed at /graphql
schema = graphene.Schema(query=Query, mutation=Mutation)
