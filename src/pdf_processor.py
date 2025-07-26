import os
import json
from PyPDF2 import PdfReader

def extract_text_simple(pdf_path):
    """
    Simple text extraction from PDF. Returns a list of dictionaries,
    one for each page, containing page_number and text.
    """
    text_chunks = []
    try:
        reader = PdfReader(pdf_path)
        for page_num, page in enumerate(reader.pages, start=1):
            try:
                text = page.extract_text()
                if text and text.strip():
                    text_chunks.append({
                        'page_number': max(1, page_num),  # ✅ use page_number, not page
                        'text': text.strip(),
                        'title': f"Page {page_num}"
                    })
            except Exception as e:
                print(f"⚠️ Skipping unreadable page {page_num} in {pdf_path}: {e}")
    except Exception as e:
        print(f"❌ Error processing {pdf_path}: {e}")
    return text_chunks

def process_documents(input_dir, docs_info):
    """
    Processes all documents listed in the input JSON.
    Returns a dictionary mapping filename to its extracted text chunks.
    Assumes PDFs are directly inside input_dir.
    """
    all_doc_chunks = {}

    if not os.path.exists(input_dir):
        print(f"⚠️ Warning: Input directory not found: {input_dir}")
        return all_doc_chunks

    for doc_info in docs_info:
        filename = doc_info.get('filename')
        if not filename:
            print("⚠️ Skipping document with missing filename.")
            continue

        pdf_path = os.path.join(input_dir, filename)
        if os.path.exists(pdf_path):
            print(f"📄 Processing {filename}...")
            chunks = extract_text_simple(pdf_path)
            all_doc_chunks[filename] = chunks
        else:
            print(f"⚠️ Warning: PDF file not found: {pdf_path}")
    return all_doc_chunks

# Test this module independently
if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        input_dir = sys.argv[1]
        input_json_path = os.path.join(input_dir, 'input.json')

        if os.path.exists(input_json_path):
            with open(input_json_path, 'r') as f:
                input_data = json.load(f)
            chunks_dict = process_documents(input_dir, input_data.get('documents', []))
            print(json.dumps(chunks_dict, indent=2))
        else:
            print("❌ input.json not found in the specified directory.")
    else:
        print("❗ Provide input directory as argument for testing.")
