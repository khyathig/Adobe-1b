import numpy as np
import json
import time
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

class RelevanceScorer:
    def __init__(self, model_name='all-MiniLM-L6-v2'):
        """
        Initializes the scorer with a pre-trained SentenceTransformer model.

        Args:
            model_name (str): Name of the Hugging Face model to use.
                              Consider 'all-mpnet-base-v2' or
                              'multi-qa-MiniLM-L6-cos-v1' for improved results.
        """
        print(f"🔍 Loading sentence transformer model: {model_name}...")
        self.model = SentenceTransformer(model_name)
        print("✅ Model loaded.")

    def create_query_string(self, persona_role, job_task):
        """
        Combines persona and task into a single query string.

        Args:
            persona_role (str): Description of the persona or role.
            job_task (str): The job or task to be done.

        Returns:
            str: Combined query string.
        """
        return f"Persona: {persona_role}. Task: {job_task}"

    def score_relevance(self, query_text, doc_chunks_dict):
        """
        Scores relevance of document chunks against a query.

        Args:
            query_text (str): Combined persona and task string.
            doc_chunks_dict (dict): { filename: [{page, text, title}], ... }

        Returns:
            list[dict]: List of scored chunks with metadata and similarity score,
                        sorted by score in descending order.
        """
        print("🧠 Encoding query...")
        start_time = time.time()
        query_embedding = self.model.encode([query_text])
        print(f"✅ Query encoded in {time.time() - start_time:.2f}s.")

        scored_subsections = []
        all_texts = []
        metadata_list = []

        print("📄 Preparing document chunks for encoding...")
        for filename, chunks in doc_chunks_dict.items():
            for chunk in chunks:
                text = chunk['text']
                all_texts.append(text)
                metadata_list.append({
                    'document': filename,
                    'page_number': max(1, chunk.get('page_number', 1)),  # ✅ FIXED HERE
                    'section_title': chunk.get('title', 'N/A'),
                    'subsection_title': chunk.get('title', 'N/A'),
                    'refined_text': text
                })


        print(f"🧾 Encoding {len(all_texts)} document chunks...")
        start_time = time.time()
        doc_embeddings = self.model.encode(all_texts)
        print(f"✅ Document embeddings computed in {time.time() - start_time:.2f}s.")

        print("📊 Calculating cosine similarities...")
        start_time = time.time()
        similarities = cosine_similarity(query_embedding, doc_embeddings)[0]

        for i, score in enumerate(similarities):
            entry = metadata_list[i].copy()
            entry['similarity_score'] = float(score)
            scored_subsections.append(entry)

        scored_subsections.sort(key=lambda x: x['similarity_score'], reverse=True)
        print(f"✅ Scoring completed in {time.time() - start_time:.2f}s.")
        return scored_subsections


# Run independently for testing
if __name__ == "__main__":
    scorer = RelevanceScorer()
    query = scorer.create_query_string(
        "Event Manager", "Find venues and catering options for a corporate event."
    )

    dummy_docs = {
        "event_guide.pdf": [
            {"page": 1, "text": "Introduction to corporate event planning.", "title": "Intro"},
            {"page": 2, "text": "Top venues in New York with capacity over 500.", "title": "Venues"}
        ],
        "services.pdf": [
            {"page": 3, "text": "Recommended catering services for large-scale events.", "title": "Catering"},
            {"page": 5, "text": "How to negotiate event contracts.", "title": "Contracts"}
        ]
    }

    results = scorer.score_relevance(query, dummy_docs)
    print(json.dumps(results, indent=2))
