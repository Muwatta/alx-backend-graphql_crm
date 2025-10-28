import datetime
from celery import shared_task
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

@shared_task
def generate_crm_report():
    log_file = "/tmp/crm_report_log.txt"
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        # Setup GraphQL client
        transport = RequestsHTTPTransport(
            url="http://localhost:8000/graphql/",
            verify=False,
            retries=3,
        )
        client = Client(transport=transport, fetch_schema_from_transport=True)

        # GraphQL query
        query = gql("""
        query {
            allCustomers {
                totalCount
            }
            allOrders {
                totalCount
                edges {
                    node {
                        totalAmount
                    }
                }
            }
        }
        """)

        result = client.execute(query)

        total_customers = result["allCustomers"]["totalCount"]
        total_orders = result["allOrders"]["totalCount"]
        total_revenue = sum(
            edge["node"]["totalAmount"] for edge in result["allOrders"]["edges"]
        )

        with open(log_file, "a") as f:
            f.write(f"{timestamp} - Report: {total_customers} customers, {total_orders} orders, {total_revenue} revenue\n")

    except Exception as e:
        with open(log_file, "a") as f:
            f.write(f"{timestamp} - Error generating report: {e}\n")
