import datetime
import requests
from datetime import datetime
from celery import shared_task
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

@shared_task
def generate_crm_report():
    """Generates weekly CRM report and logs to /tmp/crm_report_log.txt"""
    url = "http://localhost:8000/graphql/"
    query = """
    {
        customersCount
        ordersCount
        totalRevenue
    }
    """

    try:
        response = requests.post(url, json={"query": query})
        data = response.json().get("data", {})

        customers = data.get("customersCount", 0)
        orders = data.get("ordersCount", 0)
        revenue = data.get("totalRevenue", 0)

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        report = f"{timestamp} - Report: {customers} customers, {orders} orders, {revenue} revenue\n"

        with open("/tmp/crm_report_log.txt", "a") as f:
            f.write(report)

    except Exception as e:
        with open("/tmp/crm_report_log.txt", "a") as f:
            f.write(f"{datetime.now()} - Error: {e}\n")
