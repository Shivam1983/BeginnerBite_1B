import os
import time
from datetime import datetime
import joblib
from src.utils.file_io import write_json, read_json_input
from src.round1a_deps.heading_detector import _clf as r1a_clf, _median_body as r1a_median_body
from src.round1a_deps.pdf_parser import parse_spans
from src.round1a_deps.feature_extractor import extract_features
from src.round1b.text_chunker import get_sections_from_outline
from src.round1b.relevance_model import get_embeddings, calculate_similarity
from src.round1b.train_round1b_ranker import is_instruction_text # NEW: Import the feature function

try:
    _relevance_ranker = joblib.load("models/relevance_ranker.joblib")
    print("Custom relevance ranker model loaded.")
except FileNotFoundError:
    print("Error: models/relevance_ranker.joblib not found. Please train the Round 1B model first.")
    exit(1)


def analyze_documents_batch(input_json_path, pdf_input_dir, output_filename):
    start_time = time.time()
    os.makedirs(os.path.dirname(output_filename), exist_ok=True)

    input_data = read_json_input(input_json_path)
    
    documents_with_titles = input_data.get("documents", [])
    input_documents_list = [d['filename'] for d in documents_with_titles]

    persona = input_data.get("persona", {})
    job_to_be_done = input_data.get("job_to_be_done", {})

    persona_role = persona.get("role", "N/A")
    job_task = job_to_be_done.get("task", "N/A")
    combined_query = f"Persona: {persona_role}. Task: {job_task}"
    
    query_embedding = get_embeddings([combined_query])[0]

    all_sections_with_scores = []
    all_sub_sections_with_scores = []

    for doc_filename in input_documents_list:
        pdf_path = os.path.join(pdf_input_dir, doc_filename)
        if not os.path.exists(pdf_path):
            print(f"Warning: Document '{doc_filename}' not found at '{pdf_path}'. Skipping.")
            continue

        print(f"Processing document: {doc_filename}")

        spans_for_r1a = parse_spans(pdf_path)
        X_for_r1a = extract_features(spans_for_r1a, r1a_median_body)
        preds_for_r1a = r1a_clf.predict(X_for_r1a)
        
        r1a_outline_list = []
        for i, p_r1a in enumerate(preds_for_r1a):
            if p_r1a > 0:
                s_r1a = spans_for_r1a[i]
                r1a_outline_list.append({
                    "level": f"H{p_r1a}",
                    "text": s_r1a["text"],
                    "page": s_r1a["page"]
                })
        
        r1a_outline_dict = {"outline": r1a_outline_list}
        
        sections_data = get_sections_from_outline(pdf_path, r1a_outline_dict)
        
        for section in sections_data:
            section_title = section['title']
            section_text_content = section['text_content']
            section_page = section['page']

            section_embedding = get_embeddings([section_title + " " + section_text_content])[0]
            
            similarity_score = calculate_similarity(query_embedding, section_embedding)
            
            # --- NEW FEATURE: Add the instruction flag to the feature vector ---
            is_instruction = is_instruction_text(section_title + " " + section_text_content)
            relevance_feature_vector = [[similarity_score, is_instruction] + query_embedding.tolist() + section_embedding.tolist()]
            # ------------------------------------------------------------------

            relevance_score = _relevance_ranker.predict_proba(relevance_feature_vector)[0][1]

            all_sections_with_scores.append({
                "document": doc_filename,
                "page_number": section_page,
                "section_title": section_title,
                "importance_rank": relevance_score
            })

            sub_chunks = section_text_content.split('\n\n')
            
            for sub_chunk_text in sub_chunks:
                sub_chunk_text = sub_chunk_text.strip()
                if not sub_chunk_text: continue

                sub_chunk_embedding = get_embeddings([sub_chunk_text])[0]
                
                sub_similarity_score = calculate_similarity(query_embedding, sub_chunk_embedding)
                
                # --- NEW FEATURE: Add the instruction flag to the sub-section feature vector ---
                is_instruction_sub = is_instruction_text(sub_chunk_text)
                sub_relevance_feature_vector = [[sub_similarity_score, is_instruction_sub] + query_embedding.tolist() + sub_chunk_embedding.tolist()]
                # -----------------------------------------------------------------------------

                sub_chunk_relevance = _relevance_ranker.predict_proba(sub_relevance_feature_vector)[0][1]

                all_sub_sections_with_scores.append({
                    "document": doc_filename,
                    "refined_text": sub_chunk_text,
                    "page_number": section_page,
                    "relevance_score": sub_chunk_relevance
                })
    
    all_sections_with_scores.sort(key=lambda x: x['importance_rank'], reverse=True)
    all_sub_sections_with_scores.sort(key=lambda x: x['relevance_score'], reverse=True)
    
    extracted_sections_final = all_sections_with_scores[:9]
    sub_section_analysis_final = all_sub_sections_with_scores[:9]
    
    for i, section in enumerate(extracted_sections_final):
        section['importance_rank'] = i + 1
        
    for sub_section in sub_section_analysis_final:
        del sub_section['relevance_score']

    end_time = time.time()
    processing_timestamp = datetime.now().isoformat()

    final_output = {
        "metadata": {
            "input_documents": [d['filename'] for d in documents_with_titles],
            "persona": persona,
            "job_to_be_done": job_to_be_done,
            "processing_timestamp": processing_timestamp
        },
        "extracted_sections": extracted_sections_final,
        "sub_section_analysis": sub_section_analysis_final
    }

    write_json(final_output, output_filename)