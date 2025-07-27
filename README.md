
# Doc-Insight: Persona-Aware PDF Outline Generator

**Doc-Insight** is a lightweight tool built for Round 1B of the DocHackathon 2025, focused on extracting structured insights from a collection of related documents. It understands a specific user persona and job-to-be-done, and generates a ranked outline of relevant sections and subsections from multiple PDFs.

---

## Problem Statement

Given a set of related PDF documents, along with:
- A defined persona (e.g., Researcher, Travel Planner, Analyst)
- A concrete job-to-be-done (e.g., summarize reports, plan a trip)

The task is to identify and extract the most relevant parts of the documents—structured as ranked sections and refined subsections—based on semantic relevance to the user’s goal.

---

## What the Tool Does

- Parses and processes PDF documents using PyMuPDF
- Extracts section titles using visual and textual cues
- Scores and ranks sections using Sentence Transformers (offline-compatible)
- Extracts and refines top subsections from selected sections
- Outputs a structured `JSON` file with metadata, extracted sections, and granular analysis

---

## Folder Structure

```

.
├── src/
│   ├── main.py
│   ├── output\_generator.py
│   ├── pdf\_processor.py
│   └── relevance\_scorer.py
├── config.py
├── .dockerignore
├── .gitignore
├── Dockerfile
├── README.md
├── requirements.txt
├── input/
│   ├── config.json
│   └── \*.pdf
└── output/
└── challenge1b\_output.json

````

---
## Sample Input (`input/config.json`)

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

-----

## Sample Output (`output/challenge1b_output.json`)

```json
{
  "metadata": {
    "input_documents": [],
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

-----

## How to Run with Docker

### Step 1: Build the Docker image

```bash
docker build -t doc-insight .
```

### Step 2: Run the container

```bash
docker run --rm \
  -v "$(pwd)/input:/app/input" \
  -v "$(pwd)/output:/app/output" \
  doc-insight
```

Make sure `config.json` and the required PDFs are present in the `input/` folder.

-----

## Technical Stack

  * Python 3.9
  * PyMuPDF (for PDF parsing and layout-based section detection)
  * Sentence Transformers (for semantic ranking)
  * Cosine similarity (for scoring relevance)
  * Works offline, under CPU and memory constraints

-----

## Authors

This project was developed by:

  * Dedeepya Sindu Bellamkonda ([LinkedIn](https://www.linkedin.com/in/dedeepya200/))
  * Khyati Gutta ([LinkedIn](https://www.linkedin.com/in/khyathigutta/))

If you're reviewing this as part of the hackathon, thank you for your time. We're happy to walk through the approach or collaborate further.

-----

## Extensions and Ideas

This setup is modular and can be extended into:

  * A web UI using Streamlit or Gradio
  * Integration with Notion or Google Docs
  * REST API for batch processing
  * Fine-tuning for domain-specific personas (e.g., Legal, Healthcare, Research)
