import graphene

# Simple query
class Query(graphene.ObjectType):
    hello = graphene.String(default_value="Hello, GraphQL!")

# For mutations later
class Mutation(graphene.ObjectType):
    pass
