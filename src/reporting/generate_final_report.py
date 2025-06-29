# src/reporting/generate_final_report.py

from markdown_pdf import MarkdownPdf, Section
import os

# --- Configuration ---
DOCS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'docs'))
REPORT_MD_FILE = os.path.join(DOCS_DIR, "report.md")
OUTPUT_PDF = "Quantoro_Assignment_Report.pdf"


def main():
    """Converts the main project report.md file into a PDF."""
    print(f"--- Generating Final PDF Report from {REPORT_MD_FILE} ---")

    if not os.path.exists(REPORT_MD_FILE):
        print(f"Error: Report file not found at {REPORT_MD_FILE}")
        return

    try:
        # Read the entire markdown file content
        with open(REPORT_MD_FILE, 'r', encoding='utf-8') as f:
            markdown_content = f.read()

        # Create a PDF object with a table of contents
        pdf = MarkdownPdf(toc_level=2)

        # Add the markdown content as a single section
        # The `toc=True` default will generate a TOC based on headers
        pdf.add_section(Section(markdown_content))

        # Save the final PDF to the project root directory
        output_path = os.path.abspath(os.path.join(DOCS_DIR, '..', OUTPUT_PDF))
        pdf.save(output_path)

        print(f"\nSuccessfully generated PDF report: {output_path}")
        print("--- Report Generation Complete ---")

    except Exception as e:
        print(f"An error occurred during PDF generation: {e}")

if __name__ == "__main__":
    main()
