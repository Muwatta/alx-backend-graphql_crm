import graphene

# Task 0: minimal Query class
class Query(graphene.ObjectType):
    hello = graphene.String()

    def resolve_hello(self, info):
        return "Hello, GraphQL!"

# Define the schema
schema = graphene.Schema(query=Query)
