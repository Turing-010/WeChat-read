# 5 人 7 天干完 20 人数周的活：Spec-Driven Development 如何重新定义 AI 编程：PDF文本转写

> 仅转写原PDF文本层，页码为物理页序。图表、代码版面、未加载区域的限制见AI笔记与META；文本提取为空不表示原页为空白。

[原始PDF](RAW.pdf) · [AI学习笔记](AI_规格驱动AI编程.md) · [来源与核验](META.json)

## PDF 第1页

[查看原页](RAW.pdf#page=1)

```text
5 ⼈ 7 天⼲完 20 ⼈数周的活：Spec-Driven Development 如何重
新定义 AI 编程
王砚舒（彦纾） 阿⾥技术 2026年9⽉4⽇ 03:08 浙江 37⼈
这是2026年的第 58 篇⽂章
（ 本⽂阅读时间：约 20 分钟 ）
前⾔：「5 ⼈ 7 天」 实验
本⽂分享⼀个案例。5⼈、7天，⽤ Qoder 开发 QoderWork，完成了传统情况下需要 20 ⼈
数周的⼯作量。它的时间线值得逐⽇复盘：
DAY 0：不写⼀⾏代码，只写 Spec。
团队花了⼀整天做四件事：定义 MVP 边界、拆解模块、为每个模块撰写 Spec、将所有 Spec
汇⼊ Repo Wiki。这⼀天的产出是零⾏代码，但它决定了后⾯六天的⼀切。
DAY 1-2：⽤ Qoder 完成架构开发。
框架与容器同步开发。每个⼈都是 “Spec ⼯程师”，即定义代码应该⻓什么样的⼈；通过 Skill
驱动并⾏推进，Quest 模式同时执⾏多个开发任务。两天时间，系统⻣架成型。
DAY 3-4：Spec 迭代增量需求。
发现新需求或 BUG？不⽤排期，⽴即写⼀个增量 Spec，委派 Quest 执⾏。AI ⾃动写代码并
提交 PR，⼈负责 Review 与合并。单⼈⽇均处理多个 PR，效率抬升。
```

## PDF 第2页

[查看原页](RAW.pdf#page=2)

```text
DAY 5-6：打磨、Dogfooding 。
⽤ QoderWork 的早期版本测试 QoderWork ⾃身。发现问题就写 Spec，Quest 修复。这是
⼀个⾃举式的正反馈循环。
DAY 7：正式发布上线。
七天，从零到⼀个可⽤的产品。
这个案例之所以震撼，不是因为“AI 写代码很快”，快只是表象。真正值得追问的是：为什么 5
个⼈能驾驭 AI 同时推进这么多并⾏任务⽽不失控？
答案藏在 DAY 0，那个看似 「什么都没做」的⽇⼦⾥，那⼀天写下的 Spec，就是整个项⽬的
锚点。这套⽅法论有⼀个正式的名字：Spec-Driven Development（SDD ）。
01
SDD 是什么：代码只是 Spec 的副产品
1.1 ⼀句话定义
Spec-Driven Development：将规格说明（Specification）作为唯⼀真实来源（Single
Source of Truth），代码作为其派⽣产物。
⽤更直⽩的话说，就是先定义 WHAT，再让 AI 做 HOW。
如果我们做过 API-First Development、Design by Contract、或者严格的 TDD ，就会觉
得 SDD 似曾相识。但 SDD 的核⼼差异在于，它是为 AI 编程时代 量身设计的⼯程⽅法。
在传统开发中，Spec 写得好不好主要影响沟通效率；在 AI 编程时代，Spec 写得好不好 直接
决定代码质量。因为 AI 不会追问”这个边界情况怎么处理“，它只会按照⽤户给的上下⽂尽⼒推
断。推断对了是运⽓，推断错了是 Bug。
1.2 不是⼀个⼈的发明，⽽是⼀个时代的汇聚
SDD 没有单⼀发明者。2025 年，多个⽅向同时收敛到了这个理念：
Karpathy 的 Vibe Coding （2025.2.2）作为反⾯参照，暴露了 "不管代码、只管
vibes" 的致命问题，倒逼社区思考 "AI 编程到底需要什么样的约束"；
GitHub 推出 Spec Kit，提供了 agent-agnostic 的 SDD ⼯具链；
AWS 发布 Kiro，成为第⼀个内置 SDD ⼯作流的 IDE；
Fission-AI 的 OpenSpec，⾛轻量迭代路线；
阿⾥的 QoderWork，通过 Qoder Quest 模式实践了 SDD 的规模化执⾏。
```

## PDF 第3页

[查看原页](RAW.pdf#page=3)

```text
这种多⽅同时推动的局⾯，说明 SDD 是 AI 编程发展到当前阶段的结构性需求。
1.3 Microsoft 的那句点评
Microsoft 对 SDD 有⼀个精辟的评价，如下。
"SDD is version control for your thinking."
传统的版本控制管理的是代码的演变历史，SDD 管理的是思考的演变历史：为什么做这个功
能、边界在哪⾥、成功标准是什么。当代码可以被 AI 秒级重写时，真正有价值的是代码背后的
决策。
02
SDD 完整流程拆解
2.1四阶段模型
SDD 的标准流程分为四个阶段：
1 Specify（规格定义）-> Plan（⽅案规划）-> Implement（代码实现）-> Validate（验证
阶段 主导者 核⼼产出 关键动作
Specify ⼈ spec.md 定义问题、边界、成功标准
Plan ⼈ + AI plan.md 架构选型、模块划分、接⼝定义
Implement AI 代码 + 测试 按 plan 逐任务实现
Validate ⼈ + AI 测试报告 ⾃动化测试 + ⼈⼯ Review
⼈机分⼯的核⼼原则：⼈定义 WHAT，AI 实现 HOW。
在实践中，Specify 和 Plan 之间会有多轮迭代，Implement 和 Validate 之间也是持续循环
的。
2.2 三⽂件体系：Spec Kit 的核⼼设计
GitHub 的 Spec Kit 提出了⼀个简洁的三⽂件体系：
spec.md —— 需求规格
这是「唯⼀真实来源」。它回答“做什么”和“为什么做”，不涉及“怎么做”。
```

## PDF 第4页

[查看原页](RAW.pdf#page=4)

```text
1 # Feature: ⽤户权限管理模块
2 ## Problem Statement
3 当前系统缺乏细粒度的权限控制。所有⽤户要么是管理员（全部权限），
4 要么是普通⽤户（只读权限）。产品团队需要⽀持⾄少 5 种⻆⾊，
5 以满⾜不同部⻔的差异化需求。
6 ## Success Metrics
7 - ⽀持⾃定义⻆⾊，每个⻆⾊可配置不少于 20 种独⽴权限
8 - 权限校验 API 响应 P95 < 50ms
9 - 权限变更实时⽣效，⽆需⽤户重新登录
10 - 向后兼容：现有管理员/普通⽤户的权限⾏为不变
11 ## User Stories
12 1. 作为系统管理员，我可以创建⾃定义⻆⾊并分配权限组合
13 2. 作为部⻔主管，我可以将部⻔成员批量分配到指定⻆⾊
14 3. 作为普通⽤户，我的权限变更后⽆需重新登录即可⽣效
15 ## Acceptance Criteria
16 - [ ] RBAC 模型⽀持⻆⾊继承（最多 3 层）
17 - [ ] 单⽤户可拥有多个⻆⾊，权限取并集
18 - [ ] 提供权限变更审计⽇志，保留 90 天
19 - [ ] 权限校验⽀持通配符匹配（如 `resource:*:read`）
20 ## Non-Goals
21 - 本期不实现跨组织的权限委托
22 - 不⽀持基于时间段的临时权限
23 - 不涉及 UI 层的权限管理界⾯（由前端团队单独出 Spec）
24 ## Constraints
25 - 必须兼容现有的 OAuth2.0 认证流程
26 - 权限数据存储使⽤现有 PostgreSQL 实例，不引⼊新的存储组件
27 - 权限模型设计需参考 AWS IAM Policy 语法规范
我们需要注意这个 Spec 的⼏个特征，如下。
成功标准是可测试的："P95 < 50ms" ⽽⾮ "系统应该很快"；
Non-Goals 明确划定了边界：告诉 AI "这些不要做"；
Constraints 约束了技术选型：防⽌ AI ⾃作主张引⼊新组件。
plan.md —— 架构⽅案
基于 spec.md ⽣成的技术⽅案。这⼀步通常由 AI 起草，⼈负责审核修改。
1 # Plan: ⽤户权限管理模块
2 ## Architecture Decision
3 采⽤ RBAC (Role-Based Access Control) 模型，使⽤ Casbin 作为权限引擎。
4 ## Module Breakdown
5 1. `permission-model` - 权限模型定义与 Casbin 适配层
6 2. `permission-api` - RESTful API 层
```

## PDF 第5页

[查看原页](RAW.pdf#page=5)

```text
7 3. `permission-cache` - Redis 缓存层（解决 P95 < 50ms 要求）
8 4. `permission-audit` - 审计⽇志模块
9 ## Interface Contracts
10 ### POST /api/v1/roles
11 ### GET /api/v1/users/{userId}/permissions
12 ### PUT /api/v1/roles/{roleId}/permissions
13 （接⼝详细定义省略）
14 ## Risk Assessment
15 - ⻛险：⻆⾊继承层级过深可能导致权限计算性能下降
16 - 缓解：限制最⼤继承深度为 3 层，权限结果做预计算缓存
tasks.md —— 任务清单
将 plan 拆解为可执⾏的原⼦任务，每个任务对应⼀个可独⽴验证的交付物。
1 # Tasks
2 ## Task 1: 数据库 Schema 设计
3 - 创建 roles、permissions、role_permissions、user_roles 四张表
4 - ⽀持⻆⾊继承的 parent_role_id 字段
5 - 验证：migration 脚本可在空库上成功执⾏
6 ## Task 2: Casbin 适配层
7 - 实现 RBAC 模型的 Casbin 配置
8 - ⽀持通配符匹配
9 - 验证：单元测试覆盖率 > 90%
10 ## Task 3: 权限校验 API
11 - 实现 GET /api/v1/users/{userId}/permissions
12 - 集成 Redis 缓存
13 - 验证：压测 P95 < 50ms
14 （后续任务省略）
2.3 constitution.md：不可变的项⽬原则
除了三⽂件体系，Spec Kit 还引⼊了⼀个重要概念 constitution.md。这是项⽬级别的“宪
法”，定义了不可违背的约束条件，所有 Spec 都必须遵守。
1 # Project Constitution
2 ## Immutable Principles
3 ### 1. API Design
4 - 所有 API 遵循 RESTful 规范，版本化路径（/api/v1/...）
5 - 错误响应统⼀使⽤ RFC 7807 Problem Details 格式
6 - 所有 API 必须有 OpenAPI 3.0 ⽂档
7 ### 2. Security
8 - 所有⽤户输⼊必须经过校验和清洗
9 - 敏感数据（密码、Token）禁⽌出现在⽇志中
```

## PDF 第6页

[查看原页](RAW.pdf#page=6)

```text
10 - 数据库查询必须使⽤参数化查询，禁⽌字符串拼接
11 ### 3. Code Quality
12 - 单元测试覆盖率不低于 80%
13 - 所有公共⽅法必须有⽂档注释
14 - 禁⽌引⼊未经安全审计的第三⽅依赖
15 ### 4. Infrastructure
16 - 所有服务必须⽀持优雅关闭（Graceful Shutdown）
17 - 配置项通过环境变量注⼊，禁⽌硬编码
18 - ⽇志格式统⼀使⽤结构化 JSON
constitution.md 的价值在于，它把团队的技术决策固化为 AI 的「潜意识」。没有它，每个
Spec 都需要重复声明“要⽤参数化查”“要写单元测试”这些基本约束。
03
Spec 怎么写：好 Spec 与坏 Spec 的⽣死线
Spec 写作是 SDD 中最关键、也最容易被低估的环节。经验印证了这⼀点——DAY 0 花整整
⼀天写 Spec，正是因为 Spec 的质量直接决定了 DAY 1-6 的效率。
3.1 好 Spec 的六要素
要素 作⽤ 示例
Problem Statement 定义 "为什么做" "当前系统不⽀持细粒度权限控制"
Success Metrics 定义 "做到什么程度算完" "P95 < 50ms，覆盖 20+ 权限类型"
User Stories 定义 "谁在什么场景下⽤" "作为管理员，我可以创建⾃定义⻆⾊"
Acceptance Criteria 定义 "怎么验证" "单⽤户多⻆⾊，权限取并集"
Non-Goals 定义 "什么不做" "本期不做跨组织权限委托"
Constraints 定义 "技术约束" "必须兼容现有 OAuth2.0 流程"
3.2 好 Spec vs 坏 Spec：⼀组对⽐
坏 Spec：
1 系统需要⼀个快速的搜索功能。搜索结果应该相关且准确。
2 界⾯要美观易⽤。
这个 Spec 有四个致命问题：
1. 模糊——“快速”是多快？100ms？1s？10s？
```

## PDF 第7页

[查看原页](RAW.pdf#page=7)

```text
2. 遗漏边界——搜索什么？全⽂？标题？⽀持模糊匹配吗？
3. 缺乏理由——为什么需要搜索功能？解决什么问题？
4. 混⼊了 HOW——“界⾯要美观”是 UI Spec 的范畴，不应出现在后端功能 Spec ⾥。
好 Spec：
1 ## Problem Statement
2 ⽤户反馈在 10,000+ ⽂档的知识库中找到⽬标⽂档平均需要 3 分钟。
3 ⽬标是将查找时间缩短到 10 秒以内。
4 ## Success Metrics
5 - 搜索 API 响应时间 P95 < 200ms
6 - 搜索结果 Top-5 相关性准确率 > 85%（基于⼈⼯标注测试集）
7 - ⽀持中英⽂混合查询
8 ## Non-Goals
9 - 不实现语义搜索（本期仅关键词匹配 + 分词）
10 - 不⽀持搜索附件内容（仅搜索⽂档标题和正⽂）
差异的本质：好 Spec 是可测试的，坏 Spec 是可解释的。
「系统应该很快」给了 AI ⽆限的解释空间，它可能选择⼀个“对它来说够快”的实现。「P95 <
200ms」则是⼀个硬约束，AI 必须确保实现满⾜这个指标，否则就是 fail。
3.3 粒度控制：⼀个实⽤的检验标准
Spec 的粒度很难拿捏。太粗，AI 会⾃作主张填补⼤量细节；太细，本质上就是在写伪代码，
失去了 SDD 的意义。
Spec Kit 提出了⼀个优雅的检验标准：
"⽤不同技术栈实现这个 Spec，Spec 是否仍然有效？"
如果 Spec 写了“使⽤ Redis 的 ZSET 结构存储排⾏榜”，那它只对 Redis ⽅案有效，换成
PostgreSQL 实现就失效了。这说明把 HOW 混进了 WHAT。
如果 Spec 写了“排⾏榜需⽀持实时更新，延迟不超过 1 秒，⽀持 Top-100 查询”，那⽆论底
层⽤ Redis、PostgreSQL 还是⾃研存储，这个 Spec 都成⽴。这才是正确的粒度。
当然，Constraints 部分可以出现技术约束，但那是“外部限制”（⽐如“必须使⽤现有
PostgreSQL 实例”），不是「实现⽅案」。
3.4 淘特团队的实战经验
淘特团队在实践 SDD 时发现⼀个重要规律：Spec 编写需要 3-5 次迭代才合格。
```

## PDF 第8页

[查看原页](RAW.pdf#page=8)

```text
第⼀版 Spec 通常问题百出，⽐如遗漏边界条件、成功标准模糊、Non-Goals 不够明确等。
让 AI 基于第⼀版 Spec ⽣成 plan 之后再回头审视 Spec，往往能暴露出⼤量盲点。这个
「Spec -> Plan -> Review Spec -> 修改 Spec -> 重新 Plan」的循环通常要跑 3-5 轮。
这是把传统开发中 “开发到⼀半发现需求有问题”的代价前移到了成本最低的阶段，改⼀⾏
Spec 的成本远低于改⼀百⾏代码。
04
⼯具⽣态全景
SDD 已经形成了⼀个快速发展的⼯具⽣态，以下是主要⼯具的对⽐。
OpenSpec (Fissio
维度 Spec Kit (GitHub) Kiro (AWS) QoderWork (阿⾥)
n-AI)
Agent-agnostic 框 SDD-native Qoder Quest 执⾏
定位 轻量迭代⼯具
架 IDE 引擎
Agent ⽀
8+ Agent 25+ ⼯具 内置 Agent Qoder ⽣态
持
三⽂件体系 + consti 完整 IDE 集 Spec + Quest 并⾏
核⼼特点 轻量、快速迭代
tution 成 执⾏
AWS ⽣态项
适⽤场景 通⽤项⽬ ⼩型快速迭代 阿⾥⽣态项⽬
⽬
中（需理解 Ques
学习曲线 中 低 中
t）
Spec 即⼯
核⼼理念 Spec 即⽂档 Spec 即对话 Spec 即任务单
作流
4.1 各⼯具的差异化选择建议
追求通⽤性：选 Spec Kit。它不绑定任何特定 Agent，⽀持 Claude、GPT、Gemini 等主流
模型，三⽂件体系清晰易懂。43.7k Star 说明社区认可度⾼。
追求轻量和速度：选 OpenSpec。它的核⼼理念是 "Spec 不需要⼀步到位，可以在对话中迭
代完善"，对⼩型项⽬⾮常友好。
在 AWS ⽣态内：Kiro 是最省⼼的选择。SDD ⼯作流直接内嵌在 IDE 中，不需要⾃⼰搭建⼯
具链。
QoderWork 的 Quest 模式是最贴合 SDD 的执⾏引擎，「5 ⼈ 7 天」案例就是明证。Spec
写好后直接委派 Quest 执⾏，AI ⾃动写代码、提 PR、跑测试。
```

## PDF 第9页

[查看原页](RAW.pdf#page=9)

```text
05
实战数据：成功与失败都摆上台⾯
5.1 成功案例的硬数据
API 变更效率提升
⼀篇 arXiv 论⽂记录了⾦融领域的 SDD 实践：API 变更周期缩短75%。原因在于当 API 的
Spec 已经完整定义了接⼝契约、错误码、数据格式时，AI 可以直接⽣成符合 Spec 的代码，
省去了⼤量的沟通和返⼯。
代码错误率下降
研究数据显示，⼈⼯精炼 Spec 可以将 LLM 代码错误减少 50%。这说明好的 Spec 消除了
AI 的“猜测空间”，错误往往来⾃ AI 对模糊需求的错误推断。
Stripe 的规模化实践
Stripe 通过 Harness Engineering ⽅法（SDD 是其重要组成部分）交付了 1300 个 AI
PR。这个数字的意义在于「可控」，1300 个 PR 没有引发系统性问题，说明 Spec 约束下的
AI 编程是可以规模化的。
5.2 失败案例的警示数据
⽆ Spec 约束的安全灾难
Veracode 2025 年的报告揭示：45% 的 AI ⽣成代码包含安全漏洞。注意前提，这是⽆
Spec 约束时的数据。当 Spec 中明确定义了安全约束（如“必须使⽤参数化查询” “敏感数据
禁⽌出现在⽇志中”），漏洞率会⼤幅下降。
这 45% 和前⾯的「错误减少 50%」形成了鲜明对⽐。
场景 关键指标
⽆ Spec 约束的 AI 编程 45% 代码含安全漏洞
有 Spec 约束的 AI 编程 代码错误减少 50%
代码重复率的隐性成本
GitClear 对 2.11 亿⾏代码的研究发现，AI 编程时代的代码重复率 4 年增⻓ 4 倍。这不难理
解，AI 倾向于「复制粘贴式」的解决⽅案，因为它的训练数据中充满了类似的模式。SDD 通过
constitution.md 中的代码规范约束和 plan.md 中的模块化设计，可以在⼀定程度上缓解这个
问题，但⽆法完全消除。
```

## PDF 第10页

[查看原页](RAW.pdf#page=10)

```text
06
SDD vs Vibe Coding：⼀场必须正⾯交锋的辩论
6.1 什么是 Vibe Coding
2025 年 2 ⽉ 2 ⽇，Andrej Karpathy 在社交媒体上创造了 Vibe Coding 这个概念。
"Forget that the code even exists."（忘掉代码的存在。）
Vibe Coding 的核⼼主张是，不要去读代码、不要去理解代码，⽤⾃然语⾔描述你要什么，让
AI 全权处理。如果报错了，就把错误信息扔给 AI，让它⾃⼰修。
这听起来很诱⼈。在某些场景下，它确实有效，⽐如快速原型验证、个⼈⼯具脚本、⼀次性的
数据处理任务。
但问题在于，它不可持续。
6.2 "三个⽉墙"：Vibe Coding 的⽣死劫
社区观察到⼀个反复出现的模式，被称为「三个⽉墙」，如下。
阶段 时间 状态 典型表现
兴奋期 1-3 个⽉ ⾼产出 "AI 太神了！⼀天搞定⼀个功能！"
平台期 4-9 个⽉ 停滞 "为什么新功能总是破坏旧功能？"
衰退期 10-15 个⽉ 崩溃 "这坨代码没⼈能维护了，不如重写"
为什么会撞墙？因为 Vibe Coding 本质上是 零上下⽂的编程。
当项⽬只有⼏百⾏代码时，AI 可以“看到”全貌，它的推断和猜测⼤概率是对的。但当项⽬膨胀
到⼏万⾏、⼏⼗个模块、⼏百个接⼝时，AI 的上下⽂窗⼝装不下全部代码，它开始基于局部信
息做决策，⽽这些决策往往和其他模块冲突。
SDD 的 Spec 恰好解决了这个问题：Spec 是代码的压缩表示。10 万⾏代码的项⽬，它的
Spec 体系可能只有⼏千⾏⽂本。AI 可以轻松读完所有 Spec，理解全局约束后再动⼿改代
码。
6.3 核⼼差异对⽐
维度 Vibe Coding SDD
核⼼假设 AI 能理解你的意图 AI 需要明确的规格才能正确执⾏
```

## PDF 第11页

[查看原页](RAW.pdf#page=11)

```text
维度 Vibe Coding SDD
启动速度 极快 较慢（需要先写 Spec）
可维护性 差（⽆⽂档、⽆约束） 好（Spec 即⽂档）
可协作性 差（只有作者知道 "vibes"） 好（Spec 是共享语⾔）
安全性 差（45% 安全漏洞） 较好（Spec 约束安全边界）
适⽤规模 ⼩项⽬（< 1000 ⾏） 中⼤型项⽬
天花板 三个⽉墙 取决于 Spec 体系质量
6.4 我的判断：不是⾮此即彼
Vibe Coding 和 SDD 是⼀个光谱的两端。对于⼀个验证想法的周末项⽬，写 Spec 是过度⼯
程化；对于⼀个要⻓期维护的⽣产系统，Vibe Coding 是慢性⾃杀。
更务实的选择是混合策略：
1. 探索阶段⽤ Vibe Coding——快速试错，验证可⾏性；
2. ⼀旦决定要做，⽴刻补 Spec——把探索阶段的发现固化为规格；
3. 进⼊正式开发后严格 SDD——所有变更先改 Spec 再改代码。
实践就是这个策略的⼀个变体。DAY 0 写 Spec 之前，团队必然已经对 QoderWork 的产品形
态有了充分的探索和讨论（那属于更早的 Vibe 阶段），但⼀旦决定动⼿做，⽴刻切换到
Spec-Driven 模式。
07
SDD 与 Harness Engineering 的关系
AI 编程⽅法论的演进，存在⼀条清晰的三层递进链：
1 Prompt Engineering -> Context Engineering -> Harness Engineering
Prompt Engineering：关注「怎么写好⼀条指令」；
Context Engineering：关注「怎么给 AI 提供⾜够且精准的上下⽂」；
Harness Engineering：关注「怎么构建⼀个系统性的框架来约束和驱动 AI」。
SDD 位于 Context Engineering 和 Harness Engineering 的交叉地带。
从 Context Engineering 的⻆度看，Spec 就是⼀种⾼度结构化的上下⽂提供⽅式，它不把所
有代码丢给 AI（那太嘈杂），也不只说⼀句话（那太模糊），转⽽提供了⼀个恰到好处的信息
```

## PDF 第12页

[查看原页](RAW.pdf#page=12)

```text
密度。
从 Harness Engineering 的⻆度看，SDD 是 HE 的⼀个重要应⽤模式：constitution.md 是
约束层，spec.md 是需求层，plan.md 是执⾏层，tasks.md 是调度层。这四层组合在⼀起，
构成了⼀个完整的「AI 驾驭框架」（Harness）。
Stripe 交付 1300 个 AI PR 的实践就是 HE ⽅法论的典型案例，其中，SDD 是 “确保每个
PR 都有明确规格和验收标准”的关键组件。
08
五⼤陷阱与局限性：诚实⾯对 SDD 的阴暗⾯
在拥抱 SDD 之前，我们需要正视以下五⼤陷阱。
陷阱⼀：过度规格化（Over-Specification）
症状：Spec 写得⽐代码还⻓，每个实现细节都规定得死死的。
后果：本质上退化为“⽤⾃然语⾔写伪代码”，完全失去了 SDD 「⼈定义 WHAT、AI 实现
HOW」的核⼼优势。
缓解：⽤前⽂提到的粒度检验标准，“换⼀个技术栈实现，这个 Spec 是否仍然有效？”如果答
案是否，说明在 Spec ⾥混⼊了 HOW。
陷阱⼆：规格腐烂（Spec Rot）
症状：代码已经迭代了⼗⼏个版本，但 Spec 还停留在 V1。
后果：Spec 和代码脱节，新⼈看 Spec 理解的和看代码理解的是两个系统。当需要 AI 做增量
开发时，它基于过时的 Spec ⽣成的代码必然和现有代码冲突。
缓解：团队的做法值得借鉴。DAY 3-4 中，“发现需求或 BUG ⽴即写增量 Spec”。Spec 的
更新是和代码变更同步的⽇常操作。
陷阱三：规格官僚化（Spec Bureaucracy）
症状：改⼀个按钮的颜⾊也要⾛「写 Spec -> Review Spec -> 更新 Plan -> ⽣成 Tasks」
的全流程。
后果：团队开始绕过 Spec 流程直接改代码，SDD 名存实亡。
缓解：区分重⼤变更和微⼩变更，不是所有变更都需要完整的 Spec 流程。⼀个实⽤的判断标
准是，如果这个变更可能影响其他模块的⾏为，就需要 Spec；如果它是纯粹的局部修改（改⽂
```

## PDF 第13页

[查看原页](RAW.pdf#page=13)

```text
案、调样式），直接改就⾏。
陷阱四：虚假信⼼（False Confidence）
症状：因为有了详尽的 Spec，团队放松了对 AI ⽣成代码的审查。
后果：Spec 只定义了「做什么」，它不能保证 AI 的实现是正确的、安全的、⾼效的。45%
的安全漏洞数据提醒我们，即使有 Spec，AI 代码仍需要严格的 Review。
缓解：Spec 替代的是需求⽂档，不是 Code Review。 SDD 的 Validate 阶段是整个流程中
最后也最重要的安全⽹。
陷阱五：⼯具复杂性（Tool Overhead）
症状：为了「做好 SDD」，团队引⼊了 Spec Kit + Kiro + CI/CD 集成 + ⾃定义校验脚本 +
Spec Linter...
后果：⼯具链本身成为了负担，团队花在配置⼯具上的时间超过了写 Spec 的时间。
缓解：从最简单的⽅案开始。 ⼀个 spec.md ⽂件 + ⼀个你已经在⽤的 AI Agent，这就够
了；不要为了 SDD ⽽ SDD。
正⾯回应：「SDD 是 Markdown 版的瀑布模型」批评
这是 SDD ⾯临的最尖锐的批评，值得认真对待。
批评者的逻辑是，SDD 要求先写完 Spec 再写代码，这本质上就是瀑布模型。先完整定义需
求，再线性地实现。⽽瀑布模型早已被敏捷运动证伪，SDD 不过是换了个⻢甲。
我的判断：这个批评有⼀半道理，但结论是错的。
「有⼀半道理」是因为，如果我们把 SDD 实践成“花两周写⼀个巨⼤的 Spec，然后完全不改
地执⾏”，那确实是瀑布模型的翻版，必然失败。
「结论是错的」是因为，SDD 的 Spec 是活的，不是死的。 团队的 DAY 3-4 就是最好的反
驳，Spec 是随时可以增量更新的活⽂档。发现新需求？加⼀个增量 Spec；发现 BUG？补⼀
个约束条件。这更接近“持续需求细化”。
更本质的区别在于迭代粒度：
瀑布模型的迭代粒度是 整个项⽬（需求全部定义完 -> 全部开发完 -> 全部测试完）
SDD 的迭代粒度是 单个功能模块（⼀个模块的 Spec -> 该模块的 Plan -> 该模块的实现
-> 该模块的验证，然后进⼊下⼀个模块）
```

## PDF 第14页

[查看原页](RAW.pdf#page=14)

```text
SDD 实际上更接近「Spec 级别的迭代」，每个 Spec 就是⼀个最⼩可交付单元，写完就执
⾏、执⾏完就验证、验证完就下⼀个。这和敏捷的 Sprint 理念是兼容的，只是把 User Story
升级成了更结构化的 Spec。
另外⼀个反对「瀑布论」的事实是：SDD 中 Spec 的平均⽣命周期远短于瀑布模型中需求⽂档
的⽣命周期。 ⼀个 Spec 从编写到被 AI 实现可能只需要⼏⼩时甚⾄⼏分钟，⽽瀑布模型的需
求⽂档⽣命周期以⽉计。
当然，SDD 确实 有瀑布化的⻛险。但这是实践问题，不是⽅法论问题。⼀把菜⼑可以切菜也
可以伤⼈，问题不在⼑上。
09
SDD 的未来：三级光谱模型
SDD 并不是⼀个固定不变的⽅法论，它正在沿着⼀个三级光谱演进：
级 当前状
名称 特征 代表实践
别 态
当前主 编码前写 Spec，但 Spec 和代码 Spec Kit, ⼤多数
L1 Spec-First
流 可能漂移 团队
Spec-Anchor 先进实 Spec 和代码持续同步，测试强制执 Kiro 的内置⼯作
L2
ed 践 ⾏⼀致性 流
Spec-as-Sou 未来愿 ⼈只编辑 Spec，代码完全由 AI ⽣
L3 尚⽆成熟实践
rce 景 成和维护
L1 Spec-First：编码前写 Spec，但 Spec 可能漂移
这是⽬前⼤多数团队的实践状态。Spec 在项⽬初期发挥了巨⼤价值，但随着项⽬推进，Spec
和代码之间的漂移⼏乎不可避免，因为没有⾃动化机制来强制保持⼀致。
L2 Spec-Anchored：持续同步，测试强制执⾏
这是当前先进团队正在探索的状态。核⼼思路是，⽤⾃动化测试来锚定 Spec 和代码的⼀致
性。
具体做法：从 Spec 的 Acceptance Criteria ⾃动⽣成测试⽤例，任何代码变更都必须通过这
些测试。如果代码变了但测试（即 Spec 的⾃动化映射）没变，CI 会拒绝合并。这就像“类型
系统”防⽌类型错误⼀样，“Spec 测试”防⽌ Spec 漂移。
AWS Kiro 正在朝这个⽅向做，它的 SDD ⼯作流中内置了 Spec -> Test 的⾃动⽣成链路。
```

## PDF 第15页

[查看原页](RAW.pdf#page=15)

```text
L3 Spec-as-Source：⼈只编辑 Spec，代码完全⽣成
这是 SDD 的终极愿景，代码是被「编译」的——从 Spec 编译⽽来。
在这个范式下，⼈类⼯程师的⼯作完全聚焦在 Spec 层⾯。需要改功能？改 Spec；需要修
Bug？改 Spec；需要重构？改 Spec。AI 负责将 Spec 的变更⾃动反映到代码中。
这听起来像科幻，但想想看，团队的 DAY 3-4 已经有了 L3 的雏形：发现 BUG -> 写增量
Spec -> Quest ⾃动修复代码并提 PR。如果这个循环⾜够顺滑、覆盖⾜够全⾯，L3 就不再
是幻想。
Thoughtworks 技术雷达也在关注这个趋势。在 Vol.33（2025.11）中，SDD 被放
在 Assess 环，这意味着“值得研究，但尚未准备好全⾯采⽤”。到了 Vol.34，越来越多团队
开始采⽤ SDD，它正在向 Trial 环迁移。
10
结语：DAY 0 是最贵的⼀天，也是最值的⼀天
回到前⽂所说的「5 ⼈ 7 天」案例。
如果只看表⾯，我们会觉得奇迹发⽣在 DAY 1-6：AI ⻜速写代码、⾃动提 PR、并⾏推进多个
任务。
但真正的关键⼿在 DAY 0。
DAY 0 的⼀天「什么都没做」，实际上做了最重要的⼀件事：把⼈类的思考，即需求边界、成
功标准、技术约束、⾮⽬标清单结构化地固化到了 Spec 中。
这些 Spec 成为了后⾯六天的导航系统。5 个⼈之所以能驾驭 AI 并⾏推进⼤量任务⽽不失
控，正是因为每个 Quest 都有⼀个清晰的 Spec 锚定，AI 知道要做什么、不做什么、做到什
么程度算完。
这就是 SDD 的本质价值。它不让 AI 变聪明，它让 AI 变可控。
在 AI 编程能⼒以⽉为单位⻜速进化的今天，「让 AI 变聪明」不是我们需要操⼼的事，模型⼚
商会“卷”。⼈们真正需要操⼼的是：当 AI 越来越强⼤时，能不能驾驭它？
SDD 给出的答案是，与其试图理解和控制 AI 的每⼀⾏代码，不如把精⼒放在定义那个
「WHAT」——WHAT 永远是⼈类的领地。
从今天开始，试着在下⼀个功能需求前先写⼀个 spec.md。
```

## PDF 第16页

[查看原页](RAW.pdf#page=16)

```text
不需要完美，3-5 次迭代后它会变好；不需要⼯具链，⼀个 Markdown ⽂件就够了；不需要
全员推⼴，从⼀个⼈、⼀个模块开始就⾏。
DAY 0 是最「贵」的⼀天，也是最「值」的⼀天。
欢迎留⾔⼀起参与讨论~
阅读 5840
留⾔ 8
写留⾔
```

## PDF 第17页

[查看原页](RAW.pdf#page=17)

```text
⻄⽠吃了夏天 ⼴东 9⽉4⽇ 1
写完了，⼀堆bug，性能问题完全不提，就是说写完了，写完了，好⽤能不能⽤两回事
奥 浙江 9⽉13⽇
AI Coding 也就只能出 Demo，针对性能和体验，⽆法输⼊给 AI 充⾜的上下⽂。
🇩 🇸 上海 9⽉21⽇
还是需要⼈知道怎么去实现的，ai写的代码cr后要改好多，同样⼀句话，它写出来的代码每次
都不⼀样
海妖 上海 9⽉13⽇
spec 流程债务太重怎么解决呢
⼩李讲道理 ⼭东 9⽉8⽇
@元宝总结⼀下
元宝 ⼴东 9⽉8⽇
⽂章讲的是 Spec-Driven Development（SDD，规格驱动开发），核⼼是⽤ Spec 来驾
驭 AI 编程。帮你把要点拆⼀下：
1、什么是 SDD：把规格说明（Spec）作为唯⼀真实来源，⼈定义 WHAT，AI 实
现 HOW。代码只是 Spec 的副产品。
2、案例引⼦：5 ⼈ 7 天做出 QoderWork，完成了传统 20 ⼈数周的量。关键不在 AI 快，
⽽在 DAY 0 花⼀整天只写 Spec，后⾯六天所有任务都有锚点。
3、标准流程：Specify（需求）→ Plan（⽅案）→ Implement（实现）→ Validate（验
证）。GitHub Spec Kit 的三⽂件体系是 spec.md、plan.md、tasks.md，再加⼀个不可变
的 constitution.md。
4、好 Spec 的⽣死线：可测试，⽽不是可解释。要写"P95 < 200ms"，别写"系统要快"。
还要有 Non-Goals 和 Constraints，明确告诉 AI 什么不做、受什么限制。
5、SDD vs Vibe Coding：Vibe Coding 适合⼩项⽬快速验证，但会撞上"三个⽉墙"；
SDD 适合中⼤型⻓期维护的项⽬。实务上是光谱两端，可以混合⽤。
6、五⼤陷阱：过度规格化、规格腐烂、规格官僚化、虚假信⼼、⼯具复杂化。
7、未来演进：L1 Spec-...
内容由AI⽣成
⼤⽯头 北京 9⽉4⽇
上⾯的套件⽤来做技术评审都不⾏，技术评审⽂档有合适的⽅案么
Teemo 浙江 9⽉4⽇
虽然但是 这篇⽂章 ai 味有点太浓了 不考虑 human-writing ⼀点嘛
```

## PDF 第18页

[查看原页](RAW.pdf#page=18)

```text
[未提取到文字，请对照原页和核验记录。]
```

