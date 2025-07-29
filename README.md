# BeginnerBytes - PDF Analyzer (Adobe Hackathon 2025)

**Team Name:** beginnerbytes
**Members:** Revanth, Shivam, Ashutosh
**Challenge:** Adobe India Hackathon - Connecting the Dots

Automatically extract hierarchical headings (Title, H1, H2, H3) from raw PDF files and generate structured JSON outlines.

---

## 📚 Table of Contents

* [📁 Directory Structure](#-directory-structure)
* [🔄 Flow Chart](#-flow-chart)
* [🚀 Challenge Overview](#-challenge-overview)
* [👥 Team Details](#-team-details)
* [🧠 Our Approach](#-our-approach)
* [⚙ Setup & Installation](#-setup--installation)
* [🐳 Dockerization](#-dockerization)
* [📤 Output Format](#-output-format)
* [🛠 Tech Stack](#-tech-stack)
* [📬 Contact](#-contact)
* [⭐ Support](#-support)

---

## 📁 Directory Structure

```text
Adobe_hackathon2025/
├── analyze_pdf.py
├── run_project.py
├── install_requirements.py
├── setup.py
├── run_docker.bat
├── run_docker.sh
├── Dockerfile
├── docker-compose.yml
├── .gitignore
├── .dockerignore
├── DOCKER.md
├── DOCKER_COMMANDS.md
├── DOCKER_INSTALL.md
├── README.md
├── NEW_README.md
├── pip.conf
├── requirements.txt
├── requirements-minimal.txt
├── test_imports.py
├── input_pdfs/
├── pdf_analyzer/
│   ├── __init__.py
│   ├── __main__.py
│   ├── cli/
│   ├── config/
│   ├── core/
│   ├── model/
│   └── utils/
├── scripts/
├── src/
└── tests/
```

---

## 🔄 Flow Chart

```text
PDF → Extract spans → Feature vector (x,y,size,bold) → ML Classifier → Heading Level Prediction → JSON Outline
```

---

## 🚀 Challenge Overview

### Round 1B: Persona-Driven Document Intelligence

* Input: 3–10 PDFs + Persona + Job
* Output: Ranked relevant sections and refined subsection content in JSON
* Constraints:

  * Time: ≤ 60 sec
  * Model Size: ≤ 1GB
  * Offline, CPU-only

---

## 👥 Team Details

* **Team Name:** beginnerbytes
* **Members:** Revanth, Shivam, Ashutosh

---

## 🧠 Our Approach

1. **Span Extraction:**

   * For each line of the PDF, we extracted X/Y coordinates, font size, bold flag, and spacing.

2. **Manual Annotation:**

   * Labeled over **2000+** lines with correct heading levels (Title, H1, H2, H3).

3. **Model Training:**

   * Used features to train a lightweight ML classifier (Decision Tree).

4. **Inference:**

   * Trained model is used to predict heading levels for any new PDF.
   * Outputs structured JSON with correct levels and page numbers.

---

## ⚙ Setup & Installation

### Prerequisites

* Python 3.8+
* pip
* Docker (optional)

### Local Setup

```bash
git clone <REPO_URL> && cd Adobe_hackathon2025
python -m venv venv
# Activate virtual environment
# For PowerShell
.\venv\Scripts\Activate.ps1
# For CMD
.\venv\Scripts\activate.bat
pip install --upgrade pip
pip install -r requirements.txt
```

### Training the Model (Optional)

```bash
# Step 1: Generate annotation template
python scripts/export_spans.py

# Step 2: Label the data → save as data/annotations.csv

# Step 3: Train the model
python -m src.main --round train data/input_pdfs output/
```

### Running Inference

```bash
python -m src.main --round 1A data/input_pdfs output/
```

---

## 🐳 Dockerization

### Build Image

```bash
docker build --platform linux/amd64 -t pdf-analyzer .
```

### Run Inference (No Internet)

```bash
docker run --rm -v "${PWD}/data/input_pdfs:/app/input" -v "${PWD}/output:/app/output" --network none pdf-analyzer
```

### Output:

* All PDFs in `/app/input` are processed
* Corresponding `<filename>.json` is written to `/app/output`

---

## 📤 Output Format

```json
{
  "title": "Understanding AI",
  "outline": [
    { "level": "H1", "text": "Introduction", "page": 1 },
    { "level": "H2", "text": "What is AI?", "page": 2 },
    { "level": "H3", "text": "History of AI", "page": 3 }
  ]
}
```

---

## 🛠 Tech Stack

* Python 3.8+
* PyMuPDF (fitz)
* Scikit-learn (Decision Tree)
* Docker

---

## 📬 Contact

For any queries, reach out at: [revanthkurapati56@gmail.com](mailto:revanthkurapati56@gmail.com)

---

## ⭐ Support

If you found this project helpful, please **star** the repo 🙌
