# import csv
# from backend.graph_db import run_query


# def clean_value(value):
#     if value is None:
#         return ""
#     value = str(value).strip()
#     if value.lower() == "nan":
#         return ""
#     return value.replace('"', '\\"')


# def parse_age(value):
#     value = clean_value(value)
#     if not value:
#         return "null"
#     try:
#         return str(int(float(value)))
#     except Exception:
#         return "null"


# def load_people(csv_path):
#     with open(csv_path, newline="", encoding="utf-8") as file:
#         reader = csv.DictReader(file)

#         for row in reader:
#             person_id = clean_value(row.get("person_id"))
#             first_name = clean_value(row.get("First Name"))
#             last_name = clean_value(row.get("Last Name"))
#             full_name = clean_value(row.get("Full Name"))
#             gender = clean_value(row.get("Gender"))   # M / F
#             age = parse_age(row.get("Age"))

#             if not person_id or not full_name:
#                 continue

#             query = f"""
#             MERGE (p:Person {{id: "{person_id}"}})
#             SET p.name = "{full_name}",
#                 p.first_name = "{first_name}",
#                 p.last_name = "{last_name}",
#                 p.Gender = "{gender}",
#                 p.Age = {age}
#             """
#             run_query(query)


# def load_relationships(csv_path):
#     with open(csv_path, newline="", encoding="utf-8") as file:
#         reader = csv.DictReader(file)

#         for row in reader:
#             a_id = clean_value(row.get("PersonA_ID"))
#             b_id = clean_value(row.get("PersonB_ID"))
#             rel = clean_value(row.get("Related To")).upper()

#             if not a_id or not b_id or not rel:
#                 continue

#             if rel not in {"CHILD", "SPOUSE", "SIBLING"}:
#                 continue

#             query = f"""
#             MATCH (p1:Person {{id: "{a_id}"}})
#             MATCH (p2:Person {{id: "{b_id}"}})
#             CREATE (p1)-[:{rel}]->(p2)
#             """
#             run_query(query)


# def run_pipeline():
#     print("Loading people...")
#     load_people("data/family_members.csv")

#     print("Loading relationships...")
#     load_relationships("data/family_relationships.csv")

#     print("DONE ✅")


# if __name__ == "__main__":
#     run_pipeline()



import csv
from pathlib import Path
from backend.graph_db import run_query

BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "data"


def esc(value):
    if value is None:
        return ""
    return str(value).strip().replace("\\", "\\\\").replace('"', '\\"')


def to_int_or_null(value):
    if value is None:
        return "null"
    s = str(value).strip()
    if not s:
        return "null"
    try:
        return str(int(float(s)))
    except Exception:
        return "null"


def clear_graph():
    run_query("MATCH (n) DETACH DELETE n")


def load_people(csv_path: Path):
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        for row in reader:
            person_id = esc(row.get("person_id") or row.get("id"))
            name = esc(row.get("Full Name") or row.get("full_name"))
            if not person_id or not name:
                continue

            first_name = esc(row.get("First Name"))
            middle_name = esc(row.get("Middle Name (s)"))
            maiden_name = esc(row.get("Maiden Name"))
            last_name = esc(row.get("Last Name"))
            born = esc(row.get("Born"))
            died = esc(row.get("Died"))
            age = to_int_or_null(row.get("Age"))
            gender = esc(row.get("Gender"))
            notes = esc(row.get("Notes"))

            query = f"""
            MERGE (p:Person {{id: "{person_id}"}})
            SET
                p.name = "{name}",
                p.full_name = "{name}",
                p.first_name = "{first_name}",
                p.middle_name = "{middle_name}",
                p.maiden_name = "{maiden_name}",
                p.last_name = "{last_name}",
                p.born = "{born}",
                p.died = "{died}",
                p.age = {age},
                p.gender = "{gender}",
                p.notes = "{notes}"
            """
            run_query(query)


def load_relationships(csv_path: Path):
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        for row in reader:
            a_id = esc(row.get("PersonA_ID") or row.get("person_a_id"))
            b_id = esc(row.get("PersonB_ID") or row.get("person_b_id"))
            rel = esc(row.get("Related To") or row.get("related_to")).upper()

            if not a_id or not b_id or not rel:
                continue

            if rel == "CHILD":
                query = f"""
                MATCH (a:Person {{id: "{a_id}"}})
                MATCH (b:Person {{id: "{b_id}"}})
                MERGE (a)-[:CHILD]->(b)
                """
                run_query(query)

            elif rel == "SIBLING":
                query = f"""
                MATCH (a:Person {{id: "{a_id}"}})
                MATCH (b:Person {{id: "{b_id}"}})
                MERGE (a)-[:SIBLING]->(b)
                MERGE (b)-[:SIBLING]->(a)
                """
                run_query(query)

            elif rel == "SPOUSE":
                query = f"""
                MATCH (a:Person {{id: "{a_id}"}})
                MATCH (b:Person {{id: "{b_id}"}})
                MERGE (a)-[:SPOUSE]->(b)
                MERGE (b)-[:SPOUSE]->(a)
                """
                run_query(query)


def run_pipeline():
    members_csv = DATA_DIR / "family_members.csv"
    relationships_csv = DATA_DIR / "family_relationships.csv"

    print("Clearing old graph...")
    clear_graph()

    print("Loading people...")
    load_people(members_csv)

    print("Loading relationships...")
    load_relationships(relationships_csv)

    print("DONE ✅")


if __name__ == "__main__":
    run_pipeline()