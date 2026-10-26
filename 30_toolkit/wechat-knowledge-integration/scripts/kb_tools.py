"""Read-only knowledge-library checks, 10-section study-note quality gate checks, and account-index generation.

Uses the Python standard library. Never moves or removes source materials.
"""
import argparse
import hashlib
import json
import re
from datetime import date as Date
from pathlib import Path
from urllib.parse import unquote, urlsplit


REQUIRED_H2_PREFIXES = (
    '## 1. TL;DR',
    '## 2. ',
    '## 3. 知识框架',
    '## 4. ',
    '## 5. 数据速查',
    '## 6. 踩坑与教训',
    '## 7. 记忆锚点',
    '## 8. 复习卡片',
    '## 9. 知识关联',
    '## 10. 原文参考资料',
)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def visible_markdown(text):
    """Ignore fenced and inline code: example links and comments are source material."""
    out, fence = [], None
    for line in text.splitlines():
        match = re.match(r'^\s*(`{3,}|~{3,})', line)
        if fence:
            if match and match.group(1)[0] == fence[0] and len(match.group(1)) >= len(fence):
                fence = None
            continue
        if match:
            fence = match.group(1)
            continue
        out.append(re.sub(r'(`+).*?\1', '', line))
    return '\n'.join(out)


def local_links(text):
    for match in re.finditer(r'\]\((<[^>]+>|[^\s)]+)(?:\s+"[^"]*")?\)', visible_markdown(text)):
        target = match.group(1).strip('<>')
        if target.startswith('#') or urlsplit(target).scheme:
            continue
        yield unquote(target.split('#', 1)[0])


def verify(root, baseline=None, allowed_changes=()):
    root = Path(root).resolve()
    errors, warnings, ids = [], [], {}
    counts = {'articles': 0, 'hashes': 0, 'local_links': 0}

    def current_path(folder, value, label, scope=None):
        if not isinstance(value, str) or not value:
            errors.append(f'{label}: invalid current path')
            return None
        target = (folder / value).resolve()
        boundary = (scope or root).resolve()
        if not target.is_relative_to(boundary):
            errors.append(f'{label}: path escapes {boundary}: {value}')
            return None
        if not target.exists():
            errors.append(f'{label}: missing {value}')
            return None
        return target

    def checked_hash(path, expected, label):
        if path is not None and expected is not None:
            if not path.is_file():
                errors.append(f'{label}: hash input is not a file')
                return
            counts['hashes'] += 1
            if digest(path) != expected:
                errors.append(f'{label}: sha256 mismatch')

    for meta_path in sorted(root.glob('*/*/META.json')):
        counts['articles'] += 1
        try:
            meta = json.loads(meta_path.read_text(encoding='utf-8'))
        except (ValueError, OSError) as exc:
            errors.append(f'{meta_path}: invalid JSON: {exc}')
            continue
        folder, aid = meta_path.parent, meta.get('article_id')
        if not isinstance(aid, str) or not re.fullmatch(r'art-\d+', aid):
            errors.append(f'{meta_path}: invalid article_id')
        elif aid in ids:
            errors.append(f'duplicate article_id {aid}: {ids[aid]} / {meta_path}')
        else:
            ids[aid] = str(meta_path)
        for kind, value in meta.get('files', {}).items():
            current_path(folder, value, f'{aid} files.{kind}', folder)
        for capture in meta.get('captures', []):
            target = current_path(folder, capture.get('path'), f'{aid} capture', folder)
            checked_hash(target, capture.get('sha256'), f'{aid} capture')
            if target is not None and target.is_dir():
                for item in capture.get('files', []):
                    member = current_path(target, item.get('path'), f'{aid} attachment', target)
                    checked_hash(member, item.get('sha256'), f'{aid} attachment')
        conversion = meta.get('conversion') or {}
        for kind in ('input', 'output'):
            if conversion.get(kind):
                item = conversion[kind]
                target = current_path(folder, item.get('path'), f'{aid} conversion.{kind}', folder)
                checked_hash(target, item.get('sha256'), f'{aid} conversion.{kind}')
        for item in meta.get('received_artifacts', []):
            target = current_path(folder, item.get('path'), f'{aid} received_artifact', folder)
            checked_hash(target, item.get('sha256'), f'{aid} received_artifact')
        processing = meta.get('processing') or {}
        for value in processing.get('outputs', []):
            current_path(folder, value, f'{aid} processing output', folder)
        gen_summary = processing.get('generated_summary')
        if isinstance(gen_summary, dict) and gen_summary.get('path'):
            target = current_path(folder, gen_summary.get('path'), f'{aid} processing.generated_summary', folder)
            checked_hash(target, gen_summary.get('sha256'), f'{aid} processing.generated_summary')
        for value in (meta.get('knowledge_integration') or {}).get('topics', []):
            current_path(folder, value, f'{aid} topic')
    for path in sorted(root.rglob('*.md')):
        if '.git' in path.parts:
            continue
        try:
            text = path.read_text(encoding='utf-8')
        except (UnicodeError, OSError) as exc:
            errors.append(f'{path}: unreadable Markdown: {exc}')
            continue
        for target in local_links(text):
            counts['local_links'] += 1
            resolved = (path.parent / target).resolve()
            if not resolved.is_relative_to(root):
                try:
                    if not resolved.exists():
                        warnings.append(f'external link missing {path.relative_to(root)}: {target}')
                except PermissionError:
                    warnings.append(f'external link outside sandbox {path.relative_to(root)}: {target}')
                continue
            if not resolved.exists():
                errors.append(f'broken link {path.relative_to(root)}: {target}')
    for relative, expected in (baseline or {}).items():
        if relative in set(allowed_changes):
            continue
        path = (root / relative).resolve()
        if not path.is_relative_to(root):
            errors.append(f'baseline path escapes root: {relative}')
        elif not path.is_file() or digest(path) != expected:
            errors.append(f'baseline changed or missing: {relative}')
    return {**counts, 'errors': errors, 'warnings': warnings}


def check_note_content(text, label='note'):
    """Validate a single 10-section AI_*.md study note against quality gates."""
    issues = []
    if not text.startswith('---\n'):
        issues.append(f'{label}: missing YAML frontmatter')
    visible = visible_markdown(text)
    h1s = re.findall(r'^# [^\n]+', visible, flags=re.M)
    if len(h1s) != 1:
        issues.append(f'{label}: expected 1 H1 outside code blocks, found {len(h1s)}')
    for prefix in REQUIRED_H2_PREFIXES:
        if not any(line.startswith(prefix) for line in visible.splitlines()):
            issues.append(f'{label}: missing section starting with {prefix!r}')
    if '```mermaid' not in text:
        issues.append(f'{label}: missing mermaid diagram')
    if '> [!note]- 校对报告' not in text:
        issues.append(f'{label}: missing folded > [!note]- 校对报告')
    else:
        body_before_audit = visible.split('> [!note]- 校对报告', 1)[0]
        inline_cites = re.findall(r'(?:\bp\.\s*\d+|第\s*\d+\s*页)', body_before_audit)
        if inline_cites:
            issues.append(f'{label}: inline page citations before audit callout: {inline_cites[:5]}')
    if '## 8. 复习卡片' in text and '## 9. 知识关联' in text:
        sec8 = text.split('## 8. 复习卡片', 1)[1].split('## 9. 知识关联', 1)[0]
        cards = [line for line in sec8.splitlines() if '::' in line and not line.strip().startswith('>')]
        if not (5 <= len(cards) <= 10):
            issues.append(f'{label}: expected 5..10 flashcards in section 8, found {len(cards)}')
    return issues


def check_notes(target_dir, sync_meta=False, updated_at=None):
    """Check all AI_*.md notes under an account directory or library root, optionally syncing META.json."""
    target_dir = Path(target_dir).resolve()
    meta_paths = sorted(target_dir.glob('*/META.json')) or sorted(target_dir.glob('*/*/META.json'))
    issues = []
    checked = 0
    synced = 0
    stamp = updated_at or Date.today().isoformat()

    for meta_path in meta_paths:
        meta = json.loads(meta_path.read_text(encoding='utf-8'))
        folder = meta_path.parent
        ai_rel = (meta.get('files') or {}).get('ai_summary') or meta.get('ai_note')
        if not ai_rel:
            ai_candidates = sorted(folder.glob('AI_*.md'))
            ai_rel = ai_candidates[0].name if ai_candidates else None
        if not ai_rel or not (folder / ai_rel).is_file():
            issues.append(f'{folder.name}: missing AI study note file')
            continue
        note_path = folder / ai_rel
        text = note_path.read_text(encoding='utf-8')
        checked += 1
        note_issues = check_note_content(text, f'{folder.name}/{ai_rel}')
        issues.extend(note_issues)
        if sync_meta and not note_issues:
            actual_sha = digest(note_path)
            meta.setdefault('files', {})['ai_summary'] = ai_rel
            proc = meta.setdefault('processing', {})
            gen = proc.setdefault('generated_summary', {})
            gen['path'] = ai_rel
            gen['sha256'] = actual_sha
            meta['ai_note'] = ai_rel
            meta['ai_note_status'] = 'completed'
            meta['ai_note_updated_at'] = stamp
            meta_path.write_text(json.dumps(meta, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
            synced += 1
    return {'checked_notes': checked, 'synced_meta': synced, 'errors': issues}


def account_index(account):
    account = Path(account).resolve()
    items, ids = [], set()
    for path in sorted(account.glob('*/META.json')):
        meta = json.loads(path.read_text(encoding='utf-8'))
        if meta.get('article_id') in ids:
            raise ValueError('duplicate article_id')
        ids.add(meta.get('article_id'))
        title = meta.get('title')
        if not isinstance(title, str) or not title.strip():
            raise ValueError(f'missing original title: {path}')
        date = meta.get('published_at')
        if date is not None and not re.fullmatch(r'\d{4}-\d{2}-\d{2}(?:T.*)?', date):
            raise ValueError(f'invalid published_at: {path}')
        if date is not None:
            Date.fromisoformat(date[:10])
        links = {}
        for key in ('ai_summary', 'raw'):
            value = meta.get('files', {}).get(key)
            if value is None:
                links[key] = '—'
                continue
            target = (path.parent / value).resolve()
            if not target.is_relative_to(path.parent.resolve()) or not target.is_file():
                raise ValueError(f'invalid index target: {target}')
            label = 'AI 总结' if key == 'ai_summary' else '原文 PDF'
            rel = target.relative_to(account).as_posix()
            links[key] = f'[{label}](<{rel}>)' if ' ' in rel else f'[{label}]({rel})'
        safe_title = title.replace('|', '\\|').replace('\n', ' ')
        items.append((date or '', str(meta.get('article_id') or ''), f"| {safe_title} | {links['ai_summary']} | {links['raw']} |"))
    items.sort(key=lambda item: (item[0], item[1]), reverse=True)
    return '\n'.join(['| 文章原标题 | AI 总结 | 原文 PDF |', '| --- | --- | --- |'] + [item[2] for item in items]) + '\n'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    check = sub.add_parser('verify', help='Read-only IDs, current paths, hashes and Markdown links')
    check.add_argument('--root', type=Path, required=True)
    check.add_argument('--baseline', type=Path, help='JSON mapping library-relative paths to sha256')
    check.add_argument('--allow-change', action='append', default=[], help='Explicit baseline exception; repeatable')
    notes = sub.add_parser('check-notes', help='Validate 10-section AI_*.md study notes and optionally sync META.json')
    notes.add_argument('--account', type=Path, required=True, help='Account folder or library root')
    notes.add_argument('--sync-meta', action='store_true', help='Update generated_summary sha256 and ai_note_status in META.json')
    notes.add_argument('--updated-at', type=str, default=None, help='Optional YYYY-MM-DD date string for ai_note_updated_at')
    index = sub.add_parser('index', help='Render one account README; dry run unless --write')
    index.add_argument('--account', type=Path, required=True)
    index.add_argument('--write', action='store_true')
    args = parser.parse_args()
    if args.command == 'verify':
        baseline = json.loads(args.baseline.read_text()) if args.baseline else None
        report = verify(args.root, baseline, args.allow_change)
        print(json.dumps(report, ensure_ascii=False, indent=2))
        raise SystemExit(1 if report['errors'] else 0)
    if args.command == 'check-notes':
        report = check_notes(args.account, sync_meta=args.sync_meta, updated_at=args.updated_at)
        print(json.dumps(report, ensure_ascii=False, indent=2))
        raise SystemExit(1 if report['errors'] else 0)
    content = account_index(args.account)
    if args.write:
        output = args.account / 'README.md'
        output.write_text(content, encoding='utf-8')
        print(str(output.resolve()))
    else:
        print(content, end='')


if __name__ == '__main__':
    main()
