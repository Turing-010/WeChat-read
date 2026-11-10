---
name: wechat-knowledge-integration
description: Use when organizing local WeChat article collections, updating incremental theme indexes, generating source-grounded study notes, tutoring from the library, or maintaining topic syntheses and legacy archive links. Does not collect articles through the WeChat UI.
---

# 微信文章就地整理与学习

先读用户指定资料库的 `agent.md`，再读本次文章、公众号 `themes.json` 与有关学习记录。常用库为 `/Users/iw/Documents/WeChat_read`；其规则优先于本技能的通用约定。

## 按请求进入对应步骤

1. **收集**：接收用户现有采集渠道的材料。新文章保留在 `00_inbox/<公众号>/<文章目录>/`；原 PDF、文本、HTML、图片及采集 metadata 保持原样。根目录历史公众号目录保留，旧档仅关联，不默认搬家、复制、改名或删除原件。
2. **整理**：先扫描新增文章，按正文实质筛选并增量归入 `themes.json`。导语用于初筛，边界材料须读正文；保留旧主题顺序、学习证据、个人内容。索引只报告文件与匹配证据，不把旧档或空 NOTE 当作已学。
3. **学习**：复用已有笔记。从当前问题或上次停点开始，一次讲一个核心机制，给一个需要用户独立解释、预测或迁移的问题；收到回答后纠偏，再推进。用户要完整精读笔记时，使用 [笔记规范](references/obsidian-note-prompt.md)。已有 `NOTE.md` 的个人回答原样保留；AI讲解、用户原话、评价与待验证推断分区记录，不代填收获。
4. **归纳**：依据已有综述、实际新增来源与个人回答做增量更新，注明版本、支持证据、冲突和边界。`synthesized` 仅表示资料已纳入综述；跨公众号 `20_topics/` 按需更新。生成综述不自动提升个人掌握状态。

Opus 构建、Flash 解惑、Argon 归纳是用户选择的角色分工；实际调用什么工具或模型就如实记录。没有调用凭据时不把这些名称写成产物署名；当前助手可按授权承担同类工作。

## 来源与学习证据

- 原 PDF 是版面和物理页码基准；`content.txt`、HTML 与图片可辅助核对长代码。每种采集产物都可能缺失或截断，先核对同篇身份与关键内容，再使用；不把文件名或格式当成完整性证明。
- 新生成完整精读时通读正文并检查全部页图；定点勘误只检查必要来源，准确记录范围，不冒称重做全篇核验。原文主张、AI 推断、未运行代码和用户实测分别标明。
- `AI_精读.md` 存在表示笔记已生成，`NOTE.md` 存在表示记录已建立。用户学习状态只依据实际回答或实践，未记录就是未记录；索引状态及证据字段遵守目标库 `agent.md`。
- 引用按当前文件位置计算相对路径。常用库 inbox 文章到 `20_topics/` 为 `../../../20_topics/`；旧档文章为 `../../20_topics/`。实际检查目标存在。
- 旧档以原文 URL 优先匹配；仅标题相似不足以确认同篇，结合公众号、发布日期及版本证据。冲突列为候选；不混用不同采集版本的页码或哈希。

## 工具与收尾

在资料库根目录运行索引工具；`--scan-new` 是只读扫描，生成命令只更新 README，不替用户回答或重写学习状态：

```bash
python3 30_toolkit/generate_inbox_readme.py 00_inbox/腾讯云开发者 --scan-new
python3 30_toolkit/generate_inbox_readme.py --all
```

以下 `SKILL_DIR` 指本技能实际安装位置，`KB_ROOT` 指本次资料库：

```bash
python3 "$SKILL_DIR/scripts/kb_tools.py" check-notes --account "$KB_ROOT/00_inbox/腾讯云开发者"
python3 "$SKILL_DIR/scripts/kb_tools.py" verify --root "$KB_ROOT"
```

`check-notes` 检查结构，不证明理解或技术正确；核对实际检查数量，0 篇不能称笔记通过。`--sync-meta` 仅用于显式授权的旧档维护，不给 inbox 强造 META。

整理或改动索引前后执行全库只读链接与元数据核验，区分原有和新增问题。可证同篇且同版本时修复失效链接；无法确认的来源、个人引用或哈希异常如实列出，保留原件，不修改预期哈希来掩盖异常。纯学习问答无需每轮全库扫描。

交付本次变更、实际检查范围与剩余问题，然后回到当前学习问题。无需重新收集、全库重写或批量生产未请求的笔记。
