import unittest, tempfile, json, hashlib, importlib.util
from pathlib import Path
MODULE = Path(__file__).with_name('kb_tools.py')
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()

VALID_NOTE = """---
title: "测试精读笔记"
source: "测试公众号 / 作者"
date: "2026-09-07"
type: "技术精读"
tags: [测试]
status: "待复习"
---

# 测试精读笔记

## 1. TL;DR
核心摘要。

## 2. 问题定义与背景
背景定义。

## 3. 知识框架
```mermaid
flowchart TD
    A[开始] --> B[结束]
```

## 4. 核心内容拆解
正文拆解。

## 5. 数据速查表
| 指标 | 原文数值 | 语境 / 条件 |
| :--- | :--- | :--- |
| 延迟 | 10ms | 测试条件 |

## 6. 踩坑与教训 / 可迁移的设计原则
| 错误做法 | 失败表现或原因 | 原文应对（可迁移的设计原则） |
| :--- | :--- | :--- |
| 盲目重试 | 雪崩 | 熔断退避 |

## 7. 记忆锚点
- 核心锚点口诀。

## 8. 复习卡片
问题1::答案1
问题2::答案2
问题3::答案3
问题4::答案4
问题5::答案5

## 9. 知识关联
- [原文](RAW.pdf) · [[候选双链]]

## 10. 原文参考资料
- 原文标题：《测试文章》

> [!note]- 校对报告
> - 页码溯源：p.1–2 核心内容。
"""

class KnowledgeToolsTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name)
  if not MODULE.exists():self.fail('尚未实现kb_tools.py')
  spec=importlib.util.spec_from_file_location('kb_tools',MODULE);self.mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(self.mod)
 def tearDown(self):self.tmp.cleanup()
 def article(self,name='文章',aid='art-0001',date='2026-09-07',note_text=None):
  d=self.root/'公众号'/name;d.mkdir(parents=True);(d/'RAW.pdf').write_bytes(b'synthetic PDF fixture')
  (d/'AI_文章.md').write_text(note_text or '# 笔记\n\n[原文](RAW.pdf)\n', encoding='utf-8')
  m={'article_id':aid,'title':name+'原标题','account':'公众号','published_at':date,'files':{'raw':'RAW.pdf','ai_summary':'AI_文章.md'},'captures':[{'capture_id':'capture-001','path':'RAW.pdf','sha256':sha(d/'RAW.pdf'),'original_path':'旧位置不存在.pdf','files':[]}],'reading_status':'unread'}
  (d/'META.json').write_text(json.dumps(m,ensure_ascii=False), encoding='utf-8');return d,m
 def test_original_paths_are_not_current_links(self):
  self.article();self.assertEqual(self.mod.verify(self.root)['errors'],[])
 def test_detects_raw_change(self):
  d,m=self.article();(d/'RAW.pdf').write_bytes(b'changed');self.assertTrue(any('sha256' in e for e in self.mod.verify(self.root)['errors']))
 def test_duplicate_id_rejected(self):
  self.article();self.article('第二篇');self.assertTrue(any('duplicate' in e for e in self.mod.verify(self.root)['errors']))
 def test_real_broken_link_rejected_code_links_ignored(self):
  d,m=self.article();(d/'AI_文章.md').write_text('# 笔记\n\n```text\n[代码样例](不存在.md)\n```\n\n[真正链接](缺失.md)\n', encoding='utf-8')
  es=self.mod.verify(self.root)['errors'];self.assertEqual(len(es),1);self.assertIn('缺失.md',es[0])
 def test_index_latest_first_unknown_last_and_no_write(self):
  self.article('旧',date='2026-09-03');self.article('新',aid='art-0002',date='2026-10-11');self.article('未知',aid='art-0003',date=None)
  text=self.mod.account_index(self.root/'公众号');self.assertLess(text.index('新原标题'),text.index('旧原标题'));self.assertLess(text.index('旧原标题'),text.index('未知原标题'));self.assertFalse((self.root/'公众号/README.md').exists());self.assertNotIn('2026-10-11',text)
 def test_index_validates_links_before_any_write(self):
  d,m=self.article();(d/'RAW.pdf').unlink()
  with self.assertRaises(ValueError):self.mod.account_index(self.root/'公众号')
 def test_baseline_protects_note_and_keeps_scope_explicit(self):
  d,m=self.article();(d/'NOTE.md').write_text('本人想法', encoding='utf-8');baseline={'公众号/文章/NOTE.md':sha(d/'NOTE.md')};(d/'NOTE.md').write_text('被改写', encoding='utf-8')
  self.assertTrue(any('baseline' in e for e in self.mod.verify(self.root,baseline=baseline)['errors']))
 def test_check_notes_and_sync_meta(self):
  d,m=self.article(note_text=VALID_NOTE)
  res=self.mod.check_notes(self.root/'公众号',sync_meta=True,updated_at='2026-10-16')
  self.assertEqual(res['errors'],[])
  self.assertEqual(res['synced_meta'],1)
  self.assertEqual(self.mod.verify(self.root)['errors'],[])
  updated_meta=json.loads((d/'META.json').read_text(encoding='utf-8'))
  self.assertEqual(updated_meta['ai_note_status'],'completed')
  self.assertEqual(updated_meta['processing']['generated_summary']['sha256'],sha(d/'AI_文章.md'))
 def test_check_notes_rejects_inline_page_citations(self):
  bad_note=VALID_NOTE.replace('核心摘要。','核心摘要（p.3）。')
  self.article(note_text=bad_note)
  res=self.mod.check_notes(self.root/'公众号')
  self.assertTrue(any('inline page citations' in e for e in res['errors']))
if __name__=='__main__': unittest.main()
