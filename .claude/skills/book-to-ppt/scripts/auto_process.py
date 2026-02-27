"""
完整自动化处理流程 - 从扫描版PDF到PPT
包括下载指导、安装验证、OCR处理、章节识别、PPT生成
"""
import sys
import os
from pathlib import Path
import subprocess

# UTF-8 encoding
sys.stdout.reconfigure(encoding='utf-8')

def print_section(title):
    """Print section header"""
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70 + "\n")

def check_tesseract():
    """Check if Tesseract is installed"""
    print_section("步骤 1/7：检查 Tesseract OCR")

    try:
        result = subprocess.run(
            ['tesseract', '--version'],
            capture_output=True,
            text=True,
            encoding='utf-8'
        )

        if result.returncode == 0:
            print("✓ Tesseract 已安装！")
            print(f"\n版本信息：\n{result.stdout}")
            return True
        else:
            print("✗ Tesseract 未找到")
            return False
    except FileNotFoundError:
        print("✗ Tesseract 未安装")
        return False

def show_download_instructions():
    """Show download and installation instructions"""
    print_section("步骤 2/7：安装 Tesseract OCR")

    print("请按照以下步骤安装 Tesseract OCR：\n")

    print("方法 1：使用镜像下载脚本（推荐）")
    print("-" * 70)
    print("1. 双击运行：C:\\Users\\Administrator\\Documents\\下载Tesseract.bat")
    print("2. 等待下载完成")
    print("3. 运行安装程序")

    print("\n方法 2：浏览器手动下载")
    print("-" * 70)
    print("1. 复制以下地址到浏览器：")
    print("   https://mirrors.tuna.tsinghua.edu.cn/github-release/UB-Mannheim/tesseract/LatestRelease/")
    print("2. 下载文件：tesseract-ocr-w64-setup-5.3.3.20231005.exe")
    print("3. 双击运行安装程序")

    print("\n安装时必须勾选：")
    print("  ✓ Chinese (Simplified) 语言包")
    print("  ✓ Add to PATH（添加到环境变量）")

    print("\n安装路径：")
    print("  默认：C:\\Program Files\\Tesseract-OCR")

    print("\n" + "-" * 70)
    print("\n⏎ 按回车键继续...")
    input()

def test_ocr_first_pages():
    """Test OCR on first few pages"""
    print_section("步骤 3/7：测试 OCR（前 5 页）")

    pdf_path = Path(r"C:\Users\Administrator\Documents\（已压缩）人比AI凶—万维刚(1).pdf")
    test_output = Path(r"C:\Users\Administrator\Documents\ocr_test")

    if not pdf_path.exists():
        print(f"✗ PDF文件不存在：{pdf_path}")
        return False

    print(f"PDF文件：{pdf_path.name}")
    print(f"输出目录：{test_output}")
    print(f"\n开始 OCR 测试（5页，预计 2-3 分钟）...\n")

    # Import OCR libraries
    try:
        from pdf2image import convert_from_path
        import pytesseract
    except ImportError as e:
        print(f"✗ 缺少依赖库：{e}")
        print("\n请运行：pip install pytesseract pdf2image pillow")
        return False

    # Convert and OCR
    try:
        print("正在转换 PDF 为图片...")
        images = convert_from_path(
            pdf_path,
            dpi=200,
            first_page=1,
            last_page=5
        )
        print(f"✓ 转换了 {len(images)} 页")

        print("\n正在进行 OCR 识别...")
        results = []

        for i, image in enumerate(images, 1):
            print(f"  处理第 {i}/5 页...", end=' ')

            text = pytesseract.image_to_string(
                image,
                lang='chi_sim+eng',
                config='--psm 6'
            )

            # Save individual page
            test_output.mkdir(parents=True, exist_ok=True)
            txt_file = test_output / f"page_{i}.txt"

            with open(txt_file, 'w', encoding='utf-8') as f:
                f.write(f"Page {i}\n{text}")

            results.append({
                'page': i,
                'file': str(txt_file),
                'chars': len(text),
                'preview': text[:100].replace('\n', ' ')
            })

            print(f"✓ {len(text)} 字符")

        # Show results
        print("\n" + "-" * 70)
        print("OCR 结果预览：")
        print("-" * 70)

        for r in results:
            print(f"\n第 {r['page']} 页 ({r['chars']} 字符):")
            print(f"  {r['preview']}...")

        # Calculate success rate
        total_chars = sum(r['chars'] for r in results)
        avg_chars = total_chars / len(results)

        print("\n" + "-" * 70)
        print(f"统计：平均每页 {avg_chars:.0f} 字符")

        if avg_chars > 100:
            print("✓ OCR 效果良好！")
            return True
        else:
            print("⚠ OCR 效果一般，但可以继续")
            return True

    except Exception as e:
        print(f"\n✗ OCR 测试失败：{e}")
        import traceback
        traceback.print_exc()
        return False

def ask_user_continue():
    """Ask user if they want to continue with full processing"""
    print_section("继续处理完整 PDF？")

    print("测试已完成！现在您可以选择：\n")
    print("A. 继续处理全部 417 页（预计 1-2 小时）")
    print("B. 提供章节页码手动处理（5分钟）")
    print("C. 取消")

    choice = input("\n请选择 (A/B/C): ").strip().upper()

    return choice

def process_full_pdf():
    """Process entire PDF with OCR"""
    print_section("步骤 4/7：OCR 处理全部 417 页")

    pdf_path = Path(r"C:\Users\Administrator\Documents\（已压缩）人比AI凶—万维刚(1).pdf")
    output_dir = Path(r"C:\Users\Administrator\Documents\ocr_full")

    print(f"这将需要 1-2 小时...")
    print(f"建议：您可以先休息一下，或处理其他事情")

    confirm = input("\n确定要继续吗？(Y/N): ").strip().upper()

    if confirm != 'Y':
        print("已取消")
        return None

    try:
        from pdf2image import convert_from_path
        import pytesseract
        import json
    except ImportError:
        print("✗ 缺少依赖库")
        return None

    output_dir.mkdir(parents=True, exist_ok=True)

    # Process all pages
    print("\n开始处理...\n")

    # Convert in batches to avoid memory issues
    batch_size = 50
    total_pages = 417

    all_results = []

    for start_page in range(1, total_pages + 1, batch_size):
        end_page = min(start_page + batch_size - 1, total_pages)

        print(f"处理第 {start_page}-{end_page} 页...")

        try:
            images = convert_from_path(
                pdf_path,
                dpi=200,
                first_page=start_page,
                last_page=end_page
            )

            for i, image in enumerate(images, start_page):
                print(f"  第 {i}/{total_pages} 页...", end=' ')

                text = pytesseract.image_to_string(
                    image,
                    lang='chi_sim+eng',
                    config='--psm 6'
                )

                # Save page
                txt_file = output_dir / f"page_{i:03d}.txt"

                with open(txt_file, 'w', encoding='utf-8') as f:
                    f.write(text)

                all_results.append({
                    'page': i,
                    'file': str(txt_file),
                    'chars': len(text)
                })

                print(f"✓")

        except Exception as e:
            print(f"  ✗ 错误：{e}")
            continue

    # Save summary
    summary_file = output_dir / "ocr_summary.json"
    with open(summary_file, 'w', encoding='utf-8') as f:
        json.dump({
            'total_pages': len(all_results),
            'results': all_results
        }, f, indent=2, ensure_ascii=False)

    # Combine all text
    print("\n合并所有文本...")
    combined_file = output_dir / "full_text.txt"

    with open(combined_file, 'w', encoding='utf-8') as f:
        for i in range(1, total_pages + 1):
            txt_file = output_dir / f"page_{i:03d}.txt"
            if txt_file.exists():
                with open(txt_file, 'r', encoding='utf-8') as f_page:
                    f.write(f"\n{'='*60}\n")
                    f.write(f"Page {i}\n")
                    f.write(f"{'='*60}\n")
                    f.write(f_page.read())

    print(f"✓ OCR 完成！")
    print(f"  输出目录：{output_dir}")
    print(f"  完整文本：{combined_file}")

    return combined_file

def detect_chapters(full_text_file):
    """Detect chapter structure"""
    print_section("步骤 5/7：识别章节结构")

    if not full_text_file or not full_text_file.exists():
        print("✗ 需要先完成 OCR 处理")
        return None

    print(f"读取文件：{full_text_file}")

    with open(full_text_file, 'r', encoding='utf-8') as f:
        text = f.read()

    # Look for chapter patterns
    import re

    patterns = [
        r'第[一二三四五六七八九十百千零\d]+章',
        r'Chapter\s+\d+',
        r'第\d+章',
        r'[一二三四五六七八九十]+[、\s]\s*[^第\n]{2,20}',
    ]

    lines = text.split('\n')
    potential_chapters = []

    for i, line in enumerate(lines):
        line = line.strip()

        if not line or len(line) > 50:
            continue

        for pattern in patterns:
            if re.search(pattern, line):
                potential_chapters.append({
                    'line_number': i,
                    'title': line
                })
                break

    # Group by proximity (chapters are usually on different pages)
    chapters = []
    if potential_chapters:
        # Filter out duplicates within 10 lines
        seen = set()
        for ch in potential_chapters:
            line_num = ch['line_number']
            key = line_num // 10

            if key not in seen:
                seen.add(key)
                chapters.append(ch)

    print(f"\n发现 {len(chapters)} 个可能的章节：\n")

    for i, ch in enumerate(chapters[:20], 1):
        print(f"  {i}. {ch['title']}")

    if len(chapters) > 20:
        print(f"\n... 还有 {len(chapters) - 20} 个")

    return chapters

def main():
    """Main workflow"""
    print("\n" + "="*70)
    print("  扫描版 PDF 自动化处理流程")
    print("  《人比AI凶—万维刚》 → 完整 PPT")
    print("="*70)

    print("\n总计 417 页扫描版 PDF")
    print("预计总时间：2-3 小时\n")

    # Step 1: Check Tesseract
    has_tesseract = check_tesseract()

    if not has_tesseract:
        # Step 2: Show download instructions
        show_download_instructions()

        # Re-check
        print("\n请确认安装完成...")
        input("⏎ 按回车键继续...")

        if not check_tesseract():
            print("\n✗ Tesseract 仍未安装")
            print("请完成安装后重新运行此脚本")
            return 1

    # Step 3: Test OCR
    print("\n准备测试 OCR...")
    input("⏎ 按回车键开始测试...")

    test_success = test_ocr_first_pages()

    if not test_success:
        print("\n✗ OCR 测试失败")
        print("请检查：")
        print("1. Tesseract 是否正确安装")
        print("2. 是否安装了中文语言包")
        return 1

    # Step 4: Ask what to do next
    choice = ask_user_continue()

    if choice == 'A':
        # Full processing
        full_text_file = process_full_pdf()

        if full_text_file:
            # Step 5: Detect chapters
            chapters = detect_chapters(full_text_file)

            if chapters:
                print_section("步骤 6/7：章节识别完成")

                print("\n是否继续生成 PPT？")
                print("需要：")
                print("1. 上传到 NotebookLM（手动）")
                print("2. 生成 PPT 大纲")
                print("3. 创建最终 PPT")

                ready = input("\n准备好了吗？(Y/N): ").strip().upper()

                if ready == 'Y':
                    print_section("步骤 7/7：生成 PPT")
                    print("\n请按照以下步骤操作：")
                    print("1. 将 OCR 文本上传到 NotebookLM")
                    print("2. 使用 notebooklm_client.py 生成大纲")
                    print("3. 使用 ppt_generator.py 创建 PPT")
                    print("4. 使用 ppt_merger.py 合并 PPT")

                    print("\n详细说明请查看：")
                    print("C:\\Users\\Administrator\\Documents\\OCR_安装步骤.txt")

    elif choice == 'B':
        print_section("手动提供章节页码")
        print("\n请打开 PDF 查看目录，提供章节页码：")
        print("\n格式示例：")
        print("  第一章：第 1-50 页")
        print("  第二章：第 51-100 页")
        print("  ...")
        print("\n输入页码后，我会手动分割 PDF 并生成 PPT")

    else:
        print("\n已取消")

    print_section("处理流程结束")
    print("\n所有输出文件保存在：")
    print("  C:\\Users\\Administrator\\Documents\\")
    print("\n感谢使用！")

    return 0

if __name__ == '__main__':
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n⚠️ 用户中断")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ 发生错误：{e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
