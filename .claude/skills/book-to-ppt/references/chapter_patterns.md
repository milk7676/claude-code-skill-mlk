# Chapter Pattern Reference

## Chinese Chapter Patterns

### Common Format Examples

1. **第X章 / 第X节**
   - 第一章 概述
   - 第二章 系统设计
   - 第三章 实现方案

2. **数字序号**
   - 一、引言
   - 二、背景
   - 三、方法论

3. **中文数字**
   - 第一章节
   - 第二部分
   - 第三篇

### Regular Expression Patterns

```python
# Basic patterns
r'^第[一二三四五六七八九十百千零\d]+章\s*'
r'^第[一二三四五六七八九十百千零\d]+节\s*'
r'^[一二三四五六七八九十百千零\d]+[、\s]\s*'

# Combined pattern
CN_PATTERN = r'^(第?[一二三四五六七八九十百千零\d]+[章节部分]|[一二三四五六七八九十百千零\d]+[、.])\s*'
```

## English Chapter Patterns

### Common Format Examples

1. **Chapter X**
   - Chapter 1: Introduction
   - Chapter 2 - Literature Review
   - CHAPTER 3: Methodology

2. **Part X**
   - Part I: Background
   - Part II: Analysis
   - Part III: Conclusion

3. **Numbered**
   - 1. Introduction
   - 2. System Design
   - 3. Implementation

### Regular Expression Patterns

```python
# Chapter patterns
r'^Chapter\s+\d+'
r'^CHAPTER\s+\d+'
r'^Part\s+\d+'

# Numbered patterns
r'^\d+\.\s+[A-Z]'
r'^\d+\.\d+\s+[A-Z]'  # 1.1, 1.2, etc.
```

## Mixed Language Patterns

For books with both Chinese and English:

```python
MIXED_PATTERNS = [
    r'^第\d+章',  # 第一章, 第1章
    r'^Chapter\s+\d+',  # Chapter 1
    r'^Part\s+\d+',  # Part 1
    r'^\d+\.\s+',  # 1. Title
]
```

## Detection Algorithm

1. **Extract text from each page**
2. **Check each line against patterns**
3. **Record first match per page**
4. **Validate chapter sequence**

### Validation Rules

- Chapter numbers should be sequential
- Avoid false positives (e.g., "see chapter 5" in text)
- Check font size/weight (titles often larger/bold)

## Edge Cases

### Table of Contents
Skip TOC pages by detecting:
- Page range (usually early in book)
- Multiple chapter titles on one page
- "目录" or "Contents" in header

### Section Numbers vs Chapter Numbers
Distinguish by:
- Context (section usually follows chapter)
- Numbering format (1.1 vs 1)
- Hierarchy in document structure

### Appendices
Handle special chapters:
- 附录 / Appendix
- 参考文献 / References
- 索引 / Index

## Advanced Detection

For complex books, use AI-assisted detection:

```python
def is_chapter_with_ai(page_text: str) -> bool:
    prompt = f"""
    Is the following text a chapter title?
    Answer YES or NO.

    Text: {page_text[:500]}
    """
    # Call AI API
    # ...
```