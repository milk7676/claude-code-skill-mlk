"""
Process Scanned PDF - Find best approach
"""
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

pdf_path = Path(r"C:\Users\Administrator\Documents\（已压缩）人比AI凶—万维刚(1).pdf")
output_dir = Path(r"C:\Users\Administrator\Documents\pdf_processing")
output_dir.mkdir(parents=True, exist_ok=True)

print("\n" + "="*60)
print("开始处理扫描版PDF")
print("="*60)
print(f"\n文件: {pdf_path.name}")
print(f"输出目录: {output_dir}")

# Step 1: Check if there's any text at all
print("\n步骤 1/5: 检查PDF文字层...")
print("-"*60)

import pdfplumber

text_found = False
sample_pages = [0, 100, 200, 300, 400]

with pdfplumber.open(pdf_path) as pdf:
    print(f"总页数: {len(pdf.pages)}\n")

    for page_num in sample_pages:
        if page_num >= len(pdf.pages):
            continue
        page = pdf.pages[page_num]
        text = page.extract_text() or ""

        status = "有文字" if text.strip() else "无文字"
        print(f"  第{page_num+1}页: {status} ({len(text)} 字符)")

        if text.strip():
            text_found = True
            # Save sample
            sample_file = output_dir / f"page_{page_num+1}_sample.txt"
            with open(sample_file, 'w', encoding='utf-8') as f:
                f.write(f"Page {page_num+1}\n{text}")

if text_found:
    print("\n✓ 发现文字层！可以直接提取")
else:
    print("\n✗ 确认是扫描版PDF，需要OCR")

# Step 2: Try different approaches
print("\n步骤 2/5: 分析处理方案...")
print("-"*60)

if text_found:
    print("方案A: 直接提取文字（推荐）")
    print("方案B: 使用pdfplumber完整提取")
else:
    print("方案A: OCR处理（需要Tesseract）")
    print("方案B: 在线OCR服务")
    print("方案C: 手动指定章节页码")

# Step 3: Extract what we can
print("\n步骤 3/5: 提取可用内容...")
print("-"*60)

all_text = []
with pdfplumber.open(pdf_path) as pdf:
    total = len(pdf.pages)
    for i, page in enumerate(pdf.pages):
        if (i + 1) % 50 == 0 or i == 0:
            print(f"  处理中: {i+1}/{total} 页")
        text = page.extract_text() or ""
        all_text.append({
            'page': i + 1,
            'text': text,
            'has_text': bool(text.strip())
        })

# Save results
import json
results_file = output_dir / "analysis_results.json"
with open(results_file, 'w', encoding='utf-8') as f:
    json.dump({
        'pdf': str(pdf_path),
        'total_pages': len(all_text),
        'pages_with_text': sum(1 for p in all_text if p['has_text']),
        'pages_without_text': sum(1 for p in all_text if not p['has_text']),
        'pages': all_text[:10]  # First 10 pages as sample
    }, f, ensure_ascii=False, indent=2)

print(f"\n✓ 分析结果已保存: {results_file}")

# Step 4: Try to find chapter structure
print("\n步骤 4/5: 查找章节结构...")
print("-"*60)

import re

potential_chapters = []
for page_data in all_text[:100]:  # Check first 100 pages
    text = page_data['text']
    lines = text.split('\n')

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # Look for chapter patterns
        if any(keyword in line for keyword in ['第', '章', 'Chapter', 'Part']):
            if len(line) < 50:  # Likely a title
                potential_chapters.append({
                    'page': page_data['page'],
                    'title': line
                })

if potential_chapters:
    print(f"\n✓ 发现 {len(potential_chapters)} 个可能的章节标题:")
    for i, ch in enumerate(potential_chapters[:10], 1):
        print(f"  {i}. 第{ch['page']}页: {ch['title']}")
else:
    print("\n未找到明显的章节标记")

# Step 5: Recommendations
print("\n步骤 5/5: 处理建议...")
print("-"*60)

pages_with_text = sum(1 for p in all_text if p['has_text'])
total = len(all_text)
ratio = pages_with_text / total * 100

print(f"\n文字覆盖率: {ratio:.1f}% ({pages_with_text}/{total} 页)")

if ratio > 80:
    print("\n✓ 推荐: 直接提取文字，然后处理")
    next_step = "extract_text"
elif ratio > 20:
    print("\n⚠ 部分页面有文字，建议:")
    print("  1. 提取有文字的页面")
    print("  2. OCR 处理无文字的页面")
    next_step = "hybrid"
else:
    print("\n✗ 大部分是扫描版，需要完整OCR")
    print("\n选项:")
    print("  A. 安装Tesseract进行OCR（1-2小时）")
    print("  B. 使用在线OCR服务（10-30分钟）")
    print("  C. 手动提供章节页码（5分钟，最快）")
    next_step = "ocr_needed"

print("\n" + "="*60)
print("分析完成！")
print("="*60)

# Save recommendation
rec_file = output_dir / "recommendation.txt"
with open(rec_file, 'w', encoding='utf-8') as f:
    f.write(f"PDF分析结果\n")
    f.write(f"{'='*60}\n\n")
    f.write(f"文件: {pdf_path.name}\n")
    f.write(f"总页数: {total}\n")
    f.write(f"有文字页数: {pages_with_text}\n")
    f.write(f"文字覆盖率: {ratio:.1f}%\n\n")
    f.write(f"建议处理方式: {next_step}\n\n")

    if potential_chapters:
        f.write(f"发现的章节标题:\n")
        for ch in potential_chapters[:20]:
            f.write(f"  第{ch['page']}页: {ch['title']}\n")

print(f"\n建议已保存: {rec_file}")
print(f"\n所有输出文件在: {output_dir}")
