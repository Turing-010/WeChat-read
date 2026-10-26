# Agent skill 迭代式编写实战：PDF文本转写

> 这是原始PDF文本层转写，不是学习摘要。页码为PDF物理页序；图表、代码版面和图片文字不能完整表达在此文本层。已查看图像的内容和质量问题见AI学习笔记及META.json。

[原文PDF](RAW.pdf) · [AI学习笔记](AI_Agent Skill迭代式编写.md) · [处理与质量记录](META.json)

## PDF 第1页

[查看原页](RAW.pdf#page=1)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
Agent skill 迭代式编写实战
原创
物流技术团队 2026年6月12日 00:02 浙江
大淘宝技术 34人
本文总结Agent Skill编写经验，将其定义为模块化领域知
识资
产，类似给AI的“操作
手册”，适用于半自动化及专家经验导向场景。核心设计遵循三层渐进式披露架构，强
调用决策树替代模糊判断
、确定性操作脚
本化，并建立内部自查与外部评估双重验证
机制
。Skill本质是以文件系
统结构替代复杂运
行
时服务，实现零依
赖部署。相比专用
Agent框架，它更轻量但确定性稍弱，旨在将隐性专家经验转化为可复用、可验证的知
识资
产。
前言
本文是笔者年初以来摸索 agent skill 编写过程中的经验总结，配图生成自 QoderWork。分
享的内容包括了：
笔者对于 agent skill 概念和特性的理解，以及适用的场景
迭代式编写 agent skill 的实
践经验
关
于 skill：概念
、特性与应用场景
▐ 什么是 Agent Skill
Agent Skill 是模块化的能力包，沉淀
了领域知
识的资
产 bundle，资
产包括自然语言指令、
元数据和可选资源（脚
本、模板），让 AI Agent 在需要时自动加载和使用。如果说 MCP
为 agent 提供 了 "手 " 来 操 作工 具 ， 那么 skill 就 是 " 操 作手 册 " ， 教 agent 怎
么用 这 些工
具。
从时间线
看，2025 年 10 月中旬 Anthropic 正式
发布 Claude Skills，两个月后 Agent
Skills 作为开放标准
发布，Cursor、OpenCode、Qoder 等主流工具陆续跟进。
```

## PDF 第2页

[查看原页](RAW.pdf#page=2)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
通俗理解：skill 就是给 agent 准备的业务 SOP 使用说明、模板素材，以及常见问题的处理方式。
大礼包，涵盖执
流程、
行
背景知
识
、工具
▐ Agent skill 的形态
skill 基于文件系
与加载。
标准 Skill 目录结构如下：
统驱动，agent 工具通过 skill 标准的 tool 和终端/文件操作能力完成发现
SKILL.md 是整个 skill 的核心，由两
部分组成：
YAM
L frontmatter：skill 的元数据，agent 通过此判断
是否触发。
description 是关键，通常写明适用场景和关键触发词。
Markdown 正文：面向 agent 的执
再展
开约束细节。
行 SOP，建议用「总-分」结构，先说核心规则，
references/ 放补充文档，如模板文件
径按需引用，不要把大量内容堆进主文件。
、详细规范、示例代码等，在 SKILL.md 中通过路
scripts/ 放确定性操作的执
脚
行
本（Python/Bash 等）。能写成脚
理——脚
本的稳定性和可复现性远高于让 agent 猜。
本的就不要靠 agent 推
扩展阅读：如何处理带有三方库依
赖
的 python 脚
本：uv run
+
pep 723
▐ Agent Skill 的核心特性
```

## PDF 第3页

[查看原页](RAW.pdf#page=3)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
▐ 适合使用 Agent Skill 的场景
以下场景特别适合：
半自动化重复流程：同一业务流程频繁执
行
，部分依
赖
主观判断，无法完全自动化
领域知
识导向：业务流程依
赖
专家知
识，llm 泛化能力难以覆盖
上下文受限：agent 职责多样且上下文窗口有限，处理其他任务时不希望无关知
识占位
不适合的场景：
简单
任务：直接用基础提示词，靠 llm 泛化能力即可
流程完全确定性：写代码自动化更合适
agent 职责高度单一：把 skill 内容放进 system prompt，脚
本用 mcp/tools 代替，
没必要包装成 skill
Agent Skill 编写经验
推荐先装
好这两个元 skill 再上手：
https://skills.sh/anthropics/skills/skill-creator 用于生成 skill
https://skills.sh/softaworks/agent-toolkit/skill-judge 用于评估 skill
▐ 设计时遵循三层渐进式加载架构
```

## PDF 第4页

[查看原页](RAW.pdf#page=4)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
渐进式披露（Progressive Disclosure）是 Agent Skill 最核心的设计思想，把技能信息拆
成三层：
第一层：目录/概要（成本最低，agent 平时只需知道手册目录）
第二层：详细指令（按需加载，需要时才打开具体章节）
第三层：完整资源（包含详细步骤和工具脚
本）
设计 skill 时就要想清楚：哪些内容必须在 skill.md，哪些可以下沉到 reference。
▐ 迭代式开
发
```

## PDF 第5页

[查看原页](RAW.pdf#page=5)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
以下是开
发过程中一些具体的可优化 skill 效果的实
践
用决策树替代模糊判断
决策树是正向约束，能让 agent 在需要做判断时
的 skill 的片段示例
行
为可控。以下是一个异步消息问题排查
1
2
3
4
5
6
### 结果处理规则
**补全未发出消息：** 若有序事件的前序有日志、
**消费失败处理：** 判断某 tag 是否失败，标准为 `
- 若后续**有
** `Y`（重试成功）→ 取**第一条**失败
- 若后续**无** `Y`（持续失败）→ 取**每一条**失败
**错误详情查询（消费失败）：**
后序无日志，在报告表格中补充后序事件
行
resultFlag = N` 且该 tag 后续
行
，调用错误详情查询
行
，调用错误详情查询
skill-judge 把决策树列为高质量 skill 的明确标志，在 D1（知
个维度都是加分项：
识增量）和 D8（实用性）两
Green flags (indicators of high knowledge delta):- Decision trees for non-obvious
choices (&q
uot;when X fails, try Y because Z&q
uot;)
D8 Usability 检 查项 ： - Decision trees: For m
ulti-path scenarios, is there clear
guidance on which path to take?
原因很简单：skill 的核心价值是封装专家才有
楚，而不是用模糊语言把判断
描述的可执
的判断知
识。决策树把"应该怎
么判断"写清
压力甩给 agent。agent 不需要推理，顺着树走就行
。比模糊
行
性高很多。写 skill 时遇到分支判断，优先用树形结构，而不是让 agent 自
行
决策。
负向约束要配替代方
案
```

## PDF 第6页

[查看原页](RAW.pdf#page=6)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
告诉 agent 不能做什么（bad case/anti pattern）时，同步给出合法替代方
案，约束力会强
很多。以下是一个单元测试编写 skill 的片段，给出了 mock 时的 bad case 和相应的解决
方
案
1
2
3
4
5
6
### Mocking Restrictions
**Do NOT mock:**
`
-
public static
` fields (e.g.,
`@AppSwitch`
-annotated configurations)
restore originals post-test
- POJO classes or OneLog objects - initialize simple POJOs programmati
- Stateless static methods (e.g., utility methods for conversion/assem
不要只说"
不能做什么"，要给"那应该怎
agent 会自己找一个——结果往往不是你想要的。
么做"。这也是一种 few shot。没有
替代方
案的话，
skill 执
后自查机制
行
决策树解决的是执
行
前的分支判断
出物是否合格。以下是一个单元测试生成 skill 的执
——走哪条路。自查机制解决的是另一半：执
后自查列表示例
完了，产
行
行
1
2
3
4
5
6
7
8
9
## Post-Generation Review
After generating tests, review against this specification to ensure:
- Correct test file location and naming
- Proper mock configuration without prohibited patterns
- Complete verification of return values, state mutations, and invocat
- AssertJ assertion patterns are used consistently
- No reflection-based testing or private member verification
- Similar tests are grouped into parameterized tests where appropriate
- Parameterized tests use appropriate source types and handle null val
agent 的自然倾向是完成任务就结束，不会主动回头
检验。很多规范性错误恰恰在"完成"之
后才能发现。把自查写进 skill，就是强制插入一个反射节点，把"我觉得做完了"
变成"我验证
过做完了"。
自查可以从两个角度来：
规范符合性：对照约束检查，确认没做错
覆盖完整性：对照领域知
识检查，确认没遗漏
```

## PDF 第7页

[查看原页](RAW.pdf#page=7)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
决策树是收敛的（从多条路中选一条），自查清单是发散的（从一个结果出发，在多个维度
验证）。
有明确输出规范的 skill（代码生成、迁移、测试等），skill 成熟后建议补上自查机
制
。
skill 的外部验证：eval 机制
自查是 skill 执
动态验证：用真实输
行
时的内部静态验证，由 agent 对照清单自检。skill-creator 还提供了外部
入跑 skill，对比有无 skill 的
输出差距，而不是靠感觉判断
好坏。
eval 的四个环节：
测试用例：设计 2-3 个真实用户会说的提示词，同一提示词分别跑「有
skill（或旧版本）」，保留两份输出用于对比
skill」和「无
。提示词要有足够的复杂度和具体背景——
skill 的触发本身依
赖
agent 对 description 的语义
识别，过于简单
的 prompt 可能根本
不会触发 skill，也就测不出任何东西
断言：有客观标准的 skill 设计可验证检查项（如"
输出文件是否包含字段 X"），主观类
skill 基于人工反馈
迭代循环：评估 → 修改 → 重跑 → 再评估，每轮聚焦有明确问题的用例，直到没有明显
差距。注意：每轮只看少数用例，容易把 skill 改成只对这几个 case 有
效。改的时候要
从具体反馈里抽出通用规律，而不是针对
测试用例做针对性修补
description 触发率优化：skill 内容稳定后
单独优化 description，用 should-trigger /
should-not-trigger 样本 测 试 召 回 精 度 ， 重 点关 注"近 似 场 景 误 触 发
"和"该触 发 却 未 触
发
"两类边界
内部自查是运
行
时护栏，外部 eval 是开
发
期的标准线，定位不同，都
有用。
▐ 多人协作 skill 管理
skills.sh 提供了配套的 skill 管理工具。如果要多人协作共享 skill，可以在 code 平台上建
一个仓库，根目录放 skills 目录，下面存放各个 skill。需要用时运
以下命令交互式安装：行
```

## PDF 第8页

[查看原页](RAW.pdf#page=8)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
▐ 扩展视角：skill 是简化版的专用 agent
熟悉 ReAct / LangGraph 等框架的话，可以用这张映射表快速建立认知：
LangGraph 的条件边由调度器执
行
，skill 里的决策树由模型阅读并模拟——前者是代码控
制流，后者是自然语言编码的推理路径。这个差异决定了二者的适用边界。
Skill 体系
的本质：用文件系
由服务），以零基础设施依
赖
统结构 + 文本决策树，替代运
行
换取极简部署。确定性不如专用 agent，但对
时服务（向量库、图引擎、路
大
多数专业流程
```

## PDF 第9页

[查看原页](RAW.pdf#page=9)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
场景够用。
以 web 概念类比，基于 langChain 等框架开
发相当于 IaaS/SaaS——自建 workflow、管理
上下文、实现 tools、
接入 mcp。skill 更像 FaaS，agent 工具作为基座已经提供了 skill 的
发现与加载，以及基于 bash 的文本操作
脚
本执
行
能力，skill 专注业务流程抽象就够了。
需要更高准确性/SLA 时，也可以选
择把 skill "翻译
"为专用 agent：用 mcp/tools 替代脚
本，用流程编排替代决策树，用 observation 节点替代自查。
、
FaaS 不适合长连接
逻 辑 复杂 到 context agent。
、
高频低延迟或复杂有
爆 炸的 场 景 ， skill 状态事务。同样，对流程确定性要求 100%、或
也 撑不 住 ，还 是 要 回 到 LangGraph 定制 专用
总结
```

## PDF 第10页

[查看原页](RAW.pdf#page=10)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
本文系
点：
统梳理了 Agent Skill 从概念理解到迭代编写的完整实
践路径。核心要点可归纳为三
一是明确定位，Skill 本质是轻量级
场景，而非替代专用 Agent 框架；
的领域知
识封装，适用于半自动化、专家经验导向的
二是遵循设计原则，采用三层渐进式加载架构，用决策树替代模糊判断，负向约束配合
替代方
案，并建立内部自查与外部 eval 的双重验证机制；
三是迭代式开
发，借助 skill-creator 和 skill-judge 等工具，通过"生成→评估→修订"的
快速循环提升 Skill 质量。
对于希望将业务经验沉淀为可复用 AI 能力的团队，Skill 提供了一条零基础设施依
赖、
低部
署成本的可
行
路径。但需谨记其适用边界——当流程确定性要求 100% 或逻辑复杂度导致上
下文爆炸时，仍可选
择
LangGraph 等专用 Agent 框架进
行定向优化。最终，Skill 的价值不
在于技术本身，而在于能否将隐性专家经验转化为显性、可执
行、可验证的知
识资
产。
团队介绍
本文作者其
林
，来自淘天集团-物流技术团队。本团队
深耕于物流的数字化协同与运营领域；
为淘天业务提供多样的物流经营管理方
案及工具；为商家提供高效低成本的物流解决
方
为消费者提供便捷靠谱的物流体验。我们团队有自研的先进的技术框架，有成熟的敏捷实
开
发模式，以先进的技术框架及开
发模式
不
断升级自己，以满足和驱动庞
大、复杂、
多
变
案；
践
的
电商物流体系
展。
发
¤ 拓展阅读 ¤
3DXR技术 | 终端技术 | 音视频技术
服务端技术 | 技术质量 | 数据算法
大淘宝技术
大淘宝技术官方账号
967篇原创内容
公众号
```

## PDF 第11页

[查看原页](RAW.pdf#page=11)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
阅读 9690
留言 2
写留言
桥口山东 6月13日
点赞，再有
详细的实际案例就好了
墨香同学的… 浙江 6月12日
```
