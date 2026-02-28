# Claude Code Skills Collection - MLK

这是一个精心策划的 **Claude Code 自定义技能集合**，用于增强 AI 编程助手的能力。

## 📋 目录

- [快速开始](#快速开始)
- [技能列表](#技能列表)
- [安装说明](#安装说明)
- [使用指南](#使用指南)
- [项目结构](#项目结构)
- [贡献指南](#贡献指南)
- [许可证](#许可证)

## 🚀 快速开始

```bash
# 克隆此仓库
git clone https://github.com/milk7676/claude-code-skill-mlk.git

# 复制技能到本地 Claude Code 目录
cp -r claude-code-skill-mlk/.claude/skills/* ~/.claude/skills/

# 重启 Claude Code 会话
# 技能将自动加载
```

## 🎯 技能列表

### 1. Author Works Analysis（作者作品分析）

**作者作品分析与整理工具**

系统梳理作者的作品脉络、思想演变和创作历程。

**使用场景：**
- 了解一位新作者的作品体系
- 对比作者思想变化轨迹
- 建立个人作者数据库
- 研究特定领域作者群体

**示例：**
```
用户: /author-works-analysis 帮我整理万维钢的作品
系统: 自动创建表格，列出所有作品、核心观点、思想演变
```

**包含内容：**
- 数据收集方法论
- 字段设计参考
- 实战案例分析

---

### 2. Book to PPT（书籍转演示文稿）

**PDF 书籍自动转换为 PowerPoint 演示文稿**

完整的自动化工作流，从 PDF 提取到 PPT 生成。

**核心功能：**
- ✅ 按章节拆分 PDF（支持中英文）
- ✅ 提取 Markdown 内容
- ✅ 集成 NotebookLM 生成大纲
- ✅ 使用 iSlide 插件创建 PPT
- ✅ 合并章节为完整演示文稿

**使用方法：**
```bash
# 完整工作流（需要 NotebookLM URL）
python scripts/workflow.py path/to/book.pdf --notebook-url "https://notebooklm.google.com/notebook/..."

# 自定义输出目录
python scripts/workflow.py book.pdf --notebook-url "URL" --output-dir ./my_output

# 不使用 iSlide（使用基本主题）
python scripts/workflow.py book.pdf --notebook-url "URL" --no-islide
```

**系统要求：**
- Windows 操作系统
- Microsoft PowerPoint
- NotebookLM 技能
- iSlide 插件（可选）

**工作流程：**
```
PDF Book → 按章拆分 → 提取 Markdown → 上传 NotebookLM → 生成大纲 → 创建 PPT → 合并完整文稿
```

---

### 3. Content Workflow（内容工作流）

**从需求到最终演示的完整内容创作流程**

一站式处理文章、演示文稿和演讲稿的创作。

**功能覆盖：**
1. **需求收集** - 主题、受众、长度、目标
2. **参考资料处理** - 上传并研究参考文档
3. **文章大纲生成** - 结构化内容框架
4. **正文写作** - 基于大纲撰写完整文章
5. **PPT 大纲** - 演示文稿结构设计
6. **演讲稿** - 演讲者备注和谈话要点
7. **PPT 生成** - 使用 pptx 技能创建演示文稿

**适用场景：**
- 创建带演讲稿的演示文稿
- 将参考资料转换为结构化内容
- 构建完整的内容包（文章 + 幻灯片 + 脚本）

---

### 4. NotebookLM（笔记本研究助手）

**直接从 Claude Code 查询 Google NotebookLM**

基于文档的、带引用的答案，大幅减少幻觉。

**核心特性：**
- 🔍 基于文档的精准答案
- 📚 源引用支持
- 🌐 浏览器自动化
- 🔐 持久身份验证
- 📝 笔记本库管理

**使用场景：**
```
- 明确提及 NotebookLM
- 分享 NotebookLM URL
- 查询笔记本/文档
- 添加文档到 NotebookLM 库
- 使用 "ask my NotebookLM" 等短语
```

**智能添加笔记本：**
```bash
# 步骤 1: 查询笔记本了解内容
python scripts/run.py ask_question.py --question "What is the content of this notebook?" --notebook-url "[URL]"

# 步骤 2: 根据发现的信息添加
python scripts/run.py notebook_manager.py add --url "[URL]" --name "[名称]" --description "[描述]" --topics "[主题]"
```

**快捷命令：**
- `list_notebooks.bat` - 列出所有笔记本
- `add_notebook.bat` - 添加新笔记本
- `query_test.bat` - 测试查询

**包含工具：**
- 身份验证管理器
- 笔记本管理器
- 浏览器会话处理
- 清理管理器

---

### 5. MLK（自定义技能模板）

**自定义技能模板**

用于快速创建新技能的基础模板。

**使用方法：**
1. 复制 `mlk` 目录
2. 重命名为新技能名称
3. 编辑 `SKILL.md` 定义功能
4. 添加实现代码（可选）

---

## 📦 安装说明

### 方法一：全局安装（推荐）

```bash
# 复制到用户级技能目录
cp -r .claude/skills/* ~/.claude/skills/
```

### 方法二：项目级安装

```bash
# 复制到特定项目的技能目录
cp -r .claude/skills/* /path/to/project/.claude/skills/
```

### 方法三：选择性安装

只安装需要的技能：
```bash
# 只安装 NotebookLM
cp -r .claude/skills/notebooklm ~/.claude/skills/

# 只安装 Book to PPT
cp -r .claude/skills/book-to-ppt ~/.claude/skills/
```

## 📚 使用指南

### 在 Claude Code 中调用技能

1. **斜杠命令：** 直接使用技能名称
   ```
   /notebooklm 查询我的文档
   /author-works-analysis 分析这位作者
   ```

2. **自然语言触发：** 描述需求，Claude 会自动选择合适技能
   ```
   帮我把这本书转成 PPT
   分析一下这个作者的作品脉络
   ```

3. **查看可用技能：**
   ```
   /skills
   ```

### 技能开发

创建新技能的步骤：

1. **创建技能目录：**
   ```bash
   mkdir ~/.claude/skills/my-skill
   ```

2. **创建 SKILL.md：**
   ```yaml
   ---
   name: my-skill
   description: 技能描述
   argument-hint: "[参数说明]"
   ---

   # 技能名称

   技能详细说明...
   ```

3. **添加实现代码（可选）：**
   - Python: `scripts/my_script.py`
   - JavaScript: `index.js`
   - TypeScript: `index.ts`

4. **重启 Claude Code**

## 📁 项目结构

```
claude-code-skill-mlk/
├── .claude/
│   └── skills/                    # 技能目录
│       ├── author-works-analysis/  # 作者作品分析
│       │   ├── SKILL.md
│       │   ├── examples/
│       │   └── reference/
│       ├── book-to-ppt/           # 书籍转 PPT
│       │   ├── SKILL.md
│       │   ├── scripts/
│       │   └── references/
│       ├── content-workflow/      # 内容工作流
│       │   ├── SKILL.md
│       │   ├── assets/
│       │   └── references/
│       ├── notebooklm/            # NotebookLM 集成
│       │   ├── SKILL.md
│       │   ├── scripts/
│       │   ├── images/
│       │   └── references/
│       ├── mlk/                   # 自定义模板
│       │   └── SKILL.md
│       ├── *.skill                # 技能文件格式版本
│       └── ...
├── .gitignore
└── README.md
```

## 🤝 贡献指南

欢迎贡献新的技能或改进现有技能！

### 贡献流程

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/amazing-skill`)
3. 提交更改 (`git commit -m 'Add amazing skill'`)
4. 推送到分支 (`git push origin feature/amazing-skill`)
5. 开启 Pull Request

### 技能提交检查清单

- [ ] 技能有清晰的名称和描述
- [ ] SKILL.md 包含完整的使用说明
- [ ] 包含示例代码或使用场景
- [ ] 必要的依赖已文档化
- [ ] 通过基本功能测试

## 🔧 故障排除

### 技能未加载

**问题：** 重启后技能不可用

**解决方案：**
1. 检查技能路径是否正确：`~/.claude/skills/` 或 `project/.claude/skills/`
2. 验证 SKILL.md 格式是否正确
3. 查看 Claude Code 日志

### Python 技能依赖问题

**问题：** ModuleNotFoundError 或其他导入错误

**解决方案：**
```bash
# 安装必要依赖
pip install -r .claude/skills/skill-name/requirements.txt

# 或使用虚拟环境
python -m venv ~/.claude/venv
source ~/.claude/venv/bin/activate
pip install -r requirements.txt
```

### NotebookLM 认证失败

**问题：** 无法连接到 NotebookLM

**解决方案：**
```bash
# 运行诊断
cd .claude/skills/notebooklm
python diagnose.py

# 检查身份验证
test_auth_status.bat
```

## 📖 更多资源

- [Claude Code 官方文档](https://code.claude.com/docs)
- [技能开发指南](https://code.claude.com/docs/en/skills)
- [NotebookLM 官方文档](https://notebooklm.google.com)

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

## 👤 作者

**milk7676** - [GitHub](https://github.com/milk7676)

## 🙏 致谢

- Claude Code 团队提供的强大平台
- 所有贡献者的技能和改进

---

**⭐ 如果这个项目对您有帮助，请给一个 Star！**

**最后更新：** 2026-02-27
