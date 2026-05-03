from fastapi.testclient import TestClient

import backend.routes.family as family
from backend.main import app


client = TestClient(app)


def test_exists_handles_falkordb_string_booleans(monkeypatch):
    monkeypatch.setattr(family, "run_query", lambda query: [["ok"], [["false"]]])
    assert family.exists("RETURN false") is False

    monkeypatch.setattr(family, "run_query", lambda query: [["ok"], [["true"]]])
    assert family.exists("RETURN true") is True


def test_normalize_list_splits_falkordb_list_strings():
    assert family.normalize_list("[Asha Sharma, Priya Sharma]") == [
        "Asha Sharma",
        "Priya Sharma",
    ]


def test_search_checks_grandparents_before_parents(monkeypatch):
    monkeypatch.setattr(family, "grandparents_of", lambda name: {"grandparents": ["Raghav Sharma"]})
    monkeypatch.setattr(family, "parents_of", lambda name: {"parents": ["Vijay Sharma"]})

    response = client.get("/search", params={"query": "grandparents of Rohan Sharma"})

    assert response.status_code == 200
    assert response.json() == {"result": ["Raghav Sharma"]}


def test_ask_ai_accepts_common_family_question_variants(monkeypatch):
    monkeypatch.setattr(family, "parents_of", lambda name: {"parents": ["Vijay Sharma", "Kavita Sharma"]})
    monkeypatch.setattr(family, "children_of", lambda name: {"children": ["Asha Sharma", "Rohan Sharma"]})
    monkeypatch.setattr(family, "grandparents_of", lambda name: {"grandparents": ["Raghav Sharma"]})
    monkeypatch.setattr(family, "siblings_of", lambda name: {"siblings": ["Rohan Sharma", "Priya Sharma"]})
    monkeypatch.setattr(family, "cousins_of", lambda name: {"cousins": ["Kunal Rao"]})
    monkeypatch.setattr(family, "second_cousins_of", lambda name: {"second_cousins": ["Rhea Patel"]})
    monkeypatch.setattr(family, "spouse_of", lambda name: {"spouse": ["Vijay Sharma"]})

    cases = {
        "parents of Rohan Sharma": ["Vijay Sharma", "Kavita Sharma"],
        "Who are kids of Vijay Sharma?": ["Asha Sharma", "Rohan Sharma"],
        "Who are grand parents of Rohan Sharma?": ["Raghav Sharma"],
        "brothers and sisters of Asha Sharma": ["Rohan Sharma", "Priya Sharma"],
        "cousins of Rohan Sharma": ["Kunal Rao"],
        "second cousins of Rohan Sharma": ["Rhea Patel"],
        "Who is Kavita Sharma married to?": ["Vijay Sharma"],
    }

    for question, expected in cases.items():
        response = client.get("/ask", params={"q": question})
        assert response.status_code == 200
        assert response.json()["answer"] == expected


def test_ask_ai_stats_order_prefers_gender_over_total_people(monkeypatch):
    monkeypatch.setattr(
        family,
        "family_stats",
        lambda: {
            "total_people": 54,
            "total_relationships": 160,
            "male_count": 27,
            "female_count": 27,
            "over_50": 8,
            "unmarried_over_21": 5,
        },
    )

    response = client.get("/ask", params={"q": "How many male and female members are there?"})

    assert response.status_code == 200
    assert response.json()["answer"] == ["Males: 27", "Females: 27"]
