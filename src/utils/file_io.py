import json
import os
import pandas as pd

def read_annotations():
    """This is a placeholder as R1B does not use annotations.csv directly."""
    pass

def write_json(data, output_path):
    """
    Writes a dictionary to a JSON file.
    Ensures the output directory exists before writing.
    """
    # Defensive check: Ensure output_path is a file path, not a directory.
    # This check is crucial to prevent the PermissionError.
    if os.path.isdir(output_path):
        print(f"Error: Cannot write file to a directory. Got: '{output_path}'")
        exit(1)
    
    # Ensure the directory for the output file exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def read_json_input(input_json_path):
    """
    Reads a JSON file containing persona, job_to_be-done, and input_documents.
    """
    if not os.path.exists(input_json_path):
        print(f"Error: Input JSON file not found at {input_json_path}")
        exit(1)
    try:
        with open(input_json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from {input_json_path}: {e}")
        exit(1)
    except Exception as e:
        print(f"Error reading input JSON file {input_json_path}: {e}")
        exit(1)