# Approach Explanation

Our approach for this challenge is a modular Python pipeline designed to analyze a collection of documents, understand a user's intent, and extract the most relevant information. The system is built to be generic, handling diverse documents and personas, and adheres strictly to the offline, CPU-only execution constraints. The architecture is divided into three main stages: Document Processing, Relevance Scoring, and Output Generation.

***

### **1. Pipeline Orchestration and Input**

The entire process is managed by a main pipeline script. We've designed the system to accept all necessary information for a test case through a single `input.json` file. This file defines the **document collection**, the **persona**, and the **job-to-be-done** , which allows our solution to remain generic as required. This orchestrator is responsible for passing data between the different modules in a clean and sequential manner.

***

### **2. Document Processing and Text Extraction**

The first logical step in our pipeline is to ingest the provided PDF documents. We use the `PyPDF2` library for its lightweight and reliable text extraction capabilities, which require no external dependencies or network calls. The `pdf_processor` module reads each PDF specified in the `input.json`, extracts text content on a page-by-page basis, and structures it into chunks. Each chunk contains the text, the source document's filename, and the page number, preparing the content for the next stage.

***

### **3. Core Logic: Semantic Relevance Scoring**

The intelligence of our system lies in the `relevance_scorer` module. This module determines how relevant each text chunk is to the user's goal.

* **Query Formulation**: We create a single, context-rich query string by combining the `persona` description and the `job_to_be_done` task. This gives the model a clear understanding of what to look for.

* **Semantic Model**: We use the `sentence-transformers` library with the `'all-MiniLM-L6-v2'` model. This model is powerful enough for nuanced semantic understanding but small and efficient enough to meet the model size and execution time constraints on a CPU.

* **Scoring and Ranking**: The model converts both the query and all document chunks into numerical vector embeddings. We then calculate the **cosine similarity** between the query embedding and each chunk embedding. The resulting score represents how semantically similar the text is to the user's need. Finally, all chunks are sorted by this score in descending order, ensuring the most relevant results are ranked highest, directly addressing the core scoring criteria.

***

### **4. Output Generation**

The final module, `output_generator`, takes the sorted list of relevant chunks and formats it into the required `output.json` file. It constructs the `metadata`, `extracted_sections`, and `subsection_analysis` fields, populating them with the top-ranked results and adding an `importance_rank` to each entry. This ensures our output is well-structured and directly usable.

[cite_start]The final module, `output_generator`, takes the sorted list of relevant chunks and formats it into the required `output.json` file[cite: 38]. It constructs the `metadata`, `extracted_sections`, and `subsection_analysis` fields, populating them with the top-ranked results and adding an `importance_rank` to each entry. This ensures our output is well-structured and directly usable.
