# BeginnerBytes - Persona-Driven PDF Intelligence (Adobe Hackathon 2025)

**Team Name:** beginnerbytes
**Members:** Revanth, Shivam, Ashutosh
**Challenge:** Adobe India Hackathon - Connecting the Dots (Round 1B)

Build a smart document intelligence system that extracts and ranks the most relevant sections/sub-sections from a PDF collection based on a specific persona and job-to-be-done.

---

## 📚 Table of Contents

* [📌 Problem Statement](#-problem-statement)
* [🧠 Key Features](#-key-features)
* [🛠 Tech Stack](#-tech-stack)
* [📁 Project Directory Structure](#-project-directory-structure)
* [🧭 System Architecture](#-system-architecture)
* [⚙ Setup & Installation](#-setup--installation)
* [🏋 Training the Ranker](#-training-the-ranker)
* [🚀 Inference Execution](#-inference-execution)
* [🐳 Docker Usage](#-docker-usage)
* [✅ Constraints & Compliance](#-constraints--compliance)
* [🎯 Contributions](#-contributions)
* [🔮 Future Improvements](#-future-improvements)
* [📬 Contact & Support](#-contact--support)

---

## 📌 Problem Statement

In Round 1B, we were required to build a system that:

1. Takes **3–10 PDF documents** as input
2. Accepts a **persona description** and a **job-to-be-done**
3. **Analyzes and extracts** the most relevant sections & sub-sections from the documents
4. Returns a **ranked JSON output** as follows:

```json
{
  "metadata": {
    "input_documents": [...],
    "persona": "...",
    "job_to_be_done": "...",
    "timestamp": "YYYY-MM-DDThh:mm:ssZ"
  },
  "selected_sections": [
    { "document": "doc1.pdf", "page": 2, "section_title": "Methodology", "importance_rank": 1 }
  ],
  "selected_subsections": [
    { "document": "doc2.pdf", "page": 5, "subsection_title": "Findings", "importance_rank": 1 }
  ]
}
```

---

## 🧠 Key Features

* Reuses structured output from **Round 1A** (outline with headings)
* Uses **semantic embeddings** from `all-MiniLM-L6-v2` (Sentence Transformers)
* Computes **cosine similarity** between query (persona+job) and section embeddings
* Trains a **Random Forest Ranker** on handcrafted relevance data
* Outputs top N sections and sub-sections with `importance_rank`
* Fully **offline**, **Docker-compatible**, and **modular**

---

## 🛠 Tech Stack

* Python 3.10
* Sentence-Transformers
* scikit-learn
* PyMuPDF (fitz)
* Pandas, NumPy, Joblib
* Click (CLI)
* Docker

---

## 📁 Project Directory Structure

```bash
BeginnerBytes_1B/
├── app.py                      # Entrypoint for app execution
├── main.py                     # CLI runner
├── Dockerfile                  # AMD64-compatible Docker config
├── docker-compose.yml          # Optional compose support
├── requirements.txt            # Project dependencies
├── requirements-lite.txt       # Lightweight dependency version
├── .gitignore                  # Ignore virtual env, data, models, etc.
│
├── data/
│   └── round1b_relevance_data.json      # Labeled training data (persona-task-section)
│
├── models/
│   ├── heading_model.joblib            # Round 1A heading detector
│   ├── relevance_ranker.joblib         # Trained section ranker
│   └── sentence_transformer_model/     # all-MiniLM-L6-v2 downloaded locally
│       ├── config.json
│       ├── vocab.txt
│       └── ... (other transformer config files)
│
├── output/
│   ├── sample1_output.json
│   ├── sample2_output.json
│   └── sample3_output.json
│
├── pdfs_input/
│   ├── sample1/
│   ├── sample2/
│   └── sample3/
│
├── processing_data/
│   └── relevance_training_data.json
│
├── scripts/
│   └── sentence_transformer_model.py  # Sentence embedding utilities
│
├── src/
│   ├── round1a_deps/                  # Modules reused from Round 1A
│   └── round1b/
│       ├── document_analyzer.py
│       ├── relevance_model.py
│       ├── text_chunker.py
│       └── train_ranker.py
```

---

## 🧭 System Architecture

```
[Persona + Job] → Query Embedding
       ↓
     [PDFs] → Section Extraction (Round 1A)
       ↓
  Section Chunking
       ↓
  Section Embedding
       ↓
(Embeddings + Cosine Similarity + Level)
       ↓
 RandomForest Ranker
       ↓
 Rank & Filter Top N
       ↓
 Final JSON Output
```

---

## ⚙ Setup & Installation

```bash
git clone <repo_url> && cd BeginnerBytes_1B
python -m venv venv
source venv/bin/activate  # or activate.bat for Windows
pip install -r requirements.txt
```

### Download Sentence Transformer

```bash
from sentence_transformers import SentenceTransformer
SentenceTransformer('all-MiniLM-L6-v2').save_pretrained('models/sentence_transformer_model')
```

---

## 🏋 Training the Ranker

```bash
python src/round1b/train_ranker.py \
  --input data/round1b_relevance_data.json \
  --output models/relevance_ranker.joblib
```

---

## 🚀 Inference Execution

```bash
python src/main.py data/input_pdfs/sample1 output/
```

Repeat for each sample folder (sample2/, sample3/, etc.)

---

## 🐳 Docker Usage

```bash
# Build
docker build --platform linux/amd64 -t beginnerbytes_1b:latest .

# Run
docker run --rm -v "$(pwd):/app" --network none beginnerbytes_1b:latest data/input_pdfs/sample1 output/
```

---

## ✅ Constraints & Compliance

| Requirement          | Our Solution                  |
| -------------------- | ----------------------------- |
| ⏱ Execution Time     | ≤ 60 sec (passes)             |
| 📦 Model Size        | ≤ 1 GB (uses \~200MB)         |
| 🔌 Offline Execution | Enforced via `--network none` |
| ⚙ CPU Only           | Docker AMD64 base image       |

---

## 🎯 Contributions

* Integrated Round 1A output as feature input
* Combined semantic + structural features for ranking
* Modular pipeline with reproducible outputs
* Fully offline Dockerized solution

---

## 🔮 Future Improvements

* Enhance training set diversity for better generalization
* Add visual UI for interacting with results
* Test with scanned PDFs (OCR)
* Adopt transformer-based ranking (e.g., cross-encoders)

---

## 📬 Contact & Support

Reach out to: **[revanthkurapati2004@gmail.com](mailto:revanthkurapati2004@gmail.com)**
If you found this project useful, please **🌟 star** the repository!
