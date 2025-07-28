import sys
import os
import warnings
warnings.simplefilter(action="ignore" , category=FutureWarning)

# DEFENSIVE FIX: Manually add the project root to the Python path.
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.join(current_dir)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

import click
from src.round1b.document_analyzer import analyze_documents_batch

@click.command()
@click.argument("sample_path", type=click.Path(exists=True, file_okay=False, dir_okay=True))
@click.argument("output_dir", type=click.Path(file_okay=False, dir_okay=True))
def main(sample_path, output_dir):
    """
    Main entry point for the Round 1B Persona-Driven Document Intelligence solution.
    
    SAMPLE_PATH: Path to the sample directory containing the input JSON and PDFs (e.g., data/input_pdfs/sample1).
    OUTPUT_DIR: Path to the output directory for the final JSON result.
    """
    input_json_path = os.path.join(sample_path, "round1b_inputs.json")
    pdf_input_dir = sample_path
    
    # Construct a unique output filename based on the sample name
    sample_name = os.path.basename(os.path.normpath(sample_path))
    output_filename = os.path.join(output_dir, f"{sample_name}_output.json")

    print(f"Starting persona-driven document analysis for sample '{sample_path}'...")
    analyze_documents_batch(input_json_path, pdf_input_dir, output_filename)
    print(f"Round 1B analysis completed. Output saved to {output_filename}")

if __name__ == "__main__":
    main()

