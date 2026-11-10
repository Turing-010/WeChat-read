"""Regression checks using disposable libraries; never writes the real inbox."""

import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

import generate_inbox_readme as indexer


class InboxIndexTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="inbox-index-test-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.folder = self.root / "00_inbox" / "测试公众号"
        self.folder.mkdir(parents=True)

    def article(self, name="示例文章", **metadata):
        article = self.folder / name
        article.mkdir(exist_ok=True)
        data = {"title": name, "publish_time": 1788223500, "source": self.folder.name}
        data.update(metadata)
        (article / "metadata.json").write_text(json.dumps(data), encoding="utf-8")
        return article

    def themes(self, entries, **theme_fields):
        theme = {"id": "T01", "name": "测试主题", "articles": entries,
                 "synthesis_doc": "_themes/T01.md"}
        theme.update(theme_fields)
        (self.folder / "themes.json").write_text(
            json.dumps({"themes": [theme], "skipped": []}), encoding="utf-8")

    def legacy(self, name="旧档示例", **metadata):
        article = self.root / "腾讯技术工程" / name
        article.mkdir(parents=True, exist_ok=True)
        data = {"title": "示例文章", "account": "腾讯技术工程",
                "published_at": "2026-09-01", "files": {"ai_summary": "AI_summary.md"}}
        data.update(metadata)
        (article / "META.json").write_text(json.dumps(data), encoding="utf-8")
        (article / "AI_summary.md").write_text("旧档 AI 摘要", encoding="utf-8")
        return article

    def render(self):
        return indexer.generate_inbox_readme(self.folder).read_text(encoding="utf-8")

    def cli(self, *args, env=None):
        return subprocess.run(
            [sys.executable, "-B", str(Path(indexer.__file__).resolve()), *args],
            cwd=self.root, capture_output=True, text=True, env=env)

    def test_generated_material_and_empty_note_do_not_claim_personal_learning(self):
        article = self.article()
        (article / "AI_精读.md").write_text("AI 导读", encoding="utf-8")
        (article / "NOTE.md").write_text("我的回答：（待填写）", encoding="utf-8")
        self.themes([{"dir_name": article.name}])

        readme = self.render()

        self.assertIn("📘 AI笔记已生成", readme)
        self.assertIn("个人学习状态", readme)
        self.assertIn("未记录", readme)
        self.assertIn("`0/1`", readme)
        self.assertNotIn("已精读待归纳", readme)
        self.assertNotIn("Opus精读", readme)

    def test_learning_claims_require_existing_evidence_inside_this_library(self):
        entries = []
        cases = [
            ("无记录", None, None, "未记录"),
            ("未开始", "not_started", None, "未开始"),
            ("进行中", "in_progress", None, "学习中"),
            ("讲清且有证据", "can_explain", "valid", "能讲清"),
            ("应用且有证据", "can_apply", "valid", "能应用"),
            ("复测", "review_due", "valid", "复测到期"),
            ("证据丢失", "can_explain", "missing.md", "待核验"),
            ("未提供证据", "can_apply", None, "待核验"),
            ("库外证据", "can_apply", str(Path(indexer.__file__).resolve()), "待核验"),
        ]
        for name, state, evidence, _ in cases:
            article = self.article(name)
            entry = {"dir_name": name}
            if state:
                entry["learning_status"] = state
            if evidence == "valid":
                (article / "NOTE.md").write_text("本人复述记录", encoding="utf-8")
                evidence = f"{name}/NOTE.md#我的复述"
            if evidence:
                entry["learning_evidence"] = evidence
            entries.append(entry)
        self.themes(entries)

        readme = self.render()

        for name, _, _, expected in cases:
            row = next(line for line in readme.splitlines() if f"[{name}]" in line)
            self.assertIn(expected, row, name)
        self.assertIn("`2/9`", readme)
        self.assertIn("复测到期 **1** 篇", readme)
        self.assertIn("待核验 **3** 篇", readme)
        self.assertIn("个人记录统计", readme)

    def test_synthesized_flag_needs_the_theme_document_and_never_marks_learning(self):
        article = self.article()
        self.themes([{"dir_name": article.name, "synthesized": True}])

        readme = self.render()

        row = next(line for line in readme.splitlines() if f"[{article.name}]" in line)
        self.assertIn("待核验", row)
        self.assertIn("未记录", row)
        self.assertNotIn("✅ 已纳入综述", row)

        (self.folder / "_themes").mkdir()
        (self.folder / "_themes/T01.md").write_text("AI 综述", encoding="utf-8")
        readme = self.render()
        row = next(line for line in readme.splitlines() if f"[{article.name}]" in line)
        self.assertIn("✅ 已纳入综述", row)
        self.assertIn("未记录", row)
        self.assertIn("`0/1`", readme)

    def test_unclassified_material_counts_are_exclusive_when_note_and_legacy_overlap(self):
        article = self.article(url="https://mp.weixin.qq.com/s/example")
        (article / "NOTE.md").write_text("待填写", encoding="utf-8")
        self.legacy(source_url="https://mp.weixin.qq.com/s/example")

        readme = self.render()

        self.assertIn("资料统计（互斥分类）", readme)
        self.assertIn("已建学习记录 **1** 篇", readme)
        self.assertIn("已有旧档 **0** 篇", readme)
        self.assertIn("未记录 **1** 篇", readme)
        self.assertNotIn("**-1**", readme)
        self.assertIn("旧档总结", readme)

    def test_all_scan_new_never_writes_any_readme(self):
        self.article()
        readme = self.folder / "README.md"
        readme.write_text("保留本人入口", encoding="utf-8")

        result = self.cli("--all", "--scan-new")

        self.assertEqual(0, result.returncode, result.stderr)
        self.assertIn("增量扫描结果", result.stdout)
        self.assertEqual("保留本人入口", readme.read_text(encoding="utf-8"))

    def test_invalid_json_is_reported_and_existing_readme_is_preserved(self):
        article = self.article()
        self.themes([{"dir_name": article.name}])
        legacy = self.legacy()
        data = article / "data.json"
        data.write_text("{}", encoding="utf-8")
        for path in [article / "metadata.json", data, self.folder / "themes.json", legacy / "META.json"]:
            with self.subTest(path=path.name):
                original = path.read_text(encoding="utf-8")
                path.write_text("{ broken", encoding="utf-8")
                (self.folder / "README.md").write_text("保留本人入口", encoding="utf-8")
                result = self.cli(str(self.folder))
                path.write_text(original, encoding="utf-8")
                self.assertNotEqual(0, result.returncode)
                self.assertIn(str(path), result.stderr)
                self.assertEqual("保留本人入口", (self.folder / "README.md").read_text(encoding="utf-8"))

    def test_missing_article_metadata_preserves_existing_readme(self):
        article = self.article()
        (article / "metadata.json").unlink()
        (self.folder / "README.md").write_text("保留本人入口", encoding="utf-8")

        result = self.cli(str(self.folder))

        self.assertNotEqual(0, result.returncode)
        self.assertIn(str(article), result.stderr)
        self.assertEqual("保留本人入口", (self.folder / "README.md").read_text(encoding="utf-8"))

    def test_batch_json_failure_preserves_even_previously_scanned_readmes(self):
        valid = self.root / "00_inbox/A_valid"
        invalid = self.root / "00_inbox/Z_invalid"
        for folder in [valid, invalid]:
            (folder / "article").mkdir(parents=True)
            (folder / "README.md").write_text("保留入口", encoding="utf-8")
            (folder / "article/metadata.json").write_text("{}", encoding="utf-8")
        (invalid / "article/metadata.json").write_text("bad json", encoding="utf-8")

        result = self.cli("--all")

        self.assertNotEqual(0, result.returncode)
        for folder in [valid, invalid]:
            self.assertEqual("保留入口", (folder / "README.md").read_text(encoding="utf-8"))

    def test_wechat_dates_are_shanghai_time_under_different_host_timezones(self):
        self.article(publish_time=1704038400)  # 2023-12-31 16:00 UTC.
        outputs = []
        for host_timezone in ("UTC", "America/Los_Angeles"):
            env = dict(os.environ, TZ=host_timezone)
            result = self.cli(str(self.folder), env=env)
            self.assertEqual(0, result.returncode, result.stderr)
            outputs.append((self.folder / "README.md").read_text(encoding="utf-8"))
            scan = self.cli(str(self.folder), "--scan-new", env=env)
            self.assertEqual(0, scan.returncode, scan.stderr)
            self.assertIn("2024-01-01", scan.stdout)
        self.assertEqual(outputs[0], outputs[1])
        self.assertIn("2024-01-01 00:00", outputs[0])
        self.assertIn("Asia/Shanghai", outputs[0])

    def test_legacy_title_needs_account_and_date_corroboration(self):
        article = self.article(source="不同公众号")
        self.legacy()

        readme = self.render()

        self.assertIn("旧档候选", readme)
        self.assertIn("已有旧档 **0** 篇", readme)
        self.assertNotIn("[🔗旧档总结]", readme)

        self.article(source="腾讯技术工程")
        readme = self.render()
        self.assertIn("已有旧档 **1** 篇", readme)
        self.assertIn("[🔗旧档总结]", readme)

        self.article(source="腾讯技术工程", publish_time=1704038400)
        readme = self.render()
        self.assertIn("旧档候选", readme)
        self.assertIn("已有旧档 **0** 篇", readme)

    def test_conflicting_title_matches_remain_candidates_but_exact_url_wins(self):
        self.article(source="腾讯技术工程", url="https://mp.weixin.qq.com/s/right")
        first = self.legacy("第一个旧档", source_url="https://mp.weixin.qq.com/s/right")
        second = self.legacy("第二个旧档", source_url="https://mp.weixin.qq.com/s/other")

        readme = self.render()

        self.assertIn("第一个旧档/AI_summary.md", readme)
        self.assertNotIn("第二个旧档/AI_summary.md", readme)

        self.article(source="腾讯技术工程", url="")
        readme = self.render()
        self.assertIn("旧档候选", readme)
        self.assertIn("已有旧档 **0** 篇", readme)
        self.assertIn(first.name, readme)
        self.assertIn(second.name, readme)
        self.assertNotIn("[🔗旧档总结]", readme)

    def test_pending_material_is_separate_from_skipped_and_new_articles(self):
        self.article("正文不完整")
        self.article("活动预告")
        self.article("技术正文")
        self.themes([{"dir_name": "技术正文"}])
        path = self.folder / "themes.json"
        data = json.loads(path.read_text())
        data["pending"] = [{"dir_name": "正文不完整", "reason": "正文仅含图片，待人工核验"}]
        data["skipped"] = [{"dir_name": "活动预告", "reason": "活动报名"}]
        path.write_text(json.dumps(data))

        readme = self.render()

        self.assertIn("待核验材料 **1** 篇", readme)
        self.assertIn("按既有分类纳入主题 **1** 篇", readme)
        self.assertIn("待归类新文章 **0** 篇", readme)
        row = next(line for line in readme.splitlines() if "[正文不完整]" in line)
        self.assertIn("待人工核验", row)
        scan = self.cli(str(self.folder), "--scan-new")
        self.assertEqual(0, scan.returncode, scan.stderr)
        self.assertIn("发现 0 篇未归类新文章", scan.stdout)
        self.assertIn("待核验 1 篇", scan.stdout)

    def test_learning_guide_is_not_presented_as_a_completed_synthesis(self):
        self.article()
        self.themes([{"dir_name": "示例文章", "synthesized": True}], document_kind="learning_guide")
        (self.folder / "_themes").mkdir()
        (self.folder / "_themes/T01.md").write_text("导学；没有归纳正文")
        readme = self.render()
        self.assertIn("导学（尚未归纳）", readme)
        self.assertIn("已纳入综述 **0** 篇", readme)

    def test_duplicate_or_overlapping_pending_preserves_readme_and_rejects_scan(self):
        self.article()
        for conflict in ("duplicate", "theme", "skipped"):
            with self.subTest(conflict=conflict):
                data = {"pending": [{"dir_name": "示例文章"}]}
                if conflict == "duplicate":
                    data["pending"].append({"dir_name": "示例文章"})
                elif conflict == "theme":
                    data["themes"] = [{"articles": [{"dir_name": "示例文章"}]}]
                else:
                    data["skipped"] = ["示例文章"]
                (self.folder / "themes.json").write_text(json.dumps(data))
                (self.folder / "README.md").write_text("保留现有入口")
                for flags in ((), ("--scan-new",)):
                    result = self.cli(str(self.folder), *flags)
                    self.assertNotEqual(0, result.returncode)
                    self.assertIn("pending", result.stderr)
                    self.assertIn("示例文章", result.stderr)
                self.assertEqual("保留现有入口", (self.folder / "README.md").read_text())


if __name__ == "__main__":
    unittest.main()
