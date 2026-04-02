from fastapi.testclient import TestClient
from backend.main import app
import backend.routes.family as family

client = TestClient(app)


def fake_run_query(query: str):
    if 'RETURN count(p)' in query and 'MATCH (p:Person)' in query and 'gender' not in query and 'age' not in query:
        return [[], [[54]]]
    if 'RETURN count(r)' in query:
        return [[], [[118]]]
    if 'p.gender = "M"' in query:
        return [[], [[27]]]
    if 'p.gender = "F"' in query:
        return [[], [[27]]]
    if 'p.age > 50' in query and 'spouse_count' not in query:
        return [[], [[8]]]
    if 'spouse_count = 0' in query:
        return [[], [[11]]]
    if 'MATCH (p:Person)' in query and 'RETURN p.name' in query:
        return [[], [["Rohan Sharma"], ["Priya Sharma"]]]
    if 'MATCH (p:Person {name: "Rohan Sharma"})-[:CHILD]->(parent)' in query:
        return [[], [["Kavita Sharma"], ["Vijay Sharma"]]]
    if 'MATCH (p:Person {name: "Asha Sharma"})-[:SIBLING]->(b:Person {name: "Rohan Sharma"})' in query:
        return [[], [[True]]]
    return [[], []]


def setup_module():
    family.run_query = fake_run_query


def test_stats():
    resp = client.get("/stats")
    assert resp.status_code == 200
    data = resp.json()
    assert data["total_people"] == 54
    assert data["male_count"] == 27


def test_search_person():
    resp = client.get("/search_person/Rohan")
    assert resp.status_code == 200
    assert "Rohan Sharma" in resp.json()


def test_parents():
    resp = client.get("/parents/Rohan Sharma")
    assert resp.status_code == 200
    assert resp.json()["parents"] == ["Kavita Sharma", "Vijay Sharma"]


def test_relationship():
    resp = client.get("/relationship/Asha Sharma/Rohan Sharma")
    assert resp.status_code == 200
    assert "relationship" in resp.json()