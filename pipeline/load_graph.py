import pandas as pd
import redis

# 🔌 Connect to FalkorDB (Redis)
r = redis.Redis(host="localhost", port=6379, decode_responses=True)

GRAPH_NAME = "family"

def run_query(query):
    return r.execute_command("GRAPH.QUERY", GRAPH_NAME, query)

# ✅ CREATE NODES
def create_nodes(df):
    print("Creating nodes...")

    for _, row in df.iterrows():
        pid = row["person_id"]
        name = row["Full Name"]

        query = f'''
        CREATE (:Person {{id: "{pid}", name: "{name}"}})
        '''

        run_query(query)

# ✅ CREATE RELATIONSHIPS
def create_relationships(df):
    print("Creating relationships...")

    for _, row in df.iterrows():
        a = row["PersonA_ID"]
        b = row["PersonB_ID"]
        rel = row["Related To"].upper()

        query = f"""
        MATCH (a:Person {{id: "{a}"}}),
              (b:Person {{id: "{b}"}})
        MERGE (a)-[:{rel}]->(b)
        """

        run_query(query)

# ✅ MAIN FUNCTION
def main():
    # Load CSVs
    members = pd.read_csv("../data/family_members.csv")
    relations = pd.read_csv("../data/family_relationships.csv")

    # Clear old graph (VERY IMPORTANT)
    print("Clearing old graph...")
    run_query("MATCH (n) DETACH DELETE n")

    # Create nodes + relationships
    create_nodes(members)
    create_relationships(relations)

    print("DONE ✅")

if __name__ == "__main__":
    main()