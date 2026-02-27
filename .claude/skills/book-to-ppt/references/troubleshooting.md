# Troubleshooting Guide

## PDF Processing Issues

### No Chapters Detected

**Symptom**: Script reports "No chapters detected"

**Solutions**:
1. Check PDF text extraction quality
   ```python
   # Test text extraction
   import pdfplumber
   with pdfplumber.open('book.pdf') as pdf:
       for i, page in enumerate(pdf.pages[:5]):
           print(f"Page {i}:\n{page.extract_text()[:500]}\n")
   ```

2. Add custom patterns for your book
   - Edit `pdf_splitter.py`
   - Add patterns to `ChapterPattern.CN_PATTERNS` or `EN_PATTERNS`

3. Manual chapter specification
   ```python
   # Specify page numbers manually
   chapter_pages = [(0, "Introduction"), (10, "Chapter 1"), ...]
   ```

### Poor PDF Quality (Scanned Documents)

**Symptom**: Extracted text is garbled or missing

**Solutions**:
1. Use OCR preprocessing
   ```bash
   # Install OCR tools
   pip install pytesseract pillow

   # Preprocess PDF with OCR
   ocrmypdf input.pdf output_ocr.pdf
   ```

2. Use image-based PDF extraction
   ```python
   # Extract images from PDF
   from pdf2image import convert_from_path
   images = convert_from_path('scanned.pdf')
   ```

## NotebookLM Integration Issues

### Browser Automation Failures

**Symptom**: Cannot connect to NotebookLM

**Solutions**:
1. Check Playwright installation
   ```bash
   playwright install chromium
   ```

2. Manual login process
   - Run script once with `headless=False`
   - Login to NotebookLM manually
   - Browser profile will be saved for future runs

3. Alternative: Manual upload workflow
   ```python
   # Skip automation, generate file list
   python scripts/pdf_splitter.py book.pdf --output-dir ./chapters

   # Manually upload generated files to NotebookLM
   # Then use generated outlines
   ```

### API Not Available

**Symptom**: NotebookLM has no official API

**Workarounds**:
1. Use browser automation (playwright)
2. Manual copy-paste workflow
3. Alternative services:
   - Claude API
   - OpenAI API
   - Local LLM (Ollama, LLaMA)

## PowerPoint Automation Issues

### PowerPoint Not Opening

**Symptom**: "Cannot create PowerPoint application"

**Solutions**:
1. Ensure PowerPoint is installed
   ```python
   import win32com.client
   try:
       ppt = win32com.client.Dispatch("PowerPoint.Application")
       print("PowerPoint available")
   except:
       print("Install PowerPoint")
   ```

2. Run as Administrator
   - Right-click → Run as administrator

3. Check Windows version
   - Requires Windows 10/11
   - PowerPoint 2016 or later

### iSlide Plugin Not Found

**Symptom**: "Could not apply iSlide theme"

**Solutions**:
1. Verify iSlide installation
   - Open PowerPoint
   - Check Ribbon for "iSlide" tab
   - Reinstall if missing

2. Disable iSlide (use basic themes)
   ```bash
   python scripts/workflow.py book.pdf --no-islide
   ```

3. Use custom template
   ```python
   # Create template manually
   # Then use as base for new presentations
   template_path = "assets/default_template.pptx"
   presentation = Presentation(template_path)
   ```

### Memory Issues (Large Presentations)

**Symptom**: Script crashes with many slides

**Solutions**:
1. Process in batches
   ```python
   # Process 10 chapters at a time
   batch_size = 10
   for i in range(0, len(chapters), batch_size):
       batch = chapters[i:i+batch_size]
       process_batch(batch)
   ```

2. Close PowerPoint between steps
   ```python
   # Explicitly close and reopen
   ppt.Quit()
   ppt = None
   ppt = win32com.client.Dispatch("PowerPoint.Application")
   ```

## General Issues

### Import Errors

**Symptom**: "ModuleNotFoundError: No module named 'X'"

**Solution**: Install dependencies
```bash
pip install pdfplumber PyPDF2 python-pptx pywin32 playwright
playwright install chromium
```

### Encoding Issues (Chinese Text)

**Symptom**: "UnicodeDecodeError" or garbled text

**Solutions**:
1. Specify UTF-8 encoding
   ```python
   with open(path, 'r', encoding='utf-8') as f:
       content = f.read()
   ```

2. Use system encoding fallback
   ```python
   import locale
   encoding = locale.getpreferredencoding()
   ```

3. Set environment variable
   ```bash
   set PYTHONIOENCODING=utf-8
   ```

### File Path Issues (Windows)

**Symptom**: "FileNotFoundError" or path errors

**Solutions**:
1. Use raw strings for paths
   ```python
   path = r"C:\Users\Name\file.pdf"
   ```

2. Use pathlib (recommended)
   ```python
   from pathlib import Path
   path = Path("C:/Users/Name/file.pdf")
   ```

3. Escape backslashes
   ```python
   path = "C:\\Users\\Name\\file.pdf"
   ```