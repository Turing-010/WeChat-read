#!/usr/bin/env python3
"""Generate an enhanced README.md learning workbench & index for a WeChat inbox folder.

Capabilities:
1. Reads each article subfolder's metadata.json / data.json (official WeChat publish_time, title, author, url).
2. Automatically detects in-place study artifacts inside each article directory:
   - AI_精读.md (or AI_*.md): Opus deep study note
   - NOTE.md: Flash interactive Q&A & personal study notes
3. Automatically cross-references root-level legacy archive folders (大淘宝技术, 腾讯技术工程, 阿里技术, 数字生命卡兹克)
   to mark articles that already exist in the legacy archive and link directly to their existing AI summaries.
4. Supports theme-based learning aggregation via `themes.json` & `_themes/` synthesis articles:
   - Renders a Theme Learning Workbench (grouped by theme in recommended study order) + Chronological Full Index + Folded Skipped Articles.
   - Supports `--scan-new` to detect newly crawled articles not yet classified in `themes.json` for incremental updates.
"""

import argparse
import datetime
import json
import os
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple


LEGACY_ACCOUNT_DIRS = ["大淘宝技术", "腾讯技术工程", "阿里技术", "数字生命卡兹克"]


def normalize_title(title: str) -> str:
    """Normalize article title for cross-referencing against legacy archives."""
    if not title:
        return ""
    s = title.replace("&amp;", "&").replace("&quot;", '"').replace("&#39;", "'")
    s = s.replace("\u00a0", " ")
    return re.sub(r"[\s\W_]+", "", s).lower()


def load_legacy_archives(kb_root: Path) -> Dict[str, Dict]:
    """Scan root-level legacy account directories and index by normalized title and source_url."""
    by_title: Dict[str, Dict] = {}
    by_url: Dict[str, Dict] = {}

    for acc in LEGACY_ACCOUNT_DIRS:
        acc_dir = kb_root / acc
        if not acc_dir.is_dir():
            continue
        for item in acc_dir.iterdir():
            if not item.is_dir() or item.name.startswith("."):
                continue
            meta_file = item / "META.json"
            if not meta_file.exists():
                continue
            try:
                meta = json.loads(meta_file.read_text(encoding="utf-8"))
            except Exception:
                continue

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
                "account": acc,
                "dir_name": item.name,
                "abs_dir": item,
                "article_id": meta.get("article_id", ""),
                "title": title,
                "ai_summary": ai_summary if (ai_summary and (item / ai_summary).exists()) else None,
                "note": note_file if (note_file and (item / note_file).exists()) else None,
            }

            norm_t = normalize_title(title)
            if norm_t:
                by_title[norm_t] = record
            url = meta.get("source_url")
            if url:
                by_url[url.strip()] = record

    return {"by_title": by_title, "by_url": by_url}


def scan_article_folder(item: Path, folder: Path, legacy_index: Dict[str, Dict]) -> Dict:
    """Extract metadata, local study files, and legacy archive match for a single article subfolder."""
    meta_path = item / "metadata.json"
    data_path = item / "data.json"
    meta = {}
    if meta_path.exists():
        try:
            meta = json.loads(meta_path.read_text(encoding="utf-8"))
        except Exception as e:
            print(f"Warning: Failed to parse {meta_path}: {e}", file=sys.stderr)

    if not meta.get("publish_time") and data_path.exists():
        try:
            data_json = json.loads(data_path.read_text(encoding="utf-8"))
            if not meta:
                meta = data_json
            else:
                for k, v in data_json.items():
                    if k not in meta or not meta[k]:
                        meta[k] = v
        except Exception as e:
            print(f"Warning: Failed to parse {data_path}: {e}", file=sys.stderr)

    pdf_file = next((f.name for f in sorted(item.glob("*.pdf"))), None)
    html_file = next(
        (f.name for f in sorted(item.glob("*.html")) if not f.name.endswith("_raw.html")),
        None,
    )

    # Detect in-place study notes (AI_精读.md or AI_*.md) and personal NOTE.md
    ai_note_file = None
    if (item / "AI_精读.md").exists():
        ai_note_file = "AI_精读.md"
    else:
        ai_candidates = sorted(f.name for f in item.glob("AI_*.md"))
        if ai_candidates:
            ai_note_file = ai_candidates[0]

    user_note_file = "NOTE.md" if (item / "NOTE.md").exists() else None

    pub_ts = meta.get("publish_time")
    if pub_ts:
        pub_dt = datetime.datetime.fromtimestamp(pub_ts).strftime("%Y-%m-%d %H:%M")
        pub_date_short = datetime.datetime.fromtimestamp(pub_ts).strftime("%Y-%m-%d")
    else:
        pub_dt = "未知时间"
        pub_date_short = "未知日期"
        pub_ts = 0

    title = (meta.get("title") or item.name).replace("\\x26amp;", "&").replace("&amp;", "&")
    url = meta.get("url", "")
    author = (meta.get("author") or "").replace("\\x26amp;", "&").replace("&amp;", "&")

    # Check legacy archive match
    legacy_match = None
    if url and url.strip() in legacy_index["by_url"]:
        legacy_match = legacy_index["by_url"][url.strip()]
    else:
        norm_t = normalize_title(title) or normalize_title(item.name)
        if norm_t in legacy_index["by_title"]:
            legacy_match = legacy_index["by_title"][norm_t]

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
        study_parts.append(f"**[📘Opus精读](<{d}/{a['ai_note']}>)**")
    if a["user_note"]:
        study_parts.append(f"**[📝NOTE](<{d}/{a['user_note']}>)**")

    if a["legacy"]:
        leg = a["legacy"]
        rel_dir = os.path.relpath(leg["abs_dir"], folder)
        if leg["ai_summary"]:
            study_parts.append(f"[🔗旧档总结](<{rel_dir}/{leg['ai_summary']}>)")
        else:
            study_parts.append(f"[🔗旧档](<{rel_dir}/>)")

    base_str = " · ".join(parts) if parts else "—"
    if study_parts:
        return f"{base_str}<br>{' · '.join(study_parts)}"
    return base_str


def compute_article_status(a: Dict, theme_entry: Optional[Dict] = None) -> str:
    """Compute human-readable learning status badge for an article."""
    if theme_entry and theme_entry.get("synthesized"):
        return "✅ 已纳入综述"
    if a["ai_note"] or a["user_note"]:
        return "📖 已精读待归纳"
    if a["legacy"] and a["legacy"].get("ai_summary"):
        return "🔗 已有旧档"
    if theme_entry and theme_entry.get("is_new"):
        return "🆕 新增待学"
    return "⏳ 队列待学"


def scan_new_articles(folder_path: Path) -> int:
    """Print newly crawled articles that are not yet classified in themes.json."""
    folder = folder_path.resolve()
    themes_file = folder / "themes.json"
    known_dirs = set()
    if themes_file.exists():
        data = json.loads(themes_file.read_text(encoding="utf-8"))
        for t in data.get("themes", []):
            for item in t.get("articles", []):
                known_dirs.add(item["dir_name"])
        for s in data.get("skipped", []):
            known_dirs.add(s["dir_name"] if isinstance(s, dict) else s)

    new_items = []
    for item in sorted(folder.iterdir()):
        if not item.is_dir() or item.name.startswith(".") or item.name.startswith("_"):
            continue
        if item.name not in known_dirs:
            meta_f = item / "metadata.json"
            meta = json.loads(meta_f.read_text(encoding="utf-8")) if meta_f.exists() else {}
            txt_f = item / "content.txt"
            snippet = ""
            if txt_f.exists():
                raw_txt = txt_f.read_text(encoding="utf-8", errors="ignore")
                snippet = re.sub(r"\s+", " ", raw_txt)[:300]
            pub_ts = meta.get("publish_time", 0)
            pub_dt = (
                datetime.datetime.fromtimestamp(pub_ts).strftime("%Y-%m-%d")
                if pub_ts
                else "未知日期"
            )
            new_items.append((pub_ts, pub_dt, item.name, meta.get("author", ""), snippet))

    new_items.sort(reverse=True)
    print(f"=== {folder.name} 增量扫描结果：发现 {len(new_items)} 篇未归类新文章 ===")
    for idx, (_, pub_dt, dname, author, snippet) in enumerate(new_items, 1):
        print(f"[{idx}] {pub_dt} | 目录: {dname} | 作者: {author or '未知'}")
        if snippet:
            print(f"    摘要: {snippet}...")
    return len(new_items)


def generate_inbox_readme(folder_path: Path) -> Path:
    folder = folder_path.resolve()
    if not folder.is_dir():
        raise NotADirectoryError(f"Target folder does not exist or is not a directory: {folder}")

    # Locate knowledge base root (parent of 00_inbox)
    kb_root = folder.parent.parent if folder.parent.name == "00_inbox" else folder.parent
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
        try:
            themes_data = json.loads(themes_path.read_text(encoding="utf-8"))
        except Exception as e:
            print(f"Warning: Failed to parse {themes_path}: {e}", file=sys.stderr)

    lines: List[str] = []

    if themes_data:
        # Build theme lookup and track unclassified articles
        classified_dirs = set()
        dir_to_theme_badge: Dict[str, str] = {}
        dir_to_theme_entry: Dict[str, Dict] = {}

        themes_list = themes_data.get("themes", [])
        skipped_list = themes_data.get("skipped", [])

        for t in themes_list:
            tid = t.get("id", "")
            tname = t.get("name", "")
            for entry in t.get("articles", []):
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

        unclassified_articles = [
            a for a in articles_sorted if a["dir_name"] not in classified_dirs
        ]

        # Compute summary counts
        tech_articles = [
            articles_by_dir[d]
            for d in classified_dirs
            if dir_to_theme_badge.get(d) != "⏭️ 跳过"
        ]
        cnt_synthesized = 0
        cnt_learned = 0
        cnt_legacy = 0
        cnt_queued = 0
        for a in tech_articles:
            st = compute_article_status(a, dir_to_theme_entry.get(a["dir_name"]))
            if st.startswith("✅"):
                cnt_synthesized += 1
            elif st.startswith("📖"):
                cnt_learned += 1
            elif st.startswith("🔗"):
                cnt_legacy += 1
            else:
                cnt_queued += 1

        lines.extend(
            [
                f"# {folder.name} · 主题学习工作台与文章索引",
                "",
                f"> **四步学习闭环**：① `wechatMPtool` 收集入库 $\\to$ ② `README` 主题聚合索引（以 **PDF** 为基准） $\\to$ ③ **Opus** 初次深度构建（`AI_精读.md`）+ **Gemini Flash** 快速问答解惑（`NOTE.md`） $\\to$ ④ **Gemini Argon** 归纳演进主题综述（`_themes/*.md` & `20_topics/`）。",
                f">",
                f"> **当前收录统计**：共 **{len(articles_sorted)}** 篇 ｜ 有效技术干货 **{len(tech_articles)}** 篇（聚合为 **{len(themes_list)}** 大主题） ｜ 非技术/活动折叠 **{len(skipped_dirs)}** 篇 ｜ 待归类新文章 **{len(unclassified_articles)}** 篇",
                f"> **技术学习进度**：✅ 已纳入综述 **{cnt_synthesized}** 篇 ｜ 📖 已精读待归纳 **{cnt_learned}** 篇 ｜ 🔗 已有旧档总结 **{cnt_legacy}** 篇 ｜ ⏳ 队列待学 **{cnt_queued}** 篇",
                "",
            ]
        )

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
                "| 主题编号与名称 | 篇数 | 学习进度 | 主题综述产出（Gemini Argon） | 关联全库 20_topics 专题 |",
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
                if compute_article_status(articles_by_dir[e["dir_name"]], e).startswith(
                    ("✅", "📖", "🔗")
                )
            )
            synth_rel = t.get("synthesis_doc", f"_themes/{tid}_{tname}.md")
            synth_exists = (folder / synth_rel).exists()
            if synth_exists:
                synth_link = f"**[📘 {Path(synth_rel).stem}](<{synth_rel}>)**"
            else:
                synth_link = f"`待生成 ({synth_rel})`"

            related_topics = t.get("related_topics", [])
            topic_links = (
                " · ".join(f"[{ item['name'] }](<{ item['path'] }>)" for item in related_topics)
                if related_topics
                else "—"
            )
            lines.append(
                f"| [**{tid} · {tname}**](#{tid}) | {len(t_entries)} 篇 | `{done_cnt}/{len(t_entries)}` | {synth_link} | {topic_links} |"
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
            synth_exists = (folder / synth_rel).exists()
            synth_badge = (
                f"**[📘 打开主题综述文章](<{synth_rel}>)**"
                if synth_exists
                else f"⏳ 待使用 Gemini Argon 生成（预定路径：`{synth_rel}`）"
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
                    f"- **主题综述产出**：{synth_badge} ｜ **关联全库专题**：{topic_links}",
                    "",
                    "| 推荐序 | 学习状态 | 发布日期 | 文章原标题（作者） | 基准 PDF 与学习产物 | 一句话核心看点 |",
                    "| :---: | :---: | :---: | :--- | :--- | :--- |",
                ]
            )

            for idx, entry in enumerate(t.get("articles", []), 1):
                dname = entry["dir_name"]
                if dname not in articles_by_dir:
                    continue
                a = articles_by_dir[dname]
                status_str = compute_article_status(a, entry)
                safe_t = a["title"].replace("|", "\\|").replace("\n", " ")
                author_str = f"（{a['author']}）" if a["author"] else ""
                t_link = f"[{safe_t}](<{dname}/>){author_str}"
                focus = entry.get("focus", "—").replace("|", "\\|")
                lines.append(
                    f"| {idx} | {status_str} | {a['publish_date_short']} | {t_link} | {format_artifact_links(a, folder)} | {focus} |"
                )
            lines.append("")

        # Section 3: Folded Skipped Articles
        if skipped_dirs:
            lines.extend(
                [
                    "---",
                    "",
                    "## 三、 非技术 / 峰会宣传 / 社区通知（已折叠排除）",
                    "",
                    "<details>",
                    f"<summary>点击展开已过滤的 <b>{len(skipped_dirs)}</b> 篇非技术/活动通知文章（保留原文件夹，不进入技术学习主线）</summary>",
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
                "| 序号 | 发布时间 | 所属主题 | 学习状态 | 文章原标题 | 基准 PDF 与学习产物 |",
                "| :---: | :---: | :--- | :---: | :--- | :--- |",
            ]
        )
        for idx, a in enumerate(articles_sorted, 1):
            dname = a["dir_name"]
            t_badge = dir_to_theme_badge.get(dname, "🆕 未归类")
            if t_badge == "⏭️ 跳过":
                st = "⏭️ 跳过"
            else:
                st = compute_article_status(a, dir_to_theme_entry.get(dname))
            safe_t = a["title"].replace("|", "\\|").replace("\n", " ")
            t_link = f"[{safe_t}](<{dname}/>)"
            lines.append(
                f"| {idx} | {a['publish_date']} | {t_badge} | {st} | {t_link} | {format_artifact_links(a, folder)} |"
            )
        lines.extend(["", "</details>", ""])

    else:
        # No themes.json yet -> Render enhanced chronological table with in-place study & legacy archive detection
        cnt_learned = sum(1 for a in articles_sorted if a["ai_note"] or a["user_note"])
        cnt_legacy = sum(
            1 for a in articles_sorted if a["legacy"] and a["legacy"].get("ai_summary")
        )
        cnt_todo = len(articles_sorted) - cnt_learned - cnt_legacy

        lines.extend(
            [
                f"# {folder.name} 文章索引与学习进度",
                "",
                f"本目录收录来自「{folder.name}」公众号的文章材料，共 **{len(articles_sorted)}** 篇。",
                f"- **学习进度统计**：📖 本目录已生成精读/笔记 **{cnt_learned}** 篇 ｜ 🔗 根目录已有旧档总结 **{cnt_legacy}** 篇 ｜ ⏳ 待学习 **{cnt_todo}** 篇",
                f"- 所有文章按微信官方发布时间从**最新到旧**倒序排列（如需按学习主题聚类，可在当前目录配置 `themes.json`）：",
                "",
                "| 序号 | 发布时间 | 学习状态 | 文章原标题 | 基准 PDF 与学习产物 |",
                "| :---: | :---: | :---: | :--- | :--- |",
            ]
        )

        for idx, a in enumerate(articles_sorted, 1):
            safe_title = a["title"].replace("|", "\\|").replace("\n", " ")
            author_str = f"（{a['author']}）" if a["author"] else ""
            title_link = f"[{safe_title}](<{a['dir_name']}/>){author_str}"
            status_str = compute_article_status(a)
            lines.append(
                f"| {idx} | {a['publish_date']} | {status_str} | {title_link} | {format_artifact_links(a, folder)} |"
            )
        lines.append("")

    readme_path = folder / "README.md"
    readme_path.write_text("\n".join(lines), encoding="utf-8")
    return readme_path


def main():
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
        for sub in sorted(inbox_root.iterdir()):
            if sub.is_dir() and not sub.name.startswith("."):
                sub_dirs = [
                    d for d in sub.iterdir() if d.is_dir() and not d.name.startswith(".") and not d.name.startswith("_")
                ]
                if sub_dirs:
                    out = generate_inbox_readme(sub)
                    print(f"Updated README: {out} ({len(sub_dirs)} articles)")
        return

    target = Path(args.folder)
    if args.scan_new:
        scan_new_articles(target)
    else:
        out_file = generate_inbox_readme(target)
        print(f"README successfully generated at: {out_file}")


if __name__ == "__main__":
    main()
