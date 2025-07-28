from sentence_transformers import SentenceTransformer

# Specify a lightweight model that fits the < 1GB constraint
model_name = 'all-MiniLM-L6-v2' 
model = SentenceTransformer(model_name)

# This command saves the model files to your project directory
# Note: Replace 'Challenge_1B' with the actual path if it's different
model.save_pretrained('./models/sentence_transformer_model/')