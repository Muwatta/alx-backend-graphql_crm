import datetime
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport



def log_crm_heartbeat():
    import datetime
    log_file = "/tmp/crmheartbeatlog.txt"

    with open(log_file, "a") as f:
        f.write(f"{datetime.datetime.now()} - CRM Heartbeat OK\n")

    # Optional GraphQL heartbeat check
    transport = RequestsHTTPTransport(
        url="http://localhost:8000/graphql/",
        verify=False,
        retries=3,
    )
    client = Client(transport=transport, fetch_schema_from_transport=True)

    query = gql("""
    query {
        hello
    }
    """)

    try:
        result = client.execute(query)
        with open(log_file, "a") as f:
            f.write(f"GraphQL hello field: {result}\n")
    except Exception as e:
        with open(log_file, "a") as f:
            f.write(f"GraphQL heartbeat failed: {e}\n")
