# from fastapi import APIRouter
# from backend.graph_db import run_query
# from backend.ai import generate_cypher_query
# import re
# import random
# import ast 

# router = APIRouter()


# # -------------------- HELPERS --------------------
# def explain_relationship(path):
#     return f"Path: {' → '.join(path)}"


# def infer_relationship_from_path(path):
#     if len(path) < 2:
#         return "unknown"

#     if len(path) == 3:
#         return f"{path[0]} is parent of {path[-1]}"

#     if len(path) == 4:
#         return f"{path[0]} is grandparent of {path[-1]}"

#     return f"{path[0]} is related to {path[-1]}"


# # -------------------- PARENTS --------------------
# @router.get("/parents/{name}")
# def get_parents(name: str):
#     query = f"""
#     MATCH (p:Person {{name: "{name}"}})-[:CHILD]->(parent)
#     RETURN parent.name
#     """
#     rows = run_query(query)[1]
#     return {"parents": [row[0] for row in rows]}


# # -------------------- GRANDPARENTS --------------------
# @router.get("/grandparents/{name}")
# def get_grandparents(name: str):
#     query = f"""
#     MATCH (p:Person {{name: "{name}"}})-[:CHILD]->(parent)-[:CHILD]->(grandparent)
#     RETURN grandparent.name
#     """
#     rows = run_query(query)[1]
#     return {"grandparents": [row[0] for row in rows]}


# # -------------------- SIBLINGS --------------------
# @router.get("/siblings/{name}")
# def get_siblings(name: str):
#     query = f"""
#     MATCH (p:Person {{name: "{name}"}})-[:CHILD]->(parent)<-[:CHILD]-(sibling)
#     WHERE sibling.name <> "{name}"
#     RETURN sibling.name
#     """
#     rows = run_query(query)[1]
#     return {"siblings": [row[0] for row in rows]}


# # -------------------- RELATIONSHIP --------------------
# @router.get("/relationship/{p1}/{p2}")
# def get_relationship(p1: str, p2: str):

#     # child
#     q1 = f"""
#     MATCH (a:Person {{name: "{p1}"}})-[:CHILD]->(b:Person {{name: "{p2}"}})
#     RETURN b.name
#     """
#     if len(run_query(q1)[1]) > 0:
#         return {"relationship": f"{p1} is child of {p2}"}

#     # parent
#     q2 = f"""
#     MATCH (a:Person {{name: "{p1}"}})<-[:CHILD]-(b:Person {{name: "{p2}"}})
#     RETURN a.name
#     """
#     if len(run_query(q2)[1]) > 0:
#         return {"relationship": f"{p1} is parent of {p2}"}

#     # sibling
#     q3 = f"""
#     MATCH (a:Person {{name: "{p1}"}})-[:CHILD]->(p)<-[:CHILD]-(b:Person {{name: "{p2}"}})
#     RETURN p.name
#     """
#     if len(run_query(q3)[1]) > 0:
#         return {"relationship": f"{p1} is sibling of {p2}"}

#     return {"relationship": "unknown"}


# # -------------------- AI QUERY --------------------
# @router.get("/ask")
# def ask_question(q: str):

#     # direct relationship question
#     match = re.match(r"How is (.+?) related to (.+?)\??$", q, re.IGNORECASE)
#     if match:
#         p1 = match.group(1).strip()
#         p2 = match.group(2).strip()
#         return get_relationship(p1, p2)

#     cypher_query = generate_cypher_query(q)

#     cypher_query = cypher_query.replace("shortestPath", "")
#     cypher_query = cypher_query.replace("*1..1", "")
#     cypher_query = cypher_query.replace("*1..4", "*")
#     cypher_query = cypher_query.replace("1..4", "*")

#     rows = run_query(cypher_query)[1]
#     answers = [row[0] for row in rows]

#     if len(answers) > 0 and isinstance(answers[0], list):
#         shortest = min(answers, key=len)
#         return {
#             "relationship": infer_relationship_from_path(shortest),
#             "explanation": explain_relationship(shortest)
#         }

#     return {"answer": answers}


# # -------------------- STATS --------------------
# @router.get("/stats")
# def get_stats():
#     try:
#         # total people
#         q1 = "MATCH (p:Person) RETURN count(p)"
#         total_people = run_query(q1)[1][0][0]

#         # total relationships
#         q2 = "MATCH ()-[r]->() RETURN count(r)"
#         total_relationships = run_query(q2)[1][0][0]

#         # male count
#         q3 = """
#         MATCH (p:Person)
#         WHERE p.Gender = "M"
#         RETURN count(p)
#         """
#         male_count = run_query(q3)[1][0][0]

#         # female count
#         q4 = """
#         MATCH (p:Person)
#         WHERE p.Gender = "F"
#         RETURN count(p)
#         """
#         female_count = run_query(q4)[1][0][0]

#         # age > 50
#         q5 = """
#         MATCH (p:Person)
#         WHERE p.Age > 50
#         RETURN count(p)
#         """
#         over_50 = run_query(q5)[1][0][0]

#         return {
#             "total_people": total_people,
#             "total_relationships": total_relationships,
#             "male_count": male_count,
#             "female_count": female_count,
#             "over_50": over_50
#         }

#     except Exception as e:
#         return {"error": str(e)}
    
# @router.get("/search")
# def search(query: str):
#     try:
#         q = query.lower().strip()

#         if "of" not in q:
#             return {"message": "Please ask like: 'parents of X'"}

#         name = query.split("of", 1)[-1].strip()

#         # parents of X
#         if "parent" in q:
#             cypher = f"""
#             MATCH (p:Person {{name: "{name}"}})-[:CHILD]->(parent)
#             RETURN parent.name
#             """
#             rows = run_query(cypher)[1]
#             return {"result": [row[0] for row in rows]}

#         # siblings of X
#         elif "sibling" in q:
#             cypher = f"""
#             MATCH (p:Person {{name: "{name}"}})-[:CHILD]->(parent)<-[:CHILD]-(sibling)
#             WHERE sibling.name <> "{name}"
#             RETURN sibling.name
#             """
#             rows = run_query(cypher)[1]
#             return {"result": [row[0] for row in rows]}

#         # children of X
#         elif "child" in q:
#             cypher = f"""
#             MATCH (child:Person)-[:CHILD]->(p:Person {{name: "{name}"}})
#             RETURN child.name
#             """
#             rows = run_query(cypher)[1]
#             return {"result": [row[0] for row in rows]}

#         # grandparents of X
#         elif "grandparent" in q:
#             cypher = f"""
#             MATCH (p:Person {{name: "{name}"}})-[:CHILD]->()-[:CHILD]->(grandparent)
#             RETURN grandparent.name
#             """
#             rows = run_query(cypher)[1]
#             return {"result": [row[0] for row in rows]}

#         else:
#             return {"message": "Try: parents of X, siblings of X, children of X, grandparents of X"}

#     except Exception as e:
#         return {"error": str(e)}
    
# @router.get("/relationship/{name1}/{name2}")
# def relationship(name1: str, name2: str):
#     try:
#         # 1. Same person
#         if name1 == name2:
#             return {"relationship": "Same person"}

#         # 2. Check siblings
#         cypher = f"""
#         MATCH (a:Person {{name: "{name1}"}})-[:CHILD]->(p)<-[:CHILD]-(b:Person {{name: "{name2}"}})
#         RETURN COUNT(*) > 0
#         """
#         if run_query(cypher)[1][0][0]:
#             return {"relationship": "Siblings"}

#         # 3. Check if name1 is parent of name2
#         cypher = f"""
#         MATCH (b:Person {{name: "{name2}"}})-[:CHILD]->(a:Person {{name: "{name1}"}})
#         RETURN COUNT(*) > 0
#         """
#         if run_query(cypher)[1][0][0]:
#             return {"relationship": f"{name1} is parent of {name2}"}

#         # 4. Check if name1 is child of name2
#         cypher = f"""
#         MATCH (a:Person {{name: "{name1}"}})-[:CHILD]->(b:Person {{name: "{name2}"}})
#         RETURN COUNT(*) > 0
#         """
#         if run_query(cypher)[1][0][0]:
#             return {"relationship": f"{name1} is child of {name2}"}

#         # 5. Grandparent
#         cypher = f"""
#         MATCH (a:Person {{name: "{name1}"}})<-[:CHILD]-()-[:CHILD]-(b:Person {{name: "{name2}"}})
#         RETURN COUNT(*) > 0
#         """
#         if run_query(cypher)[1][0][0]:
#             return {"relationship": f"{name1} is grandparent of {name2}"}

#         # 6. Grandchild
#         cypher = f"""
#         MATCH (a:Person {{name: "{name1}"}})-[:CHILD]->()-[:CHILD]->(b:Person {{name: "{name2}"}})
#         RETURN COUNT(*) > 0
#         """
#         if run_query(cypher)[1][0][0]:
#             return {"relationship": f"{name1} is grandchild of {name2}"}

#         return {"relationship": "No direct relationship found"}

#     except Exception as e:
#         return {"error": str(e)} 
    
# @router.get("/search_person/{name}")
# def search_person(name: str):
#     query = f"""
#     MATCH (p:Person)
#     WHERE p.name CONTAINS '{name}'
#     RETURN p.name
#     LIMIT 10
#     """
#     result = run_query(query)
#     rows = result[1] if len(result) > 1 else []
#     return [row[0] for row in rows if row and row[0] is not None]


# import random

# @router.get("/random_person")
# def random_person():
#     query = """
#     MATCH (p:Person)
#     RETURN p.name
#     """
#     result = run_query(query)
#     rows = result[1] if len(result) > 1 else []
#     names = [row[0] for row in rows if row and row[0] is not None]

#     if not names:
#         return {"error": "No people found"}

#     return random.choice(names)


# @router.get("/person/{name}")
# def get_person(name: str):
#     def normalize_collection(value):
#         if value is None:
#             return []

#         if isinstance(value, list):
#             return [x for x in value if x not in (None, "", "NULL")]

#         if isinstance(value, str):
#             value = value.strip()
#             if not value:
#                 return []

#             # if FalkorDB returned a string like '["A", "B"]'
#             try:
#                 parsed = ast.literal_eval(value)
#                 if isinstance(parsed, list):
#                     return [x for x in parsed if x not in (None, "", "NULL")]
#             except Exception:
#                 pass

#             # fallback: treat it as one value
#             return [value]

#         return [value]

#     query = f"""
#     MATCH (p:Person {{name: "{name}"}})
#     OPTIONAL MATCH (p)-[:CHILD]->(parent)
#     OPTIONAL MATCH (child)-[:CHILD]->(p)
#     OPTIONAL MATCH (p)-[:CHILD]->(common_parent)<-[:CHILD]-(sibling)
#     WHERE sibling.name <> "{name}"
#     RETURN
#         p.name,
#         p.Gender,
#         p.Age,
#         collect(DISTINCT parent.name),
#         collect(DISTINCT child.name),
#         collect(DISTINCT sibling.name)
#     """

#     result = run_query(query)
#     rows = result[1] if len(result) > 1 else []

#     if not rows:
#         return {"error": "Person not found"}

#     row = rows[0]

#     return {
#         "name": row[0],
#         "gender": row[1],
#         "age": row[2],
#         "parents": normalize_collection(row[3]),
#         "children": normalize_collection(row[4]),
#         "siblings": normalize_collection(row[5]),
#     }
    
# @router.get("/graph/{name}")
# def get_family_graph(name: str):
#     def rows(result):
#         return result[1] if len(result) > 1 else []

#     # check person exists
#     exists_query = f'''
#     MATCH (p:Person {{name: "{name}"}})
#     RETURN p.name
#     LIMIT 1
#     '''
#     exists_result = run_query(exists_query)
#     exists_rows = rows(exists_result)

#     if not exists_rows:
#         return {"error": "Person not found"}

#     nodes = [{"id": name, "label": name, "kind": "self"}]
#     edges = []
#     seen_nodes = {name}

#     def add_node(person_name: str, kind: str):
#         if person_name and person_name not in seen_nodes:
#             nodes.append({"id": person_name, "label": person_name, "kind": kind})
#             seen_nodes.add(person_name)

#     # parents
#     parent_query = f'''
#     MATCH (p:Person {{name: "{name}"}})-[:CHILD]->(parent)
#     RETURN DISTINCT parent.name
#     '''
#     for row in rows(run_query(parent_query)):
#         parent = row[0]
#         add_node(parent, "parent")
#         edges.append({"source": name, "target": parent, "label": "parent"})

#     # children
#     child_query = f'''
#     MATCH (child:Person)-[:CHILD]->(p:Person {{name: "{name}"}})
#     RETURN DISTINCT child.name
#     '''
#     for row in rows(run_query(child_query)):
#         child = row[0]
#         add_node(child, "child")
#         edges.append({"source": name, "target": child, "label": "child"})

#     # siblings
#     sibling_query = f'''
#     MATCH (p:Person {{name: "{name}"}})-[:CHILD]->(parent)<-[:CHILD]-(sibling)
#     WHERE sibling.name <> "{name}"
#     RETURN DISTINCT sibling.name
#     '''
#     for row in rows(run_query(sibling_query)):
#         sibling = row[0]
#         add_node(sibling, "sibling")
#         edges.append({"source": name, "target": sibling, "label": "sibling"})

#     # spouse
#     spouse_query = f'''
#     MATCH (p:Person {{name: "{name}"}})-[:SPOUSE]-(spouse)
#     RETURN DISTINCT spouse.name
#     '''
#     for row in rows(run_query(spouse_query)):
#         spouse = row[0]
#         add_node(spouse, "spouse")
#         edges.append({"source": name, "target": spouse, "label": "spouse"})

#     connected_people = sorted([n["label"] for n in nodes if n["label"] != name])

#     return {
#         "center": name,
#         "nodes": nodes,
#         "edges": edges,
#         "connected_people": connected_people,
#     }

import logging
import random
import re
from typing import Any, Dict, List

from fastapi import APIRouter
from pydantic import BaseModel

from backend.graph_db import run_query

router = APIRouter()
logger = logging.getLogger("family.routes")


# -----------------------------
# HELPERS
# -----------------------------
def esc(value: str) -> str:
    return str(value).replace("\\", "\\\\").replace('"', '\\"').strip()


def rows(result) -> List[List[Any]]:
    return result[1] if isinstance(result, list) and len(result) > 1 else []


def first_col_list(query: str) -> List[Any]:
    result = run_query(query)
    return [row[0] for row in rows(result) if row and row[0] is not None]


def scalar(query: str, default=0):
    result = run_query(query)
    rs = rows(result)
    if not rs or not rs[0]:
        return default
    return rs[0][0]


def normalize_list(value: Any) -> List[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return [x for x in value if x not in (None, "", "NULL")]
    if value in ("", "NULL"):
        return []
    return [value]


def exists(query: str) -> bool:
    result = run_query(query)
    rs = rows(result)
    return bool(rs and rs[0] and rs[0][0])


def search_people_internal(name: str) -> List[str]:
    candidates = []
    seen = set()

    for term in {name, name.title(), name.upper(), name.lower()}:
        term = term.strip()
        if not term:
            continue
        query = f'''
        MATCH (p:Person)
        WHERE p.name CONTAINS "{esc(term)}"
        RETURN p.name
        LIMIT 20
        '''
        for value in first_col_list(query):
            if value not in seen:
                candidates.append(value)
                seen.add(value)

    return candidates


def get_person_internal(name: str) -> Dict[str, Any]:
    query = f'''
    MATCH (p:Person {{name: "{esc(name)}"}})
    OPTIONAL MATCH (p)-[:CHILD]->(parent)
    OPTIONAL MATCH (child)-[:CHILD]->(p)
    OPTIONAL MATCH (p)-[:SIBLING]->(sibling)
    OPTIONAL MATCH (p)-[:SPOUSE]->(spouse)
    RETURN
        p.name,
        p.gender,
        p.age,
        p.born,
        p.died,
        p.notes,
        collect(DISTINCT parent.name),
        collect(DISTINCT child.name),
        collect(DISTINCT sibling.name),
        collect(DISTINCT spouse.name)
    '''
    result = run_query(query)
    rs = rows(result)
    if not rs:
        return {"error": "Person not found"}

    row = rs[0]
    return {
        "name": row[0],
        "gender": row[1],
        "age": row[2],
        "born": row[3],
        "died": row[4],
        "notes": row[5],
        "parents": normalize_list(row[6]),
        "children": normalize_list(row[7]),
        "siblings": normalize_list(row[8]),
        "spouse": normalize_list(row[9]),
    }


def parents_of(name: str) -> Dict[str, List[str]]:
    query = f'''
    MATCH (p:Person {{name: "{esc(name)}"}})-[:CHILD]->(parent)
    RETURN DISTINCT parent.name
    '''
    return {"parents": first_col_list(query)}


def children_of(name: str) -> Dict[str, List[str]]:
    query = f'''
    MATCH (child:Person)-[:CHILD]->(p:Person {{name: "{esc(name)}"}})
    RETURN DISTINCT child.name
    '''
    return {"children": first_col_list(query)}


def grandparents_of(name: str) -> Dict[str, List[str]]:
    query = f'''
    MATCH (p:Person {{name: "{esc(name)}"}})-[:CHILD]->()-[:CHILD]->(grandparent)
    RETURN DISTINCT grandparent.name
    '''
    return {"grandparents": first_col_list(query)}


def siblings_of(name: str) -> Dict[str, List[str]]:
    query = f'''
    MATCH (p:Person {{name: "{esc(name)}"}})-[:CHILD]->(parent)<-[:CHILD]-(sibling)
    WHERE sibling.name <> "{esc(name)}"
    RETURN DISTINCT sibling.name
    '''
    return {"siblings": first_col_list(query)}


def spouse_of(name: str) -> Dict[str, List[str]]:
    query = f'''
    MATCH (p:Person {{name: "{esc(name)}"}})-[:SPOUSE]->(spouse)
    RETURN DISTINCT spouse.name
    '''
    return {"spouse": first_col_list(query)}


def cousins_of(name: str) -> Dict[str, List[str]]:
    query = f'''
    MATCH (me:Person {{name: "{esc(name)}"}})-[:CHILD]->(parent)-[:SIBLING]->(aunt_uncle)<-[:CHILD]-(cousin)
    WHERE cousin.name <> "{esc(name)}"
    RETURN DISTINCT cousin.name
    '''
    return {"cousins": first_col_list(query)}


def second_cousins_of(name: str) -> Dict[str, List[str]]:
    query = f'''
    MATCH (me:Person {{name: "{esc(name)}"}})-[:CHILD]->(parent)-[:CHILD]->(grandparent)
          -[:SIBLING]->(grand_aunt_uncle)<-[:CHILD]-(parent_cousin)<-[:CHILD]-(second_cousin)
    WHERE second_cousin.name <> "{esc(name)}"
    RETURN DISTINCT second_cousin.name
    '''
    return {"second_cousins": first_col_list(query)}


def family_stats() -> Dict[str, Any]:
    total_people = scalar('MATCH (p:Person) RETURN count(p)', 0)
    total_relationships = scalar('MATCH ()-[r]->() RETURN count(r)', 0)
    male_count = scalar('MATCH (p:Person) WHERE p.gender = "M" RETURN count(p)', 0)
    female_count = scalar('MATCH (p:Person) WHERE p.gender = "F" RETURN count(p)', 0)
    over_50 = scalar('MATCH (p:Person) WHERE p.age > 50 RETURN count(p)', 0)

    unmarried_over_21 = scalar(
        '''
        MATCH (p:Person)
        OPTIONAL MATCH (p)-[:SPOUSE]->(sp)
        WITH p, count(sp) AS spouse_count
        WHERE p.age > 21 AND spouse_count = 0
        RETURN count(p)
        ''',
        0,
    )

    return {
        "total_people": total_people,
        "total_relationships": total_relationships,
        "male_count": male_count,
        "female_count": female_count,
        "over_50": over_50,
        "unmarried_over_21": unmarried_over_21,
    }


def relationship_between(name1: str, name2: str) -> Dict[str, str]:
    a = esc(name1)
    b = esc(name2)

    if a == b:
        return {"relationship": "Same person"}

    if exists(f'''
        MATCH (p:Person {{name: "{b}"}})-[:CHILD]->(parent:Person {{name: "{a}"}})
        RETURN count(parent) > 0
    '''):
        return {"relationship": f"{name1} is parent of {name2}"}

    if exists(f'''
        MATCH (p:Person {{name: "{a}"}})-[:CHILD]->(parent:Person {{name: "{b}"}})
        RETURN count(parent) > 0
    '''):
        return {"relationship": f"{name1} is child of {name2}"}

    if exists(f'''
        MATCH (a:Person {{name: "{a}"}})-[:SIBLING]->(b:Person {{name: "{b}"}})
        RETURN count(b) > 0
    '''):
        return {"relationship": "Siblings"}

    if exists(f'''
        MATCH (a:Person {{name: "{a}"}})-[:SPOUSE]->(b:Person {{name: "{b}"}})
        RETURN count(b) > 0
    '''):
        return {"relationship": "Spouse"}

    if exists(f'''
        MATCH (grandparent:Person {{name: "{a}"}})<-[:CHILD]-()-[:CHILD]-(child:Person {{name: "{b}"}})
        RETURN count(child) > 0
    '''):
        return {"relationship": f"{name1} is grandparent of {name2}"}

    if exists(f'''
        MATCH (grandchild:Person {{name: "{a}"}})-[:CHILD]->()-[:CHILD]->(grandparent:Person {{name: "{b}"}})
        RETURN count(grandparent) > 0
    '''):
        return {"relationship": f"{name1} is grandchild of {name2}"}

    if exists(f'''
        MATCH (a:Person {{name: "{a}"}})-[:CHILD]->(p1)-[:SIBLING]->(p2)<-[:CHILD]-(b:Person {{name: "{b}"}})
        RETURN count(b) > 0
    '''):
        return {"relationship": "First cousins"}

    if exists(f'''
        MATCH (a:Person {{name: "{a}"}})-[:CHILD]->(p1)-[:CHILD]->(gp1)-[:SIBLING]->(gp2)<-[:CHILD]-(p2)<-[:CHILD]-(b:Person {{name: "{b}"}})
        RETURN count(b) > 0
    '''):
        return {"relationship": "Second cousins"}

    return {"relationship": "No direct relationship found"}


def graph_for(name: str) -> Dict[str, Any]:
    person = get_person_internal(name)
    if "error" in person:
        return person

    center = person["name"]
    nodes = [{"id": center, "label": center, "kind": "self"}]
    edges = []
    seen = {center}

    def add_node(label: str, kind: str):
        if label and label not in seen:
            nodes.append({"id": label, "label": label, "kind": kind})
            seen.add(label)

    for p in person["parents"]:
        add_node(p, "parent")
        edges.append({"source": p, "target": center, "label": "parent"})

    for c in person["children"]:
        add_node(c, "child")
        edges.append({"source": center, "target": c, "label": "child"})

    for s in person["siblings"]:
        add_node(s, "sibling")
        edges.append({"source": center, "target": s, "label": "sibling"})

    for sp in person["spouse"]:
        add_node(sp, "spouse")
        edges.append({"source": center, "target": sp, "label": "spouse"})

    return {
        "center": center,
        "nodes": nodes,
        "edges": edges,
        "connected_people": sorted([x for x in seen if x != center]),
    }


# -----------------------------
# CORE ROUTES
# -----------------------------
@router.get("/stats")
def get_stats():
    return family_stats()


@router.get("/parents/{name}")
def get_parents(name: str):
    return parents_of(name)


@router.get("/children/{name}")
def get_children(name: str):
    return children_of(name)


@router.get("/grandparents/{name}")
def get_grandparents(name: str):
    return grandparents_of(name)


@router.get("/siblings/{name}")
def get_siblings(name: str):
    return siblings_of(name)


@router.get("/spouse/{name}")
def get_spouse(name: str):
    return spouse_of(name)


@router.get("/cousins/{name}")
def get_cousins(name: str):
    return cousins_of(name)


@router.get("/second_cousins/{name}")
def get_second_cousins(name: str):
    return second_cousins_of(name)


@router.get("/search_person/{name}")
def search_person(name: str):
    return search_people_internal(name)


@router.get("/random_person")
def random_person():
    query = '''
    MATCH (p:Person)
    RETURN p.name
    '''
    names = first_col_list(query)
    if not names:
        return {"error": "No people found"}
    return random.choice(names)


@router.get("/person/{name}")
def get_person(name: str):
    return get_person_internal(name)


@router.get("/graph/{name}")
def get_graph(name: str):
    return graph_for(name)


@router.get("/relationship/{name1}/{name2}")
def get_relationship(name1: str, name2: str):
    return relationship_between(name1, name2)


# -----------------------------
# RELATION LOOKUP ROUTE
# -----------------------------
@router.get("/search")
def search(query: str):
    q = query.lower().strip()

    if " of " not in q:
        return {"message": "Use queries like: parents of X, children of X, cousins of X"}

    target_name = query.split("of", 1)[-1].strip()

    if "parent" in q:
        return {"result": parents_of(target_name)["parents"]}
    if "grandparent" in q:
        return {"result": grandparents_of(target_name)["grandparents"]}
    if "sibling" in q:
        return {"result": siblings_of(target_name)["siblings"]}
    if "child" in q:
        return {"result": children_of(target_name)["children"]}
    if "cousin" in q and "second" not in q:
        return {"result": cousins_of(target_name)["cousins"]}
    if "second cousin" in q:
        return {"result": second_cousins_of(target_name)["second_cousins"]}
    if "spouse" in q:
        return {"result": spouse_of(target_name)["spouse"]}

    return {"message": "Try: parents of X, grandparents of X, siblings of X, children of X, cousins of X"}


# -----------------------------
# NATURAL LANGUAGE QA
# -----------------------------
@router.get("/ask")
def ask_question(q: str):
    text = q.strip()
    lower = text.lower()

    # relation between two people
    m = re.match(r"how is (.+?) related to (.+?)\??$", text, re.IGNORECASE)
    if m:
        return relationship_between(m.group(1).strip(), m.group(2).strip())

    # family members of type
    patterns = [
        (r"who are the parents of (.+?)\??$", parents_of, "parents"),
        (r"who are the children of (.+?)\??$", children_of, "children"),
        (r"who are the grandparents of (.+?)\??$", grandparents_of, "grandparents"),
        (r"who are the siblings of (.+?)\??$", siblings_of, "siblings"),
        (r"who are the first cousins of (.+?)\??$", cousins_of, "cousins"),
        (r"who are the second cousins of (.+?)\??$", second_cousins_of, "second_cousins"),
        (r"who is the spouse of (.+?)\??$", spouse_of, "spouse"),
    ]

    for pattern, func, key in patterns:
        m = re.match(pattern, text, re.IGNORECASE)
        if m:
            payload = func(m.group(1).strip())
            return {"query": pattern, "answer": payload.get(key, [])}

    # stats questions
    stats = family_stats()

    if "over the age of 50" in lower or "over 50" in lower:
        return {"query": "stats.over_50", "answer": [stats["over_50"]]}

    if "males vs" in lower or "male vs" in lower or "males and females" in lower:
        return {
            "query": "stats.male_count + stats.female_count",
            "answer": [f'Males: {stats["male_count"]}', f'Females: {stats["female_count"]}'],
        }

    if "unmarried" in lower and "21" in lower:
        return {"query": "stats.unmarried_over_21", "answer": [stats["unmarried_over_21"]]}

    if "random person" in lower:
        return {"query": "random_person", "answer": [random_person()]}

    return {
        "query": "fallback",
        "answer": ["I could not confidently map that question yet. Try a parents, grandparents, siblings, cousins, or relationship question."],
    }


# -----------------------------
# TOOL-STYLE ENDPOINTS
# -----------------------------
class ToolCall(BaseModel):
    name: str
    arguments: Dict[str, Any] = {}


@router.get("/mcp/tools")
def list_tools():
    return {
        "tools": [
            "stats",
            "parents",
            "children",
            "grandparents",
            "siblings",
            "spouse",
            "cousins",
            "second_cousins",
            "search_person",
            "random_person",
            "person",
            "graph",
            "relationship",
        ]
    }


@router.post("/mcp/call")
def call_tool(call: ToolCall):
    name = call.name
    args = call.arguments or {}

    if name == "stats":
        return family_stats()
    if name == "parents":
        return parents_of(args.get("name", ""))
    if name == "children":
        return children_of(args.get("name", ""))
    if name == "grandparents":
        return grandparents_of(args.get("name", ""))
    if name == "siblings":
        return siblings_of(args.get("name", ""))
    if name == "spouse":
        return spouse_of(args.get("name", ""))
    if name == "cousins":
        return cousins_of(args.get("name", ""))
    if name == "second_cousins":
        return second_cousins_of(args.get("name", ""))
    if name == "search_person":
        return search_people_internal(args.get("name", ""))
    if name == "random_person":
        return random_person()
    if name == "person":
        return get_person_internal(args.get("name", ""))
    if name == "graph":
        return graph_for(args.get("name", ""))
    if name == "relationship":
        return relationship_between(args.get("name1", ""), args.get("name2", ""))

    return {"error": f"Unknown tool: {name}"}