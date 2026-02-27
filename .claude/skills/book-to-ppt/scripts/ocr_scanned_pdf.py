"""
OCR Processing Script for Scanned PDFs
Uses document-skills/pdf OCR implementation
"""
import sys
from pathlib import Path
import json

# Set UTF-8 encoding
sys.stdout.reconfigure(encoding='utf-8')

def check_tesseract():
    """Check if Tesseract OCR is installed"""
    import shutil
    tesseract_path = shutil.which('tesseract')

    if tesseract_path:
        print(f"✓ Tesseract found at: {tesseract_path}")
        return True
    else:
        print("✗ Tesseract OCR not found!")
        print("\nPlease install Tesseract OCR:")
        print("1. Download: https://github.com/UB-Mannheim/tesseract/wiki")
        print("2. Install: tesseract-ocr-w64-setup-5.x.x.exe")
        print("3. IMPORTANT: Select 'Chinese (Simplified)' language pack")
        print("4. Add to PATH: C:\\Program Files\\Tesseract-OCR")
        return False

def ocr_pdf_pages(pdf_path, output_dir, max_pages=None):
    """
    OCR PDF pages and save as text files

    Args:
        pdf_path: Path to PDF file
        output_dir: Output directory for text files
        max_pages: Maximum pages to process (None = all)
    """
    try:
        from pdf2image import convert_from_path
        import pytesseract
    except ImportError as e:
        print(f"Error: {e}")
        print("\nPlease install: pip install pytesseract pdf2image pillow")
        return False

    pdf_path = Path(pdf_path)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"\n{'='*60}")
    print(f"OCR Processing: {pdf_path.name}")
    print(f"{'='*60}\n")

    # Convert PDF to images
    print("Converting PDF to images...")
    try:
        images = convert_from_path(
            pdf_path,
            dpi=300,  # Higher DPI for better OCR
            first_page=1,
            last_page=max_pages
        )
    except Exception as e:
        print(f"Error converting PDF: {e}")
        print("\nNOTE: pdf2image requires poppler to be installed.")
        print("Download from: http://blog.alivate.com.au/poppler-windows/")
        return False

    print(f"✓ Converted {len(images)} pages\n")

    # Process each page
    results = []

    for i, image in enumerate(images, 1):
        print(f"[{i}/{len(images)}] OCR processing...", end=' ')

        try:
            # OCR with Chinese and English
            text = pytesseract.image_to_string(
                image,
                lang='chi_sim+eng',
                config='--psm 6'
            )

            # Save individual page
            txt_file = output_dir / f"page_{i:03d}.txt"
            with open(txt_file, 'w', encoding='utf-8') as f:
                f.write(text)

            results.append({
                'page': i,
                'file': str(txt_file),
                'chars': len(text)
            })

            print(f"✓ {len(text)} chars")

        except Exception as e:
            print(f"✗ Error: {e}")

    # Save summary
    summary_file = output_dir / "ocr_summary.json"
    with open(summary_file, 'w', encoding='utf-8') as f:
        json.dump({
            'pdf': str(pdf_path),
            'total_pages': len(images),
            'processed': len(results),
            'results': results
        }, f, indent=2, ensure_ascii=False)

    # Combine all text
    combined_file = output_dir / "full_text.txt"
    with open(combined_file, 'w', encoding='utf-8') as f:
        for i in range(1, len(images) + 1):
            txt_file = output_dir / f"page_{i:03d}.txt"
            if txt_file.exists():
                with open(txt_file, 'r', encoding='utf-8') as page:
                    f.write(f"\n{'='*60}\n")
                    f.write(f"Page {i}\n")
                    f.write(f"{'='*60}\n")
                    f.write(page.read())

    print(f"\n{'='*60}")
    print(f"✓ OCR Complete!")
    print(f"{'='*60}")
    print(f"Output directory: {output_dir}")
    print(f"  - Individual pages: page_*.txt ({len(results)} files)")
    print(f"  - Combined text: full_text.txt")
    print(f"  - Summary: ocr_summary.json")

    return True

def main():
    import argparse

    parser = argparse.ArgumentParser(
        description='OCR processing for scanned PDFs'
    )
    parser.add_argument('pdf', help='Path to scanned PDF')
    parser.add_argument('--output', default='./ocr_output',
                       help='Output directory')
    parser.add_argument('--max-pages', type=int,
                       help='Maximum pages to process (for testing)')

    args = parser.parse_args()

    # Check Tesseract
    if not check_tesseract():
        return 1

    # Process PDF
    success = ocr_pdf_pages(
        args.pdf,
        args.output,
        args.max_pages
    )

    return 0 if success else 1

if __name__ == '__main__':
    sys.exit(main())
