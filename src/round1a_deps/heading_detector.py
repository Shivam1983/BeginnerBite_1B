# import joblib, os
# from .pdf_parser import parse_spans
# from .feature_extractor import extract_features
# from src.utils.file_io import write_json

# # Load the trained model and median_body font size
# _data = joblib.load("models/heading_model.joblib")
# _clf, _median_body = _data["model"], _data["median_body"]

# def extract_outline_batch(input_dir, output_dir):
#     os.makedirs(output_dir, exist_ok=True)
#     for f in os.listdir(input_dir):
#         if f.lower().endswith(".pdf"):
#             in_p = os.path.join(input_dir, f)
#             spans = parse_spans(in_p)
#             X = extract_features(spans, _median_body)
#             preds = _clf.predict(X)





#             # Initialize variables for continuous text aggregation
#             combined_outline = []
#             current_level = None
#             current_text = ""
#             current_page = None

#             # Iterate through predictions and spans to aggregate
#             for i, p in enumerate(preds):
#                 s = spans[i]
#                 text = s["text"].strip() # Ensure text is stripped here too
#                 page = s["page"]

#                 if p == -1: # Handle Title separately, if found. It's usually a single line.
#                     # This span is a title, it's handled separately later, so we skip it for outline aggregation.
#                     continue

#                 if p > 0:  # This is a heading (H1, H2, H3, etc.)
#                     # Check if it's a continuation of the previous heading
#                     if current_level == p and current_page == page:
#                         # Same heading level and on the same page, combine text
#                         current_text += " " + text
#                     else:
#                         # New heading or different level/page, save previous if it exists
#                         if current_level is not None:
#                             combined_outline.append({
#                                 "level": f"H{current_level}",
#                                 "text": current_text.strip(),
#                                 "page": current_page
#                             })
#                         # Start new heading aggregation
#                         current_level = p
#                         current_text = text
#                         current_page = page
#                 else: # This is body text (label 0) or unclassified, not part of the outline
#                     if current_level is not None:
#                         # A heading sequence ended, save it
#                         combined_outline.append({
#                             "level": f"H{current_level}",
#                             "text": current_text.strip(),
#                             "page": current_page
#                         })
#                         current_level = None
#                         current_text = ""
#                         current_page = None

#             # After loop, add any remaining aggregated heading (if the document ends with a heading)
#             if current_level is not None:
#                 combined_outline.append({
#                     "level": f"H{current_level}",
#                     "text": current_text.strip(),
#                     "page": current_page
#                 })

#             # Re-extract title: Find the first occurrence of label -1
#             # combine all spans with label -1 as the title
#             title = " ".join(s["text"] for s, p in zip(spans, preds) if p == -1)
#             # If no -1 found, default to filename
#             title = next((s["text"] for s, p in zip(spans, preds) if p == -1), os.path.basename(in_p))

#             # Construct the output JSON structure
#             output_data = {
#                 "title": title,
#                 "outline": combined_outline # Use the combined_outline here
#             }

#             # Save the JSON output
#             write_json(output_data, os.path.join(output_dir, f[:-4]+".json"))






import joblib, os
from .pdf_parser import parse_spans
from .feature_extractor import extract_features

# Load the trained model and median_body font size
_data = joblib.load("models/heading_model.joblib")
_clf, _median_body = _data["model"], _data["median_body"]