# import ast
# import requests
# import streamlit as st
# from typing import Any, Dict, List, Optional

# BASE_URL = "http://127.0.0.1:8000"
# REQUEST_TIMEOUT = 15


# # -----------------------------
# # PAGE SETUP
# # -----------------------------
# st.set_page_config(
#     page_title="Family Tree AI Browser",
#     page_icon="🌳",
#     layout="wide",
#     initial_sidebar_state="expanded",
# )


# # -----------------------------
# # STYLING
# # -----------------------------
# def inject_css() -> None:
#     st.markdown(
#         """
#         <style>
#             .stApp {
#                 background: linear-gradient(180deg, #f8fbff 0%, #eef4ff 48%, #f8fbff 100%);
#             }

#             .block-container {
#                 padding-top: 1.5rem;
#                 padding-bottom: 2rem;
#                 max-width: 1280px;
#             }

#             .hero {
#                 background: linear-gradient(135deg, #0f172a 0%, #1e3a8a 60%, #2563eb 100%);
#                 color: white;
#                 padding: 28px 30px;
#                 border-radius: 24px;
#                 box-shadow: 0 20px 40px rgba(15, 23, 42, 0.15);
#                 margin-bottom: 1.2rem;
#             }

#             .hero h1 {
#                 font-size: 2.2rem;
#                 line-height: 1.15;
#                 margin: 0;
#                 font-weight: 800;
#                 letter-spacing: -0.02em;
#             }

#             .hero p {
#                 margin-top: 10px;
#                 margin-bottom: 0;
#                 color: rgba(255, 255, 255, 0.88);
#                 font-size: 1rem;
#             }

#             .tag-row {
#                 margin-top: 16px;
#                 display: flex;
#                 flex-wrap: wrap;
#                 gap: 10px;
#             }

#             .tag {
#                 padding: 7px 12px;
#                 border-radius: 999px;
#                 background: rgba(255, 255, 255, 0.12);
#                 border: 1px solid rgba(255, 255, 255, 0.15);
#                 font-size: 0.85rem;
#                 color: white;
#             }

#             .section-card {
#                 background: white;
#                 border: 1px solid #e5e7eb;
#                 border-radius: 20px;
#                 padding: 18px 18px 12px 18px;
#                 box-shadow: 0 10px 25px rgba(15, 23, 42, 0.05);
#                 margin-bottom: 1rem;
#             }

#             .section-title {
#                 font-size: 1.1rem;
#                 font-weight: 700;
#                 color: #0f172a;
#                 margin-bottom: 4px;
#             }

#             .section-subtitle {
#                 font-size: 0.92rem;
#                 color: #64748b;
#                 margin-bottom: 14px;
#             }

#             .result-box {
#                 background: #f8fafc;
#                 border: 1px solid #e2e8f0;
#                 border-radius: 16px;
#                 padding: 14px;
#                 margin-top: 10px;
#             }

#             .chip-wrap {
#                 display: flex;
#                 flex-wrap: wrap;
#                 gap: 8px;
#                 margin-top: 6px;
#             }

#             .chip {
#                 display: inline-block;
#                 padding: 8px 12px;
#                 border-radius: 999px;
#                 background: #eff6ff;
#                 border: 1px solid #bfdbfe;
#                 color: #1e3a8a;
#                 font-size: 0.9rem;
#                 font-weight: 600;
#             }

#             .small-note {
#                 color: #64748b;
#                 font-size: 0.85rem;
#                 margin-top: 6px;
#             }

#             div[data-testid="stMetric"] {
#                 background: white;
#                 border: 1px solid #e5e7eb;
#                 border-radius: 18px;
#                 padding: 12px 8px;
#                 box-shadow: 0 10px 25px rgba(15, 23, 42, 0.04);
#             }

#             .footer-note {
#                 text-align: center;
#                 color: #64748b;
#                 margin-top: 10px;
#                 font-size: 0.9rem;
#             }
#         </style>
#         """,
#         unsafe_allow_html=True,
#     )


# inject_css()


# # -----------------------------
# # HELPERS
# # -----------------------------
# def api_get(path: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
#     url = f"{BASE_URL}{path}"
#     try:
#         response = requests.get(url, params=params, timeout=REQUEST_TIMEOUT)
#         response.raise_for_status()
#         return {"ok": True, "data": response.json()}
#     except requests.exceptions.RequestException as exc:
#         return {"ok": False, "error": str(exc)}


# def unwrap_list(payload: Any) -> List[Any]:
#     if payload is None:
#         return []

#     if isinstance(payload, list):
#         flattened: List[Any] = []
#         for item in payload:
#             if isinstance(item, list):
#                 flattened.extend(item)
#             else:
#                 flattened.append(item)
#         return flattened

#     return [payload]


# def normalize_value_list(value: Any) -> List[str]:
#     if value is None:
#         return []

#     if isinstance(value, list):
#         cleaned = []
#         for item in value:
#             if item is None:
#                 continue
#             if isinstance(item, str) and item.strip():
#                 cleaned.append(item)
#             elif not isinstance(item, str):
#                 cleaned.append(str(item))
#         return cleaned

#     if isinstance(value, str):
#         value = value.strip()
#         if not value:
#             return []

#         try:
#             parsed = ast.literal_eval(value)
#             if isinstance(parsed, list):
#                 cleaned = []
#                 for item in parsed:
#                     if item is None:
#                         continue
#                     if isinstance(item, str) and item.strip():
#                         cleaned.append(item)
#                     elif not isinstance(item, str):
#                         cleaned.append(str(item))
#                 return cleaned
#         except Exception:
#             pass

#         return [value]

#     return [str(value)]


# def render_chip_list(items: List[Any]) -> None:
#     items = normalize_value_list(items)

#     if not items:
#         st.info("No results found.")
#         return

#     chips_html = '<div class="chip-wrap">'
#     for item in items:
#         chips_html += f'<span class="chip">{item}</span>'
#     chips_html += "</div>"
#     st.markdown(chips_html, unsafe_allow_html=True)


# def section_header(title: str, subtitle: str) -> None:
#     st.markdown(
#         f'''
#         <div class="section-card">
#             <div class="section-title">{title}</div>
#             <div class="section-subtitle">{subtitle}</div>
#         ''',
#         unsafe_allow_html=True,
#     )


# def section_footer() -> None:
#     st.markdown("</div>", unsafe_allow_html=True)


# def render_json(data: Any) -> None:
#     st.json(data)


# def build_graphviz_dot(graph_data: Dict[str, Any]) -> str:
#     color_map = {
#         "self": "#1d4ed8",
#         "parent": "#16a34a",
#         "child": "#ea580c",
#         "sibling": "#7c3aed",
#         "spouse": "#db2777",
#     }

#     lines = [
#         "digraph Family {",
#         'graph [pad="0.3", nodesep="0.6", ranksep="1.0"];',
#         'node [shape=box, style="filled,rounded", fontname="Helvetica", fontsize="12", color="#cbd5e1"];',
#         'edge [fontname="Helvetica", fontsize="10", color="#64748b"];',
#     ]

#     for node in graph_data.get("nodes", []):
#         node_id = node["id"]
#         label = node["label"]
#         kind = node.get("kind", "self")
#         fill = color_map.get(kind, "#475569")
#         font_color = "white"
#         penwidth = "2" if kind == "self" else "1"
#         lines.append(
#             f'"{node_id}" [label="{label}", fillcolor="{fill}", fontcolor="{font_color}", penwidth="{penwidth}"];'
#         )

#     for edge in graph_data.get("edges", []):
#         source = edge["source"]
#         target = edge["target"]
#         label = edge["label"]

#         if label in ("sibling", "spouse"):
#             lines.append(
#                 f'"{source}" -> "{target}" [label="{label}", dir=none, color="#94a3b8"];'
#             )
#         else:
#             lines.append(
#                 f'"{source}" -> "{target}" [label="{label}"];'
#             )

#     lines.append("}")
#     return "\n".join(lines)


# # -----------------------------
# # HERO
# # -----------------------------
# st.markdown(
#     """
#     <div class="hero">
#         <h1>Family Tree AI Browser</h1>
#         <p>
#             Explore your family knowledge graph with a clean interface for statistics, relationship lookups,
#             natural-language questions, and graph-backed family insights.
#         </p>
#         <div class="tag-row">
#             <span class="tag">Streamlit Frontend</span>
#             <span class="tag">FastAPI Backend</span>
#             <span class="tag">FalkorDB Graph</span>
#             <span class="tag">Groq-powered AI</span>
#         </div>
#     </div>
#     """,
#     unsafe_allow_html=True,
# )


# # -----------------------------
# # SIDEBAR
# # -----------------------------
# st.sidebar.title("🌳 Family Tree AI")
# st.sidebar.markdown("Use the sections below to explore the graph and ask questions.")
# page = st.sidebar.radio(
#     "Choose a section",
#     [
#         "Dashboard",
#         "Search Relations",
#         "Graph Browser",
#         "Ask AI",
#         "Compare People",
#         "API Health Check",
#     ],
# )

# st.sidebar.markdown("---")
# st.sidebar.markdown("**Backend URL**")
# st.sidebar.code(BASE_URL)


# # -----------------------------
# # PAGE: DASHBOARD
# # -----------------------------
# if page == "Dashboard":
#     stats_resp = api_get("/stats")

#     if not stats_resp["ok"]:
#         st.error(f"Could not load stats: {stats_resp['error']}")
#     else:
#         stats = stats_resp["data"]
#         st.subheader("📊 Family Overview")

#         c1, c2, c3, c4, c5 = st.columns(5)
#         c1.metric("Total People", stats.get("total_people", "-"))
#         c2.metric("Relationships", stats.get("total_relationships", "-"))
#         c3.metric("Male Count", stats.get("male_count", "-"))
#         c4.metric("Female Count", stats.get("female_count", "-"))
#         c5.metric("Over 50", stats.get("over_50", "-"))

#         st.markdown("\n")

#         left, right = st.columns([1.2, 1])

#         with left:
#             section_header(
#                 "Quick Demo Checks",
#                 "Use these suggested tests to validate the backend and showcase your system during a demo.",
#             )
#             demo_items = [
#                 "Parents of Rohan Sharma → Kavita Sharma, Vijay Sharma",
#                 "Grandparents of Rohan Sharma → Kusum Patel, Devendra Patel, Meera Sharma, Raghav Sharma",
#                 "Siblings of Asha Sharma → Priya Sharma, Rohan Sharma",
#                 "AI question: Who are the grandparents of Rohan Sharma?",
#                 "Search query: parents of Rohan Sharma",
#             ]
#             for item in demo_items:
#                 st.markdown(f"- {item}")
#             section_footer()

#         with right:
#             section_header(
#                 "System Status",
#                 "A compact summary of what this app is currently using.",
#             )
#             st.success("Frontend connected to backend")
#             st.write("- Streamlit UI")
#             st.write("- FastAPI REST API")
#             st.write("- FalkorDB knowledge graph")
#             st.write("- AI-assisted natural language querying")
#             section_footer()


# # -----------------------------
# # PAGE: SEARCH RELATIONS
# # -----------------------------
# elif page == "Search Relations":
#     st.subheader("🔎 Search Family Relations")

#     col1, col2 = st.columns([1.1, 0.9])

#     with col1:
#         section_header(
#             "Lookup a relationship",
#             "Choose a relation type and enter a full name exactly as stored in your database.",
#         )

#         name = st.text_input("Person name", value="Rohan Sharma")
#         relation_type = st.selectbox(
#             "Relation type",
#             ["parents", "grandparents", "siblings", "children"],
#         )

#         if st.button("Run Lookup", use_container_width=True):
#             resp = api_get("/search", params={"query": f"{relation_type} of {name}"})

#             if not resp["ok"]:
#                 st.error(resp["error"])
#             else:
#                 st.markdown('<div class="result-box">', unsafe_allow_html=True)
#                 st.write(f"**Result for:** {relation_type} of {name}")
#                 render_chip_list(resp["data"].get("result", []))
#                 st.markdown("</div>", unsafe_allow_html=True)

#         section_footer()

#     with col2:
#         section_header(
#             "🔍 Search People",
#             "Search by partial name, explore random people, and view full profiles.",
#         )

#         search_query = st.text_input("Search person")

#         if st.button("🎲 Random Person"):
#             res = api_get("/random_person")
#             if res["ok"]:
#                 data = res["data"]
#                 if isinstance(data, dict) and data.get("error"):
#                     st.error(data["error"])
#                 else:
#                     st.success(f"Random: {data}")
#             else:
#                 st.error(res["error"])

#         if search_query:
#             results = api_get(f"/search_person/{search_query}")

#             if results["ok"]:
#                 result_data = normalize_value_list(results["data"])

#                 if result_data:
#                     selected = st.selectbox("Select person", result_data)

#                     if st.button("View Profile"):
#                         profile = api_get(f"/person/{selected}")

#                         if profile["ok"]:
#                             p = profile["data"]

#                             if isinstance(p, dict) and p.get("error"):
#                                 st.error(p["error"])
#                             else:
#                                 st.markdown("### 👤 Profile")

#                                 m1, m2, m3 = st.columns(3)
#                                 with m1:
#                                     st.metric("Name", p.get("name", "-"))
#                                 with m2:
#                                     st.metric("Gender", p.get("gender", "-"))
#                                 with m3:
#                                     st.metric("Age", p.get("age", "-"))

#                                 st.markdown('<div class="result-box">', unsafe_allow_html=True)
#                                 st.write("**Parents**")
#                                 render_chip_list(p.get("parents", []))
#                                 st.markdown("</div>", unsafe_allow_html=True)

#                                 st.markdown('<div class="result-box">', unsafe_allow_html=True)
#                                 st.write("**Children**")
#                                 render_chip_list(p.get("children", []))
#                                 st.markdown("</div>", unsafe_allow_html=True)

#                                 st.markdown('<div class="result-box">', unsafe_allow_html=True)
#                                 st.write("**Siblings**")
#                                 render_chip_list(p.get("siblings", []))
#                                 st.markdown("</div>", unsafe_allow_html=True)
#                         else:
#                             st.error(profile["error"])
#                 else:
#                     st.warning("No results found")
#             else:
#                 st.error(results["error"])

#         section_footer()


# # -----------------------------
# # PAGE: GRAPH BROWSER
# # -----------------------------
# elif page == "Graph Browser":
#     st.subheader("🌐 Family Graph Browser")

#     if "graph_person" not in st.session_state:
#         st.session_state.graph_person = "Rohan Sharma"

#     top_left, top_right = st.columns([2, 1])

#     with top_left:
#         person_name = st.text_input(
#             "Enter person name",
#             value=st.session_state.graph_person,
#             key="graph_person_input"
#         )

#     with top_right:
#         st.markdown("<br>", unsafe_allow_html=True)
#         load_graph = st.button("Load Graph", use_container_width=True)

#     if load_graph:
#         st.session_state.graph_person = person_name.strip()

#     graph_resp = api_get(f"/graph/{st.session_state.graph_person}")

#     if not graph_resp["ok"]:
#         st.error(graph_resp["error"])
#     else:
#         graph_data = graph_resp["data"]

#         if isinstance(graph_data, dict) and graph_data.get("error"):
#             st.error(graph_data["error"])
#         else:
#             st.markdown('<div class="result-box">', unsafe_allow_html=True)
#             st.write(f"**Visual graph for:** {graph_data['center']}")
#             st.graphviz_chart(build_graphviz_dot(graph_data), use_container_width=True)
#             st.markdown("</div>", unsafe_allow_html=True)

#             col1, col2 = st.columns([1.2, 1])

#             with col1:
#                 st.markdown('<div class="result-box">', unsafe_allow_html=True)
#                 st.write("**Connected people**")
#                 render_chip_list(graph_data.get("connected_people", []))
#                 st.markdown("</div>", unsafe_allow_html=True)

#             with col2:
#                 options = normalize_value_list(graph_data.get("connected_people", []))
#                 next_person = st.selectbox(
#                     "Browse connected person",
#                     [""] + options,
#                     key="connected_person_select"
#                 )
#                 if next_person and st.button("Open Selected Person", use_container_width=True):
#                     st.session_state.graph_person = next_person
#                     st.rerun()

#             profile_resp = api_get(f"/person/{st.session_state.graph_person}")
#             if profile_resp["ok"] and not profile_resp["data"].get("error"):
#                 p = profile_resp["data"]

#                 st.markdown("### 👤 Current Person Profile")
#                 m1, m2, m3 = st.columns(3)
#                 with m1:
#                     st.metric("Name", p.get("name", "-"))
#                 with m2:
#                     st.metric("Gender", p.get("gender", "-"))
#                 with m3:
#                     st.metric("Age", p.get("age", "-"))

#                 c1, c2, c3 = st.columns(3)
#                 with c1:
#                     st.markdown('<div class="result-box">', unsafe_allow_html=True)
#                     st.write("**Parents**")
#                     render_chip_list(p.get("parents", []))
#                     st.markdown("</div>", unsafe_allow_html=True)

#                 with c2:
#                     st.markdown('<div class="result-box">', unsafe_allow_html=True)
#                     st.write("**Children**")
#                     render_chip_list(p.get("children", []))
#                     st.markdown("</div>", unsafe_allow_html=True)

#                 with c3:
#                     st.markdown('<div class="result-box">', unsafe_allow_html=True)
#                     st.write("**Siblings**")
#                     render_chip_list(p.get("siblings", []))
#                     st.markdown("</div>", unsafe_allow_html=True)


# # -----------------------------
# # PAGE: ASK AI
# # -----------------------------
# elif page == "Ask AI":
#     st.subheader("🤖 Ask the Family Tree AI")

#     section_header(
#         "Natural language querying",
#         "Ask family questions in plain English. The backend will convert the question into graph logic and return the result.",
#     )

#     examples = [
#         "Who are the grandparents of Rohan Sharma?",
#         "Who are the parents of Rohan Sharma?",
#         "Who are the siblings of Asha Sharma?",
#         "How is Asha Sharma related to Rohan Sharma?",
#     ]

#     example_choice = st.selectbox("Quick example", ["Custom"] + examples)
#     default_question = "Who are the grandparents of Rohan Sharma?"
#     if example_choice != "Custom":
#         default_question = example_choice

#     question = st.text_area(
#         "Enter your question",
#         value=default_question,
#         height=120,
#     )

#     if st.button("Ask AI", use_container_width=True):
#         if not question.strip():
#             st.warning("Please enter a question.")
#         else:
#             resp = api_get("/ask", params={"q": question.strip()})
#             if not resp["ok"]:
#                 st.error(resp["error"])
#             else:
#                 data = resp["data"]
#                 c1, c2 = st.columns([1, 1])
#                 with c1:
#                     st.markdown('<div class="result-box">', unsafe_allow_html=True)
#                     st.write("**Answer**")
#                     if "answer" in data:
#                         render_chip_list(data.get("answer", []))
#                     elif "relationship" in data:
#                         st.success(data.get("relationship"))
#                         if data.get("explanation"):
#                             st.caption(data.get("explanation"))
#                     elif "error" in data:
#                         st.error(data.get("error"))
#                     else:
#                         render_json(data)
#                     st.markdown("</div>", unsafe_allow_html=True)

#                 with c2:
#                     st.markdown('<div class="result-box">', unsafe_allow_html=True)
#                     st.write("**Raw Response**")
#                     render_json(data)
#                     st.markdown("</div>", unsafe_allow_html=True)

#     section_footer()


# # -----------------------------
# # PAGE: COMPARE PEOPLE
# # -----------------------------
# elif page == "Compare People":
#     st.subheader("🔗 Compare Two People")

#     left, right = st.columns(2)
#     with left:
#         person1 = st.text_input("First person", value="Asha Sharma")
#     with right:
#         person2 = st.text_input("Second person", value="Rohan Sharma")

#     if st.button("Find Relationship", use_container_width=True):
#         if not person1.strip() or not person2.strip():
#             st.warning("Please enter both names.")
#         else:
#             resp = api_get(f"/relationship/{person1.strip()}/{person2.strip()}")
#             if not resp["ok"]:
#                 st.error(resp["error"])
#             else:
#                 data = resp["data"]
#                 st.markdown('<div class="result-box">', unsafe_allow_html=True)
#                 relationship = data.get("relationship", "No result")
#                 st.success(relationship)
#                 render_json(data)
#                 st.markdown("</div>", unsafe_allow_html=True)

#     st.markdown(
#         "<div class='small-note'>Try: Asha Sharma + Rohan Sharma, or Kusum Patel + Rohan Sharma.</div>",
#         unsafe_allow_html=True,
#     )


# # -----------------------------
# # PAGE: API HEALTH CHECK
# # -----------------------------
# elif page == "API Health Check":
#     st.subheader("🩺 Backend Health Check")

#     home_resp = api_get("/")
#     stats_resp = api_get("/stats")

#     c1, c2 = st.columns(2)
#     with c1:
#         st.markdown('<div class="result-box">', unsafe_allow_html=True)
#         st.write("**Root Endpoint**")
#         if home_resp["ok"]:
#             st.success("Backend root reachable")
#             render_json(home_resp["data"])
#         else:
#             st.error(home_resp["error"])
#         st.markdown("</div>", unsafe_allow_html=True)

#     with c2:
#         st.markdown('<div class="result-box">', unsafe_allow_html=True)
#         st.write("**Stats Endpoint**")
#         if stats_resp["ok"]:
#             st.success("Stats endpoint reachable")
#             render_json(stats_resp["data"])
#         else:
#             st.error(stats_resp["error"])
#         st.markdown("</div>", unsafe_allow_html=True)


# st.markdown("<div class='footer-note'>Built with Streamlit + FastAPI + FalkorDB + Groq</div>", unsafe_allow_html=True)

import requests
import streamlit as st
from typing import Any, Dict, List, Optional

AGRAPH_IMPORT_ERROR: Optional[str] = None
try:
    from streamlit_agraph import agraph, Node, Edge, Config

    HAS_AGRAPH = True
except Exception as exc:
    HAS_AGRAPH = False
    AGRAPH_IMPORT_ERROR = str(exc)

BASE_URL = "http://127.0.0.1:8000"
REQUEST_TIMEOUT = 15


# -----------------------------
# PAGE SETUP
# -----------------------------
st.set_page_config(
    page_title="Family Tree AI Browser",
    page_icon="🌳",
    layout="wide",
    initial_sidebar_state="expanded",
)


# -----------------------------
# STYLING
# -----------------------------
def inject_css() -> None:
    st.markdown(
        """
        <style>
            .stApp {
                background: linear-gradient(180deg, #f8fbff 0%, #eef4ff 48%, #f8fbff 100%);
            }

            .block-container {
                padding-top: 1.5rem;
                padding-bottom: 2rem;
                max-width: 1280px;
            }

            .hero {
                background: linear-gradient(135deg, #0f172a 0%, #1e3a8a 60%, #2563eb 100%);
                color: white;
                padding: 28px 30px;
                border-radius: 24px;
                box-shadow: 0 20px 40px rgba(15, 23, 42, 0.15);
                margin-bottom: 1.2rem;
            }

            .hero h1 {
                font-size: 2.2rem;
                line-height: 1.15;
                margin: 0;
                font-weight: 800;
                letter-spacing: -0.02em;
            }

            .hero p {
                margin-top: 10px;
                margin-bottom: 0;
                color: rgba(255, 255, 255, 0.88);
                font-size: 1rem;
            }

            .tag-row {
                margin-top: 16px;
                display: flex;
                flex-wrap: wrap;
                gap: 10px;
            }

            .tag {
                padding: 7px 12px;
                border-radius: 999px;
                background: rgba(255, 255, 255, 0.12);
                border: 1px solid rgba(255, 255, 255, 0.15);
                font-size: 0.85rem;
                color: white;
            }

            .section-card {
                background: white;
                border: 1px solid #e5e7eb;
                border-radius: 20px;
                padding: 18px 18px 12px 18px;
                box-shadow: 0 10px 25px rgba(15, 23, 42, 0.05);
                margin-bottom: 1rem;
            }

            .section-title {
                font-size: 1.1rem;
                font-weight: 700;
                color: #0f172a;
                margin-bottom: 4px;
            }

            .section-subtitle {
                font-size: 0.92rem;
                color: #64748b;
                margin-bottom: 14px;
            }

            .result-box {
                background: #f8fafc;
                border: 1px solid #e2e8f0;
                border-radius: 16px;
                padding: 14px;
                margin-top: 10px;
            }

            .chip-wrap {
                display: flex;
                flex-wrap: wrap;
                gap: 8px;
                margin-top: 6px;
            }

            .chip {
                display: inline-block;
                padding: 8px 12px;
                border-radius: 999px;
                background: #eff6ff;
                border: 1px solid #bfdbfe;
                color: #1e3a8a;
                font-size: 0.9rem;
                font-weight: 600;
            }

            .footer-note {
                text-align: center;
                color: #64748b;
                margin-top: 10px;
                font-size: 0.9rem;
            }

            div[data-testid="stMetric"] {
                background: white;
                border: 1px solid #e5e7eb;
                border-radius: 18px;
                padding: 12px 8px;
                box-shadow: 0 10px 25px rgba(15, 23, 42, 0.04);
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


inject_css()


# -----------------------------
# HELPERS
# -----------------------------
def api_get(path: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    url = f"{BASE_URL}{path}"
    try:
        response = requests.get(url, params=params, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        return {"ok": True, "data": response.json()}
    except requests.exceptions.RequestException as exc:
        return {"ok": False, "error": str(exc)}


def api_post(path: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    url = f"{BASE_URL}{path}"
    try:
        response = requests.post(url, json=payload, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        return {"ok": True, "data": response.json()}
    except requests.exceptions.RequestException as exc:
        return {"ok": False, "error": str(exc)}


def normalize_value_list(value: Any) -> List[str]:
    if value is None:
        return []
    if isinstance(value, list):
        out = []
        for item in value:
            if item is None:
                continue
            if isinstance(item, list):
                out.extend(normalize_value_list(item))
            else:
                s = str(item).strip()
                if s:
                    out.append(s)
        return out
    s = str(value).strip()
    return [s] if s else []


def render_chip_list(items: List[Any]) -> None:
    items = normalize_value_list(items)
    if not items:
        st.info("No results found.")
        return

    html = '<div class="chip-wrap">'
    for item in items:
        html += f'<span class="chip">{item}</span>'
    html += "</div>"
    st.markdown(html, unsafe_allow_html=True)


def section_open(title: str, subtitle: str) -> None:
    st.markdown(
        f'''
        <div class="section-card">
            <div class="section-title">{title}</div>
            <div class="section-subtitle">{subtitle}</div>
        ''',
        unsafe_allow_html=True,
    )


def section_close() -> None:
    st.markdown("</div>", unsafe_allow_html=True)


def render_profile(profile: Dict[str, Any]) -> None:
    st.markdown("### 👤 Profile")
    c1, c2, c3 = st.columns(3)
    c1.metric("Name", profile.get("name", "-"))
    c2.metric("Gender", profile.get("gender", "-"))
    c3.metric("Age", profile.get("age", "-"))

    c4, c5, c6 = st.columns(3)
    with c4:
        st.markdown('<div class="result-box">', unsafe_allow_html=True)
        st.write("**Parents**")
        render_chip_list(profile.get("parents", []))
        st.markdown("</div>", unsafe_allow_html=True)

    with c5:
        st.markdown('<div class="result-box">', unsafe_allow_html=True)
        st.write("**Children**")
        render_chip_list(profile.get("children", []))
        st.markdown("</div>", unsafe_allow_html=True)

    with c6:
        st.markdown('<div class="result-box">', unsafe_allow_html=True)
        st.write("**Siblings**")
        render_chip_list(profile.get("siblings", []))
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="result-box">', unsafe_allow_html=True)
    st.write("**Spouse**")
    render_chip_list(profile.get("spouse", []))
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="result-box">', unsafe_allow_html=True)
    st.write(f"**Born:** {profile.get('born', '') or '-'}")
    st.write(f"**Died:** {profile.get('died', '') or '-'}")
    st.write(f"**Notes:** {profile.get('notes', '') or '-'}")
    st.markdown("</div>", unsafe_allow_html=True)


def build_nodes_edges(graph_data: Dict[str, Any]):
    color_map = {
        "self": "#1d4ed8",
        "parent": "#16a34a",
        "child": "#ea580c",
        "sibling": "#7c3aed",
        "spouse": "#db2777",
    }
    nodes = []
    edges = []

    for node in graph_data.get("nodes", []):
        nodes.append(
            Node(
                id=node["id"],
                label=node["label"],
                size=28 if node.get("kind") == "self" else 22,
                color=color_map.get(node.get("kind", "self"), "#475569"),
            )
        )

    for edge in graph_data.get("edges", []):
        edges.append(
            Edge(
                source=edge["source"],
                target=edge["target"],
                label=edge["label"],
            )
        )

    return nodes, edges


# -----------------------------
# HERO
# -----------------------------
st.markdown(
    """
    <div class="hero">
        <h1>Family Tree AI Browser</h1>
        <p>
            Search family members, inspect profiles, explore the graph visually,
            ask natural-language questions, and browse derived family relationships.
        </p>
        <div class="tag-row">
            <span class="tag">Streamlit</span>
            <span class="tag">FastAPI</span>
            <span class="tag">FalkorDB</span>
            <span class="tag">Graph-powered Family Browser</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# -----------------------------
# SIDEBAR
# -----------------------------
st.sidebar.title("🌳 Family Tree AI")
page = st.sidebar.radio(
    "Choose a section",
    [
        "Dashboard",
        "Explore People",
        "Graph Browser",
        "Ask AI",
        "Compare People",
        "API Health Check",
    ],
)
st.sidebar.markdown("---")
st.sidebar.code(BASE_URL)


# -----------------------------
# DASHBOARD
# -----------------------------
if page == "Dashboard":
    stats_resp = api_get("/stats")
    if not stats_resp["ok"]:
        st.error(stats_resp["error"])
    else:
        stats = stats_resp["data"]
        st.subheader("📊 Family Overview")
        c1, c2, c3, c4, c5, c6 = st.columns(6)
        c1.metric("Total People", stats.get("total_people", "-"))
        c2.metric("Relationships", stats.get("total_relationships", "-"))
        c3.metric("Male Count", stats.get("male_count", "-"))
        c4.metric("Female Count", stats.get("female_count", "-"))
        c5.metric("Over 50", stats.get("over_50", "-"))
        c6.metric("Unmarried > 21", stats.get("unmarried_over_21", "-"))

        left, right = st.columns([1.2, 1])
        with left:
            section_open("Suggested demo checks", "Good tests for showing that your graph is real.")
            for item in [
                "Parents of Rohan Sharma",
                "Grandparents of Rohan Sharma",
                "Siblings of Asha Sharma",
                "Ask: Who are the first cousins of Rohan Sharma?",
                "Random person explorer",
            ]:
                st.markdown(f"- {item}")
            section_close()

        with right:
            section_open("Project status", "This frontend is using the live backend.")
            st.success("Connected to backend")
            st.write("- Search by name")
            st.write("- Random person")
            st.write("- Full profile")
            st.write("- Graph browser")
            st.write("- Ask AI")
            section_close()


# -----------------------------
# EXPLORE PEOPLE
# -----------------------------
elif page == "Explore People":
    st.subheader("🔎 Explore People")

    left, right = st.columns([1.05, 0.95])

    with left:
        section_open("Lookup a relationship", "Query direct family relations from the graph.")
        person_name = st.text_input("Person name", value="Rohan Sharma", key="lookup_name")
        relation_type = st.selectbox(
            "Relation type",
            ["parents", "grandparents", "siblings", "children", "cousins", "second cousins", "spouse"],
        )

        if st.button("Run Lookup", use_container_width=True):
            query_text = relation_type.replace("second cousins", "second cousins")
            resp = api_get("/search", params={"query": f"{query_text} of {person_name}"})
            if not resp["ok"]:
                st.error(resp["error"])
            else:
                data = resp["data"]
                st.markdown('<div class="result-box">', unsafe_allow_html=True)
                st.write(f"**Result for:** {relation_type} of {person_name}")
                if "result" in data:
                    render_chip_list(data["result"])
                else:
                    st.json(data)
                st.markdown("</div>", unsafe_allow_html=True)
        section_close()

    with right:
        section_open("Search + random + profile", "Search partial names, fetch a random person, and view a clean profile.")
        search_query = st.text_input("Search person by partial name", value="", key="search_person_text")

        c1, c2 = st.columns([1.3, 1])
        with c1:
            if search_query:
                results_resp = api_get(f"/search_person/{search_query}")
                if results_resp["ok"]:
                    result_names = normalize_value_list(results_resp["data"])
                else:
                    result_names = []
                    st.error(results_resp["error"])
            else:
                result_names = []

            selected = st.selectbox("Matching people", [""] + result_names, key="selected_person")

        with c2:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🎲 Random Person", use_container_width=True):
                random_resp = api_get("/random_person")
                if random_resp["ok"]:
                    st.success(f"Random: {random_resp['data']}")
                else:
                    st.error(random_resp["error"])

        if selected and st.button("View Profile", use_container_width=True):
            profile_resp = api_get(f"/person/{selected}")
            if profile_resp["ok"]:
                data = profile_resp["data"]
                if isinstance(data, dict) and data.get("error"):
                    st.error(data["error"])
                else:
                    render_profile(data)
            else:
                st.error(profile_resp["error"])
        section_close()


# -----------------------------
# GRAPH BROWSER
# -----------------------------
elif page == "Graph Browser":
    st.subheader("🌐 Graph Browser")

    if "graph_person" not in st.session_state:
        st.session_state.graph_person = "Rohan Sharma"

    c1, c2 = st.columns([2, 1])
    with c1:
        new_name = st.text_input("Graph center person", value=st.session_state.graph_person)
    with c2:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Load Graph", use_container_width=True):
            st.session_state.graph_person = new_name.strip()

    graph_resp = api_get(f"/graph/{st.session_state.graph_person}")
    if not graph_resp["ok"]:
        st.error(graph_resp["error"])
    else:
        graph_data = graph_resp["data"]
        if isinstance(graph_data, dict) and graph_data.get("error"):
            st.error(graph_data["error"])
        else:
            if HAS_AGRAPH:
                nodes, edges = build_nodes_edges(graph_data)
                config = Config(
                    width="100%",
                    height=500,
                    directed=True,
                    physics=True,
                    hierarchical=False,
                    nodeHighlightBehavior=True,
                    highlightColor="#dbeafe",
                    collapsible=False,
                )
                clicked = agraph(nodes=nodes, edges=edges, config=config)
                if clicked and clicked != st.session_state.graph_person:
                    st.session_state.graph_person = clicked
                    st.rerun()
            else:
                st.info(
                    "Interactive graph package not installed or failed to load. "
                    "Install with: `pip install streamlit-agraph` in the **same environment** that runs Streamlit."
                )
                if AGRAPH_IMPORT_ERROR:
                    st.caption(f"Import error: {AGRAPH_IMPORT_ERROR}")
                st.json(graph_data)

            st.markdown('<div class="result-box">', unsafe_allow_html=True)
            st.write("**Connected people**")
            render_chip_list(graph_data.get("connected_people", []))
            st.markdown("</div>", unsafe_allow_html=True)

            options = normalize_value_list(graph_data.get("connected_people", []))
            selected_next = st.selectbox("Jump to connected person", [""] + options)
            if selected_next and st.button("Open Selected Person", use_container_width=True):
                st.session_state.graph_person = selected_next
                st.rerun()

            profile_resp = api_get(f"/person/{st.session_state.graph_person}")
            if profile_resp["ok"] and not profile_resp["data"].get("error"):
                render_profile(profile_resp["data"])


# -----------------------------
# ASK AI
# -----------------------------
elif page == "Ask AI":
    st.subheader("🤖 Ask AI")

    examples = [
        "Who are the grandparents of Rohan Sharma?",
        "Who are the parents of Kavita Sharma?",
        "Who are the siblings of Asha Sharma?",
        "Who are the first cousins of Rohan Sharma?",
        "Who are the second cousins of Rohan Sharma?",
        "How many family members are over the age of 50?",
        "How many males vs. females are there in my family?",
        "How many unmarried family members over age 21?",
        "How is Asha Sharma related to Rohan Sharma?",
    ]

    example = st.selectbox("Quick example", ["Custom"] + examples)
    default_q = "Who are the grandparents of Rohan Sharma?" if example == "Custom" else example
    question = st.text_area("Enter your question", value=default_q, height=120)

    if st.button("Ask AI", use_container_width=True):
        resp = api_get("/ask", params={"q": question})
        if not resp["ok"]:
            st.error(resp["error"])
        else:
            data = resp["data"]
            left, right = st.columns([1, 1])

            with left:
                st.markdown('<div class="result-box">', unsafe_allow_html=True)
                st.write("**Answer**")
                if "answer" in data:
                    render_chip_list(data["answer"])
                elif "relationship" in data:
                    st.success(data["relationship"])
                else:
                    st.json(data)
                st.markdown("</div>", unsafe_allow_html=True)

            with right:
                st.markdown('<div class="result-box">', unsafe_allow_html=True)
                st.write("**Raw response**")
                st.json(data)
                st.markdown("</div>", unsafe_allow_html=True)


# -----------------------------
# COMPARE PEOPLE
# -----------------------------
elif page == "Compare People":
    st.subheader("🔗 Compare People")

    left, right = st.columns(2)
    with left:
        person1 = st.text_input("First person", value="Asha Sharma")
    with right:
        person2 = st.text_input("Second person", value="Rohan Sharma")

    if st.button("Find Relationship", use_container_width=True):
        resp = api_get(f"/relationship/{person1}/{person2}")
        if not resp["ok"]:
            st.error(resp["error"])
        else:
            data = resp["data"]
            st.markdown('<div class="result-box">', unsafe_allow_html=True)
            st.success(data.get("relationship", "No result"))
            st.json(data)
            st.markdown("</div>", unsafe_allow_html=True)


# -----------------------------
# API HEALTH CHECK
# -----------------------------
elif page == "API Health Check":
    st.subheader("🩺 API Health Check")

    c1, c2 = st.columns(2)
    with c1:
        home_resp = api_get("/")
        st.markdown('<div class="result-box">', unsafe_allow_html=True)
        st.write("**Root Endpoint**")
        if home_resp["ok"]:
            st.success("Backend root reachable")
            st.json(home_resp["data"])
        else:
            st.error(home_resp["error"])
        st.markdown("</div>", unsafe_allow_html=True)

    with c2:
        stats_resp = api_get("/stats")
        st.markdown('<div class="result-box">', unsafe_allow_html=True)
        st.write("**Stats Endpoint**")
        if stats_resp["ok"]:
            st.success("Stats endpoint reachable")
            st.json(stats_resp["data"])
        else:
            st.error(stats_resp["error"])
        st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<div class='footer-note'>Built with Streamlit + FastAPI + FalkorDB</div>", unsafe_allow_html=True)