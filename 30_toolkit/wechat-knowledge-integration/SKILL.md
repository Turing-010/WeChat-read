---
name: wechat-knowledge-integration
description: Use when organizing WeChat public-account articles crawled by wechatMPtool in 00_inbox/<Account>/, clustering articles into incremental learning themes (themes.json & README.md), generating 10-section technical study notes (AI_精读.md) and guided Q&A notes (NOTE.md) with Opus/Flash, or synthesizing/updating theme review articles (_themes/Txx_*.md) and 20_topics/ with Gemini Argon. Also supports legacy root-level archive verification.
---
# 微信文章就地管理与四步主题学习工作流

将 `wechatMPtool` 采集的多模态原始数据、Opus 深度精读构建、Gemini Flash 互动解惑与 Gemini Argon 主题综述有机结合，在 `00_inbox/<公众号>/` 内实现**零搬家就地闭环（In-Place Learning）**与**持续增量演进**。

## 一、 核心目录约定（`00_inbox` 就地架构）

常用库路径为 `/Users/iw/Documents/WeChat_read`。执行前先读根目录 [agent.md](../../agent.md) 及目标公众号下的 `themes.json` 与 `README.md`。

**不再向根目录各公众号文件夹搬家复制**。所有新采集文章直接保存在 `00_inbox/<公众号>/<文章原标题>/` 下，单篇目录及公众号级文件职责如下：

| 位置 / 文件 | 职责说明 |
| :--- | :--- |
| `00_inbox/<公众号>/README.md` | 由 `30_toolkit/generate_inbox_readme.py` 自动生成的**主题学习工作台与全量索引** |
| `00_inbox/<公众号>/themes.json` | 公众号级**主题聚类状态库**（记录主题划分、推荐学习顺序、是否已纳入综述、非技术跳过项） |
| `00_inbox/<公众号>/_themes/Txx_*.md` | 由 **Gemini Argon** 生成并随新文章持续迭代的**主题综述文章** |
| `<文章目录>/<原标题>.pdf` | **原始基准 PDF**（人类阅读、视觉架构图与物理页码 `p.X` 的唯一基准，只读） |
| `<文章目录>/content.txt` & `*.html` | `wechatMPtool` 采集的完整文本与网页（辅助 AI 零截断读取长代码块，补齐 PDF 排版裁切） |
| `<文章目录>/metadata.json` | 官方 `publish_time`、完整标题、作者、微信原文 URL |
| `<文章目录>/AI_精读.md` | **Opus** 初次深度理解构建的 **10 节标准技术精读笔记** |
| `<文章目录>/NOTE.md` | **Opus** 生成的 3 道费曼导读追问 + **Gemini Flash** 快速解惑沉淀 + 本人思考记录 |

> **历史存量兼容**：根目录旧公众号文件夹（`大淘宝技术/`、`腾讯技术工程/`、`阿里技术/`、`数字生命卡兹克/`，共 301 篇）作为只读旧档保留，`generate_inbox_readme.py` 会自动比对标题/URL 并在 `00_inbox` 索引中挂载 `[🔗旧档总结]`。

---

## 二、 四步闭环操作规程

### 第一步：收集（`wechatMPtool`）
爬虫采集的公众号文件夹直接存放在 `00_inbox/<公众号>/` 下，保持原始文件结构不变。

### 第二步：整理（增量扫描、主题聚类与 `README` 索引更新）
1. **扫描新增未归类文章**：
   ```bash
   python3 30_toolkit/generate_inbox_readme.py 00_inbox/<公众号> --scan-new
   ```
2. **去噪与增量主题路由（更新 `themes.json`）**：
   - 读取新增文章的 `metadata.json` 与 `content.txt` 前段导语；
   - 将峰会宣传、参会指南、放假通知、社区招募等非技术内容加入 `themes.json` 的 `skipped` 列表（保留原文件夹，在 `README.md` 底部折叠）；
   - 将实质技术文章按核心工程问题归入既有主题 `T01`、`T02`…（或开辟新主题），按「认知建立 $\to$ 机制深挖 $\to$ 实战踩坑」排列推荐学习顺序，并填写一句话看点 `focus`。
3. **刷新索引工作台**：
   ```bash
   python3 30_toolkit/generate_inbox_readme.py --all
   ```

### 第三步：学习（Opus 初次深度构建 + Gemini Flash 快速解惑）
选定主题课表中的文章后，在**该文章文件夹内就地执行**：

1. **Opus 第一次理解与构建**：
   - **双源对读**：同时读取 `<原标题>.pdf`（逐页核查架构图、表格与页码 `p.1–N`）与 `content.txt`（提取无损源码与正文）；若同主题已有 `_themes/Txx_*.md`，一并读取并在第 2 节指明本文的**增量看点**。
   - **产出 `AI_精读.md`**：严格满足下方「10 节精读笔记规范与质量门禁」。
   - **初始化 `NOTE.md`**：若尚无 `NOTE.md`，创建并写入 3 道带 PDF 页码锚点的**费曼基线追问**，预留「Gemini Flash 互动解惑沉淀区」与「本人核心收获区」。
2. **Gemini Flash 互动解惑**：
   - 围绕用户在阅读 PDF 时提出的概念、代码或架构问题快速作答；
   - 将关键问答结论实时追加沉淀到该文章的 `NOTE.md` 中。

### 第四步：归纳（Gemini Argon 主题综述生成与增量演进）
当完成某主题下单篇或多篇文章学习后，使用 **Gemini Argon**：
1. 读取该主题已学文章的 `AI_精读.md` + `NOTE.md` 及现有 `_themes/Txx_<主题名>.md`；
2. 创建或增量升级 `_themes/Txx_<主题名>.md`（提炼跨文共同定律、多维对比矩阵、演进日志 `v1.0` $\to$ `v1.1`），并按需同步更新根目录 `20_topics/` 对应专题；
3. 将 `themes.json` 中已纳入文章标记为 `"synthesized": true`，重跑 `python3 30_toolkit/generate_inbox_readme.py --all` 将状态更新为 `✅ 已纳入综述`。

---

## 三、 10 节精读笔记规范与质量门禁（`AI_精读.md`）

详细写作规范见 [Obsidian笔记提示词](references/obsidian-note-prompt.md)，必须严格通过以下门禁：

1. **YAML Frontmatter 与唯一 H1**：
   - 包含 `title`、`source`、`date`（`YYYY-MM-DD` 发布日期）、`type: "技术精读"`、`tags`、`status: "待复习"`；
   - 代码块之外全篇严格只保留 **1 个一级标题 `# 标题`**。
2. **标准 10 大编号二级章节（`## 1.` 至 `## 10.`）**：
   - `## 1. TL;DR`：3–5 句浓缩核心痛点、关键机制、架构演进与量化收益。
   - `## 2. 问题定义与背景`（或 `## 2. 核心概念`）：界定真实痛点、边界约束及主题内增量关系。
   - `## 3. 知识框架`：必须包含至少一张 `mermaid` 全景架构图。
   - `## 4. 核心内容拆解`：按演进阶段或架构分层讲透“问题 $\to$ 机制 $\to$ 为什么有效 $\to$ 代价与边界”，利用 `content.txt` 完整保留源码细节。
   - `## 5. 数据速查表`：结构化汇总全部关键实测数据、参数与对比基准。
   - `## 6. 踩坑与教训 / 可迁移的设计原则`：采用 `| 错误做法 | 失败表现或原因 | 原文应对（可迁移的设计原则） |` 提炼防呆护栏。
   - `## 7. 记忆锚点`：1–2 条高辨识度口诀或机制判据。
   - `## 8. 复习卡片`：**5–10 条**单行 `问题::答案` 格式闪卡。
   - `## 9. 知识关联`：挂载 `../../20_topics/xxx.md`（相对于旧档）或 `../../../20_topics/xxx.md` / `../../20_topics/xxx.md` 真实相对路径链接、同主题文章链接与候选 `[[双链]]`。
   - `## 10. 原文参考资料`：列出原标题、作者、发布日期、微信 URL 及本地 PDF / `content.txt` 链接。
3. **正文零内联页码与文末折叠校对报告**：
   - 在文末 `> [!note]- 校对报告` 之前的正文中**严禁出现任何内联页码（如 `p.X` 或 `第X页`）**；
   - 底部统一放置折叠的 `> [!note]- 校对报告`，记录各章节 PDF 页码溯源（`p.X–Y`）、双源互补说明（PDF 图表 + `content.txt` 完整代码）与勘误。

---

## 四、 常用命令速查

```bash
# 1. 更新 00_inbox 下全部公众号的 README 学习工作台与索引
python3 30_toolkit/generate_inbox_readme.py --all

# 2. 增量扫描某个公众号下新爬入、未归入 themes.json 的文章
python3 30_toolkit/generate_inbox_readme.py 00_inbox/腾讯云开发者 --scan-new

# 3. （历史旧档维护）只读核验根目录存量 301 篇旧档链接与哈希
python3 30_toolkit/wechat-knowledge-integration/scripts/kb_tools.py verify --root /Users/iw/Documents/WeChat_read
```
