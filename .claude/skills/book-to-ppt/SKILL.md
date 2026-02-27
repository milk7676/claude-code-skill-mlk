---
name: book-to-ppt
description: Automated workflow to convert PDF books into PowerPoint presentations using real NotebookLM integration. Use when you need to: (1) Extract and split PDF books by chapters (Chinese/English), (2) Upload chapters to NotebookLM and generate PPT outlines, (3) Create presentations with iSlide plugin, (4) Merge chapter presentations into complete book presentation. Requires Windows + PowerPoint + NotebookLM skill + optional iSlide plugin.
---

# Book to PPT with NotebookLM

Convert PDF books into complete PowerPoint presentations using real NotebookLM for outline generation.

## Quick Start

```bash
# Complete workflow (requires NotebookLM notebook URL)
python scripts/workflow.py path/to/book.pdf --notebook-url "https://notebooklm.google.com/notebook/..."

# With custom output directory
python scripts/workflow.py book.pdf --notebook-url "URL" --output-dir ./my_output

# Without iSlide (use basic themes)
python scripts/workflow.py book.pdf --notebook-url "URL" --no-islide
```

## Workflow

```
PDF Book → Split by Chapters → Extract Markdown → Upload to NotebookLM (Manual) → Generate Outlines (NotebookLM) → Create PPTs (iSlide) → Merge into Complete Presentation
```

## Prerequisites

### 1. NotebookLM Setup

Install and configure the NotebookLM skill:

```bash
cd ~/.claude/skills/notebooklm
python scripts/run.py auth_manager.py setup  # One-time setup
python scripts/run.py auth_manager.py status  # Check authentication
```

Create a NotebookLM notebook and save its URL.

### 2. Python Dependencies

```bash
pip install pdfplumber PyPDF2 python-pptx pywin32
```

### 3. Optional: iSlide Plugin

Install from https://www.islide.cc/ for enhanced PPT styling.

## Usage

### Complete Workflow

Single command to process entire book:

```bash
python scripts/workflow.py book.pdf \
  --notebook-url "https://notebooklm.google.com/notebook/..." \
  --output-dir ./output
```

**Process:**

1. **Split PDF** - Automatic chapter detection and splitting
2. **Upload to NotebookLM** - Manual upload of markdown files (pauses for you)
3. **Generate Outlines** - Automatic via NotebookLM API
4. **Create PPTs** - Automatic using iSlide (if installed)
5. **Merge PPTs** - Automatic final assembly

### Individual Steps

#### Step 1: Split PDF

```bash
python scripts/pdf_splitter.py book.pdf --output-dir ./chapters
```

Creates:
- Chapter PDFs
- Markdown files

#### Step 2: Upload to NotebookLM

**Manual:**
1. Open your Notebook in browser
2. Click "Add source" → "Upload"
3. Upload all `.md` files from `chapters/` directory

#### Step 3: Generate Outlines

```bash
python scripts/notebooklm_client.py \
  chapters/*.md \
  --output-dir ./outlines \
  --notebook-url "https://notebooklm.google.com/notebook/..."
```

**Now uses real NotebookLM** via the `/notebooklm` skill integration.

#### Step 4: Generate PPTs

```bash
python scripts/ppt_generator.py ./outlines --output-dir ./presentations
```

Creates individual PPT files from outlines.

#### Step 5: Merge PPTs

```bash
python scripts/ppt_merger.py presentations/*.pptx --output complete_book.pptx
```

Combines all chapters into single presentation.

## Script Reference

| Script | Purpose |
|--------|---------|
| `workflow.py` | Complete end-to-end workflow with NotebookLM |
| `pdf_splitter.py` | PDF chapter detection and splitting |
| `notebooklm_client.py` | **NotebookLM integration** (calls notebooklm skill) |
| `ppt_generator.py` | PPT creation with iSlide |
| `ppt_merger.py` | Merge multiple PPTs |

## NotebookLM Integration

The skill integrates with the `/notebooklm` skill to generate outlines:

1. **Subprocess calls** - Invokes `notebooklm/scripts/ask_question.py`
2. **JSON extraction** - Parses NotebookLM response for outline JSON
3. **Error handling** - Falls back to basic structure if JSON parsing fails

**Prompt Template:**
```
Based on the chapter content, generate a PowerPoint outline in JSON format.
Requirements:
- 3-5 slides for main content
- 1 introduction slide
- 1 conclusion slide
- JSON structure: {title, subtitle, slides: [{title, content, notes}]}
```

Edit `scripts/notebooklm_client.py` to customize the prompt.

## Chapter Detection

Supports common Chinese and English chapter patterns:

**Chinese**: 第X章、X、第X节
**English**: Chapter X, Part X, X. Title

See [references/chapter_patterns.md](references/chapter_patterns.md) for customization.

## Troubleshooting

### NotebookLM Issues

**Not authenticated:**
```bash
cd ~/.claude/skills/notebooklm
python scripts/run.py auth_manager.py setup
```

**Connection timeout:** Check internet connection, retry query

**Invalid JSON response:** Script falls back to basic structure

### PDF Processing

**No chapters detected:** Check PDF text quality or add custom patterns

**Poor OCR quality:** Use OCR preprocessing or manual chapter specification

### PowerPoint Issues

**PowerPoint not opening:** Run as Administrator, verify installation

**iSlide not working:** Use `--no-islide` flag or install plugin

See [references/troubleshooting.md](references/troubleshooting.md) for detailed solutions.

## Output Structure

```
output/
├── chapters/           # Chapter PDFs and Markdown
├── outlines/           # PPT outline JSON files
├── presentations/      # Individual chapter PPTs
└── book_complete.pptx  # Final merged presentation
```

## Advanced Usage

### Custom NotebookLM Prompt

Edit `scripts/notebooklm_client.py`:

```python
def generate_outline_prompt(self, chapter_content: str, chapter_title: str = "") -> str:
    prompt = f"""Your custom prompt here...

    {chapter_content[:8000]}
    """
    return prompt
```

### Batch Processing

```bash
for book in books/*.pdf; do
  python scripts/workflow.py "$book" \
    --notebook-url "https://notebooklm.google.com/notebook/..." \
    --output-dir "./output/$(basename $book .pdf)"
done
```

## References

- [Integration Guide](references/notebooklm_integration_guide.md) - Complete integration documentation
- [Chapter Patterns](references/chapter_patterns.md) - Chapter detection patterns
- [PPT Styles](references/ppt_styles.md) - PPT styling guide
- [Troubleshooting](references/troubleshooting.md) - Common issues and solutions

## Version

**2.0** - Now with real NotebookLM integration (requires /notebooklm skill)
