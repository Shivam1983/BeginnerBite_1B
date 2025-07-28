import os
import joblib
import pandas as pd
import re # NEW: Import re for regex
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from src.utils.file_io import read_json_input
from src.round1b.relevance_model import get_embeddings

# NEW: Function to check for instruction-like patterns
def is_instruction_text(text):
    text_lower = text.lower()
    if text_lower.startswith("instructions:") or text_lower.startswith("conclusion") or text_lower.startswith("ingredients:"):
        return 1
    # Check for text that is very short and ends with a colon
    if len(text.split()) < 5 and text.strip().endswith(":"):
        return 1
    return 0


def main():
    print("Loading labeled training data for Round 1B ranking model...")
    training_data_path = "data/round1b_relevance_data.json"
    if not os.path.exists(training_data_path):
        print(f"Error: Training data not found at {training_data_path}. Please create a labeled dataset.")
        exit(1)
    
    data = read_json_input(training_data_path)
    df = pd.DataFrame(data)

    if df.empty:
        print("Error: The training data file is empty. Please add examples.")
        exit(1)
    
    print("Generating embeddings for queries and sections...")
    unique_queries = df['query'].unique()
    unique_sections = df['section_text'].unique()

    # Get embeddings for all unique queries and sections
    query_embeddings_map = {q: get_embeddings([q])[0] for q in unique_queries}
    section_embeddings_map = {s: get_embeddings([s])[0] for s in unique_sections}

    features = []
    labels = []

    print("Building a rich feature vector for training...")
    for _, row in df.iterrows():
        query_emb = query_embeddings_map[row['query']]
        section_emb = section_embeddings_map[row['section_text']]
        
        # Calculate cosine similarity
        similarity_score = (query_emb * section_emb).sum().item()
        
        # --- NEW FEATURE: Check if the section text is a generic instruction
        is_instruction = is_instruction_text(row['section_text'])
        # -----------------------------------------------------------------

        # Combine rich features:
        # 1. Cosine similarity score
        # 2. The new is_instruction feature
        # 3. Raw embeddings of the query and section
        feature_vector = [similarity_score, is_instruction] + query_emb.tolist() + section_emb.tolist()
        
        features.append(feature_vector)
        labels.append(row['label'])

    X = pd.DataFrame(features)
    y = pd.Series(labels)

    X_train, X_val, y_train, y_val = train_test_split(
        X, y, stratify=y, test_size=0.2, random_state=42)
    
    print("Training a RandomForestClassifier on the rich features...")
    clf = RandomForestClassifier(n_estimators=50, random_state=42)
    clf.fit(X_train, y_train)

    print("\nModel performance on validation set:")
    print(classification_report(y_val, clf.predict(X_val), digits=3))

    os.makedirs("models", exist_ok=True)
    joblib.dump(clf, "models/relevance_ranker.joblib")
    print("\nCustom relevance ranker model saved → models/relevance_ranker.joblib")

if __name__ == "__main__":
    main()