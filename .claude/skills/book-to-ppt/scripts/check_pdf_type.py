"""
Check if PDF is scanned or has extractable text
"""
import pdfplumber
from pathlib import Path

pdf_path = Path(r"C:\Users\Administrator\Documents\（已压缩）人比AI凶—万维刚(1).pdf")
output_file = Path(r"C:\Users\Administrator\Documents\pdf_type_check.txt")

with open(output_file, 'w', encoding='utf-8') as f:
    f.write("PDF Type Check\n")
    f.write("=" * 60 + "\n\n")

    with pdfplumber.open(pdf_path) as pdf:
        f.write(f"Total pages: {len(pdf.pages)}\n\n")

        # Check various pages
        test_pages = [0, 50, 100, 200, 300, 416]

        text_pages = 0
        image_pages = 0

        for page_num in test_pages:
            if page_num >= len(pdf.pages):
                continue

            page = pdf.pages[page_num]
            text = page.extract_text() or ""

            f.write(f"\n--- Page {page_num + 1} ---\n")
            f.write(f"Text length: {len(text)} characters\n")

            if text.strip():
                f.write(f"Has extractable text: YES\n")
                f.write(f"Preview: {text[:200]}\n")
                text_pages += 1
            else:
                f.write(f"Has extractable text: NO (likely image/scanned)\n")
                image_pages += 1

        f.write("\n" + "=" * 60 + "\n")
        f.write(f"Summary:\n")
        f.write(f"  Pages with text: {text_pages}\n")
        f.write(f"  Pages likely scanned: {image_pages}\n\n")

        # Check if this is a scanned PDF
        if text_pages == 0:
            f.write("CONCLUSION: This appears to be a SCANNED PDF.\n")
            f.write("OCR (Optical Character Recognition) is needed.\n")
        elif text_pages < image_pages:
            f.write("CONCLUSION: This PDF appears to be MIXED (some scanned pages).\n")
            f.write("OCR may be needed for some pages.\n")
        else:
            f.write("CONCLUSION: This PDF has extractable text.\n")

print(f"Check saved to: {output_file}")
