from sentence_transformers import SentenceTransformer, util
import os

MODEL_PATH = "models/sentence_transformer_model/"

_model = None

def load_relevance_model():
    """
    Loads the pre-trained Sentence-Transformer model from the local directory.
    """
    global _model
    if _model is None:
        try:
            _model = SentenceTransformer(MODEL_PATH)
            print(f"Relevance model loaded from {MODEL_PATH}")
        except Exception as e:
            print(f"Error loading Sentence-Transformer model: {e}")
            print(f"Please ensure a model is downloaded and placed in the '{MODEL_PATH}' directory.")
            exit(1)
    return _model

def get_embeddings(texts):
    """
    Generates embeddings for a list of texts using the loaded model.
    """
    model = load_relevance_model()
    embeddings = model.encode(texts, convert_to_tensor=True, device='cpu')
    return embeddings

def calculate_similarity(embedding1, embedding2):
    """
    Calculates cosine similarity between two embeddings.
    """
    return util.cos_sim(embedding1.unsqueeze(0), embedding2.unsqueeze(0)).item()