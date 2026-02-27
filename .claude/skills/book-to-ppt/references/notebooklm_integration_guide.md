# Book to PPT + NotebookLM 集成使用指南

## 功能概述

将 PDF 书籍自动转换为 PowerPoint 演示文稿的完整工作流程，使用 **真实的 NotebookLM** 生成 PPT 大纲。

## 工作流程

```
PDF 书籍
  ↓ 识别章节并分割
Markdown 文件 (每章节一个)
  ↓ 上传到 NotebookLM (手动)
NotebookLM 处理文档
  ↓ 自动生成 PPT 大纲
JSON 大纲文件
  ↓ 使用 iSlide 生成 PPT
独立 PPT 文件 (每章节一个)
  ↓ 合并所有 PPT
完整书籍 PPT
```

## 前置要求

### 1. NotebookLM 设置

确保 NotebookLM 技能已安装并配置：

```bash
# 检查认证状态
cd ~/.claude/skills/notebooklm
python scripts/run.py auth_manager.py status

# 如果未认证，运行设置
python scripts/run.py auth_manager.py setup
```

### 2. 创建 NotebookLM 笔记本

访问 https://notebooklm.google.com/ 并创建一个新笔记本。

记录笔记本 URL（类似）：
```
https://notebooklm.google.com/notebook/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
```

### 3. 安装 Python 依赖

```bash
pip install pdfplumber PyPDF2 python-pptx pywin32
```

### 4. iSlide 插件（可选）

如果需要使用 iSlide 美化功能：
- 下载：https://www.islide.cc/
- 安装到 PowerPoint

## 使用方法

### 方法一：完整工作流程

一步完成所有步骤：

```bash
cd C:\Users\Administrator\.claude\skills\book-to-ppt\scripts

python workflow.py "C:\path\to\your\book.pdf" \
  --notebook-url "https://notebooklm.google.com/notebook/..." \
  --output-dir "./output"
```

**步骤说明：**

1. **自动分割 PDF**
   - 识别章节结构（支持中英文）
   - 创建章节 PDF 文件
   - 提取 Markdown 内容

2. **手动上传到 NotebookLM**
   - 脚本会暂停等待您上传文件
   - 在浏览器中打开 NotebookLM
   - 上传生成的所有 Markdown 文件

3. **自动生成大纲**
   - 调用 NotebookLM API
   - 为每个章节生成 PPT 大纲
   - 保存为 JSON 文件

4. **生成 PPT**
   - 使用 iSlide 插件（如果已安装）
   - 根据大纲创建幻灯片
   - 每章节一个独立 PPT

5. **合并 PPT**
   - 按章节顺序合并
   - 添加标题页
   - 生成最终文件

### 方法二：分步执行

如果需要更多控制，可以分步执行：

#### 步骤 1：分割 PDF

```bash
python pdf_splitter.py "book.pdf" --output-dir "./chapters"
```

生成文件：
- `chapters/01_第一章.pdf`
- `chapters/01_第一章.md`
- `chapters/02_第二章.pdf`
- `chapters/02_第二章.md`
- ...

#### 步骤 2：上传到 NotebookLM

**手动操作：**
1. 打开 NotebookLM 笔记本
2. 点击 "Add source"
3. 选择 "Upload"
4. 上传所有 `.md` 文件

**或者使用脚本：**
```bash
# (当前版本需要手动上传，未来可能支持自动化)
```

#### 步骤 3：生成大纲

```bash
python notebooklm_client.py \
  chapters/*.md \
  --output-dir "./outlines" \
  --notebook-url "https://notebooklm.google.com/notebook/..."
```

生成文件：
- `outlines/01_第一章_outline.json`
- `outlines/02_第二章_outline.json`
- ...

#### 步骤 4：生成 PPT

```bash
python ppt_generator.py \
  "./outlines" \
  --output-dir "./presentations"
```

生成文件：
- `presentations/01_第一章.pptx`
- `presentations/02_第二章.pptx`
- ...

#### 步骤 5：合并 PPT

```bash
python ppt_merger.py \
  presentations/*.pptx \
  --output "complete_book.pptx"
```

生成最终文件：
- `complete_book.pptx`

## NotebookLM Prompt 模板

脚本使用以下 Prompt 模板生成大纲：

```
Based on the following chapter content, generate a PowerPoint presentation outline in JSON format.

Requirements:
1. Create 3-5 slides for the main content
2. Include 1 introduction slide
3. Include 1 conclusion/summary slide
4. Each slide should have a clear title and 3-5 bullet points
5. Output MUST be valid JSON with this exact structure:
{
  "title": "Presentation Title",
  "subtitle": "Chapter Subtitle",
  "slides": [
    {
      "title": "Slide Title",
      "content": ["bullet point 1", "bullet point 2"],
      "notes": "Optional speaker notes"
    }
  ]
}

Chapter Content: [这里插入章节内容，最多 8000 字符]
```

您可以在 `scripts/notebooklm_client.py` 中修改此模板。

## 大纲 JSON 格式

生成的大纲文件格式：

```json
{
  "title": "演示文稿标题",
  "subtitle": "章节副标题",
  "slides": [
    {
      "title": "幻灯片标题",
      "content": [
        "要点 1",
        "要点 2",
        "要点 3"
      ],
      "notes": "演讲者备注（可选）"
    }
  ]
}
```

## 故障排除

### 问题 1：无法连接 NotebookLM

**原因：**
- NotebookLM 技能未认证
- 网络连接问题

**解决方案：**
```bash
cd ~/.claude/skills/notebooklm
python scripts/run.py auth_manager.py status
python scripts/run.py auth_manager.py setup  # 重新认证
```

### 问题 2：章节识别失败

**原因：**
- PDF 格式不标准
- 章节标题格式特殊

**解决方案：**
1. 修改 `scripts/pdf_splitter.py` 中的章节识别模式
2. 参考 `references/chapter_patterns.md` 添加自定义模式

### 问题 3：大纲 JSON 解析失败

**原因：**
- NotebookLM 返回的不是纯 JSON
- JSON 格式错误

**解决方案：**
1. 脚本会自动尝试提取 JSON
2. 如果失败，会返回基本结构
3. 可以手动编辑生成的 JSON 文件

### 问题 4：PPT 生成失败

**原因：**
- PowerPoint 未安装
- iSlide 插件未安装

**解决方案：**
```bash
# 禁用 iSlide
python workflow.py "book.pdf" --notebook-url "..." --no-islide
```

## 高级用法

### 自定义章节识别

编辑 `scripts/pdf_splitter.py`:

```python
class ChapterPattern:
    CN_PATTERNS = [
        r'^第[一二三四五六七八九十百千零\d]+章\s*',
        # 添加您的自定义模式
        r'^YOUR_CUSTOM_PATTERN',
    ]
```

### 自定义 Prompt

编辑 `scripts/notebooklm_client.py`:

```python
def generate_outline_prompt(self, chapter_content: str, chapter_title: str = "") -> str:
    prompt = f"""您的自定义 Prompt...

    {chapter_content[:8000]}
    """
    return prompt
```

### 批量处理多本书籍

创建批处理脚本：

```bash
# batch_process.sh
for book in books/*.pdf; do
  python workflow.py "$book" \
    --notebook-url "https://notebooklm.google.com/notebook/..." \
    --output-dir "./output/$(basename $book .pdf)"
done
```

## 性能优化

### 加快处理速度

1. **减少章节内容长度**
   ```python
   # notebooklm_client.py
   content[:8000]  # 改为 [:4000]
   ```

2. **并行处理**
   - 脚本默认串行处理
   - 可修改为多线程

3. **缓存大纲**
   - 避免重新生成已有大纲
   - 检查 JSON 文件是否存在

## 输出文件结构

```
output/
├── chapters/              # 章节文件
│   ├── 01_第一章.pdf
│   ├── 01_第一章.md
│   ├── 02_第二章.pdf
│   └── 02_第二章.md
├── outlines/              # 大纲文件
│   ├── 01_第一章_outline.json
│   └── 02_第二章_outline.json
├── presentations/         # PPT 文件
│   ├── 01_第一章.pptx
│   └── 02_第二章.pptx
└── book_complete.pptx    # 最终合并的 PPT
```

## 下一步改进

可能的增强功能：

1. ✅ NotebookLM API 集成（已完成）
2. ⏳ 自动上传文档到 NotebookLM
3. ⏳ 智能章节识别（AI 辅助）
4. ⏳ 自定义 PPT 模板支持
5. ⏳ 批量处理多本书籍
6. ⏳ Web UI 界面

## 技术支持

遇到问题？

1. 查看故障排除部分
2. 检查 `references/troubleshooting.md`
3. 查看 NotebookLM 技能文档

---

**版本：** 2.0 (with real NotebookLM integration)
**更新日期：** 2026-02-05
