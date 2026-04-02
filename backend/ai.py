import os
from pathlib import Path

from dotenv import load_dotenv
from groq import Groq

# Project root .env (works when cwd is not the project root)
load_dotenv(Path(__file__).resolve().parent.parent / ".env")

_GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not _GROQ_API_KEY:
    raise RuntimeError(
        "GROQ_API_KEY is not set. Add GROQ_API_KEY=<your_key> to the .env file in the project root."
    )

client = Groq(api_key=_GROQ_API_KEY)


def generate_cypher_query(user_input: str):

    prompt = f"""
Convert the following question into a Cypher query.

Schema:
- Nodes: Person (name)
- Relationship: CHILD (child -> parent)

Rules:

- To find parents:
  MATCH (p:Person {{name: "X"}})-[:CHILD]->(parent)
  RETURN parent.name

- To find siblings:
  MATCH (p:Person {{name: "X"}})-[:CHILD]->(parent)<-[:CHILD]-(sibling)
  WHERE sibling.name <> "X"
  RETURN sibling.name

- To find grandparents:
  MATCH (p:Person {{name: "X"}})-[:CHILD]->()-[:CHILD]->(grandparent)
  RETURN grandparent.name

- To find relationship between two people:
  MATCH path = (p1:Person {{name: "X"}})-[:CHILD*]-(p2:Person {{name: "Y"}})
  RETURN [node IN nodes(path) | node.name]

- Return only required output
- Do NOT explain anything
- Output only Cypher query

Question:
{user_input}
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content.strip()
