

```markdown
# 🧠 Doc-Insight: Intelligent PDF Outline Generator

> 🚀 Built for Round 1B of the DocHackathon – “Connecting the Dots Through Docs”  
> 🧑‍💼 Persona-aware, job-focused section extraction powered by Sentence Transformers and PyMuPDF.

---

## 📌 Problem Statement

You’re handed a collection of related PDFs and a specific **persona** with a **job to accomplish**.  
The goal is to generate a structured, ranked **outline of relevant sections** and **granular subsections** tailored to that persona’s task.

---

## 🧠 What This Project Does

- ✅ Understands persona and job-to-be-done
- ✅ Analyzes PDF content using semantic embeddings
- ✅ Ranks and extracts top sections and subsections
- ✅ Outputs clean JSON for downstream use

---

## 🏗️ Folder Structure

```

challenge1b/
├── Dockerfile
├── requirements.txt
├── main.py
├── document\_processor.py
├── section\_extractor.py
├── relevance\_scorer.py
├── input/
│   ├── config.json
│   └── \*.pdf
└── output/
└── challenge1b\_output.json

````

---

## 📥 Sample Input (`input/config.json`)

```json
{
  "persona": {
    "role": "Travel Planner"
  },
  "job_to_be_done": {
    "task": "Plan a trip of 4 days for a group of 10 college friends."
  },
  "documents": [
    { "filename": "South of France - Cuisine.pdf" },
    { "filename": "South of France - Cities.pdf" }
  ]
}
````

---

## 📤 Sample Output (`output/challenge1b_output.json`)

```json
{
  "metadata": {
    "input_documents": [...],
    "persona": "Travel Planner",
    "job_to_be_done": "Plan a trip of 4 days for a group of 10 college friends.",
    "processing_timestamp": "2025-07-26T18:52:33.456Z"
  },
  "extracted_sections": [
    {
      "document": "South of France - Things to Do.pdf",
      "section_title": "Coastal Adventures",
      "importance_rank": 1,
      "page_number": 2
    }
  ],
  "subsection_analysis": [
    {
      "document": "South of France - Things to Do.pdf",
      "refined_text": "Beach hopping, scuba diving, sailing routes...",
      "page_number": 2
    }
  ]
}
```

---

## 🐳 Run With Docker

### 🧱 Step 1: Build the image

```bash
docker build -t doc-insight .
```

### 🚀 Step 2: Run the container

```bash
docker run --rm \
  -v "$(pwd)/input:/app/input" \
  -v "$(pwd)/output:/app/output" \
  doc-insight
```

---

## ⚙️ Tech Stack

* **PyMuPDF** – fast PDF parsing + heading detection
* **Sentence Transformers** – semantic scoring of sections
* **Cosine Similarity** – for relevance ranking
* **Offline-Ready** – no internet required, CPU-only

---

## 👩‍💻 Built By
* **Dedeepya Sindu Bellamkonda**
* **Khyati Gutta**

We’re passionate about making documents more intelligent and usable.

🔗 [Dedeepya’s LinkedIn](https://www.linkedin.com/in/dedeepya200/)
🔗 [Khyati’s LinkedIn](https://www.linkedin.com/in/khyathigutta/) 

---

## 🏁 Ready to Scale

This repo can be extended into:

* 🖥️ A UI (Streamlit or Gradio)
* 🧠 A Notion/Google Docs export system
* 🌐 A REST API for bulk doc analysis

Ping us if you're interested!





