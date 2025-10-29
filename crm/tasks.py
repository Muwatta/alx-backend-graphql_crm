import requests
import logging
from datetime import datetime
from celery import shared_task
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

@shared_task
def generate_crm_report():
    """
    Weekly task to generate CRM report.
    Fetches total customers, total orders, and total revenue via GraphQL.
    Logs the result to /tmp/crm_report_log.txt
    """
    try:
        query = """
        {
            allCustomers { totalCount }
            allOrders { totalCount }
            totalRevenue
        }
        """
        response = requests.post(
            "http://localhost:8000/graphql/",
            json={'query': query}
        )
        data = response.json().get('data', {})

        customers = data.get('allCustomers', {}).get('totalCount', 0)
        orders = data.get('allOrders', {}).get('totalCount', 0)
        revenue = data.get('totalRevenue', 0)

        log_path = "/tmp/crm_report_log.txt"
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with open(log_path, "a") as log:
            log.write(f"{timestamp} - Report: {customers} customers, {orders} orders, {revenue} revenue\n")

    except Exception as e:
        with open("/tmp/crm_report_log.txt", "a") as log:
            log.write(f"{datetime.now()} - Error: {str(e)}\n")