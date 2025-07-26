import os
import sys
import json
import time
# Import our modules
from pdf_processor import process_documents
from relevance_scorer import RelevanceScorer
from output_generator import generate_output, save_output

def run_pipeline(input_dir, output_dir):
    """
    Main pipeline orchestrator.
    """
    start_time = time.time()
    print("--- Starting 1B Pipeline ---")

    # --- 1. Load Input ---
    input_json_path = os.path.join(input_dir, 'input.json')
    if not os.path.exists(input_json_path):
        print(f"Error: input.json not found at {input_json_path}")
        sys.exit(1)

    with open(input_json_path, 'r') as f:
        input_data = json.load(f)
    print(f"Loaded input for test case: {input_data.get('challenge_info', {}).get('test_case_name', 'Unknown')}")

    # --- 2. Process Documents ---
    print("Step 1: Processing PDF documents...")
    doc_chunks_dict = process_documents(input_dir, input_data.get('documents', []))
    if not doc_chunks_dict:
         print("Warning: No document chunks were extracted.")
    total_chunks = sum(len(chunks) for chunks in doc_chunks_dict.values())
    print(f"Extracted {total_chunks} text chunks from documents.")

    # --- 3. Score Relevance ---
    print("Step 2: Scoring relevance...")
    scorer = RelevanceScorer(model_name='all-MiniLM-L6-v2')  # You can change the model name here
    persona_role = input_data.get('persona', {}).get('role', '')
    job_task = input_data.get('job_to_be_done', {}).get('task', '')
    query_text = scorer.create_query_string(persona_role, job_task)
    print(f"Query: {query_text}")

    if not doc_chunks_dict:
         scored_subsections = []
    else:
         scored_subsections = scorer.score_relevance(query_text, doc_chunks_dict)
    print(f"Scored {len(scored_subsections)} subsections.")

    # --- 4. Generate & Save Output ---
    print("Step 3: Generating output...")
    final_output = generate_output(input_data, scored_subsections)
    save_output(final_output, output_dir)
    print(f"Pipeline completed in {time.time() - start_time:.2f} seconds.")
    print("--- Pipeline Finished ---")


if __name__ == "__main__":
    # Expect input and output paths from command line or default
    # When run via Docker, these will be /app/input and /app/output
    default_input_dir = os.path.join(os.path.dirname(__file__), '..', 'data', 'input')   # <== changed
    default_output_dir = os.path.join(os.path.dirname(__file__), '..', 'data', 'output') # <== changed

    # Check for command line arguments (for Docker)
    if len(sys.argv) > 2:
         input_dir = sys.argv[1]
         output_dir = sys.argv[2]
    else:
         print("Using default local paths for testing.")
         input_dir = default_input_dir
         output_dir = default_output_dir

    print(f"Input Directory: {input_dir}")
    print(f"Output Directory: {output_dir}")

    if not os.path.exists(input_dir):
         print(f"Error: Input directory does not exist: {input_dir}")
         sys.exit(1)

    run_pipeline(input_dir, output_dir)
