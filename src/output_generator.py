import json
import os
from datetime import datetime

def generate_output(input_data, scored_subsections, top_sections=10, top_subsections=15):
    """
    Generate the final structured output JSON.

    Args:
        input_data (dict): Original input data (from input.json).
        scored_subsections (list): Scored chunks from relevance model.
        top_sections (int): Number of top sections to include.
        top_subsections (int): Number of top subsections to include.

    Returns:
        dict: Output dictionary with metadata, extracted sections, and subsection analysis.
    """
    # --- Metadata ---
    metadata = {
        "input_documents": input_data.get("documents", []),
        "persona": input_data.get("persona", {}),
        "job_to_be_done": input_data.get("job_to_be_done", {}),
        "processing_timestamp": datetime.utcnow().isoformat() + "Z"
    }

    # --- Extracted Sections ---
    sections = []
    for i, subsection in enumerate(scored_subsections[:top_sections]):
        sections.append({
            "document": subsection.get("document", ""),
            "page_number": subsection.get("page_number", -1),  # 🔧 FIXED
            "section_title": subsection.get("chunk_title") or f"Chunk on Page {subsection.get('page_number', 'N/A')}",
            "importance_rank": i + 1
        })

    # --- Subsection Analysis ---
    subsections = []
    for i, subsection in enumerate(scored_subsections[:top_subsections]):
        raw_text = subsection.get("refined_text", "")
        refined_excerpt = raw_text[:500] + ("..." if len(raw_text) > 500 else "")

        subsections.append({
            "document": subsection.get("document", ""),
            "page_number": subsection.get("page_number", -1),  # 🔧 FIXED
            "subsection_title": subsection.get("subsection_title") or f"Content on Page {subsection.get('page_number', 'N/A')}",
            "refined_text": refined_excerpt,
            "importance_rank": i + 1
        })

    return {
        "metadata": metadata,
        "extracted_sections": sections,
        "subsection_analysis": subsections
    }

def save_output(output_data, output_dir):
    """
    Save the output JSON to a file named output.json in the specified directory.

    Args:
        output_data (dict): Structured output dictionary.
        output_dir (str): Path to the output directory.
    """
    os.makedirs(output_dir, exist_ok=True)
    output_file_path = os.path.join(output_dir, 'output.json')
    with open(output_file_path, 'w') as f:
        json.dump(output_data, f, indent=4)
    print(f"✅ Output saved to {output_file_path}")


# --- Test Mode ---
if __name__ == "__main__":
    dummy_input = {
        "challenge_info": {"test_case_name": "test"},
        "documents": [{"filename": "doc1.pdf"}],
        "persona": {"role": "Tester"},
        "job_to_be_done": {"task": "Test the output generator"}
    }

    dummy_scored = [
        {
            "document": "doc1.pdf",
            "page_number": 1,
            "chunk_title": "Introduction",
            "subsection_title": "Introduction",
            "refined_text": "This is the introduction text which is quite long and needs to be refined to show only the most relevant part.",
            "similarity_score": 0.9
        },
        {
            "document": "doc1.pdf",
            "page_number": 2,
            "chunk_title": "Body",
            "subsection_title": "Main Body",
            "refined_text": "Body content here.",
            "similarity_score": 0.8
        }
    ]

    result = generate_output(dummy_input, dummy_scored)
    print(json.dumps(result, indent=2))
