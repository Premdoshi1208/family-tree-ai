# 👨‍👩‍👧 AI-Powered Family Tree Browser

An interactive family tree system built using **FalkorDB (RedisGraph)**, **FastAPI**, **Streamlit**, and **Plotly**, enhanced with **LLM-powered querying (Groq)**.

---

## 🚀 Overview

This project allows users to:

- Store family members and relationships in a **graph database**
- Visually explore relationships using an **interactive graph**
- Query relationships using **natural language (AI-powered)**
- Analyze connections dynamically through a **backend API**

---

## 🧠 Key Features

### 📊 Graph Database (FalkorDB)
- Stores people as nodes and relationships as edges
- Supports queries like parent, sibling, etc.

### 🎨 Interactive Visualization (Plotly)
- Dynamic graph rendering
- Zoom, pan, and explore relationships

### ⚡ Backend API (FastAPI)
- REST APIs for querying relationships
- Handles graph queries and logic

### 💻 Frontend UI (Streamlit)
- Clean dashboard for exploring family data
- Sections like:
  - Explore People
  - Graph Browser
  - Ask AI
  - Compare People

### 🤖 AI Querying (Groq LLM)
- Ask questions like:
  - “Who is my cousin?”
  - “How is A related to B?”
- Converts natural language → graph queries

---

## 🛠️ Tech Stack

- Python
- FalkorDB (RedisGraph)
- FastAPI
- Streamlit
- Plotly
- NetworkX
- Groq (LLM API)

---

## ⚙️ Setup Instructions

### 1️⃣ Clone the repository
```bash
git clone https://github.com/Premdoshi1208/family-tree-ai.git
cd family-tree-ai
