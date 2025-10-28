#!/usr/bin/python3
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
import datetime

# Configure GraphQL client
transport = RequestsHTTPTransport(
    url="http://localhost:8000/graphql/",
    verify=False,
    retries=3,
)

client = Client(transport=transport, fetch_schema_from_transport=True)

# Define the GraphQL query
query = gql("""
{
  orders {
    id
    customer {
      name
      email
    }
    status
    delivery_date
  }
}
""")

# Execute query and log results
result = client.execute(query)

timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
with open("/tmp/order_reminders_log.txt", "a") as f:
    f.write(f"[{timestamp}] Successfully fetched {len(result.get('orders', []))} orders.\n")
