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


def unique_values(values: List[Any]) -> List[Any]:
    unique = []
    seen = set()

    for value in normalize_list(values):
        if value not in seen:
            unique.append(value)
            seen.add(value)

    return unique


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
        normalized: List[Any] = []
        for item in value:
            normalized.extend(normalize_list(item))
        return normalized
    if value in ("", "NULL"):
        return []
    if isinstance(value, str):
        cleaned = value.strip()
        if cleaned.startswith("[") and cleaned.endswith("]"):
            cleaned = cleaned[1:-1].strip()
            if not cleaned:
                return []
            return [part.strip().strip('"').strip("'") for part in cleaned.split(",") if part.strip()]
        return [cleaned]
    return [value]


def exists(query: str) -> bool:
    result = run_query(query)
    rs = rows(result)
    if not rs or not rs[0]:
        return False

    value = rs[0][0]
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.strip().lower() == "true"
    return bool(value)


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


def resolve_person_name(name: str) -> str:
    raw_name = str(name).strip()
    if not raw_name:
        return ""

    query = f'''
    MATCH (p:Person {{name: "{esc(raw_name)}"}})
    RETURN p.name
    LIMIT 1
    '''
    exact = first_col_list(query)
    if exact:
        return exact[0]

    matches = search_people_internal(raw_name)
    lowered = raw_name.lower()
    for match in matches:
        if match.lower() == lowered:
            return match

    if len(matches) == 1:
        return matches[0]

    return raw_name


def get_person_internal(name: str) -> Dict[str, Any]:
    resolved_name = resolve_person_name(name)
    query = f'''
    MATCH (p:Person {{name: "{esc(resolved_name)}"}})
    RETURN
        p.name,
        p.gender,
        p.age,
        p.born,
        p.died,
        p.notes
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
        "parents": parents_of(row[0])["parents"],
        "children": children_of(row[0])["children"],
        "siblings": siblings_of(row[0])["siblings"],
        "spouse": spouse_of(row[0])["spouse"],
    }


def parents_of(name: str) -> Dict[str, List[str]]:
    resolved_name = resolve_person_name(name)
    query = f'''
    MATCH (p:Person {{name: "{esc(resolved_name)}"}})-[:CHILD]->(parent)
    RETURN DISTINCT parent.name
    '''
    return {"parents": first_col_list(query)}


def children_of(name: str) -> Dict[str, List[str]]:
    resolved_name = resolve_person_name(name)
    query = f'''
    MATCH (child:Person)-[:CHILD]->(p:Person {{name: "{esc(resolved_name)}"}})
    RETURN DISTINCT child.name
    '''
    return {"children": first_col_list(query)}


def grandparents_of(name: str) -> Dict[str, List[str]]:
    grandparents: List[str] = []
    for parent in parents_of(name)["parents"]:
        grandparents.extend(parents_of(parent)["parents"])
    return {"grandparents": unique_values(grandparents)}


def siblings_of(name: str) -> Dict[str, List[str]]:
    resolved_name = resolve_person_name(name)

    explicit_query = f'''
    MATCH (p:Person {{name: "{esc(resolved_name)}"}})-[:SIBLING]-(sibling)
    RETURN DISTINCT sibling.name
    '''
    siblings = first_col_list(explicit_query)

    parent_query = f'''
    MATCH (p:Person {{name: "{esc(resolved_name)}"}})-[:CHILD]->(parent)<-[:CHILD]-(sibling)
    WHERE sibling.name <> "{esc(resolved_name)}"
    RETURN DISTINCT sibling.name
    '''
    siblings.extend(first_col_list(parent_query))

    return {"siblings": unique_values(siblings)}


def spouse_of(name: str) -> Dict[str, List[str]]:
    resolved_name = resolve_person_name(name)
    query = f'''
    MATCH (p:Person {{name: "{esc(resolved_name)}"}})-[:SPOUSE]->(spouse)
    RETURN DISTINCT spouse.name
    '''
    return {"spouse": first_col_list(query)}


def cousins_of(name: str) -> Dict[str, List[str]]:
    resolved_name = resolve_person_name(name)
    cousins: List[str] = []

    for parent in parents_of(resolved_name)["parents"]:
        for aunt_uncle in siblings_of(parent)["siblings"]:
            cousins.extend(children_of(aunt_uncle)["children"])

    return {"cousins": [person for person in unique_values(cousins) if person != resolved_name]}


def second_cousins_of(name: str) -> Dict[str, List[str]]:
    resolved_name = resolve_person_name(name)
    second_cousins: List[str] = []

    for grandparent in grandparents_of(resolved_name)["grandparents"]:
        for grand_aunt_uncle in siblings_of(grandparent)["siblings"]:
            for parent_cousin in children_of(grand_aunt_uncle)["children"]:
                second_cousins.extend(children_of(parent_cousin)["children"])

    return {"second_cousins": [person for person in unique_values(second_cousins) if person != resolved_name]}


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
    resolved1 = resolve_person_name(name1)
    resolved2 = resolve_person_name(name2)

    if not resolved1 or not resolved2:
        return {"relationship": "No direct relationship found"}

    if resolved1 == resolved2:
        return {"relationship": "Same person"}

    if resolved2 in children_of(resolved1)["children"]:
        return {"relationship": f"{resolved1} is parent of {resolved2}"}

    if resolved2 in parents_of(resolved1)["parents"]:
        return {"relationship": f"{resolved1} is child of {resolved2}"}

    if resolved2 in siblings_of(resolved1)["siblings"]:
        return {"relationship": "Siblings"}

    if resolved2 in spouse_of(resolved1)["spouse"]:
        return {"relationship": "Spouse"}

    if resolved1 in grandparents_of(resolved2)["grandparents"]:
        return {"relationship": f"{resolved1} is grandparent of {resolved2}"}

    if resolved2 in grandparents_of(resolved1)["grandparents"]:
        return {"relationship": f"{resolved1} is grandchild of {resolved2}"}

    if resolved2 in cousins_of(resolved1)["cousins"]:
        return {"relationship": "First cousins"}

    if resolved2 in second_cousins_of(resolved1)["second_cousins"]:
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

    if "grandparent" in q:
        return {"result": grandparents_of(target_name)["grandparents"]}
    if "parent" in q:
        return {"result": parents_of(target_name)["parents"]}
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
    lower = " ".join(text.lower().split())

    # relation between two people
    relationship_patterns = [
        r"how is (.+?) related to (.+?)\??$",
        r"how are (.+?) and (.+?) related\??$",
        r"what(?: is|'s)? the relation(?:ship)? between (.+?) and (.+?)\??$",
        r"relationship between (.+?) and (.+?)\??$",
    ]
    for pattern in relationship_patterns:
        m = re.match(pattern, text, re.IGNORECASE)
        if m:
            return relationship_between(m.group(1).strip(), m.group(2).strip())

    # direct family-member questions. Keep more specific relations before broad ones.
    question_prefix = r"(?:(?:who|what) (?:are|is) (?:the )?|tell me (?:the )?|show me (?:the )?|give me (?:the )?|find (?:the )?)?"
    relation_patterns = [
        (rf"{question_prefix}second cousins? of (.+?)\??$", second_cousins_of, "second_cousins"),
        (rf"{question_prefix}(?:first cousins?|cousins?) of (.+?)\??$", cousins_of, "cousins"),
        (rf"{question_prefix}grand\s*parents? of (.+?)\??$", grandparents_of, "grandparents"),
        (rf"{question_prefix}parents? of (.+?)\??$", parents_of, "parents"),
        (rf"{question_prefix}(?:children|child|kids?) of (.+?)\??$", children_of, "children"),
        (rf"{question_prefix}(?:siblings?|brothers and sisters|brothers?|sisters?) of (.+?)\??$", siblings_of, "siblings"),
        (rf"{question_prefix}(?:spouse|husband|wife) of (.+?)\??$", spouse_of, "spouse"),
        (r"who is (.+?) married to\??$", spouse_of, "spouse"),
        (r"who is married to (.+?)\??$", spouse_of, "spouse"),
    ]

    for pattern, func, key in relation_patterns:
        m = re.match(pattern, text, re.IGNORECASE)
        if m:
            payload = func(m.group(1).strip())
            return {"query": key, "answer": payload.get(key, [])}

    # stats questions
    stats = family_stats()

    if "males vs" in lower or "male vs" in lower or "males and females" in lower or "male and female" in lower or "gender" in lower:
        return {
            "query": "stats.male_count + stats.female_count",
            "answer": [f'Males: {stats["male_count"]}', f'Females: {stats["female_count"]}'],
        }

    if ("total" in lower or "how many" in lower) and ("people" in lower or "members" in lower) and "over" not in lower and "unmarried" not in lower:
        return {"query": "stats.total_people", "answer": [stats["total_people"]]}

    if ("total" in lower or "how many" in lower) and "relationship" in lower:
        return {"query": "stats.total_relationships", "answer": [stats["total_relationships"]]}

    if "over the age of 50" in lower or "over 50" in lower:
        return {"query": "stats.over_50", "answer": [stats["over_50"]]}

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
