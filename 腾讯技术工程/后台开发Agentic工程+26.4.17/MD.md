# 原文逐页转写

文本来自本次 PDF 文本层；不补写图片、截断内容或代码。图片和布局请打开每页 PDF 链接核对。AI 解释另见学习笔记。

## PDF 第 1 页

[原页](RAW.pdf#page=1)

````text
从 Vibe  Coding 到 Agentic  Engineering ：重构后台开发全流程
腾讯程序员 2026 年 4 ⽉ 17 ⽇ 02 : 36⼴东原创 腾讯技术⼯程 739 ⼈
作者： seanguo
引⾔
做后台开发的同事应该都有这个体会：从接到需求到最终发布，我们要在  PM 、 GitPlatform 、
编辑器、 DevOps 平台、 Galileo 之间来回横跳。每次切换都在丢上下⽂ —— 刚在  PM 看完需
求描述，切到编辑器就忘了某个细节；部署完测试环境去查⽇志，⼜得回忆刚才改了哪⼏⾏代
码。
你可能听过  Vibe Coding   这个说法 —— 打开  AI 对话框，⽤⾃然语⾔描述需求，让模型直接
⽣成代码，跑通就算完。原型验证很爽，但⼀旦要上⽣产，问题就来了：⽣成的代码质量不可
控、没有审查流程、改完了  commit message 也是乱的。说到底， Vibe Coding 是 " 提⽰即祈
祷 " （ prompt-and-pray ），你把需求扔给  AI ，然后祈祷它别出错。
今年⾏业⾥逐渐形成了⼀个更成熟的概念：Agentic Engineering（智能体⼯程）。核⼼思路
是 —— ⼈负责定义⽬标、约束条件和质量标准， AI 作为⾃主智能体在结构化流程中执⾏规
划、编码、测试和迭代，每个关键节点都有⼈⼯审核。它不是让  AI 随意发挥，⽽是把  AI 的能
⼒嵌⼊到⼀套有纪律的⼯程体系⾥。
最近⼀周，我⽤  Claude Code + ⾃定义  Skill/Command/MCP 体系  做了⼀次实践：把从需
求到发布的所有环节串到⼀个终端会话⾥。 AI 全程保持对当前任务的理解，在预设的流程框
````

## PDF 第 2 页

[原页](RAW.pdf#page=2)

````text
架内⾃主执⾏；我只需要在关键节点做决策 —— 审批计划、确认部署、审查代码。回过头看，
这套东西就是  Agentic Engineering 在后台开发场景的⼀个落地样本。
这篇⽂章把整个流程拆开给⼤家看，从需求到发布每⼀步怎么跑的，踩过哪些坑，最后沉淀出
了什么（🔥 token 的⼗⼤技巧）。
不过，说实话，虽然过程很完美，但消耗的  token 数量也不容⼩觑。迫切需要更⾼的  token 额
度了
全流程概览
先看效果。下⾯是整个流程的各阶段概览 —— 从需求到发布，开发者的⾓⾊从 " 亲⾃执⾏ " 变成
了 " 审核确认 " ：
阶段 核⼼⼯具 开发者做什么
①  需求创建  + 分⽀初始化 pm-dev ⼝述需求
②  需求澄清 brainstorming 回答  2-3 个问题
③  制定实施计划 writing-plans 审核计划
④  并⾏开发 executing-plans
 + /commit ⼏乎⽆需⼲预
⑤  代码⾃审 code-review 审核报告
⑥  编译部署 dtools 确认部署参数
⑦  ⽇志排查 galileo-log-query⼿动触发测试
⑧  创建  MR /create-mr 确认  MR 信息
⑨  AI 辅助评审 /review-mr 审核  AI 评审意见
⑩  修复评审意见 /fix-mr 确认修复⽅案
⑪  合⼊发布 CI/CD 点  Merge + 灰度发布
后⾯各阶段会逐个展开细节。
⼯具体系速览
这套⼯具链分三层，理解了层次关系，后⾯的内容就好跟了：
````

## PDF 第 3 页

[原页](RAW.pdf#page=3)

````text
层次 说明 ⽰例
Skill
（技能）
核⼼业务逻辑，由系统根据上下⽂⾃动
触发，或被  Command 调⽤。每个  Skill
有独⽴的⼯具权限⽩名单和执⾏流程
pm-dev
、git-workflow、code-review、dtoo
ls、galileo-log-query、git-conte
xt、wiki-doc、service-analyzer
Command
（斜杠命
令）
⽤户通过  /xxx  主动调⽤的⼊⼝，轻量
级路由，委托给对应的  Skill 执⾏
/commit
、/create-mr、/review-mr、/fix-m
r、/analyze-codebase
MCP Serv
er
（外部服
务）
通过  Model Context Protocol 连接的外
部平台  API ，为  Skill 提供数据和操作能
⼒
GitPlatform MCP 、 PM MCP 、 Galileo MC
P 、 KnowledgeBase 知识库  MCP 、 Internal
Wiki MCP
此外还有⼀类来⾃   superpowers  插件的结构化⼯作流  Skill（brainstorming、writing-plan
s 、executing-plans、subagent-driven-development、verification-before-completion 等），它
们定义了从需求澄清到代码交付的标准流程，防⽌  AI 跳过关键步骤⾃由发挥。
下⾯以⼀个真实的⼩变更需求为例，⾛完从需求到发布的全流程 —— 「 RedeemReward 接⼝
数据上报逻辑变更：⽆论领取是否成功，都要上报结果，新增  errcode/errmsg 字段」。选这个
需求是因为它体量适中（涉及  go mod 依赖更新、结构体扩展、接⼝逻辑重构），刚好能展⽰
每个阶段的⾃动化能⼒，⼜不会因为业务本⾝太复杂⽽分散注意⼒。
阶段  1 ：需求获取与分⽀初始化
场景：⼿头没有现成的  PM 需求单，直接在终端⾥⼝述需求就⾏。
操作：输⼊   /pm-dev  命令并附上需求描述：
❯  /pm-dev RedeemReward
接⼝⾥的数据上报逻辑变更，⽆论领取是否成功，都要上报结果
（上报数据新增  errcode, errmsg 字段）。新字段要更新
git.example.com/org/component/report_data/reportstruct go mod 获取。
Claude Code 检测到当前在  master 分⽀，⼜没有  PM URL ，就弹出选择：
[!info] 使⽤的⼯具pm-dev (Skill) — PM 开发初始化⼯具，两种⼊⼝：
1. 给  PM URL →  ⾃动解析需求  ID ，拉取需求标题和正⽂
2. 不给  URL →  通过  brainstorming 澄清需求后，⾃动调⽤  PM MCP 创建需求单
创建完成后⾃动：建分⽀（feature/{username}_{short_id}）→  保存需求⽂档到   docs/p
m/  →  衔接后续开发流程
````

## PDF 第 4 页

[原页](RAW.pdf#page=4)

````text
· 没有检测到  PM 需求单信息，请选择如何继续？  → ⾃动创建新需求单
接下来  AI 会进⼊  brainstorming 模式澄清需求（详见阶段  2 ），澄清完⾃动创建  PM 需求单：
⏺  pm - stories_create
  workspace_id: "12345678"
  name: "RedeemReward 上报逻辑变更新增错误码 "
  description: "RedeemReward 接⼝的数据上报逻辑变更：⽆论领取是否成功，都要上报结果 ..."
✅  需求单创建成功
  - 标题 : RedeemReward 上报逻辑变更新增错误码
  - 链接 : https://pm.example.com/pm_fe/12345678/story/detail/1012345678001958011
⼝述需求， AI 交互澄清后，⾃动创建的需求单⽰例：
随后⾃动创建开发分⽀并保存需求⽂档：
⏺  git checkout -b feature/alice_131900001
⏺  Write(docs/pm/131900001.md)  — 保存需求⽂档
效果：⼀段⼝述  →  PM 需求单  →  规范命名的开发分⽀  →  需求⽂档落盘。全程没打开过  PM
页⾯。
直接拉取需求单⽰例：
[!tip] Skill 也可以当命令⽤pm-dev  是⼀个  Skill （系统根据上下⽂⾃动触发），但你也可以
通过   /pm-dev  显式调⽤它。实际上，所有  Skill 都⽀持以   /skill-name 的⽅式⼿动触发
—— 当你明确知道要⽤哪个  Skill 时，直接   /xxx 调⽤⽐等待⾃动触发更⾼效。
[!tip] 有现成的  PM 需求单？  直接提供链接即可：/pm-dev https://pm.example.com/xxx/stor
y/detail/10xxx， AI 会⾃动拉取需求详情并创建开发分⽀。
````

## PDF 第 5 页

[原页](RAW.pdf#page=5)

````text
补充⼀个  AI aha moment 的例⼦：
我在开发  pm-dev skill 的时候，发现项⽬管理  MCP Server 并不⽀持将链接⾥⾯的长 ID
（ 1012345678001900001 ）转成  short_id （ 131900001 ）。但是想要⾃动创建特性管理值就需
要⽤到  short_id ，那该怎么做呢？
AI 直接推测出了  short_id 和  ID 的关系！（我开发这么久的需求，见过的需求  url & short ID
⽆数，从来都没有发现两者之间的关系。这个时候我就感觉  AI 是真的能够发现我们⾁眼所发
现不到的规律。）
阶段  2 ：交互式需求澄清
[!info] 使⽤的⼯具superpowers:brainstorming (Skill) — 结构化的需求澄清流程。 AI 不会
直接写代码，⽽是先探索代码库了解现状，然后通过提问 - 回答逐步明确需求边界、技术
⽅案和实现路径，最终产出⼀份双⽅达成共识的设计⽅案。wiki-doc (Skill) /  kno
t MCP — 知识库检索。澄清过程中  AI 可以搜内部  Wiki ⽂档或通过  KnowledgeBase 知
识库做语义检索，为设计决策补充技术背景和历史⽅案参考。
````

## PDF 第 6 页

[原页](RAW.pdf#page=6)

````text
场景：需求描述就⼀句话， AI 得先搞清楚代码现状和变更细节才能动⼿。
操作： AI 先⾃动探索项⽬代码，了解  RedeemReward 接⼝和上报逻辑的现有实现：
⏺  Explore( 探索  RedeemReward 和上报逻辑 )
  Done (20 tool uses · 93.8k tokens · 56s)
然后基于代码理解，抛出关键问题：
🤔  新增的  errcode/errmsg 字段是加到现有的  Report_table_001 （数据上报表）上，
    还是⽤⼀个新的上报表？
❯  复⽤  Report_table_001 表 , 更新  go mod 以后就有新增的  2 个字段了
AI 理解后，提出两种实现⽅案并给出推荐：
⽅案  A （推荐）：在  RedeemReward 末尾统⼀上报，不提前  return
  将上报逻辑移到函数末尾，把第三⽅调⽤的  error 信息传⼊上报参数。
  - 优点：改动集中，与现有  ReportConsumeCount ⻛格⼀致
  - 缺点：需要调整  error 处理流程
⽅案  B ：在每个  return  前都加⼀次上报调⽤
  - 优点：不改变原有  return  逻辑
  - 缺点：多处重复调⽤，容易遗漏
· 你倾向哪种实现⽅式？  → ⽅案  A ：统⼀上报  (Recommended)
确认⽅案后， AI 输出完整的设计⽅案：
设计⽅案 :
1. 数据结构变更  — CardReportParam 新增  ErrCode/ErrMsg 字段
2. RedeemReward 流程变更  — ⽤  defer 确保上报⼀定执⾏
3. 变更⽂件清单 :
   ┌──────────────────────────┬──────────────────────────────────────┐
   │           ⽂件            │                 变更                  │
   ├──────────────────────────┼──────────────────────────────────────┤
   │ go.mod                   │ 升级  report_data 版本            │
   │ repo/report/card_report.go │ CardReportParam 新增字段， ReportCard │
[!info] 链式调⽤  这个阶段不需要⼿动触发 ——pm-dev  完成需求创建和分⽀初始化后，
会⾃动链式调⽤   brainstorming  进⼊需求澄清。 brainstorming 完成后⼜会接着调⽤   writi
ng-plans（阶段  3 ），形成  需求  →  澄清  →  计划 的⾃动流⽔线。
````

## PDF 第 7 页

[原页](RAW.pdf#page=7)

````text
   │                          │ 填充新字段                            │
   │ logic/redeem_reward.go      │ 重构  RedeemReward ，⽆论成败都上报        │
   └──────────────────────────┴──────────────────────────────────────┘
效果： AI 不是闭门造车 —— 先读代码、再提问、再出⽅案。设计⽂档⾃动保存到   docs/plan
s/  并  commit 。
阶段  3 ：制定实施计划
场景：设计⽅案确认后， AI ⾃动深⼊阅读代码，⽣成可执⾏的实施计划。
操作： AI 先扎进代码细节 —— 结构体字段、错误处理⽅式、 go mod 版本 —— 确保计划⾥的代
码路径和修改点都是准确的：
⏺  Read: repo/report/card_report.go, logic/redeem_reward.go, errs 包
⏺  查找  Report_table_001 结构体当前字段
⏺  当前版本  v1.0.180 还没有  errcode/errmsg 字段，更新  go mod 后新版本才会有
然后⽣成实施计划（ 223 ⾏），⾃动保存并  commit ：
⏺  Write(docs/plans/2026-03-03-claimgift-report-errcode.md)
计划拆成  4 个  Task ：
  1. 更新  report_data 依赖  — go get 升级版本，验证新字段存在
  2. CardReportParam 新增  ErrCode/ErrMsg — 修改结构体和  ReportCard 函数
  3. RedeemReward ⽆论成败都上报  — 重构流程， asyncReportRedeemReward 接收  error
  4. 最终验证  — go build/vet
[!tip] 不要重复造轮⼦pm-dev  早期版本曾经⾃⼰实现了头脑风暴 / 写计划 / 执⾏计划的功
能，后来发现   superpowers 插件已经提供了成熟的  brainstorming 、 writing-plans 、
executing-plans 等  Skill ，经过⼤量打磨，效果更好。最终把⾃制逻辑替换为链式调⽤现
成  Skill 。教训：⾃定义  Skill 的核⼼价值是编排和串联，⽽不是从零实现所有能⼒。
[!tip] 知识库补充上下⽂  在澄清过程中， AI 可以通过   wiki-doc  搜索内部  Wiki ⽂档，或通
过   knot  知识库检索已有的技术⽅案，为设计决策提供依据。
[!info] 使⽤的⼯具superpowers:writing-plans (Skill) — 结构化计划编写。 AI 深⼊读代码
细节（结构体字段、错误处理⽅式、依赖版本），确保计划⾥每个  Task 都有精确的⽂件
路径、代码变更描述和验证标准。计划⾃动保存到   docs/plans/ 并  commit ，⼈⼯审核通
过后才进⼊执⾏。
````

## PDF 第 8 页

[原页](RAW.pdf#page=8)

````text
阶段  4 ：并⾏执⾏开发任务
场景：计划审批通过，选择执⾏⽅式。
· 选择哪种执⾏⽅式？  → Subagent-Driven (Recommended)
操作： AI 按计划逐个派⼦  Agent 执⾏，每个  Task 完成后⾃动跑  spec review 和  code quality
review ：
⏺  Task 1: 更新  report_data
  ├─ Agent 执⾏  (5 tool uses · 49s)
  ├─ 新字段 : Errcode(string), Errmsg(string), 版本  v1.0.182
  └─ ✅  Spec review 通过
⏺  Task 2: CardReportParam 新增字段
  ├─ Agent 执⾏  (6 tool uses · 1m 6s)
  └─ ✅  Spec review 通过
⏺  Task 3: RedeemReward 上报重构（核⼼变更）
  ├─ Agent 执⾏  (4 tool uses · 6m 25s)
  ├─ ✅  Spec review 通过
  └─ ✅  Code quality review 通过，⽆  critical/important issues
⏺  Task 4: go build + go vet
  └─ ✅  全部通过
每个  Task 完成后⾃动⽣成规范的  Git commit ：
[!warning] ⼈⼯审核是关键  这是你审查  AI ⽅案的第⼀道关卡。计划⾥每个  Task 都有精确
的⽂件路径、代码变更描述、甚⾄具体的代码⽚段，⽅便逐条审核。 AI 可能会遗漏边界
情况或误判依赖关系，这⼀步不能省。
[!info] 使⽤的⼯具superpowers:executing-plans /  superpowers:subagent-driven-develop
ment (Skill) — 计划执⾏引擎，两种模式：
Sequential：主  Agent 按顺序逐  Task 执⾏
Subagent-Driven（推荐）：为每个  Task 派独⽴⼦  Agent 并⾏执⾏，完成后⾃动跑
spec review （功能是否符合计划）和  code quality review （代码质量检查）
/commit (Command →   git-workflow commit 模块 ) — 智能分析   git diff --cached，⽣
成  Conventional Commits 格式的  commit message （feat/ fix/ refactor 等），交互确
认后提交。还会检查是否需要拆分原⼦提交。
````

## PDF 第 9 页

[原页](RAW.pdf#page=9)

````text
d81eaee chore: upgrade report_data for new errcode/errmsg fields
18a0975 feat: add ErrCode/ErrMsg to CardReportParam and ReportCard
e978e6b feat: report RedeemReward result regardless of success or failure
效果： 4 个  Task 全部完成， 3 个实现  commit 。你只在关键节点确认就⾏。
变更⽂件汇总：
- go.mod / go.sum — 升级  report_data v1.0.180 → v1.0.182
- repo/report/card_report.go — CardReportParam 新增  ErrCode/ErrMsg ， ReportCard 填充
- logic/redeem_reward.go — RedeemReward ⽆论成败都上报，传⼊  errcode/errmsg
git commit 交互式澄清，⾃动⽣成规范的  commit 消息：
企业微信截图_47eb4fc4-7e23-4fa8-b578-bfc7b2a60a5d
规范  git commit ⽰例，更容易看出变更内容。
````

## PDF 第 10 页

[原页](RAW.pdf#page=10)

````text
subagents 并发任务⽰例， superpowers:execute-plan 会⾃动根据需要执⾏的计划，决定开
⼏个  subagent ，全程不⽤操作。你唯⼀需要的就是担⼼  token 额度。
阶段  5 ：代码审查（⾃审）
审查完成后⽣成  Markdown 报告到  docs/，并提供三种后续操作：⾃动修复所有问题  / 仅保
存报告  / 指定修复特定问题（如  C1, M2 ）。
场景：代码写完了，提交  MR 之前先⾃⼰过⼀遍，在  reviewer 看到之前就消灭明显问题。这
⼀步是 " ⾃查 "—— ⽤  AI 帮你快速扫⼀遍格式、命名、规范类的低级问题；后⾯阶段  9 的  AI 辅
助评审则是站在  reviewer 的⾓度做正式审查，两者定位不同。
操作：直接在终端⾥说就⾏：
❯  审查⼀下当前分⽀相对  master 的代码变更
AI ⾃动加载   code-review skill ，获取  diﬀ 并执⾏审查：
[!info] 使⽤的⼯具code-review (Skill) — Golang 代码审查⼯具。对   git diff 变更做系统
化审查，按严重程度（ Critical / Major / Minor / Suggestion ）和分类标签（业务逻辑  / 安
全性  / 性能影响  / 编程规范等  8 类）输出  CR 报告。内置完整的检查清单，覆盖：
Critical：空指针、 SQL 注⼊、数据竞争、资源泄漏、循环中  defer
Major：错误处理不规范（未⽤   errs.Newf/Wrapf）、嵌套超  4 层、 switch 缺
default 、并发安全
Minor：命名规范、 import 顺序、魔法数字、函数超  80 ⾏
Suggestion：可⽤   lo  简化集合操作、可⽤   copier  简化结构体复制、 Table-Driven
Tests
````

## PDF 第 11 页

[原页](RAW.pdf#page=11)

````text
⏺  git diff master...HEAD — 3 个⽂件， +21 -11 ⾏
审查报告：
┌──────────┬──────┐
│ 级别      │ 数量  │
├──────────┼──────┤
│ Critical │ 0    │
│ Major    │ 0    │
│ Minor    │ 1    │
│ Suggestion│ 1   │
└──────────┴──────┘
m1. [CR- 可读性 ] ChannelID 魔法数字缺少注释
  ⽂件 : logic/redeem_reward.go:43
  ChannelID: 3 缺少注释说明含义（会员⻚发放场景）
  建议 : 添加⾏内注释或提取为命名常量
S1. [CR- 编程规范 ] Errcode/Errmsg 字段缩进不⼀致
  ⽂件 : repo/report/card_report.go:57-58
  与上⽅字段的对⻬⽅式不⼀致
  建议 : 统⼀使⽤  gofmt 标准对⻬
⏺  Write(docs/code-review-report-20260303-153022.md) — 保存报告
· 如何处理审查结果？
  ○  ⾃动修复所有问题
  ○  仅保存报告
  ○  指定要修复的问题（输⼊编号如  m1, S1 ）
效果：code-review  相当于⼀个随时待命的  Golang 审查专家，内置了团队的编码规范和检查
清单。提  MR 前先跑⼀遍，格式、命名、规范类问题基本能清⼲净， reviewer 就不⽤在这些
细节上浪费时间了。
阶段  6 ：编译部署到测试环境
[!warning] 本⽂⽰例中跳过了⾃审修复  为了在后⾯阶段  9 （ AI 辅助代码评审）完整展⽰   /
review-mr 的⼯作流 —— 包括  AI 如何发现问题并精确提交⾏级评论到 GitPlatform—— 这
⾥选了 " 仅保存报告 " ，把两个问题留给  MR 评审阶段处理。实际开发中建议⾃审阶段就修
掉所有问题，让  reviewer 聚焦更⾼层⾯的设计和逻辑。
[!info] 使⽤的⼯具dtools (Skill) — DevOps 平台  CLI ⼯具集成。⾃动从  Makeﬁle 探测
APP/SERVER/ENV/INSTANCE 等参数（找不到时依次查  go.mod 、 trpcprotocol 协议路
径），⽀持   dpatch（包发布）、bpatch（⼆进制发布）、ipatch（镜像发布）三种模式。
````

## PDF 第 12 页

[原页](RAW.pdf#page=12)

````text
场景：代码开发完毕，部署到  pre 环境跑⼀下看看。
操作：输⼊   /dtools， AI ⾃动从  Makeﬁle 中提取部署参数：
确认部署参数：
  APP=my_app, SERVER=reward_service, ENV=pre, USER=alice
· 选择哪种发布⽅式？  → 指定实例发布  (make deploy)
AI 执⾏交叉编译和部署：
CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build -v -o .build/reward_service
dtools bpatch -env pre -app my_app -server reward_service \
  -bin .build/reward_service -user alice \
  -instances "pre.my_app.reward_service.instance001"
效果：编译  + 部署  + 修正过期配置，⼀条命令搞定。
dtools 发布⽰例：
阶段  7 ：⽇志排查与调试
还会⾃动处理  Mac →  Linux 交叉编译（CGO_ENABLED=0 GOOS=linux GOARCH=amd
64），仓库没有  Makeﬁle 时会⾃动⽣成标准化构建 / 部署模板。
[!tip] ⾃动发现配置过期  部署过程中发现  Makeﬁle ⾥的实例名   instance002  已经过期了，
AI ⾃动跑了   dtools node ls 查到当前可⽤实例是   instance001，确认后发布成功，还顺⼿
把  Makeﬁle ⾥的实例名更新了。这种 " 顺⼿修 " 的能⼒在⽇常开发中很实⽤。
[!info] 使⽤的⼯具galileo-log-query (Skill) — Galileo ⽇志查询。通过内置  Python 脚本调
⽤  Galileo Log Query API ，⽀持按  target （BG-PLATFORM.{appid}.{server}）、
````

## PDF 第 13 页

[原页](RAW.pdf#page=13)

````text
场景：部署后需要验证上报数据是否正确，或者排查异常。这⼀步⽬前还是 " 半⾃动 " 的 ——AI
能帮你查⽇志、定位问题，但测试请求还得⼈⼯⼿动发，因为  AI 不了解整条调⽤链的上下
游，没法⾃⼰构造有效的测试⽤例。后续计划在代码⾥加测试⼊⼝，让  AI 能直接发  tRPC 请
求触发模拟调⽤。
操作：直接在终端中描述查询需求：
❯  帮我查⼀下  pre 环境  reward_service 最近  10 分钟的  error ⽇志
AI 通过 Galileo API 查询，拿到结果后⾃动关联代码上下⽂分析：
🔍  问题定位：
  - redeem_reward.go:48 上报时  cfg 为  nil
  - 原因：获取配置失败的路径没有正确传⼊默认值
  - 建议修复：在  cfg == nil 时使⽤空  config ⽽⾮跳过上报
Galileo ⽇志⾃助排查⽰例：
namespace 、时间范围、查询语句、 traceID 等条件查⽇志。⾃动探测  appid/server （优
先从  Makeﬁle 、 go.mod 、 trpcprotocol 路径提取），内置防上下⽂爆炸机制（默认  limit
50 ，建议先⽤   level:error  缩⼩范围）。脚本查不到结果时会⾃动降级到 Galileo MCP
的   ask_question  接⼝。
[!tip] ⽀持多种查询⽅式
按  trace_id 查询完整调⽤链
按关键词搜索特定⽇志
按时间范围  + ⽇志级别过滤
按  target/namespace 精确定位服务
````

## PDF 第 14 页

[原页](RAW.pdf#page=14)

````text
再给⼀个例⼦，辅助排查 Galileo proﬁle 内容，帮忙快速定位了⼀个  OOM 问题。
阶段  8 ：创建  Merge Request
场景：测试通过，该提代码了。
操作：输⼊   /create-mr， AI ⾃动执⾏完整流程：
⏺  git-context:
  - 解析分⽀名  feature/alice_131900001 → 提取  story ID: 131900001
  - 校验分⽀命名规范  ✅
  - 通过  PM MCP 获取需求标题
⏺  分析  git log origin/master..HEAD 的全部  commit
⏺  预览⽣成的  MR 信息：
  项⽬ : org/team/project/backend/reward_service
  分⽀ : feature/alice_131900001 → master
[!info] 使⽤的⼯具/create-mr (Command →   git-workflow push-mr 模块 ) — MR 创建全
⾃动化：
1. 调⽤   git-context  获取  project_id 、校验分⽀命名
2. 从分⽀名提取  PM short_id ，通过  PM MCP 拉取需求标题，组装源码关键字（--story
={id} {title}）
3. 分析   git log origin/master..HEAD  全部  commit 和  diﬀ ，⽣成  MR 标题和描述（含变更
说明  + 影响范围）
4. 预览确认后，git push -u origin + 调⽤ GitPlatform MCP 创建  MR
git-context (Skill) — GitPlatform 项⽬上下⽂提取，两个复⽤模块： project-context （解
析  project_id 、校验分⽀、检查⼯作区）和  mr-locate （从  URL 或当前分⽀定位  MR 并获
取元数据）。
````

## PDF 第 15 页

[原页](RAW.pdf#page=15)

````text
  PM: --story=131900001 RedeemReward 上报逻辑变更新增错误码
  标题 : RedeemReward 上报逻辑变更，⽆论成败都上报并新增错误码
确认后⾃动推送分⽀并创建  MR ：
⏺  git push -u origin feature/alice_131900001
⏺  git-platform - create_merge_request
✅  MR 创建成功！
  - 链接 : https://git.example.com/.../reward_service/-/merge_requests/64
  - 状态 : can_be_merged
  - 必要评审⼈ : bob, charlie （ GitPlatform 项⽬已配置默认评审规则，⾃动分配）
⾃动⽣成的  MR 描述：
--story=131900001 RedeemReward 上报逻辑变更新增错误码
## 变更说明
- 升级  report_data v1.0.180 → v1.0.182 ，获取  Report_table_001 新增的  errcode/errmsg 字段
- CardReportParam 新增  ErrCode/ErrMsg 字段， ReportCard 填充到上报结构体
- RedeemReward 接⼝⽆论领取成功或失败都执⾏数据上报，传⼊错误码和错误信息
- 获取配置失败时也上报（ cfg 为  nil 安全处理）
## 影响范围
仅影响  RedeemReward 接⼝的数据上报逻辑，其他接⼝的  ReportCard 调⽤不受影响
（ ErrCode/ErrMsg 零值默认  0/"" ）
效果： MR 标题、描述、 PM 关联全部⾃动⽣成，格式规范、内容完整。
全⾃动提交  MR ⽰例，极⼤缓解了写  MR 描述的痛苦。
企业微信截图_548fd035-e052-4b9a-a260-1615df007faf
````

## PDF 第 16 页

[原页](RAW.pdf#page=16)

````text
GitPlatform MR 页⾯⽰例：
阶段  9 ： AI 辅助代码评审
场景： MR 创建后， reviewer （同事  charlie ）⽤  AI 辅助审查这个  MR 。
操作： reviewer 在⾃⼰的终端中输⼊  MR 链接：
[!info] 使⽤的⼯具/review-mr (Command →   git-workflow review 模块 ) — AI 代码审
查，精确提交⾏级评论到 GitPlatform MR ：
1. 通过   git-context 的  mr-locate 定位  MR （⽀持从  URL 解析或从当前分⽀⾃动查找）
2. 加载   code-review 的审查标准（含  Golang 规范、 trpc-go 模式、完整检查清单），仅
审查新增 / 修改的⾏
3. 每个问题标注严重程度和分类标签
4. ⽤   git show {source_branch}:{file_path}  验证⾏号准确性，确保评论定位精确
5. ⼈⼯审核后批量调⽤ GitPlatform MCP 提交评论（单条失败不阻塞其余）
````

## PDF 第 17 页

[原页](RAW.pdf#page=17)

````text
❯  /review-mr
https://git.example.com/org/team/project/backend/reward_service/-/merge_requests/64
AI ⾃动获取  MR 元数据、拉取  diﬀ 、读源⽂件验证⾏号，然后输出审查结论：
变更⽂件：
  - repo/report/card_report.go (+4 ⾏ )
  - logic/redeem_reward.go (+17 -11 ⾏ )
  - go.mod (+1 -1), go.sum (+2 -2)
主要逻辑评估：
  - 整体逻辑正确：⽆论成败都上报， cfg 为  nil 时安全处理  ✓
  - errs.Code(nil) / errs.Msg(nil) 在  trpc-go 框架中  nil 错误返回  0/""  ✓
  - 依赖升级合理  ✓
发现问题：
  Minor 1 个：
  - repo/report/card_report.go:57-58 — Errcode/Errmsg 字段赋值缩进与上⽅字段不⼀致
  Suggestion 1 个：
  - logic/redeem_reward.go:43 — ChannelID: 3 魔法数字，原有注释  // 发放场景， 3- 会员⻚
    在重构时被误删，建议补回
审查概要⽰例：
确认后， AI 将  2 条评论精确提交到 GitPlatform MR 页⾯：
[!tip] AI 能区分 " 本次引⼊ " 和 " 历史遗留 " 审查过程中  AI 发现   asyncReportRedeemRewar
d  函数名带  async 前缀但实际是同步调⽤，但它主动拉了  master 分⽀原始代码对⽐，确
认这是历史遗留⽽⾮本次引⼊，所以没有纳⼊审查范围。这个能⼒很重要 —— 没⼈喜欢
reviewer 在你的  MR ⾥提⼀堆历史债务。
````

## PDF 第 18 页

[原页](RAW.pdf#page=18)

````text
· 代码审查已完成，请选择评论提交范围： → Minor + Suggestion （共  2 条）
⏺  git-platform - create_merge_request_note
  ✅  M1 → repo/report/card_report.go:57 （含修复代码建议）
  ✅  S1 → logic/redeem_reward.go:43 （含补回注释或提取常量两种⽅案）
提交评论⽰例：极⼤提⾼了  CR 效率，不⽤再⼀个个去评论了。
AI 提交评论的关键，是找准要评论的位置。经过实测，发现  Claude  模型效果最好，
DeepSeek 模型经常找错⾏数，评论到错误的位置。
GitPlatform MR 上⾯的评论效果：
````

## PDF 第 19 页

[原页](RAW.pdf#page=19)

````text
效果：代码评审从⼈⼯逐⾏看  diﬀ 变成了  AI 初筛  + ⼈⼯把关。 AI 精确定位到⽂件和⾏号，附
带代码建议， reviewer 只需审核和决定提交哪些评论。更多真实案例见附录中的「 AI 代码评
审案例」。
阶段  10 ：修复  MR 评审意见
[!warning] AI 评审有对有错，⼈⼯审核不能省  AI 给出的评审意见不⼀定都是对的。它可
能误判代码意图、遗漏业务上下⽂、或者给出看起来合理但实际不适⽤的建议。上⾯这个
例⼦⾥  AI 提的  2 个问题碰巧都是准确的，但在更复杂的  MR 中，我们见过  AI 把正确的
错误处理标记为 " 缺少  error check" 、把刻意的空实现标记为 " 未完成代码 " 等误判。所以
reviewer 拿到  AI 的审查结果后，每⼀条都要过脑⼦判断，该采纳的采纳，不靠谱的直接
丢掉。
[!tip] 跨模型审查：避免同⼀个模型的盲区  ⼀个实⽤技巧：谁写的代码，就让别的模型来
审查。同⼀个模型写的代码再让它⾃⼰审，容易陷⼊相同的思维盲区 —— 它写代码时没考
虑到的问题，审查时⼤概率也发现不了。⽐如⽤  Claude 写的代码，可以⽤  Codex 或
Gemini 来做  AI 评审；反过来也⼀样。不同模型的知识结构和关注点不同，交叉审查能显
著提⾼问题发现率。
[!info] 使⽤的⼯具/fix-mr (Command →   git-workflow ﬁx 模块 ) — MR 评审意见⾃动修
复：
1. 通过   git-context 定位  MR ，⾃动切到源分⽀并拉最新代码
2. 调⽤ GitPlatform MCP 拉所有未解决评论（resolve_states=[1]），提取⽂件路径、⾏
号、评论内容
3. 读对应⽂件（前后各  10 ⾏上下⽂），分析问题是否仍存在并⽣成修复⽅案
4. 交互展⽰分析结果（含风险评估），确认后逐条修改
5. 修改后⾃动跑   go build ./...  验证编译，并调⽤ GitPlatform MCP 回复每条评论
````

## PDF 第 20 页

[原页](RAW.pdf#page=20)

````text
场景： MR 收到了  reviewer 的评审意见，需要逐条修。
操作：终端⾥输⼊   /fix-mr， AI ⾃动定位当前分⽀的  MR 并拉取未解决评论：
⏺  MR: #64 - RedeemReward 上报逻辑变更，⽆论成败都上报并新增错误码
  未解决评论 : 2 条
────────────────────────────────
[1] logic/redeem_reward.go:43
评论者 : charlie
评论内容 : [Suggestion] ChannelID 魔法数字  3 缺少注释说明
修复⽅案 : 为  ChannelID: 3 添加注释  "// 发放场景， 3- 会员⻚ "
────────────────────────────────
[2] repo/report/card_report.go:59-60
评论者 : charlie
评论内容 : [Minor] Errcode/Errmsg 字段赋值缩进与上⽅字段对⻬不⼀致
修复⽅案 : 调整  Errcode/Errmsg 缩进，使⽤  gofmt 标准对⻬
────────────────────────────────
· 如何处理这  2 条未解决评论？  → 全部修复
AI ⾃动执⾏修复：
[1] 修复  logic/redeem_reward.go:43
  -    ChannelID: 3,
  +    ChannelID: 3, // 发放场景， 3- 会员⻚
[2] 修复  repo/report/card_report.go:59-60
  -    Errcode:    cast.ToString(param.ErrCode),
  -    Errmsg:     param.ErrMsg,
  +    Errcode:     cast.ToString(param.ErrCode),
  +    Errmsg:      param.ErrMsg,
````

## PDF 第 21 页

[原页](RAW.pdf#page=21)

````text
⏺  go build ./...   ✅  编译通过
⏺  gofmt -d ...     ✅  格式检查通过
修复完成后，通过   /commit  提交：
fix: address CR comments for RedeemReward report changes
- 为  ChannelID 魔法数字  3 补充注释说明（会员⻚发放场景）
- 修正  Errcode/Errmsg 字段缩进，与上⽅字段对⻬⼀致
然后⾃动推送并回复评论。如果后续还有新的评审意见，再跑⼀次   /fix-mr  就⾏。
效果：评审  →  修复  →  提交  →  回复的完整闭环，全程在终端⾥完成。
阶段  11 ：合⼊发布
场景：评审意见全部修完， MR 拿到  Approve 。
操作：
1. GitPlatform 上点  Merge 合⼊主⼲
2. 03 流⽔线⾃动触发：编译  →  构建镜像  →  推送镜像仓库
3. 按发布流程灰度发布到现⽹
这⼀步⽬前还是纯⼈⼯操作 —— 合⼊和发布涉及灰度策略和线上风险，暂时不打算交给  AI 。
效果：从⼀句⼝述需求开始，到代码合⼊主⼲触发⾃动发布，整个流程的核⼼⼯作都在⼀个终
端会话⾥完成了。
开发这个需求，消耗的  token 情况如下：
总结
全流程回顾
回到开头那张概览表，这⾥补充⼀下各阶段的实际耗时：
阶段 耗时 ⼈⼯操作
①  需求创建  + 分⽀初始化 ⾃动 ⼝述需求
②  需求澄清（ brainstorming ） ~5 min 回答  2-3 个问题
[!info] 使⽤的⼯具  CI/CD 流⽔线  — DevOps 平台⾃动构建与发布
````

## PDF 第 22 页

[原页](RAW.pdf#page=22)

````text
阶段 耗时 ⼈⼯操作
③  制定实施计划 ~3 min 审核确认
④  并⾏开发（ 4 个  Task ） ~10 min ⼏乎⽆需⼲预
⑤  代码⾃审 ~2 min 审核报告
⑥  编译部署 ~3 min 确认部署参数
⑦  ⽇志排查 按需 ⼿动触发测试
⑧  创建  MR ~2 min 确认  MR 信息
⑨  AI 辅助评审 ~3 min 审核  AI 评审意见，决定提交哪些
⑩  修复评审意见（ 2 条） ~3 min 确认修复⽅案
整个流程⾛下来，开发者的⼯作⽅式发⽣了⽐较⼤的变化：
传统⽅式 Claude Code ⽅式
打开  PM 页⾯创建需求，⼿动建分⽀⼝述需求，⾃动创建需求单和分⽀
⾃⼰拆解任务、逐个实现 AI 制定计划、⼦  Agent 并⾏执⾏、⾃动  commit
⼿动  dtools 部署，排查实例名过期AI ⾃动检测过期配置并修正
⼿动写  MR 描述，对照  commit 逐条整理 AI 分析全部  commit ⾃动⽣成规范描述
在 GitPlatform 页⾯逐条看评审、⼿动改代码AI 拉取评论、定位代码、⽣成修复、⾃动提交
说到底，这就是  Agentic Engineering 的核⼼理念 —— ⼈是编排者（ Orchestrator ）， AI 是⾃
主执⾏者：
⼈负责：定义⽬标、拆解任务、审核⽅案、把关质量、最终决策 —— ⽅案选择、计划审
核、部署确认、评审把关、合⼊发布
AI 负责：在结构化流程中⾃主执⾏ —— 代码⽣成、 commit 格式化、 MR 描述整理、评审
意见定位、⽇志分析 …… 这些重复性⾼、规则明确的⼯作
Skill/Command 体系就是那个 " 结构化流程 "——brainstorming 确保先理解再动⼿， writing-
plans 确保先计划再执⾏， code-review 确保有检查清单⽽⾮凭感觉审查。它们把  AI 的能⼒约
束在可控的⼯程框架⾥，⽽不是让  AI ⾃由发挥然后祈祷结果正确。
这和  Vibe Coding 的本质区别在于： Vibe Coding 依赖运⽓， Agentic Engineering 依赖流程。
每个关键节点都有⼈⼯审核， AI 是⾼效的执⾏者，不是不受控的⾃动机。
Skill & Command 的协作架构
理解了全流程之后，来看看这套⼯具链内部是怎么协作的。整个体系可以⽤⼀张依赖图表达：
````

## PDF 第 23 页

[原页](RAW.pdf#page=23)

````text
⼏个设计上的关键决策：
Command 是薄壳：每个   /xxx  命令只有⼀⾏ —— 委托给   git-workflow  对应模块执⾏。
所以你在对话中说 " 帮我提交代码 " 也能触发  commit 流程，不⼀定⾮得打   /commit。
Skill 之间可组合：pm-dev 创建完需求单后⾃动调⽤   brainstorming， brainstorming 完了
接着调   writing-plans。git-workflow 的每个模块都复⽤   git-context  做前置准备。组合优
于重复实现。
Superpowers 管纪律： brainstorming 确保  AI 先理解再动⼿； writing-plans 确保先计划
再执⾏； executing-plans 确保按步骤推进⽽不跳跃。这些不是 " 可选的好习惯 " ，⽽是写进
Skill 定义的强制流程。
MCP 对⽤户透明：你不需要知道 " 调⽤ GitPlatform API 创建  MR" 这件事 ——Skill 通过
MCP ⾃动完成，你只看到 "MR 已创建，链接是  xxx" 。
附录
本⽂涉及的⼯具速查
⼯具 类型 对应阶段⼀句话说明
pm-dev Skill ①  需求获
取
解析  PM URL 或⾃动创建需求单，初始化开
发分⽀
brainstormingSuperpower
s
②  需求澄
清 交互式需求探索，先理解再动⼿
writing-plansSuperpower
s
③  制定计
划 深⼊代码⽣成精确的多  Task 实施计划
executing-plansSuperpower
s
④  并⾏开
发 按步骤执⾏计划，⽀持⼦  Agent 并⾏
/commit Command ④  并⾏开
发
智能⽣成  Conventional Commits 格式的  com
mit
code-review Skill ⑤  代码⾃
审 Golang 审查， 4 级严重度  × 8 类标签
dtools Skill ⑥  编译部
署 DevOps 平台  CLI ，⾃动探测参数并交叉编译
````

## PDF 第 24 页

[原页](RAW.pdf#page=24)

````text
⼯具 类型 对应阶段⼀句话说明
galileo-log-que
ry Skill ⑦  ⽇志排
查 Galileo ⽇志查询，⽀持多条件过滤
/create-mr Command ⑧  创建  MR 分析  commit ⾃动⽣成  MR 标题 / 描述
/review-mr Command ⑨  AI 评审 ⾏级代码评审，精确提交评论到 GitPlatform
/fix-mr Command ⑩  修复意
见 拉取未解决评论，逐条修复并回复
git-context Skill ⑧⑨⑩ GitPlatform 项⽬上下⽂提取，被多个⼯具复⽤
AI 代码评审案例
拿⼀个⽐本⽂⽰例更复杂的  MR （ 4 个⽂件， +252 ⾏）来看， AI 审查出了  9 个问题：
级别 数量 典型问题
Critical 1 HTTP 下载⽆超时控制， goroutine 可能永久阻塞
Major 4 竞态窗⼝、重复读配置、缺少  HTTP 状态码
Minor 2 错误封装不规范、不必要的导出字段
Suggestion 2 切⽚预分配、 handler ⽂件拆分
reviewer 审阅后调整了  AI 的部分建议（如将  C1 改为 " 建议使⽤  trpc-go http client 代替
net/http" ），然后提交了  7 条评论到 GitPlatform 。
MCP 服务配置
以下  MCP 服务为  Skill 提供外部平台的数据和操作能⼒，配置⼀次全局⽣效：
MCP 服务 ⽤途 依赖的  Skill
GitPlatform MCP Git 仓库操作、 MR 管理 git-workflow
、git-context
PM MCP 需求 / 缺陷 / 任务管理 pm-dev
、git-workflow
InternalWiki MCP Wiki ⽂档搜索与管理wiki-doc
Galileo MCP ⽇志查询与分析 galileo-log-query
KnowledgeBase MCP 知识库语义 + 关键词检索brainstorming 阶段补充技术背景
具体的  MCP 配置命令和  Token 获取⽅式，见配置仓库。
配置⽬录结构
完整的  Skill/Command/Plugin 列表和配置说明，见配置仓库。
````

## PDF 第 25 页

[原页](RAW.pdf#page=25)

````text
阅读 1 . 8 万
~/.claude-internal/              # Claude Code 全局配置⽬录
├── CLAUDE.md                    # 全局指令（操作原则、代码规范、偏好设置）
├── settings.json                # 权限⽩名单、模型选择、启⽤插件
├── commands/                    # ⾃定义斜杠命令（ /commit, /create-mr, /review-mr, /fix-mr 
└── skills/                      # 技能库（ pm-dev, git-workflow, code-review, dtools 等）
完整的  Skill/Command/Plugin 列表、官⽅插件配置、⽬录详情，均见配置仓库。
腾讯技术官⽅号。腾讯技术创新、前沿领域发布解读平台。
688 篇原创内容
腾讯技术⼯程
公众号
留⾔
还没有留⾔，来写⾸评
写留⾔
````

## PDF 第 26 页

[原页](RAW.pdf#page=26)

````text
````

