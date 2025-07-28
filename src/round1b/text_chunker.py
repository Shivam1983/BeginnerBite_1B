import fitz
from src.round1a_deps.pdf_parser import parse_spans

def get_sections_from_outline(pdf_path, outline_json):
    """
    Uses the Round 1A outline to define sections and their text content.
    """
    doc = fitz.open(pdf_path)
    sections = []

    all_spans = parse_spans(pdf_path)

    def find_span_index(target_text, target_page):
        for idx, span in enumerate(all_spans):
            if span['text'].strip() == target_text.strip() and span['page'] == target_page:
                return idx
        return -1

    for i, entry in enumerate(outline_json['outline']):
        section_title = entry['text']
        section_page = entry['page']

        start_span_idx = find_span_index(section_title, section_page)
        if start_span_idx == -1:
            continue

        end_span_idx = len(all_spans)
        if i + 1 < len(outline_json['outline']):
            next_entry = outline_json['outline'][i+1]
            next_title = next_entry['text']
            next_page = next_entry['page']
            end_span_idx = find_span_index(next_title, next_page)
            if end_span_idx == -1:
                end_span_idx = len(all_spans)

        section_content_spans = all_spans[start_span_idx : end_span_idx]
        section_text = " ".join([s['text'] for s in section_content_spans]).strip()

        sections.append({
            "title": section_title,
            "page": section_page,
            "text_content": section_text,
            "start_span_idx": start_span_idx,
            "end_span_idx": end_span_idx
        })

    if not sections and doc.page_count > 0:
        print(f"Warning: No outline found for {pdf_path}. Falling back to a single section.")
        full_text = "".join(page.get_text("text") for page in doc)
        sections.append({
            "title": "Full Document Content",
            "page": 1,
            "text_content": full_text.strip(),
            "start_span_idx": 0,
            "end_span_idx": len(all_spans)
        })

    return sections