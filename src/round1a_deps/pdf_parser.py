import fitz # PyMuPDF

def parse_spans(pdf_path):
    spans = []
    doc = fitz.open(pdf_path)
    for page in doc:
        pno = page.number + 1 # Convert to 1-indexed page number
        for block in page.get_text("dict")["blocks"]:
            for line in block.get("lines", []):
                for span in line["spans"]:
                    text = span["text"].strip()
                    if not text: continue # Skip empty spans
                    spans.append({
                        "pdf_file": pdf_path,
                        "page": pno,
                        "text": text,
                        "font_size": span["size"],
                        "x0": span["bbox"][0], # X-coordinate of left edge
                        "y0": span["bbox"][1], # Y-coordinate of top edge
                        "flags": span["flags"] # Font flags (e.g., bold, italic)
                    })
    return spans