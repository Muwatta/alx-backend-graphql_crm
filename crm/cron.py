from datetime import datetime
import requests

def log_crm_heartbeat():
    now = datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
    log_file = "/tmp/crm_heartbeat_log.txt"
    try:
        # Optional check
        response = requests.post("http://localhost:8000/graphql", json={"query": "{ hello }"})
        status = "✅ OK" if response.status_code == 200 else "⚠️ Down"
    except Exception as e:
        status = f"❌ Error: {e}"

    with open(log_file, "a") as f:
        f.write(f"{now} CRM is alive - {status}\n")

def update_low_stock():
    import requests
    import datetime

    query = """
    mutation {
      updateLowStockProducts {
        message
        updatedProducts
      }
    }
    """
    try:
        response = requests.post("http://localhost:8000/graphql", json={'query': query})
        data = response.json()
        log_msg = data.get('data', {}).get('updateLowStockProducts', {}).get('message', 'No message')
        products = data.get('data', {}).get('updateLowStockProducts', {}).get('updatedProducts', [])
    except Exception as e:
        log_msg = f"Error: {e}"
        products = []

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("/tmp/low_stock_updates_log.txt", "a") as f:
        f.write(f"[{timestamp}] {log_msg}: {products}\n")
