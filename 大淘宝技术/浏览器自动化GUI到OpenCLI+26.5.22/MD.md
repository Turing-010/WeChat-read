# 浏览器自动化：从GUI到OpenCLI：PDF文本转写

> 这是原始PDF文本层转写，不是学习摘要。页码为PDF物理页序；图表、代码版面和图片文字不能完整表达在此文本层。已查看图像的内容和质量问题见AI学习笔记及META.json。

[原文PDF](RAW.pdf) · [AI学习笔记](AI_浏览器自动化GUI到OpenCLI.md) · [处理与质量记录](META.json)

## PDF 第1页

[查看原页](RAW.pdf#page=1)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
浏览器自动化：从GUI到OpenCLI
明径 2026年5月22日 02:13 浙江
大淘宝技术 17人
文章讲述放弃不
稳定的前端UI自动化操作，采用解析并复现底层API请求的方式，来解决
浏览器自动化的效率与稳定性难题。（文章内容基于作者个人技术实
践与独立思考，旨
在分享经验，仅代表个人观点。）
为什么我们需要浏览器自动化
如今大量业务系
统都跑在浏览器里——运营配置后台、工单处理系
让这些系
统自动运转，对提效和智能化运营的价值不言而喻。
但现实是，Agent 想操控浏览器，路并不好走。
统、发布运维平台。如果能
现有
方
案的困境
```

## PDF 第2页

[查看原页](RAW.pdf#page=2)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
OpenCLI 的思路
核心想法很简单：不跟网页界面较劲，直接抓它
背后的 API。
浏览器里
出来，比点按
看到的数据，本质上都是前端从某个接口拿回来的。把这个接口找出来、把请求复现
钮靠谱得多。
▐ 快速上手
1 npm install -g @jackwener/opencli
直接使用：
1
2
3
4
opencli list
# 查看所有命令
opencli list -f yaml
# 以 YAML 列出所有命令
```

## PDF 第3页

[查看原页](RAW.pdf#page=3)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
5
6
7
8
9
10
11
12
13
14
opencli hackernews top --limit
5
# 公共 API，无需浏览器
opencli bilibili hot --limit
5
# 浏览器命令
opencli zhihu hot -f json
# JSON 输出
opencli zhihu hot -f yaml
# YAML 输出
▐ 原理分析
AI Agent 探索工作流
步骤工具 做什么
0. 打 开 浏
browser_navigate 导航到目标页面
览器
1. 观察页面 browser_snapshot 观察可交互元素（按
钮/标签/链接）
2. 首 次抓
筛选 JSON API 端点，记录 URL patter
browser_network_requests
包
n
3. 模 拟 交
browser_click
+
browser_w
点击"字幕""评论""关注"等按
钮
互
ait_for
4. 二 次抓
browser_network_requests 对比
步骤 2，找出新触发
的 API
包
5. 验证 AP
fetch(url, {credentials:'include'}) 测
browser_evaluate
I
试返回结构
6. 写代码 — 基于确认的 API 写适配
懒加载机制
1
2
> [!CAUTION]
> **你（AI Agent）必须通过浏览器打开目标网站去探索！**
器
```

## PDF 第4页

[查看原页](RAW.pdf#page=4)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
3
4
5
6
7
8
> 不要只靠 `
opencli explore
` 命令或静态分析来发现 API。
> 你拥有浏览器工具，必须主动用它们浏览网页、观察网络请求
、模拟用户交互。
### 为什么？
很多 API 是**懒加载**的（用户必须点击某个按
钮/标签才会触发网络请求）。字幕、评论、
关
五级认证策略
OpenCLI 提供 5 级认证策略。使用 cascade 命令自动探测：
1 opencli cascade https://api.example.com/hot
策略决策树：
1
2
3
4
5
6
7
8
9
直接 fetch(url) 能拿到数据？
→ ✅ Tier 1: public（公开 API，不需要浏览器）
→ ❌ fetch(url, {credentials:'include'}) 带 Cookie 能拿到？
→ ✅ Tier 2: cookie（最常见，evaluate 步骤内 fetch）
→ ❌ → 加上 Bearer / CSRF header 后能拿到？
→ ✅ Tier 3: header（如 Twitter ct0 + Bearer）
→ ❌ → 网站有 Pinia/Vuex Store？
→ ✅ Tier 4: intercept（Store Action + XHR 拦截）
→ ❌ Tier 5: ui（UI 自动化，最后手段）
适配
器
1
2
3
4
你的 pipeline 里
有
evaluate 步骤（内嵌 JS 代码）？
→ ✅ 用 TypeScript (src/clis/<site>/<name>.ts)，保存即自动动态注册
→ ❌ 纯声明式（navigate + tap + map + limit）？
→ ✅ 用 YAML (src/clis/<site>/<name>.yaml)，保存即自动注册
```

## PDF 第5页

[查看原页](RAW.pdf#page=5)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
外部CLI集成
也支持现有
CLI直接集成到OpenCLI
CLI执
流程
行
下图展示从启动到执
览器需求选
适配
择
行
的关键路径：入口加载命令清单，构建注册表；执
器或管道步骤，完成数据采集与输出。
行
阶段根据策略与浏
```

## PDF 第6页

[查看原页](RAW.pdf#page=6)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
▐ 自动生成CLI
AI 原生生成CLI流程
1. 探索与分析：explore 深度抓取页面、自动滚动、拦截网络请求
识别框架与状态管理、
推断能力与推荐参数。
2. 策 略 选
择
： 根 据 鉴 权头 / 签 名 等 特征自 动 选
（public/cookie/header/intercept/store-acti
on）。
择
策 略
3. 适配
器合成：synthesize 基于探索产物生成候选 YAML，自动模板化 URL、字段映射与
参数默认值。
4. 测试与验证：generate 串联探索→合成→注册→验证，支持目标化选
择
与回退策略。
、
Record操作录制
opencli record 采用“浏览器录制 - 智能回放”模式：启动浏览器
上的交互
行
为及产生的网络请求。
系
统通过对请求序列进
行
复用的 CLI 命令。
后，捕获用户在目标 URL
评分排序与语义分析，自动生成可
```

## PDF 第7页

[查看原页](RAW.pdf#page=7)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
执
流程如下图所示：
行
当前局限性：
请 求 体 （ Payload）缺 失 ：目前 的录制引擎 仅 捕 获请 求 元数据 （ url, method, responseBody），未能完整提取 POST/PUT 等写操作中的 Request Body。
body:
生 成 能力受 限 ： 由 于缺 乏关 键 参 数载 荷 ，自 动化脚
（如列表查询、详情获取并输出 YAML），无法有
删除）的命令生成，导致自动化闭环在“写入场景”中断
本生 成 逻 辑目前 仅 能覆 盖 只 读类接口
效支撑写操作类接口（如
创建、更新、
。
Q
oderWork自动生成CLI
为了方 便自 动生 成CLI命 令， 我 整 理 了 如下 的Skill， 其中
EXPLORER.md可在开源项目中自
行
下载。
CLI-ONESHOT.md和CLI-
```

## PDF 第8页

[查看原页](RAW.pdf#page=8)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
SKILL.md
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33
34
35
36
37
38
39
40
41
42
43
44
---
name: opencli
description: "Generate CLI adapter files (YAML/TypeScript) for the ope
---
# OpenCLI Adapter Generator
## Overview
OpenCLI is a CLI framework that wraps website APIs into local command-
## Workflow Modes
**Quick mode** (single command): Follow [CLI-ONESHOT.md](./references/
**Full mode** (complex adapters): Read [CLI-EXPLORER.md](./references/
## Output Specification
All adapter files **must** be written to
`
~/.opencli/clis/{site}/{comm
Correct examples:
`
-
~/.opencli/clis/aem/page-views.ts
`
`
-
~/.opencli/clis/twitter/lists.yaml`
`
-
~/.opencli/clis/bilibili/favorites.ts
`
## Supported Formats
| Format | Extension | When to use |
|--------|-----------|-------------|
| YAML | `
.yaml` | Simple scenarios (Cookie/Public auth, straightforwa
| TypeScript | `
.ts
` | Complex scenarios (Intercept capture, Header au
## Standard Workflow
1. **Create directory**:
`
mkdir -p ~/.opencli/clis/{site}`
2. **Generate adapter file** at the correct path (YAML or TS)
3. **Verify**:
`
opencli list | grep {site}` then
`
opencli {site} {comm
## Naming Conventions
| Element | Rule | Good | Bad |
|---------|------|------|-----|
| site | Lowercase, hyphens allowed | `
`
aem
,
`
my-site
` | `AEM`
,
`
my_
si
```

## PDF 第9页

[查看原页](RAW.pdf#page=9)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
45
46
47
48
49
50
51
52
53
| command | Lowercase, hyphen-separated | `
page-views
`
,
`
project-info
`
## Pre-Generation Checklist
- [ ] Output path is
`
~/.opencli/clis/{site}/{command}.yaml`
- [ ] Site name is lowercase (no uppercase, no underscores)
- [ ] Command name uses hyphens (no spaces, no underscores)
- [ ] File extension is
`
.yaml`
`
`
or
.ts
- [ ] Directory
`
only
~/.opencli/clis/{site}/` has been created
`
`
or
.ts
▐ 使用case：
内部会画平台CLI化
```

## PDF 第10页

[查看原页](RAW.pdf#page=10)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
BOSS招聘自动化案例展示
1.帮我和候选人沟通
2.统计招聘数据
未来软件
竞争维度：从界面到可调用性
未来的软件，不会只服务人，也会服务 Agent。
以前我们评价一个 SaaS，看的是界面顺不顺、
按
钮好不好点。但 Agent 不会欣赏你的按
钮
做得多圆。它只在乎一件事：能不能稳定调用你。
GUI 是给人用的。API 是能力底座。而 Agent 最喜欢的，其实是更清晰的执
数、返回值、失败原因。
面：命令、参
行
未 来软件 可 能 会多一个新竞 争维 度 ：不 是谁页面 更 好看 。而 是谁 更 容易 被 Agent 用、验证，再接进工作流。唯有
如此，才更有机会成为下一代工作流里的基础节点。
理 解、调
过去的软件
竞争界面，未来的软件
竞争可调用性。
```

## PDF 第11页

[查看原页](RAW.pdf#page=11)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
¤ 拓展阅读 ¤
3DXR技术 | 终端技术 | 音视频技术
服务端技术 | 技术质量 | 数据算法
大淘宝技术
大淘宝技术官方账号
967篇原创内容
公众号
阅读 6955
```
