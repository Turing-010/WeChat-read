---
name: opencli
description: "Generate CLI adapter files (YAML/TypeScript) for the opencli framework that wraps website APIs into local command-line tools."
---

# OpenCLI Adapter Generator

> 提取自《浏览器自动化：从GUI到OpenCLI》（大淘宝技术，2026-05-22，p.8–9）。

## Overview
OpenCLI is a CLI framework that wraps website APIs into local command-line tools.

## Workflow Modes
- **Quick mode** (single command): Follow `[CLI-ONESHOT.md](./references/CLI-ONESHOT.md)`
- **Full mode** (complex adapters): Read `[CLI-EXPLORER.md](./references/CLI-EXPLORER.md)`

## Output Specification
All adapter files **must** be written to `~/.opencli/clis/{site}/{command}.{ext}`.

Correct examples:
- `~/.opencli/clis/aem/page-views.ts`
- `~/.opencli/clis/twitter/lists.yaml`
- `~/.opencli/clis/bilibili/favorites.ts`

## Supported Formats
| Format | Extension | When to use |
| :--- | :--- | :--- |
| YAML | `.yaml` | Simple scenarios (Cookie/Public auth, straightforward declarative pipelines) |
| TypeScript | `.ts` | Complex scenarios (Intercept capture, Header auth, inline JS `evaluate` steps) |

## Standard Workflow
1. **Create directory**: `mkdir -p ~/.opencli/clis/{site}`
2. **Generate adapter file** at the correct path (YAML or TS)
3. **Verify**: `opencli list | grep {site}` then `opencli {site} {command}`

## Naming Conventions
| Element | Rule | Good | Bad |
| :--- | :--- | :--- | :--- |
| `site` | Lowercase, hyphens allowed | `aem`, `my-site` | `AEM`, `my_site` |
| `command` | Lowercase, hyphen-separated | `page-views`, `project-info` | `pageViews`, `project_info` |

## Pre-Generation Checklist
- [ ] Output path is `~/.opencli/clis/{site}/{command}.yaml` or `.ts`
- [ ] Site name is lowercase (no uppercase, no underscores)
- [ ] Command name uses hyphens (no spaces, no underscores)
- [ ] File extension is `.yaml` or `.ts` only
- [ ] Directory `~/.opencli/clis/{site}/` has been created
