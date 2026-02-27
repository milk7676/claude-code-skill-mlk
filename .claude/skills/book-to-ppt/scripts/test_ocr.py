"""
Test OCR on first few pages to check quality
"""
import sys
from pathlib import Path
from pdf2image import convert_from_path
import pytesseract
from PIL import Image

# 设置 UTF-8 编码
sys.stdout.reconfigure(encoding='utf-8')

pdf_path = Path(r"C:\Users\Administrator\Documents\（已压缩）人比AI凶—万维刚(1).pdf")
output_file = Path(r"C:\Users\Administrator\Documents\ocr_test_result.txt")

print("开始 OCR 测试...")
print(f"测试页数: 前5页")
print(f"输出文件: {output_file}")
print("这可能需要 2-5 分钟...\n")

with open(output_file, 'w', encoding='utf-8') as f:
    f.write("=" * 80 + "\n")
    f.write("OCR 测试结果 - 人比AI凶—万维刚\n")
    f.write("=" * 80 + "\n\n")

    try:
        # 转换前5页为图片
        print("正在将 PDF 转换为图片...")
        images = convert_from_path(pdf_path, first_page=1, last_page=5)

        f.write(f"成功转换 {len(images)} 页\n\n")

        # 对每页进行 OCR
        for i, image in enumerate(images, 1):
            print(f"正在处理第 {i} 页...")

            f.write(f"\n{'=' * 80}\n")
            f.write(f"第 {i} 页 OCR 结果\n")
            f.write(f"{'=' * 80}\n\n")

            # 使用 Tesseract OCR（中英文混合）
            # 支持中英文：chi_sim (简体中文) + eng (英文)
            text = pytesseract.image_to_string(
                image,
                lang='chi_sim+eng',
                config='--psm 6'  # 假设单列文本
            )

            f.write(text)
            f.write("\n")

            # 显示预览（前200字符）
            preview = text[:200].replace('\n', ' ')
            print(f"  预览: {preview}...")

        f.write("\n" + "=" * 80 + "\n")
        f.write("OCR 测试完成\n")

        print(f"\n✓ OCR 测试完成！")
        print(f"✓ 结果已保存到: {output_file}")

    except Exception as e:
        f.write(f"\n错误: {e}\n")
        import traceback
        traceback.print_exc()

print("\n请检查输出文件，查看 OCR 效果。")
