# Harness 工程之道：Skill 原理与最佳实践：PDF文本转写

> 仅转写原PDF文本层，页码为物理页序。图表、代码版面、未加载区域的限制见AI笔记与META；文本提取为空不表示原页为空白。

[原始PDF](RAW.pdf) · [AI学习笔记](AI_Skill原理与最佳实践.md) · [来源与核验](META.json)

## PDF 第1页

[查看原页](RAW.pdf#page=1)

```text
Harness ⼯程之道：Skill 原理与最佳实践
张梦杰 阿⾥技术 2026年8⽉17⽇ 04:05 浙江 107⼈
这是2026年的第 52 篇⽂章
（ 本⽂阅读时间：约 15 分钟 ）
Agent Skills 是⼀种轻量、开放的能⼒扩展规范，⽤于为 AI Agent 扩展专业知识和⼯
作流。本⽂从概念原理出发，结合真实的⼯程化项⽬ trade-ab-skill，系统性地讲解
Skill 的结构规范、触发机制、作⽤域优先级，以及最佳实践。（⽂章内容基于作者个⼈
技术实践与独⽴思考，旨在分享经验，仅代表个⼈观点。）
01
Skill 的产⽣与核⼼理念
1.1 从 Prompt ⼯程到 Skill ⼯程的演进
当前的⼤模型都存在⼀个共性：每轮对话都是「失忆」的，必须从零开始构建上下⽂，由此发展
出了 Prompt ⼯程。⽐如 CLAUDE.md 将团队的技术选型、编码规范、架构约束等都固化为⼀
份 Agent 可读的配置⽂档。每次会话启动时，Agent 就会⾃动加载这些信息，直接进⼊⾼效协
作模式，不需要每次都从头到尾交代背景。
但是随着复杂性的增加，问题也逐渐暴露出来。传统的 Prompt ⼯程将所有领域知识⼀股脑塞进
提示词，项⽬越复杂，Prompt 越臃肿。上下⽂窗⼝被撑满，模型的注意⼒被稀释，真正关键的
信息反⽽容易被"淹没"。并且这些知识和具体项⽬深度耦合，换个场景就得重写⼀遍，⼏乎没有
复⽤性可⾔。
```

## PDF 第2页

[查看原页](RAW.pdf#page=2)

```text
Agent Skill 的出现正是为了解决这些问题，它将领域知识和⼯作流封装为可移植、可版本控制
的⽂件夹，⽤来"教"Agent 如何处理特定任务或⼯作流，Agent 按需加载。你可以将 Skills 类
⽐成新员⼯⼿册。这也是 Anthropic 官⽅博客⽤的类⽐：Skills 是给 AI Agent 的「⼊职指
南」，把领域知识打包成可发现、模块化的能⼒。
下⾯是 Agent Skills 的官⽅定义：
"Agent Skills are a lightweight, open format for extending AI agent capabilities with
specialized knowledge and workflows."
1.2 核⼼理念：渐进性披露
Skill 体系最核⼼的设计理念是渐进性披露（Progressive Disclosure），即只在需要时才加载
需要的知识，⽽⾮⼀次性加载全部。
Skill 的渐进性披露 主要分三阶段：
Discovery（发现）阶段：当会话启动时仅会加载每个 Skill 的 name 和 description，这
部分是以常驻⽅式注⼊ Agent 上下⽂中的。
Activation（激活）阶段：当任务匹配上 description 时，将读取完整的 SKILL.md，加载
SKILL.md 中的路由表和全局规则，但还不加载⼦模块。
Execution（执⾏）阶段：按路由表加载对应的模块⽂件，按需读取参考⽂档，只加载当前
任务真正需要的知识。
该模型在实际应⽤中带来的性能提升是显著的，绝⼤部分请求仅需要部分资源。渐进性披露⽤最
⼩的上下⽂成本，换取了最⼤的知识覆盖范围，确保上下⽂窗⼝留给真正重要的信息，这就是"按
需投放知识"的核⼼经济学优势。同样也保证了决策的精准性和 Skill 的可扩展性。
1.3 System Prompt 与 Skill 的区别
⽂件类型 System Prompt Skill
定位 项⽬级全局规则、编码规范 特定领域能⼒封装
加载策略 会话启动时全量加载 渐进式按需加载
⽣效范围 当前项⽬ 可跨项⽬、跨会话（取决于作⽤域配置）
上下⽂成本 恒定占⽤，与任务⽆关也会消耗 仅在命中时加载，未命中零成本
结构化 单⽂件，扁平组织 多⽂件模块化，⽀持脚本和资源
适⽤场景 编码⻛格、项⽬约定、通⽤约束 完整⼯作流、多步骤流程、领域专家知识
简单记法：System Prompt 是"这个项⽬的规矩"，Skill 是"⼀种可复⽤的能⼒"。
```

## PDF 第3页

[查看原页](RAW.pdf#page=3)

```text
⼀个项⽬可以同时拥有 System Prompt 和多个 Skill：System Prompt 定义全局编码规范和项
⽬约定，Skill 封装特定领域的⼯作流。两者协同⼯作——System Prompt 中的规则对所有
Skill ⽣效，⽽ Skill 内部的规则仅在激活时叠加。
02
Skill 的结构组成
2.1 ⽬录结构规范
⼀个 Skill 的核⼼就是⼀个包含 SKILL.md 的⽂件夹：
1 my-skill/ # 必需：skill名称，短横线分隔
2 ├── SKILL.md # 必需：主⽂件，包括元信息 + 指令，⽂件名需全⼤写
3 ├── scripts/ # 可选：可执⾏脚本
4 ├── references/ # 可选：参考⽂档
5 ├── assets/ # 可选：模板、资源
6 └── ... # 任意额外⽂件
这种格式已被 Claude Code、Cursor、GitHub Copilot、Gemini CLI 等 40+ 主流 Agent 产品
⼀个设计良好的 Skill ⽬录结构，是渐进性披露能否有效落地的基础。核⼼思想是主⽂件做路
由，模块⽂件做执⾏。
2.2 SKILL.md ⽂件结构
SKILL.md 是每个 Skill 的唯⼀⼊⼝，也是唯⼀的"触发器"，其结构分为两部分：frontmatter
元信息和正⽂指令。
frontmatter 是 YAML 格式的元信息块，最核⼼的两个字段是 name 和 description：
1 ---
2 name: trade-ab-skill
3 description: 为⽤户提供 AB 实验的创建与修改能⼒，⽀持实验创建、调流量、
4 加桶删桶、实验下线等操作。当⽤户提到创建实验、修改实验、调流量、加桶删桶、
5 实验下线等场景时触发。
6 ---
下⾯是以 Claude Code 为例的完整 frontmatter 字段：
维度 字段 是否必填 约束 ⽤途
```

## PDF 第4页

[查看原页](RAW.pdf#page=4)

```text
最⻓ 64 字符，
只 能 ⽤ ⼩ 写 字 Skill 的唯⼀标识
⺟、数字和连字 符，同时也是⽂
name 必填 符，不能以连字 件夹名。Agent
符开头或结尾； 通过它来定位和
若省略默认使⽤ 管理 Skill
⽬录名
Skill 能否被正确
触发的关键。Ag
ent 靠这段描述
身份字段（触发 最 ⻓ 1024 字
来判断当前任务
机制） 符，不能为空；
是否该调⽤这个
description 必填 若省略默认使⽤
Skill，需要写清
SKILL.md 正 ⽂
楚做什么（WHA
第⼀段
T）以及什么时候
该 ⽤ 它 （ WHE
N）
参数提示格式， 在/菜单中显示，
如[source direc 帮助⽤户了解该
argument-hint 可选
tory] [output fo Skill 接受的输⼊
rmat] 格式
设为 true 时，
disable-model 布尔值（true/fa 禁⽌模型⾃动调
可选
-invocation lse） ⽤该 Skill，仅允
许⽤户⼿动触发
设为 false 时，
⽤户不能直接调
布尔值（true/fa
user-invocable 可选 ⽤该 Skill，只有
lse）
模型可以⾃动调
⽤
权限字段（权限
控制）
⼯ 具 名 列 表 ， ⼯具⽩名单，精
如 Read, Grep, 确控制 Skill 执
allowed-tools 可选
Glob, Write, Ba ⾏时可调⽤的⼯
sh(python:*) 具及其权限范围
指定该 Skill 使
⽤的模型；建议
模型名称，如 ha
model 可选 简单任务⽤ Haik
iku、sonnet
u 提升响应速度
并降低成本
执⾏字段（运⾏ context 可选 可选值：fork 执⾏上下⽂；设
时环境） 为 fork 时，将
```

## PDF 第5页

[查看原页](RAW.pdf#page=5)

```text
在隔离的⼦智能
体中执⾏，确保
不污染主对话上
下⽂
可选值：Explor
⼦智能体类型；
e、Plan、gener
agent 可选 当 context 设
al-purpose 或
为 fork 时⽣效
⾃定义 Agent
⽣命周期事件钩
⽀持 PreToolUs
⼦，定义 Skill
hooks 可选 e、PostToolUs
激活期间的事件
e 等钩⼦事件
处理逻辑
⽤于版本控制和
语义化版本号（s 追踪迭代，⽅便
version 可选 emver），如 1. 团队协作时知道
0.0 当前⽤的是哪个
版本
正⽂部分可以直接看 Skill 例⼦的正⽂，此处不展开赘述。
03
触发机制
Skills 的触发机制是整个系统中最为关键的环节，直接决定了 Skill 能否在恰当时机被
激活。这⼀点甚⾄⽐ Skills 内容本身质量更为重要。
3.1 ⾃动触发和⼿动触发
Skills ⽀持⾃动触发（语义匹配）和⼿动触发两种机制：
⾃动触发：靠的是 description 字段。当⽤户的意图和 Skill 描述语义匹配时，Agent 会⾃⼰判
断"这个任务我有现成的专业流程可以⽤"，然后主动加载对应的 Skill。整个过程⽤户⽆感，就像
⼀个⽼员⼯听到需求就⾃动翻出了对应的 SOP。
⼿动触发：⽤户通过斜杠命令（如 /skill-name）显式调⽤。这适合⽤户明确知道⾃⼰要⽤哪个
Skill 的场景，相当于直接点名"⽤这套流程来⼲活"。
两种机制互补：⾃动触发降低使⽤⻔槛，让 Skill 对新⽤户"隐形"⽣效；⼿动触发给⽼⽤户精确
控制权，想⽤哪个你说了算。
3.2 description 书写规范
```

## PDF 第6页

[查看原页](RAW.pdf#page=6)

```text
语义匹配机制完全依赖于 description 字段，description 是 Skill 能否被正确触发的核⼼。
Claude Code 推荐的书写公式为：功能定义 + 触发场景 + 核⼼能⼒。
写好它需要遵循⼏个原则：
同时回答 WHAT 和 WHEN。不能只说"处理⽂档"这么含糊，要明确写出这个 Skill 做什么、
在什么场景下该被调⽤。
枚举具体的触发词：Agent 做语义匹配时，关键词越具体命中率越⾼。在 description 中显
式列出⽤户可能使⽤的关键词——不只是术语，还包括⼝语化的说法。"创建实验"、"新
建"、"做个实验"、"建个AB"——这些都要写进去。
⽤第三⼈称。description 会被注⼊系统提示词，所以要写成客观描述⽽⾮对话语⽓。
写 "Generates API documentation from source code" ， ⽽ 不 是 "I can help you
generate docs"或"You can use this to..."。
划定排除边界（可选）：在描述中明确地标注出不适⽤的场景，降低误触发概率。
04
作⽤域与优先级
Skill 的作⽤域决定了它在哪些场景下可⽤。主流 Agent 产品通常⽀持两级作⽤域：
位置 ⽣效范围 适⽤场景
企业配置中⼼ 全员⽣效 强制执⾏的企业级开发规范与安全策略
⽤户主⽬录下全局配置 个⼈所有项⽬ 通⽤⼯具、个⼈偏好、跨项⽬能⼒
项⽬根⽬录或 .skills/ ⽬录 仅当前项⽬ 项⽬特定⼯作流、团队约定
Plugin 内置资源 Plugin 启动时 社区共享的能⼒包、特定框架的专⽤指令集
当多个 Skill 同时存在时，可能出现触发冲突——两个 Skill 的 description 都匹配⽤户输⼊。
优先级规则通常遵循以下层次：
企业策略 > 个⼈配置 > 项⽬配置 > Plugin 内置
05
Skill 最佳实践
5.1 Skill 正⽂即路由器：编排⽽⾮堆砌
核⼼理念：
SKILL.md 的正⽂应该是"路由器"⽽⾮"知识仓库"，它的职责是分发任务到正确的模块，⽽⾮
包含所有相关信息和业务细节；
```

## PDF 第7页

[查看原页](RAW.pdf#page=7)

```text
SKILL.md 应控制在 500⾏ 以内，500⾏⽂本等于2000～3000 token，是单个 Skill 激活
后⽐较合理的上下⽂开销。
在 SKILL.md 中引⽤辅助⽂件时，应当建⽴⼀份明确的契约：触发的时机+资源位置+预期的
产出，不能只给出路径。
最佳实践：SKILL.md 只保留路由表和全局规则，业务细节下沉到模块⽂件。
1 # ✅ 最佳实践：SKILL.md 是路由器
2 ## 意图路由表
3 | 场景示例 | 路由模块 | 加载⽂件 |
4 |-----------------|-----------|------------------------------|
5 | "创建实验" | creator | modules/creator/creator.md |
6 | "实验XX调流量" | modifier | modules/modifier/modifier.md |
7 ## 全局安全红线
8 1. 禁⽌调⽤万能⼯具
9 2. 禁⽌编造数据
10 3. 写模块限定接⼝
5.2 知识分层策略：何时拆分、如何组织
什么时候该拆⽂件？ ⼀条经验法则：当⼀个⽂件超过 300 ⾏，或某个 Step 的规则超过 100 ⾏
时，就是拆分信号。⽂件太⻓不光浪费 token，还会让 Agent 的注意⼒在⼤段⽂本中迷失。
如何组织知识分层？根据使⽤频率对知识进⾏分层组织。 越频繁⽤到的知识，离⼊⼝越近；越偶
尔查阅的知识，越往深处放。这样 Agent 每次只加载当前步骤真正需要的内容，不会把上下⽂窗
⼝塞满⽆关信息。
实践中可以⽤⼀棵简单的决策树来判断：
实践：trade-ab-skill 的分层
```

## PDF 第8页

[查看原页](RAW.pdf#page=8)

```text
1 trade-ab-skill/
2 ├── SKILL.md ← 意图路由表、全局安全红线（每次激活必读）
3 ├── modules/creator/creator.md ← 创建流程 Step 编排、scenarioId
4 ├── modules/creator/collect-phase.md ← 参数填充的 11 项执⾏清单（仅 Step
5 ├── modules/creator/validate-phase.md ← 校验规则（仅 Step 3 才读）
6 ├── modules/creator/tools.md ← MCP ⼯具接⼝列表（调接⼝时按需查阅
7 └── modules/creator/safety.md ← 安全约束详细规则（validate 阶段按
5.3 安全实践 - Tool 的权限设计与⼯具隔离
这是⼯程级 Skill 最关键的安全实践之⼀。 当 Skill 涉及多个模块、调⽤多个 MCP 接⼝时，必
须实施模块级的⼯具隔离——每个模块只能调⽤其⽩名单中的接⼝，遵循权限最⼩化原则。
设计原则：
1. ⽩名单制：每个模块的 tools.md 明确列出可⽤接⼝，⽩名单外⼀律禁⽌；
2. 危险接⼝显式禁⽤：万能⼯具（如直接 HTTP 调⽤）全局禁⽌；
3. ⼯具隔离：不同模块使⽤不同的接⼝集合，防⽌误调⽤。
最佳实践：
Claude Code 的 allowedTools 配置，控制 Skill 执⾏时可调⽤的⼯具，⽀持 Bash 的前缀
匹配控制；
trade-ab-skill 中的隔离实践：实验创建接⼝仅在 creator ⽩名单中；modifier 只能⽤实
验修改接⼝；审批/发布接⼝在所有模块中均禁⽌调⽤；modifier 模块明确标注易混淆接⼝
的禁⽌规则。
5.4 脚本增强：扩展 Skill 能⼒边界
核⼼理念：将确定性计算逻辑封装为脚本，由 Agent 调⽤执⾏⽽⾮⾃⾏推导。脚本是 Skill 突破
LLM 能⼒边界的利器。
什么时候需要写成脚本？
如果这件事让 LLM 做有概率出错，但让脚本做能 100% 确定性完成，那就该封装成脚本。
如果发现⾃⼰在 SKILL.md 中编写公式让 Agent 运⾏计算，该逻辑也应该被挪到脚本中。
场景 纯指令的局限 脚本的优势
配置⽂件读写 LLM 可能写⼊格式错误的 JSON 脚本保证格式正确，原⼦写⼊
环境检测 LLM ⽆法可靠检测系统状态 脚本直接查询，返回结构化结果
⽇志采集 LLM 不应直接处理⽹络请求 脚本封装 HTTP 调⽤，异常⾃处理
```

## PDF 第9页

[查看原页](RAW.pdf#page=9)

```text
复杂计算 LLM 算术不可靠 脚本精确计算
脚本的设计遵循四个原则：
1. ⾃愈性——脚本内部处理所有异常，始终正常退出，绝不阻断 Skill 主流程
2. 结构化输出——统⼀输出 JSON，⽅便 Agent 解析和流转
3. 幂等性——多次执⾏结果⼀致，预检脚本只追加缺失项，不覆盖已有配置
4. 安全边界——只操作指定⽂件，不触碰其他系统资源
最佳实践：
trade-ab-skill 就内置了两个关键脚本：MCP预检脚本负责在 Skill 启动前⾃动检测 MCP 依赖
是否就绪；⽇志采集脚本负责采集实验操作⽇志。Agent 只需要调⽤脚本、读取返回的 JSON，
不⽤⾃⼰去"猜"环境状态。
5.5 参数传递与动态注⼊
Skill 不仅是静态指令，更⽀持运⾏时参数传递和上下⽂预注⼊。在执⾏过程中，需要在多个阶段
之间传递参数。良好的参数传递机制应满⾜：
显式：参数来源和去向清晰可追溯
可校验：每个阶段有⻔卡检查参数完整性
防丢失：关键参数在快照中持久化
最佳实践：trade-ab-skill 的参数传递模型：采⽤快照（Snapshot）机制作为跨阶段参数传递
的载体。每个阶段将产出写⼊快照，下⼀阶段从快照读取。阶段⻔卡确保参数完整性。
动态注⼊：执⾏中的⼀些参数可以由⽤户直接提供，也可以在执⾏过程中动态获取：
businessName：通过业务信息查询接⼝按当前⽤户⼯号动态查询
scenarioId：根据⽤户输⼊的业务关键词，从对照表动态匹配
metricBindingBases：固定使⽤指定模板展开的指标数组
最佳实践：trade-ab-skill 的⽤户偏好持久化：成功操作后，将关键参数写⼊ user-
prefs.json，下次执⾏时⾃动注⼊：
1 {
2 "defaultScenarioId": "<场景ID>",
3 "defaultMetricTemplateId": "<模板ID>",
```

## PDF 第10页

[查看原页](RAW.pdf#page=10)

```text
4 "recentExperimentIds": ["<实验ID1>", "<实验ID2>"],
5 "lastUsed": "2026-06-17",
6 "usageCount": 2
7 }
5.6 测试与迭代
测试维度
Claude Code 官⽅推荐了三类核⼼测试⽅法：
触发测试：测试 description 是否能被正确匹配，准备 10 个左右的⾃然语⾔变体去触发
Skill，检查是否都能正确激活，同时验证不相关的输⼊是否会误触发。
功能⾛查：⽤⾃然语⾔驱动完整流程，检查每个阶段的输出是否符合预期。重点关注路由是
否准确分发、渐进加载是否按时序⼯作、红线规则是否被遵守、异常场景是否正确熔断。别
只跑 happy path——故意输⼊边界值、模拟⼯具不可⽤、尝试让 Agent 调⽤禁⽌接⼝，才
是真正暴露问题的场景。
性能对⽐：针对同⼀任务，分别⽤"⽆ Skill"和"有 Skill"两种⽅式各跑 5 次，对⽐ Token ⽤
量和完成质量。
如何⾼效迭代？
与传统软件的 bug 修复逻辑⼀致：发现问题 -> 定位原因 -> 修复⽂档 -> 验证效果
较为⾼效的⼀种迭代⽅法是观测驱动迭代——通过⽇志埋点收集每次执⾏的状态结果（成功/
失败/取消）、耗时、调⽤的⼯具列表，⽤数据定位薄弱环节。
最佳实践：
trade-ab-skill 的⽇志采集机制，采⽤了两阶段 traceId 配对追踪，保障了⽇志埋点的采集。
06
⽤ skill-creator 从零创建⼀个 Skill
skill-creator 是⼀个⽤来创建和打包 Skill 的辅助⼯具，本身也是⼀个 Skill。可以协助你从零
搭建⼀个 Skill。
Step 0：前置准备
确保本地已安装以下⼯具：
```

## PDF 第11页

[查看原页](RAW.pdf#page=11)

```text
Git（已配置 SSH Key，可访问公司内部代码仓库）
⼀个可以进⾏对话的 AI 助⼿，可以使⽤ Qoder 等⽀持⽂件操作的⼯具
Step 1：初始化⽬录结构
告诉 AI：
「帮我⽤ skill-creator ⽣成⼀个名为 order-query 的 Skill」
AI 会⾃动运⾏初始化脚本，⽣成标准⽬录：
1 order-query/
2 ├── SKILL.md ← 核⼼⽂件（必须）
3 ├── scripts/ ← 可执⾏脚本（可选）
4 └── references/ ← 参考⽂档（可选）
Step 2：编写 SKILL.md
告诉 AI：
「帮我编写 order-query 的详细内容，这个 Skill 的功能是 xxx，主要⽤于 xxx 场景，触发词
包括 xxx、xxx。」
AI 会帮你⽣成包含 YAML frontmatter 和正⽂的完整 SKILL.md。写作要点：description 要
包含所有可能的触发词；正⽂只写领域专有知识，不写常识；复杂内容拆到 references/ ⽬录，
SKILL.md 中⽤相对路径引⽤；控制在 500 ⾏以内。
Step 3：添加参考⽂档（可选）
如果有复杂的操作流程或参考资料：
告诉 AI：
「把 xxx 的详细流程整理成 references/workflow.md，并在 SKILL.md 中加上引⽤。」
Step 4：打包验证
告诉 AI：
「⽤ skill-creator 打包验证 order-query，检查格式是否合规。」
打包脚本会⾃动校验：frontmatter 是否完整、name 和 description 是否存在、⽬录中是否有
⾮法⽂件。有问题 AI 会直接告诉你哪⾥不对并帮你修复。
Step 5：推送到远端仓库
```

## PDF 第12页

[查看原页](RAW.pdf#page=12)

```text
告诉 AI：
「帮我把 order-query 初始化为 git 仓库，关联远端地址，提交所有⽂件并推送到 main 分
⽀。」
Step 6：后续迭代更新
修改 Skill 内容后，告诉 AI：
「帮我提交 order-query 的最新改动，commit 信息是 xxx，然后推送。」
整个流程可以浓缩为⼀张图：
1 下载 skill-creator
2 ↓
3 告诉 AI：初始化⽬录
4 ↓
5 告诉 AI：编写 SKILL.md + references
6 ↓
7 告诉 AI：打包验证
8 ↓
9 告诉 AI：git 提交并推送
10 ↓
11 告诉 AI：迭代修改并推送
12
是不是很简单？从头到尾你没有⼿动执⾏过任何命令。你只负责描述意图，AI 负责执⾏，这就是
参考⽂档
[1] Agent Skills 官⽅⽂档：https://agentskills.io
[2]《Agent Skills 橙⽪书：给AI装技能的完全指南》
[3]《Claude Code 实战 Harness ⼯程之道》
[4]《Harness ⼯程：从上下⽂管理到 Agent 系统构建》
*注：本⽂以集团内部 trade-ab-skill 项⽬为真实案例，所有代码示例均来⾃该项⽬实际运⾏的
Skill ⽂件。
```

## PDF 第13页

[查看原页](RAW.pdf#page=13)

```text
欢迎留⾔⼀起参与讨论~
阅读 9455
留⾔ 6
写留⾔
五⽑ 四川 8⽉18⽇ 1
最近在实战skill，在⾃⼰仓库迭代了⼏个，很有帮助，从⽂中也学到了标准⽬录结构，这个很
有帮助
pandaman 北京 8⽉18⽇
@元宝⽂案提取提取核⼼内容
```

## PDF 第14页

[查看原页](RAW.pdf#page=14)

```text
Jh 天津 8⽉18⽇
⽜哇
. 中国⾹港 8⽉17⽇
@元宝⽂案提取提取⽂章内容
zxf945 浙江 8⽉17⽇
@元宝⽂案提取总结下
毕竟是王哈哈 北京 8⽉17⽇
怎么⾃动化迭代skill
⾸评
```

