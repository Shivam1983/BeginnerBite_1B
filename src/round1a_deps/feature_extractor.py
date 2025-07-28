import re
import numpy as np

def extract_features(spans, median_body):
    rows = []
    for s in spans:
        t = s["text"]
        fsize = s["font_size"]
        flags = s["flags"]
        rows.append([
            fsize,
            int(bool(flags & 2)), # Check for bold flag (bit 2)
            len(t.split()),
            sum(1 for c in t if c.isupper())/max(len(t),1),
            bool(re.match(r"^\d+\.\d+", t)), # Checks for numerical prefixes like "1.1", "2.3"
            fsize/median_body if median_body else 1 # Relative font size
        ])
    return np.array(rows)