"""
PDF Book Splitter - Identify chapters and split into individual files
Supports Chinese and English books
"""

import re
from pathlib import Path
from typing import List, Tuple, Optional
import pdfplumber
from PyPDF2 import PdfReader, PdfWriter


class ChapterPattern:
    """Chapter detection patterns for Chinese and English"""

    # Chinese patterns
    CN_PATTERNS = [
        r'^第[一二三四五六七八九十百千零\d]+章\s*',  # 第X章
        r'^第[一二三四五六七八九十百千零\d]+节\s*',  # 第X节
        r'^[一二三四五六七八九十百千零\d]+[、\s]\s*',  # 一、 二、
        r'^Chapter\s*\d+',  # Mixed Chinese with English
    ]

    # English patterns
    EN_PATTERNS = [
        r'^Chapter\s+\d+',  # Chapter 1
        r'^CHAPTER\s+\d+',  # CHAPTER 1
        r'^Part\s+\d+',  # Part 1
        r'^Section\s+\d+',  # Section 1
        r'^\d+\.\s+[A-Z]',  # 1. Title
    ]

    @classmethod
    def is_chapter_title(cls, text: str) -> bool:
        """Check if text matches chapter patterns"""
        text = text.strip()

        # Try Chinese patterns
        for pattern in cls.CN_PATTERNS:
            if re.match(pattern, text, re.MULTILINE):
                return True

        # Try English patterns
        for pattern in cls.EN_PATTERNS:
            if re.match(pattern, text, re.IGNORECASE | re.MULTILINE):
                return True

        return False


class PDFSplitter:
    """Split PDF book by chapters"""

    def __init__(self, pdf_path: str, output_dir: str = "./chapters"):
        self.pdf_path = Path(pdf_path)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def extract_text_from_page(self, pdf_reader: PdfReader, page_num: int) -> str:
        """Extract text from specific page"""
        page = pdf_reader.pages[page_num]
        return page.extract_text() or ""

    def find_chapter_pages(self, pdf_path: Path) -> List[Tuple[int, str]]:
        """
        Find all chapter start pages
        Returns: List of (page_number, chapter_title)
        """
        chapter_pages = []

        with pdfplumber.open(pdf_path) as pdf:
            for i, page in enumerate(pdf.pages):
                text = page.extract_text() or ""

                # Check each line for chapter pattern
                for line in text.split('\n'):
                    if ChapterPattern.is_chapter_title(line):
                        chapter_pages.append((i, line.strip()))
                        break

        return chapter_pages

    def split_by_chapters(self) -> List[Path]:
        """
        Split PDF into chapter files
        Returns: List of paths to chapter PDFs
        """
        pdf_reader = PdfReader(str(self.pdf_path))
        total_pages = len(pdf_reader.pages)

        # Find chapter start pages
        chapter_pages = self.find_chapter_pages(self.pdf_path)

        if not chapter_pages:
            print("No chapters detected, treating entire PDF as one chapter")
            chapter_pages = [(0, "Full_Content")]

        # Add end page for last chapter
        chapter_pages.append((total_pages, "END"))

        chapter_files = []

        # Split PDF
        for i in range(len(chapter_pages) - 1):
            start_page, title = chapter_pages[i]
            end_page = chapter_pages[i + 1][0]

            # Create clean filename
            safe_title = re.sub(r'[<>:"/\\|?*]', '_', title)
            safe_title = re.sub(r'\s+', '_', safe_title)[:50]
            output_path = self.output_dir / f"{i+1:02d}_{safe_title}.pdf"

            # Write chapter PDF
            writer = PdfWriter()
            for page_num in range(start_page, end_page):
                writer.add_page(pdf_reader.pages[page_num])

            with open(output_path, 'wb') as f:
                writer.write(f)

            chapter_files.append(output_path)
            print(f"Created: {output_path.name}")

        return chapter_files

    def extract_markdown(self, chapter_pdf: Path) -> Path:
        """Extract chapter content as Markdown"""
        output_md = chapter_pdf.with_suffix('.md')

        with pdfplumber.open(chapter_pdf) as pdf:
            with open(output_md, 'w', encoding='utf-8') as f:
                for page in pdf.pages:
                    text = page.extract_text() or ""
                    f.write(text + '\n\n')

        return output_md


def main():
    import argparse

    parser = argparse.ArgumentParser(description='Split PDF book by chapters')
    parser.add_argument('pdf_path', help='Path to PDF book')
    parser.add_argument('--output-dir', default='./chapters', help='Output directory')

    args = parser.parse_args()

    splitter = PDFSplitter(args.pdf_path, args.output_dir)
    chapter_files = splitter.split_by_chapters()

    # Extract markdown for each chapter
    for chapter_pdf in chapter_files:
        md_path = splitter.extract_markdown(chapter_pdf)
        print(f"Extracted: {md_path.name}")


if __name__ == '__main__':
    main()
