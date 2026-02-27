"""
Quick PDF inspection to find chapter structure
"""
import pdfplumber
from pathlib import Path
import re
import sys

# Set UTF-8 encoding for output
sys.stdout.reconfigure(encoding='utf-8')

pdf_path = Path(r"C:\Users\Administrator\Documents\（已压缩）人比AI凶—万维刚(1).pdf")

output_file = Path(r"C:\Users\Administrator\Documents\pdf_inspection.txt")

with open(output_file, 'w', encoding='utf-8') as f:
    f.write("=" * 60 + "\n")
    f.write("PDF Inspection: 人比AI凶—万维刚\n")
    f.write("=" * 60 + "\n\n")

    with pdfplumber.open(pdf_path) as pdf:
        f.write(f"Total pages: {len(pdf.pages)}\n\n")

        f.write("Looking for chapter patterns...\n\n")

        # Check first 50 pages for chapter patterns
        for i, page in enumerate(pdf.pages[:50]):
            text = page.extract_text() or ""

            if not text.strip():
                continue

            lines = text.split('\n')

            # Check each line for potential chapter titles
            for line in lines:
                line = line.strip()
                if not line:
                    continue

                # Look for chapter-like patterns
                # Check if line is short (likely a title)
                if len(line) < 60 and len(line) > 2:
                    # Check for chapter keywords
                    chapter_keywords = ['第', '章', 'Chapter', 'Part', '章节', '篇']
                    if any(keyword in line for keyword in chapter_keywords):
                        f.write(f"Page {i+1:3d}: {line}\n")

                    # Check for numbered patterns like "1.", "一、"
                    if re.match(r'^[一二三四五六七八九十\d]+[\.\、、]', line):
                        f.write(f"Page {i+1:3d}: {line}\n")

    f.write("\n" + "=" * 60 + "\n")
    f.write("Sample text from first 10 pages:\n")
    f.write("=" * 60 + "\n\n")

    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages[:10]):
            text = page.extract_text() or ""
            if text.strip():
                f.write(f"\n--- Page {i+1} ---\n")
                f.write(text[:500] + "...\n")

print(f"Inspection saved to: {output_file}")
print("Please check the file for chapter patterns.")
