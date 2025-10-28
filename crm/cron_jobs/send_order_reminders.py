import requests
import datetime

GRAPHQL_URL = "http://localhost:8000/graphql"
LOG_FILE = "/tmp/order_reminders_log.txt"

query = """
query {
  allOrders(orderDate_Gte: "%s") {
    id
    customer {
      email
    }
  }
}
""" % ((datetime.date.today() - datetime.timedelta(days=7)).isoformat())

response = requests.post(GRAPHQL_URL, json={'query': query})
data = response.json()

timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
with open(LOG_FILE, "a") as log:
    for order in data.get("data", {}).get("allOrders", []):
        log.write(f"[{timestamp}] Reminder for Order {order['id']} sent to {order['customer']['email']}\n")

print("Order reminders processed!")
