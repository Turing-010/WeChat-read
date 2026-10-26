# 原文逐页转写

文本来自本次 PDF 文本层；不补写图片、截断内容或代码。图片和布局请打开每页 PDF 链接核对。AI 解释另见学习笔记。

## PDF 第 1 页

[原页](RAW.pdf#page=1)

````text
驾驭 AI  Coding ：⼀份⾯向团队的 Harness  Engineering 落地规范
腾讯程序员 2026 年 7 ⽉ 17 ⽇ 02 : 36⼴东原创 腾讯技术⼯程 1466 ⼈
作者： atreusliu
为什么每位成员都必须遵循这套规范？
AI Coding ⼯具正在重塑软件开发的⽅式。当团队中每个⼈都能⽤  AI 快速⽣成代码时，真正
拉开差距的不再是 " 谁写得快 " ，⽽是 " 谁写得好、谁写得稳、谁写得可维护 " 。
这套规范不是束缚，⽽是团队的共同语⾔和质量底线：
对个⼈：它帮你建⽴正确的  AI 协作习惯，避免踩坑返⼯，让  AI 真正成为你的⽣产⼒倍增
器
对团队：它确保每个⼈产出的代码风格⼀致、架构统⼀、可审查可维护，降低协作摩擦
对项⽬：它把质量标准固化到⼯具链中，让项⽬不会因为⼈员变动⽽失控
本⽂档的定位：
第⼀部分（⼀、⼆章）回答 " 为什么 " 和 " 是什么 " ：阐述  Harness Engineering 的核⼼理念
和  AI Coding ⼀体化架构设计
第⼆部分（三 ~ 九章）回答 " 怎么做 " ：提供分阶段实施路线图、具体配置步骤、⽇常开发
SOP 、反模式总结，以及基于我们构造的   harness-audit Skill 的⾃动化合规性⾃检
第三部分（⼗章）总结
关于阅读重点的⼀点说明：
MCP 、 Skills 、 Rules 、 SDD 、知识库这些概念，⽹上和司内已经有⼤量⼊门⽂章讲过 " 它们是
什么 " ，本⽂不再花篇幅重复这些⽼⽣常谈的定义。本⽂真正想讲清楚的，是另外两件事：
第⼀，它们在  Harness  体系中的功能定位。同样是  MCP 和  Skills ，单独看每⼀个⼯具
都不难理解，但放进  Harness 的  6 ⼤⽀柱⾥，各⾃承担什么⾓⾊、解决什么层⾯的问题、
在  AI ⼯作流的哪个环节发挥作⽤，这才是决定团队能不能⽤好它们的关键。
交付代码的成本已经接近免费了，但交付好代码的成本依然很⾼。 Harness Engineering
做的事情，就是把 " 好代码 " 的标准写进系统⾥，让  AI 在约束下⾃⼰⼲活。
````

## PDF 第 2 页

[原页](RAW.pdf#page=2)

````text
第⼆，它们在实际开发场景中如何相互配合。MCP 提供数据通道、 Skills 封装领域经验、
知识库注⼊业务上下⽂、 Rules 划定⾏为边界—— 这⼏样⼯具不是孤⽴存在的，真正的威
⼒在于组合使⽤。本⽂会结合具体场景（需求开发、 Bug 修复、 Code Review 等）讲清楚
它们怎么协同⼯作。
其实我们⽇常开发中，已经或多或少在⽤  Harness 的思路了，只是缺⼀个系统化的框架把这
些⼯具的使⽤⽅式和⽤法统⼀起来 ;
如果想捋清这些⼯具背后的设计逻辑，知道在⾃⼰的项⽬⾥该⽤哪⼀个、怎么搭配⽤、什么时
候不该⽤，那这份规范就是为你准备的。
第⼀部分：理念与架构
⼀、核⼼理念： Harness Engineering （驾驭⼯程）
1.1 什么是  Harness Engineering ？
2026 年  2 ⽉， OpenAI 发了⼀篇⽂章《 Harness Engineering: Leveraging Codex in an Agent-
First World 》。⼀个  3 ⼈（后来扩到  7 ⼈）的⼯程师团队，在完全禁⽌⼿写代码的条件下，⽤
AI Agent 在  5 个⽉内写了超过  100 万⾏代码，合并了  1,500 个  Pull Request，效率⼤概提
升了  10 倍。
Harness 这个词来⾃马术，本意是 " 马具 "—— 缰绳、马鞍、马镫。⼀匹没驯服的马⼒量很⼤，
但你没法让它耕地、运货、上战场。 AI 也⼀样：
LLM 本⾝没有状态、没有⼯具、没有记忆。 Harness 层就是给模型装上 " ⼿脚和记忆 " 的⼯程
基础设施。你写的所有代码、配的所有规则，都是  Harness 的⼀部分。
┌─────────────────────────────────────────────────────┐
│                   应⽤层  (Application)               │
│         IDE 插件  / CLI / Web UI / ⽤户交互            │
├─────────────────────────────────────────────────────┤
│               Harness 层  (Agent Harness)             │
│   ⼯具调⽤  · 上下⽂管理  · 权限校验  · 状态持久化        │
│   执⾏编排  · 评估验证  · 约束恢复  · 记忆系统           │
├─────────────────────────────────────────────────────┤
│                   模型层  (Model)                     │
│        LLM (Claude / GPT / DeepSeek 等 )              │
│         理解指令  · ⽣成⽂本  · 做出决策                  │
└─────────────────────────────────────────────────────┘
1.2 为什么需要  Harness ？ —— Vibe Coding 的三个致命问题
没有  Harness 约束的 " 氛围编码 " （ Vibe Coding ），⾛的是⼀条  起步极快  →  中期混乱  →  后期
崩盘  的路：
Agent = Model + Harness模型提供智能， Harness 让智能变成⽣产⼒。
````

## PDF 第 3 页

[原页](RAW.pdf#page=3)

````text
问题 现象 后果
架构混乱Agent 喜欢⾛捷径，功能 A ⽤库 X ，功能 B ⽤库 Y
（哪怕 X 也能做），完全没有分层概念
⼀旦要换底层逻辑（⽐如换数据
库），整个项⽬得⼤改
上下⽂雪崩项⽬超过 50 个⽂件后， Agent 开始 " 忘事 "—— 第 1
天⽤  user_id，第 3 天突然变成  uid
项⽬越⼤， Agent 越蠢，修⼀个
Bug 冒出两个新的
可维护性丧
失
整个开发过程是⿊盒，只有  Agent 知道代码怎么来
的，⼈没参与思考
⼈想接⼿时，从头读⼏千⾏ " 垃圾
代码 " ，还不如重写
Harness Engineering 就是来解决这些问题的：
安全边界：权限控制、审计⽇志、拒绝追踪
可观测性： Token 计数、成本追踪、决策⽇志
可靠性：重试机制、降级策略、确定性兜底
扩展性：⼯具⽣态、技能系统、多  Agent 协调
1.3 Harness 的  6 ⼤⽀柱及其在  Coding 中的映射
Harness Engineering 把  Agent 的运⾏环境拆成  6 个⽀柱，每个⽀柱在我们的开发规范中都有
对应的⼯具和实践。下⾯逐个说明。
上图来⾃于公众号⽂章 : https://mp.weixin.qq.com/s/gs5ndvlMqM-Y4jg1_D2aFw 该⽂对
Harness 做了详细的讲解，本⽂不过多赘述 ;
这⾥我们只关注实践⼯具在其中的构成。
⽀柱⼀：上下⽂管理（ Context Architecture ）
实践 ⼯具 说明
渐进式披
露 AGENTS.md 写⼀个  ~100 ⾏的⽬录⽂件，指向  ARCHITECTURE.m
d、Rules 等细分⽂档，别⼀次灌⼏千⾏
问题： AI 的上下⽂窗⼝有限且贵，怎么让  AI 在对的时间看到对的信息？
````

## PDF 第 4 页

[原页](RAW.pdf#page=4)

````text
实践 ⼯具 说明
结构化规
范
Spec .md  ⽂件（ requiremen
t.md / task.md ）
把需求和设计决策写进  Git 仓库，变成  AI 随时能调取
的 " 长期记忆 "
变更隔离 changes/
  ⽬录
⽤  Proposals 机制把 " 增量变更 " 和 " 存量代码 " 隔开，减
少对现有逻辑的误伤
知识分层 Skills 按需加载 技能信息分三层（描述  →  指令  →  详细步骤），按需逐
步加载，省  Context
知识库挂
载
知识库（ iWiki 代码库  ⾃定义
⽂件）
把团队  Wiki 、代码仓库、业务⽂档挂载为知识库， AI 对
话时⾃动或⼿动引⽤，获取业务上下⽂
代码知识
化 AI Wiki 基于代码库⾃动⽣成结构化知识⽂档， AI 不⽤逐⽂件阅
读就能理解项⽬全貌
⼏个原则：
别给  AI ⼀个⼏千⾏的规范⽂件
建分层索引，让  AI 按需深⼊
把团队  Wiki 和业务⽂档挂载为知识库，让  AI 有业务上下⽂
把仓库知识当作 " 系统记录 " （ System of Record ），别依赖聊天历史
OpenAI ⾃⼰踩过坑：早期试过 " ⼀个巨⼤的  AGENTS.md" ，失败了。正确做法是拆成多个专
注的⽂档，⽤⽬录索引串起来。
⽀柱⼆：⼯具系统（ Tool System ）
⼯具系统由三部分组成： MCP （连接外部世界）、 Skills （封装专家经验）和知识库（注⼊业
务上下⽂），三者配合构成  AI Agent 的完整能⼒体系。
MCP （ Model Context Protocol ） —— 连接外部数据源
问题： AI 怎么触达代码仓库之外的真实世界，怎么具备特定领域的专业能⼒？
````

## PDF 第 5 页

[原页](RAW.pdf#page=5)

````text
MCP 类型 作⽤ 典型场景
DB MCP ⾃动读取实时数据库  Schem
a
避免  AI 写出不存在的字段，⽣成准确的  SQ
L
Knowledge Base MC
P 挂载团队内部⽂档让  AI 有业务上下⽂，理解领域术语
API MCP 实时查询其他服务接⼝定义微服务联调时，确保接⼝参数⼀致
运维  MCP 接⼊  CI/CD 、监控系统 AI 可以直接触发构建、查看⽇志、分析告警
Skills （ Agent Skills ） —— 封装领域专家经验
Skills 是业务逻辑、领域知识和执⾏  SOP 的封装，让  AI 从 " 什么都会⼀点 " 变成 " 某个领域的专
家 " 。
Skill 类型 作⽤ 典型场景
⼯具接⼊类封装内部⼯具链的接⼊规范rainbow-config
：按标准流程接⼊七彩⽯配置中⼼
代码⽣成类固化特定模式的代码⽣成逻辑按团队架构规范⽣成  CRUD 模块、中间件接⼊代码
元技能类 让  AI 能⾃我扩展 skill-creator
：教  AI 根据现有代码创建新  Skill
搜索发现类 从社区发现可⽤能⼒ find-skills
：从  80,000+ 技能库搜索并安装  Skill
知识库（ Knowledge Base ） —— 注⼊业务上下⽂
知识库是让  AI 从 " 通⽤模型 " 变成 " 懂业务的助⼿ " 的关键。挂载团队内部⽂档、代码仓库和业
务资料后， AI 对话时能⾃动获取业务上下⽂，少猜多做。
知识库类
型 数据来源 典型场景
iWiki ⽂档库团队  Wiki 空间 挂载业务规范、技术⽅案、 API ⽂档， AI 回答时⾃动引⽤
代码库知识⼯蜂  Git 仓库挂载公共组件（如  tRPC 、七彩⽯  SDK ）， AI ⽣成代码时参考正确
⽤法
AI Wiki 代码库⾃动⽣成基于代码库⾃动⽣成结构化知识⽂档，快速理解项⽬架构和模块
逻辑
⾃定义⽂件Markdown PDF tx
t 上传需求⽂档、设计稿、会议纪要等，让  AI 有项⽬背景
知识库使⽤⽅式：
显式引⽤：在对话中输⼊   @KnowledgeBase  选择特定知识库引⽤
⾃动引⽤：开启⾃动参考开关， AI 对话时⾃动检索相关知识
团队共享：通过  Knot 平台将知识库共享给团队 / 组织，统⼀业务认知
````

## PDF 第 6 页

[原页](RAW.pdf#page=6)

````text
⽀柱三：执⾏编排与多  Agent 协作（ Execution Orchestration ）
执⾏编排不只是选模式（ Plan vs Agent ），⽽是⼀套多  Agent 协作的标准化⼯作流。团队应该
遵循 “3+1 Phase” 流程，每个阶段由不同⾓⾊的  Agent 负责：
核⼼⽐喻： MCP 是开门的钥匙， Skills 是开门后做的事情，知识库是进门前读的说明
书。三者缺⼀不可 —— 没有  MCP ， AI 是闭门造车；没有  Skills ， AI 有钥匙但不知道进门
⼲什么；没有知识库， AI 进了门也不懂业务。
问题：怎么让  AI 按部就班⽽不是乱写⼀⽓？怎么让多个  Agent ⾓⾊配合完成复杂任务？
````

## PDF 第 7 页

[原页](RAW.pdf#page=7)

````text
"3+1 Phase" 标准化⼯作流：
阶段 输⼊ AI 操作 产出 协作模式
Phase 1: 计
划 需求描述Plan 模式⽣成  requirements.md ，
⼈⼯审核后创建  task.md
结构化⽅案⽂
件
⼈类  Review ⽅
案
Phase 2: 编
码 任务清单加载  Rules 和  Skills ，调⽤  MCP ⼯
具实现代码
源代码  + 单元
测试
Generator Agen
t 执⾏
Phase 3: 交
付
待合⼊代
码
AI ⾃动做规范合规检查和代码逻辑
审查
通过核查的  P
R
Evaluator Agent
验收
Phase 4: 沉
淀
已合并需
求
⾃动把  Spec 归档，更新项⽬知识
库
持久化知识资
产 归档⾃动化
多  Agent ⾓⾊定义：
Agent ⾓⾊ 职责 加载的  Harness
Planner 理解需求、拆解任务、⽣成⽅案Plan 模式  + 项⽬  Spec
Generator 按⽅案写代码、写测试 Rules + Skills + MCP
Evaluator 代码审查、规范检查、测试验证Rules + 验收标准
Archiver 归档变更、更新知识库归档脚本  + Git
实际操作中：
⽤  Plan 模式做架构分析和⼤任务拆解（ Planner ⾓⾊）
⽤  Agent 模式做具体功能的⾃动化实现（ Generator ⾓⾊）
⽤  AI Code Review  做交付前的质量把关（ Evaluator ⾓⾊）
遵循  SDD ⼯作流：requirements.md → ⼈⼯审核  → task.md → 执⾏  → 归档
每个任务必须有明确的 " 完成标准 " （ Acceptance Criteria ）
⽀柱四：状态与记忆（ State & Memory ）
````

## PDF 第 8 页

[原页](RAW.pdf#page=8)

````text
记忆类型 实现⽅式 ⽣命周期
短期记忆 当前会话上下⽂ 单次对话
中期记忆 Memories 功能 跨会话持久化
长期记忆 Git 仓库中的  Spec ⽂件 项⽬全⽣命周期
变更记忆 Spec Deltas （changes/  ⽬录） 单次变更周期
实际操作中：
⽤  Git 记录规范变更（ Spec Deltas ），形成项⽬的长期记忆
⽤  Memories 功能让  AI 记住编程习惯和项⽬信息
每次变更归档后，⾃动更新   .codebuddy/plan/  下的归档记录
⽀柱五：评估与观测（ Evaluation & Observability ）
评估分四层：
层次 检查内容 ⼯具 / ⽅式
L1 语法 编译通过、 Lint 检查 go build
 / golangci-lint
L2 逻辑 单元测试通过 go test
 / ⾃动⽣成测试⽤例
L3 规范 符合  Rules 约束 AI ⾃动合规检查
L4 架构 不破坏现有设计 ⼈⼯  + AI 联合审查
实际操作中：
引⼊  AI 代码审查（ CR ），合⼊前⾃动检查规范合规性
代码写完后，⾃动编译和基础⾃测（闭环验证）
影响较⼤的改动，可以⾃动⽣成变更⽇志
⽀柱六：约束与恢复（ Guardrails & Recovery ）
问题：怎么让  AI 在长周期开发中保持⼀致性？
问题：怎么验证  AI ⽣成的代码是不是靠谱的？
问题：怎么防⽌  AI 越界操作，出错了怎么快速恢复？
````

## PDF 第 9 页

[原页](RAW.pdf#page=9)

````text
约束分三级：
┌──────────────────────────────────────────┐
│   硬性红线（ Rules - 不可违反）               │
│  " 所有  API 必须包含  Swagger 注解 "         │
│  " 禁⽌在  Controller 层编写业务逻辑 "       │
│  " 所有数据库查询必须使⽤  Repository 模式 "  │
├──────────────────────────────────────────┤
│   软性约束（ Skills - 推荐遵循）              │
│  " 优先使⽤项⽬已有的⼯具类 "                │
│  " ⽇志格式遵循团队统⼀标准 "                │
├──────────────────────────────────────────┤
│   安全策略（ Safety - 兜底保护）              │
│  " 涉及数据库变更，优先⽣成  SQL 脚本 "       │
│  " ⾼⻛险操作前⾃动检测影响范围 "             │
│  " 重要操作⾃动备份 "                        │
└──────────────────────────────────────────┘
恢复机制：
所有变更通过  Git 管理，随时可以回滚
Spec Deltas 机制确保变更可追溯
编译失败时⾃动回退到上⼀个稳定状态
1.4 Harness 6 ⼤⽀柱与⼯具链映射总表
⽀柱 核⼼问题 对应⼯具 团队实践
上下⽂管理AI 看到什么信
息？
Spec ⽂档  AGENTS.md
知识库
结构化规范  + 渐进式披露  + 业务
知识挂载
⼯具系统AI 能触达什么？MCP Skills 知识库 DB/API 实时接⼊  + 知识库业务
沉淀  + Skills 专家经验
执⾏编排与多  Ag
ent 协作
AI 按什么顺序
做？谁来做？
Plan 模式  SDD ⼯作流
多  Agent ⾓⾊体系
"3+1 Phase" ： Planner →  Gener
ator →  Evaluator →  Archiver
状态与记忆 AI 记住什么？Git + Memories + Spec
Deltas 长期记忆持久化
评估与观测AI 做得对不对？⾃动测试  + AI CR 编译→测试→审查闭环
约束与恢复AI 不能做什么？Rules + Safety 策略 硬性红线  + ⾃动回滚
下⽂会详细讲解具体⼯具规范。
⼆、 AI Coding ⼀体化架构
基于 Harness Engineering 的  6 个⽀柱，这⼀章把它落地成⼀套完整的架构。这套架构定义了
从 " ⼈的想法 " 到 " 能跑的代码 " 的全链路，算是团队  AI 辅助开发的技术蓝图。
````

## PDF 第 10 页

[原页](RAW.pdf#page=10)

````text
说⽩了， AI 不是⼀个孤⽴的代码⽣成器，它是嵌在整个⼯程体系⾥的⼀个节点。架构的每⼀
层都对应  Harness 的某个⽀柱，确保  AI 在约束下⼲活。
2.1 架构全景图
在开发实践过程中 , 我们整理了⼀个 AI 编码的整体架构图，从上到下分五层：输⼊层  →  ⼯作台
（ CodeBuddy ）→  底层⽀撑（ MCP ）→  输出层  →  度量层，数据⾃上⽽下流动，形成闭环：
各层职责
以下表格说明架构中每⼀层的组件和职责：
````

## PDF 第 11 页

[原页](RAW.pdf#page=11)

````text
层级 组件 职责
输⼊层Spec ⽂档（ requirement.md ） / ⾃然语⾔  / 代码
上下⽂
把⼈的想法转成  AI 能理解的结构化
输⼊
配置中⼼ Rules Skills Docs Commands Memories 加载  Harness 约束，让  AI ⾏为可控
模式引擎 Plan 模式  / Agent 模式 根据任务复杂度选执⾏策略
Agent 核
⼼ 代码⽣成  审查  测试  / 重构 执⾏具体的开发任务
MCP 层 DB API Wiki CI/CD Monitor 连接外部系统，突破代码仓库边界
输出层 代码  测试  ⽂档  / ⽇志 交付可运⾏的⼯程产物
度量层 AI 代码占⽐  交付量  Bug 率 量化  AI 辅助开发的效果
数据怎么流转
⼈的想法  → [ 输⼊层 ] → 结构化输⼊
                         ↓
              [ 配置中⼼ ] 加载约束  → [ 模式引擎 ] 选择策略
                         ↓
                    [Agent 核⼼ ] 执⾏任务
                      ↓         ↓
              [MCP 层 ] 获取外部数据    [ 输出层 ] 交付产物
                                        ↓
                                   [ 度量层 ] 量化效果  → 反馈优化规范
注意，这不是单向流⽔线，⽽是⼀个闭环 —— 度量层的数据会反馈到配置中⼼，推动  Rules 和
Skills 的迭代。⽐如度量发现  Bug 率上升了，团队就该检查是不是需要补新的  Rules 约束或者
优化现有  Skills 。
第⼆部分：落地实操
三、实施路线图（ 3 阶段渐进式）
落地不是⼀蹴⽽就的事。我们把整个过程拆成三个阶段，每个阶段有明确的⽬标和验收标准：
阶段 ⽬标 周期 核⼼产出
第⼀阶段：基
础建设
让团队每个⼈都能⽤上  AI Codi
ng ⼯具，建⽴基本约束体系1-2 周 CodeBuddy 安装  + team-harness
仓库  + 基础  Rules + 知识库配置
第⼆阶段：⼯
具接⼊
接⼊  MCP 、沉淀  Skills 、实践  P
lan 模式  SDD 2-4 周 MCP 接⼊  + Skills 沉淀  + Spec 驱
动开发流程跑通
以上两章阐述了  Harness Engineering 的核⼼理念和  AI Coding ⼀体化架构的设计蓝图。
理解了 " 为什么 " 和 " 是什么 " 之后，接下来最关键的问题就是 " 怎么做 " 。本部分聚焦于如何
⼀步步把规范落地到团队⽇常开发中。每⼀节都包含具体的操作步骤、配置⽰例和验收标
准，确保团队成员照着做就能跑通。
````

## PDF 第 12 页

[原页](RAW.pdf#page=12)

````text
阶段 ⽬标 周期 核⼼产出
第三阶段：持
续优化
建⽴⾃演进的知识体系，实现知
识飞轮效应 持续 度量看板  + 规范迭代机制  + 知识飞
轮
四、第⼀阶段：基础建设（快速启动）
⽬标：让团队每个⼈都能⽤上  AI Coding ⼯具，并建⽴基本的约束体系。
4.1 CodeBuddy 安装与配置
4.1.1 IDE 插件安装
VSCode 安装：
1. 前往  CodeBuddy 官⽹下载插件   .vsix  ⽂件
2. 进⼊  VSCode →  Extensions →   ...  →  Install from VSIX →  选择下载的插件
3. 按   Command( ⌘ ) + L  或   Ctrl + L，底部出现  CodeBuddy 图标代表安装成功
4. 登录账号，确认  Plan 模式和  Agent 模式均可正常使⽤
JetBrains 系列  IDE 安装（ GoLand PyCharm IDEA 等）：
1. 前往  CodeBuddy 官⽹下载  JetBrains 插件   .zip  ⽂件（注意：下载后不要解压）
2. 进⼊  IDE →  Plugins →   ⚙   →  Install Plugin from Disk →  选择下载的   .zip  ⽂件
3. 底部出现  CodeBuddy 图标代表安装成功
4. 登录账号，确认对话功能正常
4.1.2 CLI ⼯具安装（可选）
司内已集成三种顶级  CLI  编程⼯具，按需选择：
CLI ⼯具 安装命令 启动命令 配置⽬录
Claude Code Int
ernal
`npm install -g --registry=https://xxx.c
om/
claude-inter
nal
~/.claude-inte
rnal/
Gemini CLI Inter
nal
npm install -g --registry=ht
tps://xxx.com/
gemini-inter
nal ~/.gemini/
Codex CLI Inter
nal
npm install -g --registry=ht
tps://xxx.com/
codex-intern
al
~/.codex-inter
nal/
⚠  Mac Safari 浏览器默认会⾃动解压  zip ⽂件，建议在  Safari 设置中取消勾选 " 下载后
打开安全⽂件 " 。
前置依赖： Node.js 20 或以上版本。三者都属于⾏业最强  AI Coding ⼯具，按个⼈习惯
选择即可。
````

## PDF 第 13 页

[原页](RAW.pdf#page=13)

````text
4.1.3 CodeBuddy 核⼼配置
安装完成后，需要进⾏以下核⼼配置，让  CodeBuddy 发挥最⼤效能：
1. 模型选择
在对话框左下⾓切换模型。推荐策略：
场景 推荐模型 说明
复杂编码任务Claude-4.6-Sonnet/Opus( 更强 ) / G
PT-5.4
外部模型，编程能⼒⼀流，但会外传代码
上下⽂
简单问题  / 敏感业
务 DeepSeek-V3.2 GLM-4.7 HY-2.0 内部部署，代码不出域，安全有保障
不确定选哪个Auto （智能⾃动选择）基于问题复杂度⾃动匹配最优模型
2. Memories 配置（记忆功能）
Memories 让  CodeBuddy 记住你的编码习惯和项⽬信息，跨会话持久化。
开启⽅式：
1. 在  CodeBuddy 设置页⾯，选择  Memories 选项
2. 确认  Memories 开关已开启
主动记忆：  在  Agent 模式对话中，直接告诉  CodeBuddy 需要记住的信息：
请记住：
1.  我习惯使⽤  Go 语⾔开发，项⽬使⽤  gin 框架
2.  代码注释使⽤中⽂
3.  变量命名使⽤  camelCase ⻛格
4.  所有  API 返回统⼀使⽤  pkg/response 包的标准格式
管理记忆：  在  CodeBuddy 设置页⾯  →  Memories ，可以查看、编辑、删除已保存的记忆。
3. Commands 配置（指令式交互）
Commands 是将⾼频开发任务封装为可复⽤命令的能⼒，本质是 " 可被快速触发的标准化
Prompt" 。
创建  Command：
1. 在对话框输⼊   /，选择 " 新增  Command"
2. 输⼊  Command 名称（建议使⽤英⽂命名）
⚠  安全提醒： Claude 、 GPT 、 Gemini 等外部模型会发送代码上下⽂到外部，敏感业务
请使⽤内部部署模型。
````

## PDF 第 14 页

[原页](RAW.pdf#page=14)

````text
3. 填⼊  Command 内容（即预设的  Prompt ）
推荐的团队  Commands：
Command 名称 ⽤途 触发⽅式
/init 为项⽬初始化  AI 使⽤⼿册（⾃动⽣成  Rules ） 新项⽬⾸次使⽤时
/pre-mr-checklist 代码提交前安全  & 漏洞检测 提交  PR 前
/spec-create 创建需求  Spec ⽂档 新需求开发时
/spec-plan 基于  Spec ⽣成任务清单 需求审核通过后
/init Command ⽰例内容：
请分析此代码库，并在当前代码库  `.codebuddy/rules` ⽬录下创建  global.md ⽂件，
该⽂件将提供给未来的  CodeBuddy 实例在此代码库中运⾏使⽤。
需要补充的内容：
1.  将经常使⽤的命令包括在内，例如如何构建、如何进⾏代码检查以及如何运⾏测试
2. High-level 的代码架构和结构，重点在于" 宏观 "的架构设计
使⽤说明：
- 如果该⽂件已经存在，请对其进⾏改进
- 不要包含通⽤的开发实践
- 确保该⽂件前有以下头部元数据：
---
# CodeBuddy Rules
type: always
---
4.2 创建  team-harness 仓库
这是团队规范的唯⼀真实来源，所有  Rules 、 Skills 模板、 AGENTS.md 模板都集中管理在这
⾥。
Step 1 ：初始化仓库结构
# 创建仓库
mkdir team-harness && cd team-harness
git init
# 创建标准⽬录结构
mkdir -p rules/{global,golang,python,frontend}
mkdir -p skills/{common,business}
mkdir -p templates
⚠  验收标准：每位团队成员能在  IDE 中正常唤起  CodeBuddy 对话框， Token 使⽤量正
常，能展⽰⼀个简单项⽬实现的  prompt 。
````

## PDF 第 15 页

[原页](RAW.pdf#page=15)

````text
mkdir -p docs
# 创建核⼼⽂件
touch rules/global/base.md
touch rules/golang/go-backend.md
touch templates/AGENTS.md
touch templates/project.md
touch README.md
最终⽬录结构：
team-harness/
├── rules/                      # 团队  Rules 集合
│   ├── global/                 # 全局通⽤规则
│   │   └── base.md             # 基础规范（所有项⽬必须加载）
│   ├── golang/                 # Go 语⾔专⽤规则
│   │   └── go-backend.md
│   ├── python/                 # Python 专⽤规则
│   └── frontend/               # 前端专⽤规则
├── skills/                     # 团队  Skills 集合
│   ├── common/                 # 通⽤  Skills
│   │   ├── skill-creator/      # Skill 创建器
│   │   └── find-skills/        # Skill 搜索器
│   └── business/               # 业务  Skills
│       └── rainbow-config/     # 七彩⽯配置接⼊
├── templates/                  # 模板⽂件
│   ├── AGENTS.md               # AI 说明书模板
│   └── project.md              # 项⽬描述模板
├── docs/                       # 使⽤⽂档
│   └── onboarding.md           # 新⼈上⼿指南
└── README.md
Step 2 ：编写同步脚本
在业务项⽬中通过脚本⾃动拉取最新规范：
#!/bin/bash
# sync-harness.sh - 同步团队规范到当前项⽬
HARNESS_REPO="git@xxx.com"
HARNESS_DIR=".harness-upstream"
# 拉取最新规范
if [ -d "$HARNESS_DIR" ]; then
    cd $HARNESS_DIR && git pull && cd ..
else
    git clone $HARNESS_REPO $HARNESS_DIR
fi
````

## PDF 第 16 页

[原页](RAW.pdf#page=16)

````text
# 同步  Rules 到项⽬
mkdir -p .codebuddy/rules
cp $HARNESS_DIR/rules/global/*.md .codebuddy/rules/
cp $HARNESS_DIR/rules/golang/*.md .codebuddy/rules/  # 按语⾔选择
# 同步  Skills 到项⽬
mkdir -p .codebuddy/skills
cp -r $HARNESS_DIR/skills/common/* .codebuddy/skills/
echo " ✅  团队规范同步完成 "
Step 3 ：配置  CI ⾃动同步（可选）
在项⽬的  CI 流⽔线中加⼊⾃动同步步骤，确保每次构建前规范都是最新的。
4.3 Rules 配置（全局与项⽬级约束）
Rules 是  AI 在每次交互中必须加载的全局约束，相当于  AI 必须遵守的 " 法律 " 。 CodeBuddy
⽀持三个层级的  Rules ：
4.3.1 Rules 分层体系
层级 作⽤域 配置⽅式 加载⽅式
User Rules 所有项⽬（个⼈）CodeBuddy 设置页⾯  →  Rul
es 每次对话⾃动带⼊
Team Rules 团队所有成员Knot 平台管理下发按  type 配置（ always / manua
l）
Project Rule
s 单个项⽬ .codebuddy/rules/
  ⽬录下的  .md  ⽂件 总是⽣效  或  ⼿动  @ 引⽤
4.3.2 User Rules 配置
1. 点击  CodeBuddy 对话⾯板的设置齿轮图标
2. 进⼊  Rules 设置页⾯
3. 添加个⼈偏好规则，也可使⽤平台预置的  Rules 快速⽣成后微调
# 个⼈偏好示例
1.  回复使⽤中⽂
2.  代码注释使⽤中⽂
````

## PDF 第 17 页

[原页](RAW.pdf#page=17)

````text
3.  优先使⽤  Go 标准库
4.  变量命名使⽤  camelCase
4.3.3 Team Rules 配置（通过  Knot 平台）
Team Rules 由团队管理员在  Knot 平台统⼀管理和下发，确保团队所有成员遵循⼀致的标
准。
配置步骤：
1. 前往  Knot Rules 管理页⾯
2. 点击「新建  Team Rule 」
3. 填⼊  Rule 内容，头部必须包含  Rule Type Header ：
---
type: always
---
# 团队  Go 后端开发规范
## 架构约束
1.  严格遵循分层架构： Controller → Service → Repository → Model
2.  禁⽌在  Controller 层编写业务逻辑
...
1. 提交审批，审批通过后  Team Rule ⾃动⽣效
2. 团队成员的  CodeBuddy 会⾃动加载已⽣效的  Team Rules
4.3.4 Project Rules 配置
创建⽅式：
1. 在  CodeBuddy 对话⾯板中点击「新增  Project Rule 」
2. 输⼊  Rule 内容（注意不要修改头部元数据）
3. 设置⽣效范围：
总是⽣效：每次对话⾃动带⼊
⼿动指定：需要在对话时   @Rules  选择
Rules ⽂件结构规范：
---
description: "Go 后端开发通⽤规范 "
globs: "**/*.go"
alwaysApply: true
---
💡  Team Rule 的   type  ⽀持   always（总是⽣效）和   manual（⼿动引⽤）两种模式。
````

## PDF 第 18 页

[原页](RAW.pdf#page=18)

````text
# Go 后端开发规范
## ⼀、架构约束（硬性红线）
1.  严格遵循分层架构： Controller → Service → Repository → Model
2.  禁⽌在  Controller 层编写业务逻辑， Controller 只负责参数校验和响应封装
3.  所有数据库操作必须通过  Repository 层，禁⽌在  Service 中直接写  SQL
4.  所有对外  API 必须包含  Swagger 注解
## ⼆、代码⻛格
1. 函数 / ⽅法必须有简要注释说明⽤途
2.  错误处理不允许使⽤  _ 忽略，必须显式处理或向上传递
3.  变量命名使⽤  camelCase ，常量使⽤  ALL_CAPS
4. 单个函数不超过  80  ⾏，超过则拆分
## 三、安全策略
1.  涉及数据库变更时，优先⽣成  SQL 变更脚本，⽽⾮直接执⾏
2.  删除、移动⽂件等操作⽆需额外确认，但涉及数据库结构修改必须确认
3.  所有敏感配置（密钥、连接串）必须通过配置中⼼读取，禁⽌硬编码
## 四、开发⾏为
1.  添加新功能前，必须先分析现有代码库，优先复⽤已有模块
2.  代码变更范围最⼩化，⼀次  PR 只解决⼀个问题
3.  每次变更必须附带清晰的  commit 信息
4.  新增功能必须同步编写单元测试
4.3.5 Rules 的保存与复⽤流程
业务项⽬ team-harness 仓库开发者业务项⽬ team-harness 仓库开发者 AI 下次交互⾃动加载
新规则 1. 提交  Rules 变更  PR2. 团队  Review & 合并 3. ⾃动同步到各业务项⽬ 4.
.codebuddy/rules/ 更新
````

## PDF 第 19 页

[原页](RAW.pdf#page=19)

````text
验证  Rules ⽣效：
# 在  CodeBuddy 中测试
你好，请告诉我当前加载了哪些  Rules ？
AI 应能识别并列出已加载的规则⽂件。
4.4 编写  AGENTS.md
AGENTS.md  是  AI 的 " 说明书 " ，控制在  ~100 ⾏以内，当⽬录索引⽤，指向更细分的⽂档。
创建⽂件   AGENTS.md（放在项⽬根⽬录）：
# AI 开发助⼿说明书
## 项⽬概述
本项⽬是  [ 项⽬名称 ] ，基于  Go 微服务架构，使⽤  [ 框架名 ] 框架。
## 架构说明
- 分层架构： Controller → Service → Repository → Model
- 详细架构⽂档：参⻅  `docs/ARCHITECTURE.md`
## ⽬录结构
- `internal/` - 业务逻辑（按服务拆分⼦⽬录）
- `pkg/` - 公共⼯具库
- `api/` - API 定义（ Proto/Swagger ）
- `configs/` - 配置⽂件
- `scripts/` - 脚本⼯具
## 开发规范
- 代码规范：参⻅  `.codebuddy/rules/go-backend.md`
- 数据库规范：所有查询⾛  Repository 层
- 错误处理：统⼀使⽤  `pkg/errors`  包装错误
## 常⽤命令
- 编译：`go build ./...`
- 测试：`go test ./...`
- Lint ：`golangci-lint run`
## 当前进⾏中的需求
- 参⻅  `.codebuddy/plan/` ⽬录下的活跃需求
## 注意事项
- 添加新功能前，先检查  `pkg/`  下是否已有可复⽤的⼯具
- 数据库变更必须先⽣成  SQL 脚本
- 所有  API 变更需要更新  Swagger ⽂档
````

## PDF 第 20 页

[原页](RAW.pdf#page=20)

````text
4.5 知识库配置（详细实操）
知识库是让  AI 有业务上下⽂的核⼼⼿段。挂载团队内部⽂档、代码库和业务知识后， AI 能
从 " 通⽤智能 " 变成 " 懂你业务的专家 " 。
4.5.1 知识库类型与适⽤场景
知识库类
型 数据来源 适⽤场景 配置⼊⼝
iWiki ⽂档库团队  Wiki 空间 业务⽂档、技术⽅案、 API 说明、运维⼿
册 Knot 平台
⼯蜂代码库Git 仓库代码公共组件  SDK 、框架源码、参考实现Knot 平台
⾃定义⽂件Markdown txt PDF 需求⽂档、设计稿、会议纪要、领域知识Knot 平台
AI Wiki 基于代码库⾃动⽣
成 项⽬架构理解、模块逻辑梳理、新⼈上⼿CodeBuddy 内
置
4.5.2 在  Knot 平台创建团队共享知识库
Step 1 ：创建知识库
1. 前往  Knot 知识库管理页⾯
2. 点击「添加知识库」
3. 选择知识库类型（ iWiki ⼯蜂代码库  ⾃定义⽂件）
4. 填⼊知识库信息：
iWiki 类型：填⼊  iWiki 空间地址
⼯蜂代码库类型：填⼊  Git 仓库地址和分⽀
⾃定义⽂件类型：上传  Markdown txt PDF ⽂件
Step 2 ：配置共享范围
1. 在知识库详情页，开启「共享开关」
2. 选择需要分享的组织 / 团队
3. 提交后等待管理员审批，审批通过即完成团队共享
Step 3 ：配置数据源
在知识库的「数据源配置」页⾯，可以配置多种数据源：
需求：⽀持  TAPD 项⽬
代码：⽀持⼯蜂  Git 仓库（填⼊仓库地址和分⽀）
⽂档：⽀持  iWiki 空间
可观测：⽀持智研项⽬
⚠  AGENTS.md 是⽬录索引，不是百科全书。保持精简，让  AI 按需深⼊查阅具体⽂档。
````

## PDF 第 21 页

[原页](RAW.pdf#page=21)

````text
4.5.3 在  CodeBuddy 中启⽤知识库
Step 1 ：进⼊知识库设置
在  CodeBuddy 对话⾯板中，点击设置图标  →  进⼊「知识库」选项。
Step 2 ：开启知识库
1. 在知识库列表中，开启需要的公共知识库和个⼈知识库
2. 配置⾃动引⽤开关（推荐开启， AI 会⾃动参考相关知识）
Step 3 ：使⽤知识库的两种⽅式
# ⽅式⼀：显式引⽤（精确控制）
# 在对话输⼊框中输⼊  @KnowledgeBase ，选择特定知识库
@ 团队技术⽂档  请帮我分析当前项⽬的缓存策略是否合理
# ⽅式⼆：⾃动引⽤（省⼼省⼒）
# 开启⾃动参考开关后， AI 会根据问题⾃动检索相关知识
请帮我实现⽤户鉴权模块，参考团队现有的鉴权⽅案
4.5.4 开通  AI Wiki （推荐）
AI Wiki 是基于代码库⾃动⽣成的结构化知识库，帮助团队成员快速理解项⽬架构：
1. 在  CodeBuddy 右上⾓菜单中打开  AI Wiki
2. 按指引为当前代码库开通  AI Wiki （索引通常在  24h 内完成）
3. 开通后可直接在  IDE 中浏览项⽬⽂档，点击⽂件跳转到源码
4. 通过   @AIWiki  向  AI Wiki 提问，快速了解项⽬模块逻辑
4.5.5 推荐的团队知识库清单
优先级 知识库名称 类型 内容
P0 团队技术⽂档iWiki 架构设计、技术⽅案、接⼝⽂档
P0 核⼼公共库⼯蜂代码库tRPC SDK 、七彩⽯  SDK 、北极星  SDK 等
P1 业务需求⽂档⾃定义⽂件 产品需求⽂档、设计稿
P1 项⽬  AI Wiki AI Wiki 基于代码库⾃动⽣成的结构化⽂档
P2 运维⼿册 iWiki 部署流程、监控告警、故障处理
五、第⼆阶段：⼯具接⼊（深度集成）
⽬标：接⼊  MCP 、沉淀  Skills 、初始化  Spec ⽬录结构，在试点项⽬中实践  Plan 模式  SDD 。
⚠  验收标准：团队成员在  CodeBuddy 中提问业务相关问题时， AI 能⾃动引⽤知识库内
容给出准确回答，⽽不是泛泛⽽谈。
````

## PDF 第 22 页

[原页](RAW.pdf#page=22)

````text
5.1 MCP 配置（上下⽂边界突破）
MCP （ Model Context Protocol ）是  AI 的 " 感知触⼿ " ，让  AI 能触达代码仓库之外的真实世
界。
5.1.1 MCP 接⼊决策
⚠  何时不该⽤  MCP：
只写⼀个简单脚本查天⽓  →  直接调  API
纯逻辑推理、创意写作、代码⽣成  →  MCP ⼏乎没有⽤武之地
引⼊  MCP 的复杂度  > 它解决的问题  →  不⽤
5.1.2 CodeBuddy 插件端  MCP 配置
Step 1 ：打开  MCP 配置
1. 在  CodeBuddy 对话⾯板点击「对话设置」
2. 点击「添加  MCP 」
3. 编辑   mcp.json  配置⽂件
Step 2 ：配置  mcp.json
MCP ⽀持三种协议类型：
stdio 类型（本地命令⾏⼯具）：
{
  "mcpServers": {
````

## PDF 第 23 页

[原页](RAW.pdf#page=23)

````text
    "db-mysql": {
      "command": "npx",
      "args": ["-y", "@anthropic/mcp-server-mysql"],
      "env": {
        "MYSQL_HOST": "127.0.0.1",
        "MYSQL_PORT": "3306",
        "MYSQL_USER": "readonly_user",
        "MYSQL_PASSWORD": "${DB_PASSWORD}",
        "MYSQL_DATABASE": "your_database"
      },
      "timeout": 10000,
      "transportType": "stdio"
    }
  }
}
streamable-http 类型（推荐，远程服务）：
{
  "mcpServers": {
    "gump-tool": {
      "url": "http://127.0.0.1:3000/mcp",
      "timeout": 10000,
      "headers": {
        "Authorization": "Bearer your-token"
      },
      "transportType": "streamable-http"
    }
  }
}
sse 类型（逐步废弃，优先使⽤  streamable-http ）：
{
  "mcpServers": {
    "legacy-server": {
      "url": "http://0.0.0.0:3001/sse",
      "headers": {},
      "timeout": 10000,
      "transportType": "sse"
    }
  }
}
⚠  注意事项：
````

## PDF 第 24 页

[原页](RAW.pdf#page=24)

````text
Step 3 ：司内常⽤  MCP 配置参考
{
  "mcpServers": {
    "gongfeng": {
      "command": "npx",
      "args": ["-y", "@tencent/tgit-mcp-server@latest"],
      "env": {
        "GONGFENG_ACCESS_TOKEN": " 你的⼯蜂密钥 "
      }
    },
    "iWiki": {
      "headers": {
        "Authorization": "Bearer 你的太湖  token"
      },
      "type": "http",
      "url": "https://prod.xxx.com"
    },
    "tapd": {
      "headers": {
        "X-Tapd-Access-Token": "TAPD 个⼈ Token",
        "X-Keep-Links": "true"
      },
      "type": "http",
      "url": "http://mcp.xxx.com"
    }
  }
}
5.1.3 CLI 端  MCP 配置
Claude Code Internal：
⽤户级配置：~/.claude-internal/.claude.json
项⽬级配置：项⽬根⽬录下的   .mcp.json
Gemini CLI Internal：
配置⽂件：~/.gemini/settings.json
timeout 单位是  ms ，默认  10s ，最⼤  300s
stdio 类型的   args 必须拆开，不能合并为⼀个字符串
MCP 只在  Agent 模式下⽣效，提问时需要打开  Agent
更多  MCP 可前往  Knot MCP 市场  获取。
````

## PDF 第 25 页

[原页](RAW.pdf#page=25)

````text
注意： CLI 配置  Streamable Http 格式的  MCP ，url  需要写作   httpUrl
5.1.4 验证  MCP 连接
在  CodeBuddy 中测试：
请通过  DB MCP 读取当前数据库中  users 表的结构，列出所有字段名和类型。
如果失败，检查：
MCP Server 是否正常启动（查看  CodeBuddy 输出⾯板的⽇志）
数据库连接信息是否正确
⽹络是否可达
是否已开启  Agent 模式
5.1.5 团队  MCP 接⼊清单
优先级 MCP Server 接⼊⽬的 验收标准
P0 DB MCP AI 实时读取数据库  Schema AI 能准确描述任意表结构
P0 ⼯蜂  MCP 读取代码仓库、 Issue 、 MR AI 能读取  Issue 并给出实现思路
P1 iWiki MCP 挂载团队  Wiki ⽂档 AI 能回答业务领域问题
P1 TAPD MCP 读取需求和任务 AI 能读取需求并⽣成  Spec
P2 CI/CD MCP 触发构建和查看⽇志AI 能执⾏构建并分析失败原因
5.2 Knot 平台配置（智能体与知识管理中枢）
Knot 平台是  CodeBuddy ⽣态的管理中枢，提供知识库、 MCP 、 Rules 、 Skills 、智能体等核
⼼能⼒的统⼀管理。
5.2.1 Knot 平台核⼼功能⼀览
功能模块 ⼊⼝ 作⽤
智能体 knot.xxx.com 创建、管理、共享⾃定义智能体
研效知识库 knot.xxx.com 创建和管理团队知识库
MCP 市场 knot.xxx.com 发现和安装  MCP Server
Rules 市场 knot.xxx.com 获取和管理  Rules
Skills knot.xxx.com 管理  Agent Skills
5.2.2 在  Knot 创建⾃主规划式智能体
⾃主规划式智能体能⾃主分析任务并制定执⾏计划，适合复杂多变的场景。
Step 1 ：新建智能体
1. 前往  Knot 智能体页⾯
2. 点击「 + 新建智能体」
````

## PDF 第 26 页

[原页](RAW.pdf#page=26)

````text
3. 选择「⾃主规划」类型
Step 2 ：配置智能体
在智能体配置页⾯，填写以下信息：
配置项 说明 ⽰例
智能体名
称 简洁明了的名称 " 团队需求评审智能体 "
智能体描
述
准确描述职责和能⼒（影响⼦智能体
匹配）
" 基于  TAPD 需求与代码库，评审需求完整性和
可⾏性 "
Prompt 详细的⾓⾊设定和⾏为指引包含⾝份、⽬标、职责范围、操作指导
知识库 选择关联的知识库 团队技术⽂档、项⽬知识库
MCP 服务 选择需要的  MCP ⼯具 TAPD MCP 、⼯蜂  MCP
Rules 选择适⽤的  Rules 团队编码规范
Skills 选择需要的  Skills skill-creator 等
Client ⼯具 选择客户端⼯具 读取⽂件、执⾏命令等
Step 3 ：发布智能体
配置完成后，点击右上⾓「发布更新」。
5.2.3 配置智能体使⽤渠道
Knot 智能体⽀持多种使⽤渠道：
使⽤渠道 适⽤场景 配置⽅式
⽹页对话 ⽇常使⽤、调试 默认可⽤，⽆需额外配置
企微智能机器⼈ 团队群聊、私聊 配置  Bot ID 和  Secret
API 调⽤ 集成到现有系统 获取  API 接⼝和密钥
⽹页  URL 分享给外部⽤户 ⽣成独⽴⽹页链接
Knot CLI 命令⾏使⽤ 安装  Knot CLI ⼯具
流⽔线 CI/CD 集成 在蓝盾 /QCI 流⽔线中配置
定时运⾏ ⾃动化任务 设置定时任务频率
企微智能机器⼈配置步骤：
1. 进⼊企微⼯作台  →  搜索「智能机器⼈」→  创建机器⼈
2. 选择「⼿动创建  - API 模式」
3. 设置机器⼈基础信息
4. 将  Bot ID 和  Secret 填写到  Knot 智能体的「使⽤配置」中
5. 先保存智能机器⼈配置，再保存  Knot 配置
````

## PDF 第 27 页

[原页](RAW.pdf#page=27)

````text
6. 等待  5-8s 显⽰「已连接」后即可使⽤
5.2.4 智能体团队共享
1. 在智能体详情页  →  使⽤配置  →  权限配置
2. 编辑「可使⽤」权限，添加团队成员
3. ⼯作区也⽀持共享，在⼯作区管理页⾯开启共享开关
5.3 CodeBuddy ⼦智能体（ SubAgent ）配置
⼦智能体是  CodeBuddy 的核⼼协作能⼒ —— 让多个专业智能体在对话中⾃动配合完成复杂任
务。
5.3.1 什么是⼦智能体
在⽇常开发中，我们经常遇到固定的开发场景（需求分析、架构规划、国际化改造、重构
等），反复处理这些任务时需要反复编写相同提⽰词、引⽤知识库并选择⼯具。
⼦智能体解决这个问题：根据开发场景，灵活组合提⽰词、⼯具和知识库打造业务专属智能
体，启⽤后可在默认  Agent 对话时根据对话任务动态调⽤合适的⼦智能体协作完成任务。
5.3.2 创建⾃定义智能体
Step 1 ：创建智能体
1. 在  CodeBuddy 对话框左下⾓模式选择，点击「创建智能体」
2. 也可在对话⾯板顶部设置  →  对话  →  拉到底部的「⾃定义智能体」
Step 2 ：配置智能体
填写智能体的基本信息，组合可调⽤的⼯具、 MCP 、知识库：
配置项 说明 注意事项
名称 智能体名称 简洁明了
描述 职责描述 ⾮常重要
，会依据描述来匹配智能体
Prompt ⾏为指引 定义⾓⾊、能⼒、约束
⼯具 可调⽤的⼯具 按需选择
MCP 可调⽤的  MCP 服务 按需选择
知识库 关联的知识库 尽量选择与场景关联度⾼的，少⽽精
5.3.3 启⽤为⼦智能体（ SubAgent ）
如果需要多个智能体配合完成更复杂的⼯作场景，可以启⽤⼦智能体⾃动调⽤：
⚠  知识库选择后会在此智能体对话时主动引⽤，尽量选择仅与此场景关联度较⾼的知识
库。未选择的知识库也可在对话时主动  @ 引⽤。
````

## PDF 第 28 页

[原页](RAW.pdf#page=28)

````text
1. 给智能体添加准确的职责描述（此描述很重要，会依据描述来匹配智能体）
2. 勾选「⼦智能体」选项
提升⼦智能体被调⽤概率的技巧：
在描述中增加触发条件，例如：
当⽤户提出与数据库  / 数据查询  / 报表  / EDA 相关的请求时，必须调⽤我
5.3.4 推荐的团队⼦智能体配置
⼦智能体名称 职责描述 关联知识库关联  MCP
需求分析专家分析需求⽂档，⽣成  requirements.md 业务需求⽂档TAPD MCP
架构设计专家分析项⽬架构，给出设计建议团队技术⽂档、 AI Wiki -
数据库专家 数据库设计、 SQL 优化、 Schema 分析 - DB MCP
Code Review 专家 代码审查，检查规范合规性团队编码规范⼯蜂  MCP
运维排障专家分析⽇志、定位问题、给出修复建议运维⼿册 监控  MCP
5.3.5 公开分享智能体
创建的智能体可以通过  Knot 平台分享给团队：
1. 访问  Knot 智能体管理页⾯
2. 选择要分享的智能体（来⾃  CodeBuddy 创建的会有 "CodeBuddy 智能体 " 标识）
3. 进⼊使⽤配置，编辑可见（可使⽤）范围
4. 团队成员在  Knot 平台收藏后，智能体会出现在  CodeBuddy ⾃定义智能体列表中
5.4 Skills 配置
Skills 是给  AI 的操作⼿册 —— 把团队的专家经验、最佳实践和操作流程固化成  AI 可执⾏的指
令。
5.4.1 Skill ⽂件结构规范
---
name: "rainbow-config"
description: " 七彩⽯（ Rainbow ）配置中⼼的连接、查询和更新操作。
当需要对七彩⽯配置进⾏以下操作时使⽤：
(1) 初始化 / 连接配置中⼼
(2) 查询分组配置（ KV 型或  Table 型）
(3) 获取 / 设置单个配置参数
(4) 添加配置变更监听 "
---
# 七彩⽯配置接⼊  Skill
## 前置条件
````

## PDF 第 29 页

[原页](RAW.pdf#page=29)

````text
- 项⽬已引⼊  `pkg/rainbow`  包
- 已配置七彩⽯  AppID 和  Group
## 操作步骤
### Step 1: 初始化连接
[ 具体代码模板和说明 ...]
### Step 2: 查询配置
[ 具体代码模板和说明 ...]
### Step 3: 监听变更
[ 具体代码模板和说明 ...]
## 注意事项
- 配置缓存策略
- 错误处理规范
- 降级⽅案
5.4.2 Skills 创建与复⽤流程
````

## PDF 第 30 页

[原页](RAW.pdf#page=30)

````text
5.4.3 Skill 创建实操
Step 1 ：安装  skill-creator
在  CodeBuddy 的  Skills 管理界⾯中搜索并安装   skill-creator。
Step 2 ：让  AI 分析现有代码并创建  Skill
我需要针对  pkg/rainbow 这个七彩⽯配置⼯具包创建⼀个  Skill 。
请分析这个包的代码，按照  skill-creator 的规范⽣成⼀个标准的  Skill ⽂件。
Step 3 ：审查⽣成的  Skill ⽂件
检查  AI ⽣成的  Skill 是否包含：
✅  准确的   name 和   description（决定  AI 何时触发此  Skill ）
✅  完整的前置条件说明
✅  分步骤的操作指引
✅  代码模板和配置⽰例
✅  注意事项和错误处理
Step 4 ：验证  Skill 效果
我需要在当前项⽬中接⼊七彩⽯配置中⼼，读取  app_config 分组下的所有配置。
AI 应⾃动识别并加载   rainbow-config Skill ，按照规范⽣成接⼊代码。
Step 5 ：上传到团队  Skills 仓库
cp -r .codebuddy/skills/rainbow-config/ /path/to/team-harness/skills/business/
cd /path/to/team-harness
````

## PDF 第 31 页

[原页](RAW.pdf#page=31)

````text
git add skills/business/rainbow-config/
git commit -m "feat: 新增七彩⽯配置接⼊  Skill"
git push
5.5 Spec 与  Plan 模式（规范驱动开发）
Plan 模式是实现规范驱动开发的核⼼⼿段：在  AI 动⼿写代码之前，先⽣成结构化的需求⽂档
和任务清单，经过⼈⼯审核确认后，再按计划逐步执⾏。
5.5.1 Plan 模式开发流程（ 4 Stage ）
阶段 操作 模式 产出
Stage 1 描述需求， AI ⽣成需求
⽂档 Plan 模式 .codebuddy/plan/feat-xxx/requireme
nts.md
Stage 2 ⼈⼯逐项审核需求⽂档⼈⼯审查 审核通过的  requirements.md
Stage 3 AI ⽣成任务清单并逐步
执⾏
Agent 模
式
.codebuddy/plan/feat-xxx/task.md
 + 源代码
Stage 4 ⼈⼯审查代码，归档变
更 ⼈⼯审查 归档⽂档  + 变更⽇志
5.5.2 实操演练：以 " 新增⽤户操作⽇志模块 " 为例
Step 1 ：切换到  Plan 模式，描述需求
请使⽤  Plan 模式，分析以下需求并⽣成  .codebuddy/plan/feat-operation-log/requirements.md ：
新增⽤户操作⽇志模块，要求：
1.  记录⽤户的关键操作（登录、修改资料、删除数据等）
2.  ⽀持按⽤户 ID 、操作类型、时间范围查询⽇志
3. 提供管理后台的⽇志列表  API （分⻚）
4.  ⽇志数据保留  90  天，过期⾃动清理
请明确：功能边界、 API 接⼝定义、数据库表结构、异常处理策略和验收标准。
Step 2 ：审核  AI ⽣成的  requirements.md
□  需求理解是否准确？有没有多做或少做？
□  API 接⼝路径是否符合团队  RESTful 规范？
□  数据库表结构字段命名是否符合团队规范？索引设计是否合理？
□  90  天⾃动清理的实现⽅案是否可⾏？
````

## PDF 第 32 页

[原页](RAW.pdf#page=32)

````text
□  异常处理是否覆盖了：数据库写⼊失败、查询超时、参数⾮法等场景？
□  验收标准是否每条都可测试？
Step 3 ：确认⽆误后，⽣成任务清单并执⾏
需求审核通过。请阅读  .codebuddy/plan/feat-operation-log/requirements.md ，
⽣成  .codebuddy/plan/feat-operation-log/task.md 任务清单，
然后按任务顺序逐步实施。每完成⼀个任务后⾃动编译验证。
Step 4 ：⼈⼯审查代码并归档
# 归档
mv .codebuddy/plan/feat-operation-log .codebuddy/plan/archive/feat-operation-log
六、⽇常开发  SOP （标准操作⼿册）
6.1 SOP-A ：新需求开发
````

## PDF 第 33 页

[原页](RAW.pdf#page=33)

````text
简单需求的快捷流程（ < 半天⼯作量）：
# 直接在  Agent 模式中描述需求，⽆需⽣成  requirements.md
# 但仍需遵守  Rules 约束
请在  internal/user/service.go 中新增⼀个  GetUserProfile ⽅法，
要求：
1.  通过  user_id 查询⽤户基本信息
2.  返回  UserProfileResponse 结构体
3.  包含错误处理和⽇志记录
4.  编写对应的单元测试
6.2 SOP-B ： Bug 修复
````

## PDF 第 34 页

[原页](RAW.pdf#page=34)

````text
Bug 修复红线：
⼀个  PR 只修⼀个  Bug ，禁⽌夹带其他修改
必须编写能复现该  Bug 的测试⽤例
commit 信息格式：fix: [ 模块名 ] 修复 xxx 问题  (#issue 编号)
6.3 SOP-C ： AI 辅助  Code Review
````

## PDF 第 35 页

[原页](RAW.pdf#page=35)

````text
⽅式⼀：提交前⾃查
请对以下⽂件的变更进⾏  Code Review ：
- internal/user/service.go
- internal/user/repository.go
审查要点：
1.  是否符合分层架构规范
2.  错误处理是否完善
3.  是否有潜在的性能问题
4.  命名是否规范，注释是否清晰
5.  是否有安全隐患
⽅式⼆： Review 他⼈  PR
请阅读以下  PR 的变更内容，给出  Code Review 意⻅：
[ 粘贴  diff 或指定⽂件列表 ]
重点关注：逻辑正确性、边界情况处理、与现有代码的⼀致性、测试覆盖度
Code Review 检查清单：
类别 检查项 说明
架构 分层是否正确 Controller 不含业务逻辑， Repository 不含业务判断
架构 是否复⽤已有模块 检查  pkg/  下是否有可复⽤的⼯具
质量 错误处理 所有  error 必须显式处理，禁⽌  _ = err
质量 单元测试 核⼼逻辑必须有测试，覆盖正常和异常路径
安全 SQL 注⼊ 参数化查询，禁⽌字符串拼接  SQL
安全 敏感信息 禁⽌硬编码密钥、连接串
性能 数据库查询 检查是否有  N+1 查询、全表扫描
规范 commit 信息 格式清晰，描述修改点和原因
七、团队协作红线（不可违反）
红线 说明
先  Spec 后  Code 严禁在没有明确  Spec 的情况下直接开始  Coding
Rules 共享 项⽬级的  Rules 必须同步⾄  Git 仓库，不允许本地私有
Skill 沉淀 通⽤的逻辑处理必须抽象为  Skill 以便全队复⽤
MCP 优先 关键元数据优先通过  MCP 实时同步，⽽不是⼿动维护副本
变更可追溯 所有代码变更必须附带清晰的  commit 信息
````

## PDF 第 36 页

[原页](RAW.pdf#page=36)

````text
⼋、常见问题与反模式
8.1 反模式清单
# 反模式 现象 正确做法
1 巨型  Prompt ⼀次性把⼏千字需求丢给  AI 先  Plan 模式⽣成  requirements.m
d，拆解后逐步执⾏
2 跳过审核直接
编码
觉得需求简单，不写  Spec 直接
让  AI 写代码 半天以上的需求必须⾛  Plan 模式
3 Rules 写了不
维护
Rules ⽂件写完就放着，半年后
已经和实际规范脱节⽉度  Review 会议定期检查
4 MCP 过度接
⼊
接⼊了⼗⼏个  MCP Server ， Tok
en 消耗暴增 只接⼊  P0/P1 优先级的  MCP
5 Skill 不原⼦化⼀个  Skill 塞了太多功能 ⼀个  Skill 只解决⼀类问题
6 盲⽬信任  AI 输
出 AI ⽣成的代码不审查直接合⼊所有  AI ⽣成的代码必须经过⼈⼯
Code Review
7 Chat 历史当⽂
档 需求细节全在聊天记录⾥需求和设计决策必须持久化到  .c
odebuddy/plan/
8 ⼀个  PR 改所
有
让  AI ⼀次性实现多个不相关的功
能 ⼀个  PR 只解决⼀个问题
九、合规性⾃检：⽤  ⾃制  Skill ⼀键体检
前⾯⼏章把规范、⼯具、 SOP 都讲清楚了。但落地最⼤的痛点是 ——规范写完容易，执⾏下
去难。团队成员是否真的按规范配置了  Rules ？项⽬是否真的建了   .codebuddy/skills/？
Commit 信息是否规范？
靠⼈⼯⼀个项⽬⼀个项⽬地翻，⼜慢⼜容易漏。我们根据上⾯的规范沉淀了   harness-audi
t  Skill —— 把整套规范的检查项固化成⼀个可执⾏的合规性审计⼯具，⼀句话就能给项⽬打
分、找问题、给建议。
9.1 这个  Skill 能⼲什么
harness-audit  是⼀个  Harness 规范的⾃动化合规性检查⼯具，覆盖前⽂规范涉及的所有核⼼
维度。它能做三件事：
1. 打分：给项⽬从  7 个维度打总分（满分  100 ），按  S/A/B/C/D 五级评定
2. 诊断：列出每个维度的具体问题（哪些缺失、哪些不规范、哪些有但没⽤好）
3. 开⽅：按  P0/P1/P2/P3 优先级给出改进建议，附带操作步骤和代码⽰例
与本规范的对应关系：
审计维度 权重 对应章节 检查内容
1. AGENTS.md （ A
I 说明书） 15% §4.4 编写  AGENTS.md 是否存在、是否精简（ ~100 ⾏）、是否
包含项⽬概述 / 架构 / ⽬录 / 常⽤命令
````

## PDF 第 37 页

[原页](RAW.pdf#page=37)

````text
审计维度 权重 对应章节 检查内容
2. Rules （约束体
系） 20% §4.3 Rules 配置
.codebuddy/rules/
  ⽬录、 Frontmatter 规范、架构 / 风格 / 安
全约束完整性
3. Skills （技能沉
淀） 15% §5.4 Skills 配置
.codebuddy/skills/
  ⽬录、 Skill 数量、 SKILL.md 规范性、
业务相关性
4. MCP （上下⽂扩
展） 10% §5.1 MCP 配置
mcp.json
  是否存在、 Server 配置规范、敏感信息
是否硬编码
5. Plan 模式（ SD
D） 15% §5.5 Spec 与  Plan 模
式
.codebuddy/plan/
  ⽬录、 requirements.md / task.md 完
整性
6. 项⽬⼯程规范15% §6 ⽇常开发  SOP ⽬录结构、分层架构、 README 、依赖
管理、.gitignore
7. Commit 规范与
协作 10% §6.2 Bug 修复红线  / §
7 团队协作红线
Commit 格式（ type: [scope] descriptio
n）、变更粒度
可以看到，每个审计维度都精确对应到本规范的某⼀章节 ——Skill 就是规范的可执⾏版本。
9.2 怎么⽤
前置条件：
已安装  CodeBuddy 插件并完成基础配置（参见  §4.1 ）
已将   harness-audit Skill 放到   .codebuddy/skills/  ⽬录下，或通过团队  Skills 仓库同步
触发⽅式（在  CodeBuddy Agent 模式下输⼊即可）：
# 审计当前本地项⽬
请⽤  harness-audit Skill 对当前项⽬做⼀次合规性审计。
# 审计远程⼯蜂项⽬（需配合⼯蜂  MCP ）
请⽤  harness-audit Skill 审计这个项⽬：
https://git.xxx.com
# 只关注某⼏个维度
请⽤  harness-audit Skill 审计当前项⽬，重点检查  Rules 和  Skills 维度。
AI 会⾃动加载  Skill ，按 " 信息采集  →  逐维度评分  →  ⽣成报告 " 三阶段执⾏，最终把完整报告
写⼊   .codebuddy/reports/harness-audit-{ 项⽬名 }-{ ⽇期 }.md，并在对话中展⽰摘要。
9.3 检查结果⽰例
下⾯是对⼀个真实  Go 后端项⽬执⾏审计后的报告摘要（节选⾃完整报告）：
````

## PDF 第 38 页

[原页](RAW.pdf#page=38)

````text
📋  项⽬基本信息
项⽬ 信息
项⽬名称 go_scaﬀolding_svr
项⽬地址 git.xxx.com
项⽬负责⼈ zhangsan （基于  Git 提交记录分析）
审计分⽀ master
技术栈 Go 1.21 + tRPC-Go
最近活跃 2026-04-15 18:32
Commit 总数 287
核⼼贡献者 zhangsan (158) 、 lisi (72) 、 wangwu (35)
🎯  总体评分
┌──────────────────────────────────────────────────┐
│                                                  │
│       总分：75 / 100      等级： A 🟢  优秀          │
│                                                  │
│   0────40────60────75──89────100                 │
│   D    C     B     ▲ A    S                       │
│                                                  │
│   评语： AI 辅助开发体系完善，核⼼要素具备         │
│                                                  │
└──────────────────────────────────────────────────┘
维度 得分 满分 得分率 等级
AGENTS.md 14 15 93% 🟢  优秀
Rules 18 20 90% 🟢  优秀
Skills 12 15 80% 🟢  优秀
MCP 0 10 0% 🔴  不合格
Plan 模式 12 15 80% 🟢  优秀
⼯程规范 13 15 87% 🟢  优秀
Commit 规范 6 10 60% 🟡  良好
总计 75 100 75% 🟢  A 级
Harness 合规性 各 维 度得分 率 AGENTS.mdRulesSkillsMCPPlan ⼯程
Commit1009080706050403020100 得分率  (%)
✅  亮点
AGENTS.md ⾼度精简： 78 ⾏，符合 " ⽬录索引⽽⾮百科全书 " 的设计原则
````

## PDF 第 39 页

[原页](RAW.pdf#page=39)

````text
Rules 体系完善：.codebuddy/rules/  下有   global.md、go-backend.md、security.md  三
个⽂件，覆盖架构、风格、安全
Skills 业务相关性强：沉淀了   rainbow-config、polaris-resource 等  5 个业务  Skill
⽬录结构标准：严格遵循   cmd/internal/pkg/api 标准布局
⚠  主要问题
🔴  未配置  MCP：项⽬根⽬录⽆   mcp.json， AI ⽆法实时读取数据库  Schema 和⼯蜂
Issue
🟠  Commit 信息不规范：最近  50 条  commit 中， 30% 使⽤  "update" 、 "ﬁx bug" 等模糊
描述
🟡  Plan ⽬录未启⽤归档：.codebuddy/plan/  下没有   archive/  ⼦⽬录，已完成需求未归档
🔧  优化建议（节选）
🔴  P0 - ⽴即修复
1. 接⼊  DB MCP（耗时  30 分钟，参见  §5.1.2 ）
{
  "mcpServers": {
    "db-mysql": {
      "command": "npx",
      "args": ["-y", "@anthropic/mcp-server-mysql"],
      "env": {
        "MYSQL_HOST": "${DB_HOST}",
        "MYSQL_USER": "readonly_user",
        "MYSQL_PASSWORD": "${DB_PASSWORD}"
      },
      "timeout": 10000,
      "transportType": "stdio"
    }
  }
}
🟠  P1 - 短期改进
1. 统⼀  Commit 规范（耗时  1 周）：在团队周会同步  §6.2 Commit 格式（type: [scope] descri
ption），并配置  git hook ⾃动校验
2. 建⽴  Plan 归档机制（耗时  30 分钟）：mkdir -p .codebuddy/plan/archive，已完成需求统⼀
归档
🚀  Quick Wins
改进项 预计耗时 影响
创建  mcp.json  接⼊  DB MCP 30 分钟 AI 写  SQL 准确率提升  30%+
创建  .codebuddy/plan/archive/5 分钟 历史需求可追溯
````

## PDF 第 40 页

[原页](RAW.pdf#page=40)

````text
改进项 预计耗时 影响
配置  commit-msg hook 20 分钟 Commit 规范率从  70% →  95%+
📈  成熟度路线图
> 当前阶段：第⼆阶段（⼯具接⼊）
9.4 推荐使⽤节奏
场景 频率 ⽤途
项⽬初次接⼊规范1 次 摸清基线，定改进计划
季度团队复盘 每季度  1 次 量化规范落地效果，对⽐上季度
新项⽬⽴项后 ⽴项  2 周内 检查基础建设阶段是否到位
Code Review 之前 按需 配合  §6.3 SOP-C ，做提交前⾃查
Knot 平台共享审计 每⽉  1 次 跨项⽬对⽐，识别  S 级标杆项⽬
第三部分：总结
⼗、总结
AI Agent ⼯具能在代码质量的各个⽅⾯帮不少忙，但最终的质量把关，还是得靠操作这些⼯
具的⼈。你得知道什么是好代码，你得能判断  Agent 产出的东西够不够好，你得能在关键的
地⽅做出正确的取舍。
成本降低了，标准不能降低。⼯具变强了，⼈的判断⼒要跟着变强。
下⼀阶段⽬标：补齐  MCP 接⼊、规范  Commit 、建⽴归档机制  预计达成时间： 2 周
完整报告（含  7 个维度的逐项检查表、 Mermaid 饼图、落地⼿册对标检查等）会输出
到   .codebuddy/reports/harness-audit-go_scaffolding_svr-20260416.md。
⚠  注意：审计报告是体检结果，不是  KPI 。重点是发现问题、推动改进，不要把分数当
指标考核。规范的⽬的永远是让  AI 更好⽤、让团队效率更⾼，⽽不是为了刷分。
Django 创始⼈说过：交付代码的成本已经接近免费了，但交付好代码的成本依然很⾼。
````

## PDF 第 41 页

[原页](RAW.pdf#page=41)

````text
阅读 5 . 0 万
让各类⼯具适配规范，                              
⽽不是靠个⼈去适配各类⼯具。                                 
这就是从" ⼈驱动  AI"到"AI ⾃驱动 "的转变。            
通过这套规范体系，团队可以：
把 " 交付代码 " 的成本降低（ AI 执⾏）
把 " 交付好代码 " 的标准写进  Harness 系统⾥（规范约束）
实现 " 知识飞轮效应 "—— 新成员越多，整体效率反⽽越⾼（经验沉淀）
要掌握底层⽣存法则：流⽔的⼯具，铁打的规范。
如有不⾜ , 欢迎讨论指正。
腾讯技术官⽅号。腾讯技术创新、前沿领域发布解读平台。
688 篇原创内容
腾讯技术⼯程
公众号
````

## PDF 第 42 页

[原页](RAW.pdf#page=42)

````text
留⾔
还没有留⾔，来写⾸评
写留⾔
````

