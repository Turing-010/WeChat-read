#!/usr/bin/env python3
"""Generate an enhanced README.md learning workbench & index for a WeChat inbox folder.

Capabilities:
1. Reads each article subfolder's metadata.json / data.json (captured WeChat publish_time, title, author, url).
2. Automatically detects in-place study artifacts inside each article directory:
   - AI_精读.md (or AI_*.md): AI-generated study material (model not inferred)
   - NOTE.md: personal study records or their still-empty template
3. Automatically cross-references root-level legacy archive folders (大淘宝技术, 腾讯技术工程, 阿里技术, 数字生命卡兹克)
   to mark articles that already exist in the legacy archive and link directly to their existing AI summaries.
4. Supports theme-based learning aggregation via `themes.json` & `_themes/` synthesis articles:
   - Renders a Theme Learning Workbench (grouped by theme in recommended study order) + Chronological Full Index + Folded Skipped Articles.
   - Supports `--scan-new` to detect newly crawled articles not yet classified in `themes.json` for incremental updates.
   - Keeps insufficient source material in `pending`, distinct from skipped background material.
   - Supports an `overview_doc`, optional collapsed queues, and `learning_guide` documents without implying synthesis.
"""

import argparse
import datetime
import json
import os
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Dict, List, Optional, Tuple


LEGACY_ACCOUNT_DIRS = ["大淘宝技术", "腾讯技术工程", "阿里技术", "数字生命卡兹克"]
WECHAT_TIMEZONE = datetime.timezone(datetime.timedelta(hours=8), "Asia/Shanghai")
TIMEZONE_NOTICE = "> 发布时间统一展示为 Asia/Shanghai（UTC+8），不随运行电脑时区改变。"
LEARNING_LABELS = {
    "unrecorded": "未记录",
    "not_started": "未开始",
    "in_progress": "学习中",
    "can_explain": "能讲清",
    "can_apply": "能应用",
    "review_due": "复测到期",
    "pending_verification": "待核验",
}


def knowledge_base_root(folder: Path) -> Path:
    return folder.parent.parent if folder.parent.name == "00_inbox" else folder.parent


def read_json_object(path: Path) -> Dict:
    """Fail before writing an index when any input JSON cannot be trusted."""
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise ValueError(f"无法读取 JSON {path}: {exc}") from exc
    if not isinstance(data, dict):
        raise ValueError(f"JSON 顶层必须是对象: {path}")
    return data


def load_article_metadata(item: Path) -> Dict:
    meta = {}
    if not any((item / name).is_file() for name in ("metadata.json", "data.json")):
        raise ValueError(f"文章元数据缺失（metadata.json / data.json）: {item}")
    for name in ("metadata.json", "data.json"):
        path = item / name
        if path.exists():
            data = read_json_object(path)
            for key, value in data.items():
                if not meta.get(key):
                    meta[key] = value
    return meta


def normalize_title(title: str) -> str:
    """Normalize article title for cross-referencing against legacy archives."""
    if not title:
        return ""
    s = title.replace("&amp;", "&").replace("&quot;", '"').replace("&#39;", "'")
    s = s.replace("\u00a0", " ")
    return re.sub(r"[\s\W_]+", "", s).lower()


def load_legacy_archives(kb_root: Path) -> Dict[str, Dict]:
    """Scan root-level legacy account directories and index by normalized title and source_url."""
    by_title: Dict[str, List[Dict]] = {}
    by_url: Dict[str, List[Dict]] = {}

    for acc in LEGACY_ACCOUNT_DIRS:
        acc_dir = kb_root / acc
        if not acc_dir.is_dir():
            continue
        for item in sorted(acc_dir.iterdir()):
            if not item.is_dir() or item.name.startswith("."):
                continue
            meta_file = item / "META.json"
            if not meta_file.exists():
                continue
            meta = read_json_object(meta_file)

            title = meta.get("title", "")
            files = meta.get("files") or {}
            ai_summary = files.get("ai_summary")
            if not ai_summary:
                ai_candidates = sorted(item.glob("AI_*.md"))
                if ai_candidates:
                    ai_summary = ai_candidates[0].name

            note_file = files.get("note")
            if not note_file and (item / "NOTE.md").exists():
                note_file = "NOTE.md"

            record = {
                "account": meta.get("account") or acc,
                "dir_name": item.name,
                "abs_dir": item,
                "article_id": meta.get("article_id", ""),
                "title": title,
                "published_date": str(meta.get("published_at") or "")[:10],
                "ai_summary": ai_summary if (ai_summary and (item / ai_summary).exists()) else None,
                "note": note_file if (note_file and (item / note_file).exists()) else None,
            }

            norm_t = normalize_title(title)
            if norm_t:
                by_title.setdefault(norm_t, []).append(record)
            url = meta.get("source_url")
            if url:
                by_url.setdefault(url.strip(), []).append(record)

    return {"by_title": by_title, "by_url": by_url}


def match_legacy_archive(meta: Dict, item: Path, folder: Path, publish_date: str, legacy_index: Dict) -> Tuple[Optional[Dict], List[Dict]]:
    """URL takes priority; a title alone only proposes candidates.

    Title fallback requires both matching account and publication date and must
    identify one record. All collisions remain visible instead of overwriting.
    """
    url = (meta.get("url") or "").strip()
    candidates = legacy_index["by_url"].get(url, []) if url else []
    if len(candidates) == 1:
        return candidates[0], []
    if not candidates:
        title = normalize_title(meta.get("title") or item.name)
        candidates = legacy_index["by_title"].get(title, [])
        account = meta.get("source") or meta.get("account") or folder.name
        corroborated = [candidate for candidate in candidates
                        if candidate["account"] == account
                        and candidate["published_date"] == publish_date
                        and publish_date != "未知日期"]
        if len(corroborated) == 1:
            return corroborated[0], []
    if candidates:
        print(f"Warning: 旧档关联待核验 {item}: 找到 {len(candidates)} 个候选，未唯一确认原文 URL 或公众号与发布日期。", file=sys.stderr)
    return None, candidates


def scan_article_folder(item: Path, folder: Path, legacy_index: Dict[str, Dict]) -> Dict:
    """Extract metadata, local study files, and legacy archive match for a single article subfolder."""
    meta = load_article_metadata(item)

    pdf_file = next((f.name for f in sorted(item.glob("*.pdf"))), None)
    html_file = next(
        (f.name for f in sorted(item.glob("*.html")) if not f.name.endswith("_raw.html")),
        None,
    )

    # Detect in-place study notes (AI_精读.md or AI_*.md) and personal NOTE.md
    ai_note_file = None
    if (item / "AI_精读.md").is_file():
        ai_note_file = "AI_精读.md"
    else:
        ai_candidates = sorted(f.name for f in item.glob("AI_*.md") if f.is_file())
        if ai_candidates:
            ai_note_file = ai_candidates[0]

    user_note_file = "NOTE.md" if (item / "NOTE.md").is_file() else None

    pub_ts = meta.get("publish_time")
    if pub_ts:
        pub_dt = datetime.datetime.fromtimestamp(pub_ts, WECHAT_TIMEZONE).strftime("%Y-%m-%d %H:%M")
        pub_date_short = datetime.datetime.fromtimestamp(pub_ts, WECHAT_TIMEZONE).strftime("%Y-%m-%d")
    else:
        pub_dt = "未知时间"
        pub_date_short = "未知日期"
        pub_ts = 0

    title = (meta.get("title") or item.name).replace("\\x26amp;", "&").replace("&amp;", "&")
    url = meta.get("url", "")
    author = (meta.get("author") or "").replace("\\x26amp;", "&").replace("&amp;", "&")

    # Check legacy archive match
    legacy_match, legacy_candidates = match_legacy_archive(meta, item, folder, pub_date_short, legacy_index)

    return {
        "dir_name": item.name,
        "title": title,
        "author": author,
        "publish_time": pub_ts,
        "publish_date": pub_dt,
        "publish_date_short": pub_date_short,
        "pdf": pdf_file,
        "html": html_file,
        "url": url,
        "ai_note": ai_note_file,
        "user_note": user_note_file,
        "legacy": legacy_match,
        "legacy_candidates": legacy_candidates,
    }


def format_artifact_links(a: Dict, folder: Path) -> str:
    """Format compact links for PDF, HTML, WeChat URL, in-place AI_精读/NOTE, and legacy archive."""
    parts = []
    d = a["dir_name"]
    if a["pdf"]:
        parts.append(f"[PDF](<{d}/{a['pdf']}>)")
    if a["html"]:
        parts.append(f"[HTML](<{d}/{a['html']}>)")
    if a["url"]:
        parts.append(f"[原文]({a['url']})")

    study_parts = []
    if a["ai_note"]:
        study_parts.append(f"**[📘AI精读](<{d}/{a['ai_note']}>)**")
    if a["user_note"]:
        study_parts.append(f"**[📝NOTE](<{d}/{a['user_note']}>)**")

    if a["legacy"]:
        leg = a["legacy"]
        rel_dir = os.path.relpath(leg["abs_dir"], folder)
        if leg["ai_summary"]:
            study_parts.append(f"[🔗旧档总结](<{rel_dir}/{leg['ai_summary']}>)")
        else:
            study_parts.append(f"[🔗旧档](<{rel_dir}/>)")
    for candidate in a.get("legacy_candidates", []):
        rel_dir = os.path.relpath(candidate["abs_dir"], folder)
        study_parts.append(f"[⚠️旧档候选·{candidate['account']}（待核验）](<{rel_dir}/>)")

    base_str = " · ".join(parts) if parts else "—"
    if study_parts:
        return f"{base_str}<br>{' · '.join(study_parts)}"
    return base_str


def compute_article_status(a: Dict, theme_entry: Optional[Dict] = None, folder: Optional[Path] = None) -> str:
    """Describe available material, never infer the reader's learning state."""
    if theme_entry and theme_entry.get("synthesized"):
        if theme_entry.get("document_kind") == "learning_guide":
            return "⚠️ 综述标记待核验（目标仅为导学）"
        synthesis_doc = theme_entry.get("synthesis_doc")
        if not (folder and synthesis_doc and (folder / synthesis_doc).is_file()):
            return "⚠️ 已标记纳入综述（待核验：综述文件缺失）"
        return "✅ 已纳入综述"
    if a["ai_note"]:
        return "📘 AI笔记已生成"
    if a["user_note"]:
        return "📝 已建学习记录"
    if a["legacy"]:
        return "🔗 已有旧档"
    if a.get("legacy_candidates"):
        return "⚠️ 旧档候选待核验"
    if theme_entry and theme_entry.get("is_new"):
        return "🆕 新增资料"
    return "📄 已收录原文"


def learning_state(theme_entry: Optional[Dict], folder: Path) -> str:
    """Validate recorded status and evidence paths, not the learner's mastery.

    learning_evidence is a path or list of paths relative to the account folder;
    absolute paths are allowed only inside this knowledge library. Markdown
    fragments are allowed, but fragment contents are not assessed here.
    """
    entry = theme_entry or {}
    status = entry.get("learning_status")
    if status is None or status == "":
        return "unrecorded"
    if status in ("not_started", "in_progress"):
        return status
    if status not in ("can_explain", "can_apply", "review_due"):
        return "pending_verification"
    evidence = entry.get("learning_evidence")
    paths = [evidence] if isinstance(evidence, str) else evidence
    if not isinstance(paths, list) or not paths:
        return "pending_verification"
    kb_root = knowledge_base_root(folder).resolve()
    for value in paths:
        if not isinstance(value, str) or not value.split("#", 1)[0].strip():
            return "pending_verification"
        path = (folder / value.split("#", 1)[0]).resolve()
        if not path.is_relative_to(kb_root) or not path.is_file():
            return "pending_verification"
    return status


def compute_learning_status(theme_entry: Optional[Dict], folder: Path) -> str:
    """Format an explicit personal record, without deriving it from artifacts."""
    state = learning_state(theme_entry, folder)
    if state == "pending_verification":
        claimed = (theme_entry or {}).get("learning_status")
        label = LEARNING_LABELS.get(claimed, "学习状态无效") if isinstance(claimed, str) else "学习状态无效"
        return f"⚠️ 待核验（申报：{label}）"
    return LEARNING_LABELS[state]


def learning_summary(entries: List[Optional[Dict]], folder: Path) -> str:
    counts = Counter(learning_state(entry, folder) for entry in entries)
    return "> **个人记录统计**：" + " ｜ ".join(
        f"{label} **{counts[state]}** 篇" for state, label in LEARNING_LABELS.items()
    )


def validate_pending_classification(data: Dict, path: Path) -> None:
    """Reject duplicate or contradictory pending entries before rendering or scanning."""
    classified = {entry["dir_name"] for theme in data.get("themes", [])
                  for entry in theme.get("articles", [])}
    classified.update(entry["dir_name"] if isinstance(entry, dict) else entry
                      for entry in data.get("skipped", []))
    seen = set()
    for entry in data.get("pending", []):
        dname = entry["dir_name"]
        if dname in seen or dname in classified:
            raise ValueError(f"{path}: pending 重复或与主题/跳过清单冲突: {dname}")
        seen.add(dname)


def scan_new_articles(folder_path: Path) -> int:
    """Print newly crawled articles that are not yet classified in themes.json."""
    folder = folder_path.resolve()
    themes_file = folder / "themes.json"
    known_dirs = set()
    pending_count = 0
    if themes_file.exists():
        data = read_json_object(themes_file)
        validate_pending_classification(data, themes_file)
        for t in data.get("themes", []):
            for item in t.get("articles", []):
                known_dirs.add(item["dir_name"])
        for s in data.get("skipped", []):
            known_dirs.add(s["dir_name"] if isinstance(s, dict) else s)
        for s in data.get("pending", []):
            dname = s["dir_name"]
            known_dirs.add(dname)
            pending_count += (folder / dname).is_dir()

    new_items = []
    for item in sorted(folder.iterdir()):
        if not item.is_dir() or item.name.startswith(".") or item.name.startswith("_"):
            continue
        if item.name not in known_dirs:
            meta = load_article_metadata(item)
            txt_f = item / "content.txt"
            snippet = ""
            if txt_f.exists():
                raw_txt = txt_f.read_text(encoding="utf-8", errors="ignore")
                snippet = re.sub(r"\s+", " ", raw_txt)[:300]
            pub_ts = meta.get("publish_time", 0)
            pub_dt = (
                datetime.datetime.fromtimestamp(pub_ts, WECHAT_TIMEZONE).strftime("%Y-%m-%d")
                if pub_ts
                else "未知日期"
            )
            new_items.append((pub_ts, pub_dt, item.name, meta.get("author", ""), snippet))

    new_items.sort(reverse=True)
    print(f"=== {folder.name} 增量扫描结果：发现 {len(new_items)} 篇未归类新文章 ===")
    print("发布时间时区：Asia/Shanghai（UTC+8）")
    if pending_count:
        print(f"另有待核验 {pending_count} 篇，详见 themes.json 的 pending；补齐材料后重新评估，不算已完成技术分类。")
    for idx, (_, pub_dt, dname, author, snippet) in enumerate(new_items, 1):
        print(f"[{idx}] {pub_dt} | 目录: {dname} | 作者: {author or '未知'}")
        if snippet:
            print(f"    摘要: {snippet}...")
    return len(new_items)


def render_inbox_readme(folder_path: Path) -> str:
    """Read and render the complete index without modifying any library file."""
    folder = folder_path.resolve()
    if not folder.is_dir():
        raise NotADirectoryError(f"Target folder does not exist or is not a directory: {folder}")

    # Locate knowledge base root (parent of 00_inbox)
    kb_root = knowledge_base_root(folder)
    legacy_index = load_legacy_archives(kb_root)

    articles_by_dir: Dict[str, Dict] = {}
    for item in folder.iterdir():
        if not item.is_dir() or item.name.startswith(".") or item.name.startswith("_"):
            continue
        info = scan_article_folder(item, folder, legacy_index)
        articles_by_dir[item.name] = info

    articles_sorted = sorted(
        articles_by_dir.values(), key=lambda x: (x["publish_time"], x["dir_name"]), reverse=True
    )

    themes_path = folder / "themes.json"
    themes_data = None
    if themes_path.exists():
        themes_data = read_json_object(themes_path)
        validate_pending_classification(themes_data, themes_path)

    lines: List[str] = []

    if themes_data:
        # Build theme lookup and track unclassified articles
        classified_dirs = set()
        dir_to_theme_badge: Dict[str, str] = {}
        dir_to_theme_entry: Dict[str, Dict] = {}

        themes_list = themes_data.get("themes", [])
        skipped_list = themes_data.get("skipped", [])
        pending_dirs = []

        for t in themes_list:
            tid = t.get("id", "")
            tname = t.get("name", "")
            for entry in t.get("articles", []):
                entry["synthesis_doc"] = t.get("synthesis_doc", f"_themes/{tid}_{tname}.md")
                entry["document_kind"] = t.get("document_kind")
                dname = entry["dir_name"]
                if dname in articles_by_dir:
                    classified_dirs.add(dname)
                    dir_to_theme_badge[dname] = f"`{tid}` {tname}"
                    dir_to_theme_entry[dname] = entry

        skipped_dirs: List[Tuple[str, str]] = []
        for s in skipped_list:
            if isinstance(s, dict):
                dname = s.get("dir_name", "")
                reason = s.get("reason", "活动/峰会宣传/非技术内容")
            else:
                dname = str(s)
                reason = "活动/峰会宣传/非技术内容"
            if dname in articles_by_dir:
                classified_dirs.add(dname)
                dir_to_theme_badge[dname] = "⏭️ 跳过"
                skipped_dirs.append((dname, reason))

        for item in themes_data.get("pending", []):
            dname = item["dir_name"]
            if dname in articles_by_dir:
                classified_dirs.add(dname)
                dir_to_theme_badge[dname] = "⚠️ 材料待核验"
                pending_dirs.append((dname, item.get("reason", "材料依据不足，待核验")))

        unclassified_articles = [
            a for a in articles_sorted if a["dir_name"] not in classified_dirs
        ]

        # Compute summary counts
        tech_articles = [
            articles_by_dir[d]
            for d in classified_dirs
            if d in dir_to_theme_entry
        ]
        cnt_synthesized = 0
        cnt_ai = 0
        cnt_note = 0
        cnt_legacy = 0
        cnt_queued = 0
        cnt_unverified = 0
        for a in tech_articles:
            st = compute_article_status(a, dir_to_theme_entry.get(a["dir_name"]), folder)
            if st.startswith("✅"):
                cnt_synthesized += 1
            elif st.startswith("📘"):
                cnt_ai += 1
            elif st.startswith("📝"):
                cnt_note += 1
            elif st.startswith("🔗"):
                cnt_legacy += 1
            elif st.startswith("⚠️"):
                cnt_unverified += 1
            else:
                cnt_queued += 1

        lines.extend(
            [
                f"# {folder.name} · 主题学习工作台与文章索引",
                "",
                TIMEZONE_NOTICE,
                "> **四步学习闭环**：① 收集原文 $\\to$ ② 主题索引 $\\to$ ③ AI 辅助精读与本人问答/复述 $\\to$ ④ 跨文归纳。模型承担辅助角色，文件名不证明使用过某个模型；资料状态与个人学习记录分别统计。",
                f">",
                f"> **当前收录统计**：共 **{len(articles_sorted)}** 篇 ｜ 按既有分类纳入主题 **{len(tech_articles)}** 篇（聚合为 **{len(themes_list)}** 大主题） ｜ {themes_data.get('skipped_label', '非技术/活动折叠')} **{len(skipped_dirs)}** 篇 ｜ 待核验材料 **{len(pending_dirs)}** 篇 ｜ 待归类新文章 **{len(unclassified_articles)}** 篇",
                f"> **技术文章资料统计（互斥分类）**：✅ 已纳入综述 **{cnt_synthesized}** 篇 ｜ 📘 AI笔记已生成 **{cnt_ai}** 篇 ｜ 📝 已建学习记录 **{cnt_note}** 篇 ｜ 🔗 已有旧档 **{cnt_legacy}** 篇 ｜ ⚠️ 资料待核验 **{cnt_unverified}** 篇 ｜ 📄 其他已收录 **{cnt_queued}** 篇",
                learning_summary([dir_to_theme_entry.get(a["dir_name"]) for a in tech_articles], folder),
                "> **个人学习状态**独立记录；未记录不代表未读，资料生成不代表本人已学会。",
                "> 有证据的完成数仅计“能讲清 / 能应用”；“复测到期”另列。脚本只核验记录及本库证据文件是否存在，不评判证据内容或本人掌握程度。",
                "",
            ]
        )

        overview_doc = themes_data.get("overview_doc")
        if overview_doc and (folder / overview_doc).is_file():
            lines.extend([f"**从这里开始：[学习路线与首篇样板](<{overview_doc}>)**", ""])

        if pending_dirs:
            lines.extend(["## 待核验材料（不预判为非技术）", "", "<details>",
                          f"<summary>展开 {len(pending_dirs)} 篇材料缺口与待判项</summary>", "",
                          "| 文章 | 待核验原因 | 现有材料 |", "| --- | --- | --- |"])
            for dname, reason in pending_dirs:
                a = articles_by_dir[dname]
                safe_title = a['title'].replace('|', '\\|').replace('\n', ' ')
                safe_reason = reason.replace('|', '\\|').replace('\n', ' ')
                lines.append(f"| [{safe_title}](<{dname}/>) | {safe_reason} | {format_artifact_links(a, folder)} |")
            lines.extend(["", "</details>", ""])

        # If there are newly crawled unclassified articles, highlight them at the very top!
        if unclassified_articles:
            lines.extend(
                [
                    "## 🆕 待归类新增文章（增量扫描发现）",
                    "",
                    "以下文章为最新爬入、尚未归入 `themes.json` 的新文章。可运行 `python3 30_toolkit/generate_inbox_readme.py --scan-new` 并交由 AI 增量归入下方对应主题：",
                    "",
                    "| 序号 | 发布时间 | 文章原标题 | 基准与学习产物 |",
                    "| :---: | :---: | :--- | :--- |",
                ]
            )
            for idx, a in enumerate(unclassified_articles, 1):
                safe_t = a["title"].replace("|", "\\|").replace("\n", " ")
                t_link = f"[{safe_t}](<{a['dir_name']}/>)"
                lines.append(
                    f"| {idx} | {a['publish_date_short']} | {t_link} | {format_artifact_links(a, folder)} |"
                )
            lines.append("")

        # Section 1: Theme Overview Table
        lines.extend(
            [
                "## 一、 学习主题总览（按主题模块推进）",
                "",
                "| 主题编号与名称 | 篇数 | 有证据的个人学习记录 | 主题导学 / 综述 | 关联全库 20_topics 专题 |",
                "| :--- | :---: | :---: | :--- | :--- |",
            ]
        )
        for t in themes_list:
            tid = t.get("id", "")
            tname = t.get("name", "")
            t_entries = [
                e for e in t.get("articles", []) if e["dir_name"] in articles_by_dir
            ]
            done_cnt = sum(
                1
                for e in t_entries
                if learning_state(e, folder) in ("can_explain", "can_apply")
            )
            review_count = sum(learning_state(e, folder) == "review_due" for e in t_entries)
            synth_rel = t.get("synthesis_doc", f"_themes/{tid}_{tname}.md")
            synth_exists = (folder / synth_rel).is_file()
            if synth_exists:
                kind = "导学（尚未归纳）" if t.get("document_kind") == "learning_guide" else "综述"
                synth_link = f"**[📘 {Path(synth_rel).stem} · {kind}](<{synth_rel}>)**"
            else:
                synth_link = f"`待生成 ({synth_rel})`"

            related_topics = t.get("related_topics", [])
            topic_links = (
                " · ".join(f"[{ item['name'] }](<{ item['path'] }>)" for item in related_topics)
                if related_topics
                else "—"
            )
            lines.append(
                f"| [**{tid} · {tname}**](#{tid}) | {len(t_entries)} 篇 | `{done_cnt}/{len(t_entries)}`；复测到期 {review_count} 篇 | {synth_link} | {topic_links} |"
            )
        lines.append("")

        # Section 2: Detailed Theme Tables
        lines.extend(
            [
                "---",
                "",
                "## 二、 分主题学习课表（按推荐认知顺序排列）",
                "",
            ]
        )

        for t in themes_list:
            tid = t.get("id", "")
            tname = t.get("name", "")
            question = t.get("core_question", "")
            synth_rel = t.get("synthesis_doc", f"_themes/{tid}_{tname}.md")
            synth_exists = (folder / synth_rel).is_file()
            kind = "导学（尚未归纳）" if t.get("document_kind") == "learning_guide" else "主题综述"
            synth_badge = (
                f"**[📘 打开{kind}](<{synth_rel}>)**"
                if synth_exists
                else f"⏳ 待生成综述（预定路径：`{synth_rel}`）"
            )
            related_topics = t.get("related_topics", [])
            topic_links = (
                " · ".join(f"[{ item['name'] }](<{ item['path'] }>)" for item in related_topics)
                if related_topics
                else "—"
            )

            lines.extend(
                [
                    f"<a id=\"{tid}\"></a>",
                    f"### {tid} · {tname}",
                    "",
                    f"- **核心问题**：{question}",
                    f"- **主题文档**：{synth_badge} ｜ **关联全库专题**：{topic_links}",
                    "",
                    *(["<details>", "<summary>展开本主题完整阅读队列（优先从上方导学进入）</summary>", ""]
                      if themes_data.get("collapse_theme_tables") else []),
                    "| 推荐序 | 资料状态 | 个人学习状态 | 发布日期 | 文章原标题（作者） | 基准 PDF 与学习产物 | 一句话核心看点 |",
                    "| :---: | :---: | :---: | :---: | :--- | :--- | :--- |",
                ]
            )

            for idx, entry in enumerate(t.get("articles", []), 1):
                dname = entry["dir_name"]
                if dname not in articles_by_dir:
                    continue
                a = articles_by_dir[dname]
                status_str = compute_article_status(a, entry, folder)
                safe_t = a["title"].replace("|", "\\|").replace("\n", " ")
                author_str = f"（{a['author']}）" if a["author"] else ""
                t_link = f"[{safe_t}](<{dname}/>){author_str}"
                focus = entry.get("focus", "—").replace("|", "\\|")
                lines.append(
                    f"| {idx} | {status_str} | {compute_learning_status(entry, folder)} | {a['publish_date_short']} | {t_link} | {format_artifact_links(a, folder)} | {focus} |"
                )
            lines.append("")
            if themes_data.get("collapse_theme_tables"):
                lines.extend(["</details>", ""])

        # Section 3: Folded Skipped Articles
        if skipped_dirs:
            lines.extend(
                [
                    "---",
                    "",
                    f"## 三、 {themes_data.get('skipped_label', '非技术 / 峰会宣传 / 社区通知')}（暂不进入学习主线）",
                    "",
                    "<details>",
                    f"<summary>点击展开 <b>{len(skipped_dirs)}</b> 篇折叠材料及处理原因（保留原文件夹）</summary>",
                    "",
                    "| 序号 | 发布时间 | 文章原标题 | 过滤原因 | 原文链接 |",
                    "| :---: | :---: | :--- | :--- | :---: |",
                ]
            )
            # Sort skipped by publish_time desc
            skipped_sorted = sorted(
                skipped_dirs,
                key=lambda x: articles_by_dir[x[0]]["publish_time"],
                reverse=True,
            )
            for idx, (dname, reason) in enumerate(skipped_sorted, 1):
                a = articles_by_dir[dname]
                safe_t = a["title"].replace("|", "\\|").replace("\n", " ")
                t_link = f"[{safe_t}](<{dname}/>)"
                pdf_link = f"[PDF](<{dname}/{a['pdf']}>)" if a["pdf"] else "—"
                lines.append(
                    f"| {idx} | {a['publish_date_short']} | {t_link} | {reason} | {pdf_link} |"
                )
            lines.extend(["", "</details>", ""])

        # Section 4: Full Chronological Index
        lines.extend(
            [
                "---",
                "",
                "## 四、 按微信发布时间倒序全量索引",
                "",
                "<details>",
                f"<summary>点击展开全部 <b>{len(articles_sorted)}</b> 篇文章的时间线倒序总表</summary>",
                "",
                "| 序号 | 发布时间 | 所属主题 | 资料状态 | 个人学习状态 | 文章原标题 | 基准 PDF 与学习产物 |",
                "| :---: | :---: | :--- | :---: | :---: | :--- | :--- |",
            ]
        )
        for idx, a in enumerate(articles_sorted, 1):
            dname = a["dir_name"]
            t_badge = dir_to_theme_badge.get(dname, "🆕 未归类")
            if t_badge in ("⏭️ 跳过", "⚠️ 材料待核验"):
                st = t_badge
            else:
                st = compute_article_status(a, dir_to_theme_entry.get(dname), folder)
            safe_t = a["title"].replace("|", "\\|").replace("\n", " ")
            t_link = f"[{safe_t}](<{dname}/>)"
            lines.append(
                f"| {idx} | {a['publish_date']} | {t_badge} | {st} | {compute_learning_status(dir_to_theme_entry.get(dname), folder)} | {t_link} | {format_artifact_links(a, folder)} |"
            )
        lines.extend(["", "</details>", ""])

    else:
        # No themes.json yet -> Render enhanced chronological table with in-place study & legacy archive detection
        counts = Counter(compute_article_status(a) for a in articles_sorted)
        cnt_ai = counts["📘 AI笔记已生成"]
        cnt_note = counts["📝 已建学习记录"]
        cnt_legacy = counts["🔗 已有旧档"]
        cnt_unverified = counts["⚠️ 旧档候选待核验"]
        cnt_other = len(articles_sorted) - cnt_ai - cnt_note - cnt_legacy - cnt_unverified

        lines.extend(
            [
                f"# {folder.name} 文章索引与学习记录",
                "",
                TIMEZONE_NOTICE,
                f"本目录收录来自「{folder.name}」公众号的文章材料，共 **{len(articles_sorted)}** 篇。",
                f"- **资料统计（互斥分类）**：📘 AI笔记已生成 **{cnt_ai}** 篇 ｜ 📝 已建学习记录 **{cnt_note}** 篇 ｜ 🔗 已有旧档 **{cnt_legacy}** 篇 ｜ ⚠️ 旧档候选待核验 **{cnt_unverified}** 篇 ｜ 📄 其他已收录 **{cnt_other}** 篇",
                learning_summary([None] * len(articles_sorted), folder),
                "> 未记录不代表未读，资料生成不代表本人已学会；个人学习记录可在 themes.json 的文章条目中明确填写。",
                f"- 所有文章按微信官方发布时间从**最新到旧**倒序排列（如需按学习主题聚类，可在当前目录配置 `themes.json`）：",
                "",
                "| 序号 | 发布时间 | 资料状态 | 个人学习状态 | 文章原标题 | 基准 PDF 与学习产物 |",
                "| :---: | :---: | :---: | :---: | :--- | :--- |",
            ]
        )

        for idx, a in enumerate(articles_sorted, 1):
            safe_title = a["title"].replace("|", "\\|").replace("\n", " ")
            author_str = f"（{a['author']}）" if a["author"] else ""
            title_link = f"[{safe_title}](<{a['dir_name']}/>){author_str}"
            status_str = compute_article_status(a)
            lines.append(
                f"| {idx} | {a['publish_date']} | {status_str} | 未记录 | {title_link} | {format_artifact_links(a, folder)} |"
            )
        lines.append("")

    return "\n".join(lines)


def generate_inbox_readme(folder_path: Path) -> Path:
    rendered = render_inbox_readme(folder_path)
    readme_path = folder_path.resolve() / "README.md"
    readme_path.write_text(rendered, encoding="utf-8")
    return readme_path


def run_cli():
    parser = argparse.ArgumentParser(
        description="Generate enhanced README.md learning workbench & index for an inbox articles folder."
    )
    parser.add_argument(
        "folder",
        nargs="?",
        default="00_inbox/腾讯云开发者",
        help="Path to articles inbox directory (default: 00_inbox/腾讯云开发者)",
    )
    parser.add_argument(
        "--scan-new",
        action="store_true",
        help="Scan and list newly crawled articles not yet classified in themes.json",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Update README.md for all official account folders under 00_inbox/",
    )
    args = parser.parse_args()

    if args.all:
        inbox_root = Path("00_inbox").resolve()
        pending = []
        for sub in sorted(inbox_root.iterdir()):
            if sub.is_dir() and not sub.name.startswith((".", "_")):
                sub_dirs = [
                    d for d in sub.iterdir() if d.is_dir() and not d.name.startswith(".") and not d.name.startswith("_")
                ]
                if sub_dirs:
                    if args.scan_new:
                        scan_new_articles(sub)
                    else:
                        pending.append((sub / "README.md", render_inbox_readme(sub), len(sub_dirs)))
        # Parse every account before replacing any README in the batch.
        for out, rendered, count in pending:
            out.write_text(rendered, encoding="utf-8")
            print(f"Updated README: {out} ({count} articles)")
        return

    target = Path(args.folder)
    if args.scan_new:
        scan_new_articles(target)
    else:
        out_file = generate_inbox_readme(target)
        print(f"README successfully generated at: {out_file}")


def main():
    try:
        run_cli()
    except (ValueError, OSError, TypeError, KeyError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
