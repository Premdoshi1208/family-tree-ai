import redis

# Connect to FalkorDB (Redis)
r = redis.Redis(host="localhost", port=6379, decode_responses=True)

GRAPH_NAME = "family"

def run_query(query):
    result = r.execute_command("GRAPH.QUERY", GRAPH_NAME, query)
    return result