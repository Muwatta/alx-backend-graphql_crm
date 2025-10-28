import datetime
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

def update_low_stock():
    log_file = "/tmp/lowstockupdates_log.txt"
    with open(log_file, "a") as f:
        f.write(f"{datetime.datetime.now()} - Updating low stock products...\n")

    try:
        transport = RequestsHTTPTransport(
            url="http://localhost:8000/graphql/",
            verify=False,
            retries=3,
        )
        client = Client(transport=transport, fetch_schema_from_transport=True)
        mutation = gql("""
            mutation {
                updateLowStockProducts {
                    ok
                }
            }
        """)
        result = client.execute(mutation)
        with open(log_file, "a") as f:
            f.write(f"GraphQL Mutation Result: {result}\n")
    except Exception as e:
        with open(log_file, "a") as f:
            f.write(f"Error: {e}\n")
