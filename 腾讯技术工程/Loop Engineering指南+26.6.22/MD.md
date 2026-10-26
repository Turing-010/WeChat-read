# 原文逐页转写

文本来自本次 PDF 文本层；不补写图片、截断内容或代码。图片和布局请打开每页 PDF 链接核对。AI 解释另见学习笔记。

## PDF 第 1 页

[原页](RAW.pdf#page=1)

````text
Loop  Engineering  实践指南：在 Code  Buddy  中构建⾃主循环系统
腾讯程序员 2026 年 6 ⽉ 22 ⽇ 02 : 22⼴东原创 腾讯技术⼯程 717 ⼈
作者：eliqiao
⼀、什么是 Loop  Engineering
Loop  Engineering  是由⾕歌⼯程师 Addy  Osmani  提出的 AI  编程新范式。其核⼼理念是：围绕
⼤模型构建⾃主循环运⾏系统，使 AI  从单次响应⼯具升级为⻓期⾃治代理。
在传统的 AI  辅助开发中，开发者与 AI  的交互模式是"⼀问⼀答"——你发⼀条指令， AI  回复⼀
次，然后等待下⼀条指令。这种模式的瓶颈在于：⼈成了循环的瓶颈。每⼀步都需要⼈类介
⼊， AI  ⽆法⾃主推进复杂⼯作流。
Loop  Engineering  的解法是：让⼈从循环内部的操作者，转变为循环之上的监督者和⽬标设定
者。 你定义"做什么"和"何时算完成"， AI  ⾃⼰决定"怎么做"和"下⼀步是什么"，直到⽬标达成
或确认不可达。
类⽐传统⼯程学中的 PDCA 循环（ Plan - Do - Check - Act ），在 Loop  Engineering  中：
模型是执⾏者
Loop是控制中枢
规则框架是边界约束
这三者组合，让 AI  在可控范围内⾃主推进复杂⼯作流。
为什么现在重要
当模型能⼒⾜够强时，循环设计成为决定 AI  ⾃主性与可靠性的关键瓶颈。⼀个设计良好的循
环可以让 AI  连续⼯作数⼗轮完成复杂重构，⽽⼀个设计糟糕的循环可能在第三轮就失控。
Loop  Engineering  被视为继 Prompt  Engineering 、 Context  & Harness  Engineering  之后的" AI
编程第三次⾰命"——开发者⻆⾊从"提示词⼯程师"彻底升级为" AI  系统架构师"。
⼆、 Loop  Engineering  与 ReAct 的区别
````

## PDF 第 2 页

[原页](RAW.pdf#page=2)

````text
ReAct （ Reasoning  + Acting ）是⽬前最主流的 AI  Agent  交互范式，由 Yao  et  al . 在 2022  年
提出。其核⼼模式是：思考 →  ⾏动 →  观察 →  思考 →  ⾏动 →  观察…… 交替进⾏推理和⼯具
调⽤，直到任务完成。
Loop  Engineering  与 ReAct  经常被放在⼀起讨论，但它们解决的是不同层次的问题。理解两者
的区别，是正确实践 Loop  Engineering  的前提。
本质关系： Inner  Loop  vs  Outer  Loop
ReAct  是 Loop  Engineering  的 Inner  Loop 。
Loop Engineering （ Outer Loop ）
┌─────────────────────────────────────────────────────┐
│   ⽬标拆解  → 任务分配  → 结果汇总  → 再计划               │
│                                                       │
│  ┌─────────────────────────────────────────────────┐ │
│  │  ReAct （ Inner Loop ）                              │ │
│  │   思考  → ⾏动  → 观察  → 思考  → ⾏动  → 观察  ...     │ │
│  └─────────────────────────────────────────────────┘ │
│                                                       │
│  ┌─────────────────────────────────────────────────┐ │
│  │  ReAct （ Inner Loop ）                              │ │
│  │   思考  → ⾏动  → 观察  → 思考  → ⾏动  → 观察  ...     │ │
│  └─────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────┘
ReAct  解决的是单次任务内"怎么⼀步步做"的问题
Loop  Engineering  解决的是跨任务"做什么、谁来做、何时停、怎么续"的问题
核⼼差异对⽐
维度 ReAct Loop  Engineering
关注层次 单次任务的执⾏过程 跨任务的编排与调度
循环粒度 细粒度（单步⼯具调⽤） 粗粒度（整个任务周期）
状态管理 依赖上下⽂窗⼝内记忆 状态外置到⽂件/数据库，每次迭代全新上下⽂
停⽌条件 模型⾃⼰判断"做完了" 独⽴评估器验证可度量条件是否满⾜
验证机制 ⾃我检查（同⼀模型） 对抗验证（不同模型/独⽴评估器）
错误恢复 在同⼀上下⽂内重试 断点续跑，可跨会话恢复
并⾏能⼒ 单 Agent  串⾏ 多 Agent  并⾏ + ⼯作树隔离
运⾏周期 单次对话 可持续数⼩时甚⾄数天
⽤⼀个类⽐理解
把开发⼀个软件⽐作建⼀栋楼：
````

## PDF 第 3 页

[原页](RAW.pdf#page=3)

````text
ReAct 是⼯⼈的⼯作⽅式——"我需要砌这⾯墙，先搬砖，再和⽔泥，再砌，检查是否平
整，不平就修"。它关注的是单步操作的执⾏质量。
Loop  Engineering 是项⽬经理的⼯作⽅式——"今天完成地基，明天搭框架，后天装管
道，质检通过再进⾏下⼀步，不合格就返⼯"。它关注的是整体⼯程进度的编排与质量保
障。
没有⼯⼈的砌墙能⼒（ ReAct ），楼建不起来；没有项⽬经理的编排（ Loop  Engineering ），⼯
⼈可能把墙砌错了地⽅，或者砌完才发现管道没留⼝。
ReAct  的局限， Loop  Engineering  如何补位
局限 1 ：上下⽂窗⼝有限，⻓任务必然遗忘
ReAct  在同⼀个上下⽂窗⼝内持续推理。当任务跨越⼏⼗步操作时，早期信息被压缩或遗忘，
导致 AI  "忘记"之前做了什么、为什么这么做。
Loop  Engineering  的解法：状态外置。每轮迭代从全新上下⽂开始，从持久化⽂件中读取状
态，不依赖模型记忆。CodeBuddy 中的 Memory 、 CODEBUDDY . md 、 Rules  就是这⼀原则
的体现。
局限 2 ：⾃我检查存在盲区
ReAct  中同⼀个模型既写代码⼜检查代码，容易产⽣确认偏误——"我写的当然没问题"。
Loop  Engineering  的解法：对抗验证。执⾏者和评估者使⽤不同模型或指令。 CodeBuddy
中 /goal 的评估器⽤⼩模型独⽴判断， Team  模式中 planner / coder / reviewer  使⽤不同⻆
⾊，都是对抗验证的实践。
局限 3 ：没有跨任务的进度跟踪
ReAct  完成⼀个任务就结束，没有"做到哪了"的持久记录。如果中途崩溃，只能从头来。
Loop  Engineering  的解法：断点续跑。通过状态⽂件记录进度，崩溃后可从断点恢复。
CodeBuddy  中 /goal ⽀持 --resume 恢复未完成的 goal ， Memory  记录跨会话上下⽂。
局限 4 ：缺少编排能⼒
ReAct  是单 Agent  串⾏执⾏，⽆法同时推进多个⼦任务。
Loop  Engineering  的解法：多 Agent  并⾏ + ⼯作树隔离。 CodeBuddy  的 Team  模式⽀持多
个 Agent  同时⼯作在不同分⽀上，互不⼲扰，最后合并结果。
不是替代，是演进
Loop  Engineering  不是要替代 ReAct ，⽽是在 ReAct  之上增加编排层。两者关系：
````

## PDF 第 4 页

[原页](RAW.pdf#page=4)

````text
Prompt Engineering    → 怎么问（单次交互优化）
  ↓
ReAct                → 怎么做（单任务内的推理 - ⾏动循环）
  ↓
Loop Engineering     → 怎么管（跨任务的编排、验证、状态管理）
在 CodeBuddy  中，当你⽤ /goal 设置⼀个条件时，每⼀轮内部 AI  仍然使⽤ ReAct  模式来
思考和⾏动，但 /goal 的评估器在 Outer  Loop  层⾯判断整体进度——这就是两层循环的协
作。
三、 Loop  Engineering  的核⼼架构
五阶段循环机制
Loop  Engineering  遵循 Discover  →  Plan  →  Execute  →  Verify  →  Iterate 闭环：
阶段 说明 关键设计
Discove
r ⾃动读取 CI  失败、 issue 、代码审查等信号 输⼊源要结构化、可订阅
Plan 分解⽬标为具体步骤 温度适中，避免过早收敛
Execute执⾏代码编辑与⼯具调⽤ ⼯具调⽤要幂等、可回滚
Verify 通过测试、 lint 、类型检查等客观信号验证 验证标准必须客观、可机器
判定
Iterate 失败则⾃动修复并重新循环；成功则进⼊下
⼀任务
状态要持久化，⽀持断点续
跑
双层循环模型
Loop  Engineering  采⽤双层循环架构：
Outer Loop （编排层）
  ⽬标拆解  → 任务分配  → 结果汇总  → 再计划
  Inner Loop （执⾏层）
    感知  → 推理  → 规划  → ⾏动  → 观察
      ↑                         ↓
      评估  / 修正  ← ───────────┘
Inner  Loop = 单个 Agent  的⼯作循环（等价于 ReAct  模式）
Outer  Loop = 编排器管理多个 Inner  Loop  的⽣命周期
六要素构建体系
````

## PDF 第 5 页

[原页](RAW.pdf#page=5)

````text
要素 作⽤ 为什么重要
⾃动化 提供循环⼼跳，按计划或事件触发 没有⼼跳就没有循环
⼯作树 通过 git  为每个 Agent  创建独⽴⼯
作⽬录 并⾏开发零冲突
技能（ SKILL . m
d ）
固化项⽬知识，避免每次冷启动重
新推导 知识复⽤，降低 token  消耗
连接器（ MCP ） 打通 issue  系统、 CI  等真实⼯具链 AI  必须能感知和操作真实世
界
⼦智能体 将写代码与检查代码分离，形成对
抗验证
避免单⼀ Agent  ⾃我检查的
盲区
状态⽂件 记录进度，⽀撑断点续跑 防⽌上下⽂遗忘和信息漂移
状态外置哲学
Loop  Engineering  的⼀个关键设计原则：所有状态存储在外部系统，⽽⾮模型的上下⽂窗
⼝。 每次循环迭代从⼀个全新的上下⽂窗⼝开始，基于实际持久化内容⼯作。这彻底解决了模
型遗忘、信息漂移与上下⽂压缩问题。
四、 CodeBuddy  中的 Loop  Engineering  实现
CodeBuddy  提供了三种核⼼机制来实现 Loop  Engineering ，它们分别对应不同的循环驱动模
式：
3 . 1  /goal — 条件驱动的持续⼯作
/goal 是 Loop  Engineering  最直接的实现。你设置⼀个可验证的完成条件， CodeBuddy  跨
多轮⾃动⼯作，直到条件满⾜。
# 基本语法
/goal < 完成条件 >
# 实际示例
/goal all tests in test/auth pass and the lint step is clean
# 加兜底上限防⽌⽆限循环
/goal all tests pass or stop after 20 turns
# ⾮交互模式（ headless 运⾏）
codebuddy -p "/goal CHANGELOG.md has an entry for every PR merged this week"
写好条件的三个关键要素：
````

## PDF 第 6 页

[原页](RAW.pdf#page=6)

````text
要素 说明 示例
可度量的终态 测试结果、构建退出码、⽂件
数等
all tests in test/auth pas
s
可证明⽅式 明确怎么验证 `npm test` exits 0
 或 `git status` is clean
不可破坏的约
束 过程中不能改的东⻄ no other test file is modi
fied
评估机制：每轮结束后，由独⽴⼩模型评估器判断条件是否满⾜，三态结果：
✅  ok: true — 条件已满⾜，清除 goal ， UI  显示 ✔  Goal achieved
🔄  ok: false — 条件未满⾜， reason  注⼊ history ，继续下⼀轮
❌  ok: false, impossible: true — ⽬标不可达，⽴即清除 goal
关键设计：评估器使⽤⼩模型（如 gemini - 2 . 5 - flash ），快速且便宜，只看 transcript  不调⽤
⼯具。评估器与执⾏ Agent  使⽤不同模型，天然形成对抗验证。
3 . 2  /loop — 时间驱动的循环任务
/loop 按时间间隔重复执⾏指令，适合监控、巡检等持续性场景：
# 语法
/loop [ 时间间隔 ] < 指令 >
# 检查  CI/CD 流⽔线状态
/loop 3m 检查⼀下流⽔线是否跑完，把结果告诉我
# 定时运⾏单元测试
/loop 30m 帮我运⾏⼀次单元测试，如果有失败的⽤例告诉我
# 每⼩时汇总代码审查待办
/loop 1h 看⼀下有没有新的  PR 需要我审查
特性 说明
最⼩间隔 1  分钟
每会话上限 50  个任务
⾃动过期 3  天后⾃动清除
⽣命周期 会话级，退出后消失
执⾏时机 只在会话空闲时触发
3 . 3  Automations  — 跨会话的定时任务
````

## PDF 第 7 页

[原页](RAW.pdf#page=7)

````text
Automations  是持久化的定时任务，不随会话消失，适合需要⻓期运⾏的监控场景：
Recurring：按 cron  规则重复执⾏，如 FREQ=HOURLY;INTERVAL=1
Once：指定时间点⼀次性触发
三种⽅式的对⽐
⽅式 下⼀轮何时开始 何时停⽌ 适⽤场景
/goal 上⼀轮结束后⽴即 评估器确认条件满⾜ 有明确终态的实质性⼯作
/loop 时间间隔触发 主动停或模型判定结束 监控、巡检、定期检查
Automations 按 cron  规则 永久或设有效期 跨会话的⻓期监控
五、 Loop  Engineering  架构在 CodeBuddy  中的映射
Loop  Engineering
要素 CodeBuddy  实现 说明
⾃动化（循环⼼跳） /goal
、/loop、 Automations 三种驱动模式覆盖不同场景
⼯作树（并⾏隔离） Git  worktree  + Team  模式 多 Agent  并⾏开发互不⼲扰
技能（ SKILL . md ） Skills  机制 固化项⽬知识，避免冷启动
连接器（ MCP ） MCP  协议 打通 issue 、 CI 、数据库等⼯
具链
⼦智能体（对抗验
证） Task  ⼯具 + Team  模式 规划者/执⾏者/评审者三⻆
分⼯
状态⽂件 Memory 、 CODEBUDDY . md 、
Rules 跨会话知识持久化
六、实践案例
实践 1 ：使⽤ /goal 完成模块迁移
场景：将⼀个旧认证模块从 auth/legacy 迁移到新 API ，直到所有调⽤点都能编译且测试通
过。
/goal all tests in test/auth pass, `npm run build` exits 0, no file in auth/legacy is 
为什么这样写条件：
1 . all tests in test/auth pass — 可度量的终态，确保功能不受损
````

## PDF 第 8 页

[原页](RAW.pdf#page=8)

````text
2 . `npm run build` exits 0 — 可证明⽅式，确保编译通过
3 . no file in auth/legacy is imported anywhere — 不可破坏的约束，确保旧代码完全
移除
4 . or stop after 30 turns — 兜底上限，防⽌⽆限循环
CodeBuddy  的⾃动循环过程：
1 . Discover：扫描 auth/legacy ⽬录，识别所有导出和调⽤点
2 . Plan：列出需要修改的⽂件，制定迁移步骤
3 . Execute：逐个⽂件修改导⼊路径，更新调⽤⽅式
4 . Verify：运⾏ npm test 和 npm run build，检查编译和测试结果
5 . Iterate：如果测试失败，分析错误原因，修复后重新运⾏
每轮结束后，评估器独⽴判断："所有 auth  测试通过了吗？构建成功了吗？旧⽂件还有被引⽤
吗？"——只有三个条件全部满⾜才宣告完成。
实践 2 ：使⽤ /loop 实现 CI  监控与⾃动修复
场景：在提交 PR  后，持续监控 CI  状态，如果失败则尝试⾃动修复。
/loop 2m 检查当前分⽀的  CI 状态，如果失败了，查看失败⽇志并尝试修复，修好后提交
这个循环的⼯作流：
每  2 分钟触发
  → 读取  CI 状态
  → 如果通过  → 报告成功
  → 如果失败  → 读取错误⽇志  → 分析原因  → 修改代码  → 提交  → 等待下⼀轮验证
注意：/loop 是时间驱动的，不会⾃动停⽌。当你确认 CI  通过后，需要⼿动取消：
取消  CI 监控的定时任务
实践 3 ：使⽤ Team  模式实现对抗验证
场景：复杂重构任务，需要规划者、执⾏者、评审者三⻆分⼯。
1. 创建  Team
2. ⽣成  "planner"：负责分析代码库、制定重构⽅案
3. ⽣成  "coder"：根据⽅案执⾏代码修改
4. ⽣成  "reviewer"：独⽴审查修改结果，确保质量
5. planner 和  reviewer 使⽤不同模型 / 指令，形成对抗验证
````

## PDF 第 9 页

[原页](RAW.pdf#page=9)

````text
为什么对抗验证重要：单⼀ Agent  ⾃⼰检查⾃⼰的代码，容易产⽣盲区——"我写的代码当然
没问题"。规划者和评审者使⽤不同的视⻆和指令，能发现执⾏者忽略的问题。
实践 4 ：使⽤ Skills  固化项⽬知识
场景：团队有⼀套编码规范和架构约定，希望 AI  每次都能遵循。
在 skills/ ⽬录下创建 skill.md，将项⽬知识固化：
---
name: project-conventions
description: 项⽬编码规范和架构约定
---
## 架构约定
- 所有  API 调⽤必须经过  service 层， controller 不直接调⽤  repository
- 数据库查询必须使⽤参数绑定，禁⽌字符串拼接  SQL
- 错误处理遵循统⼀异常体系 ...
## 命名规范
- Service 类以  Service 结尾
- Repository 类以  Repository 结尾
...
效果：每次 AI  ⼯作时⾃动加载这些约定，不需要你在每次对话中重复说明。这正是 Loop
Engineering  中"技能"要素的体现——避免每次冷启动重新推导。
实践 5 ：使⽤ MCP  连接器打通⼯具链
场景：让 AI  能读取 Jira  issue 、触发 Jenkins  构建、查询数据库。
通过 MCP  协议接⼊第三⽅⼯具：
{
  "mcpServers": {
    "jira": {
      "command": "mcp-jira",
      "args": ["--project", "MYPROJ"]
    },
    "jenkins": {
      "command": "mcp-jenkins",
      "args": ["--url", "https://ci.example.com"]
    }
  }
}
````

## PDF 第 10 页

[原页](RAW.pdf#page=10)

````text
接⼊后，在 /goal 循环中 AI  可以：
/goal all issues labeled "bug" in current sprint have a corresponding test that passes
AI  能直接读取 Jira  issue  列表、编写测试、运⾏验证——整个 Discover  →  Plan  →  Execute  →
Verify  →  Iterate  闭环都在真实⼯具链中运⾏。
实践 6 ：使⽤ Rules  和 Memory  实现状态外置
场景：⻓期运⾏的重构任务，需要跨会话保持上下⽂。
Rules（.codebuddy/rules）：定义硬性约束， AI  每次启动都会读取：
- 所有数据库查询必须使⽤参数绑定
- 修改  API 接⼝必须同步更新  OpenAPI ⽂档
- 每个  PR 不超过  300 ⾏变更
Memory：记录跨会话的偏好和上下⽂：
- ⽤户偏好使⽤  pytest ⽽⾮  unittest
- 当前项⽬使⽤  Python 3.11 ，类型注解必须完整
- ⽤户上次重构到  step 3 ，下次继续从  step 4 开始
效果：每次新的循环迭代从全新的上下⽂窗⼝开始时， Rules  和 Memory  提供了"状态外
置"——关键信息不依赖模型的记忆，⽽是从持久化存储中读取。这正是 Loop  Engineering  "状
态外置哲学"的体现。
七、最佳实践与注意事项
写好 /goal 条件的 checklist
1 . 终态可度量：⽤"测试通过""构建成功""⽂件数为 0 "这类客观指标，避免"代码质量提升"这
类主观判断
2 . 验证⽅式明确：指定⽤什么命令/⼯具来验证，如 `pytest test/auth` exits 0
3 . 约束不可破坏：明确过程中不能改的东⻄，如"不修改其他模块的测试"
4 . 兜底上限：始终加 or stop after N turns，防⽌⽆限循环消耗 token
5 . 条件不超过 4000  字符：这是 /goal 的硬性限制
避免常⻅陷阱
````

## PDF 第 11 页

[原页](RAW.pdf#page=11)

````text
陷阱 说明 解法
验证责任不可转
移
⽆⼈值守的循环也是⽆⼈值守地犯
错
关键变更仍需⼈⼯审查， Loop
不代替 Code  Review
理解债务加速累
积
代码库真实状态与开发者理解之间
的鸿沟随循环加速扩⼤
定期 review  AI  的变更，保持对
代码库的理解
认知投降⻛险 开发者极易停⽌独⽴判断，系统给
什么就接受什么
把 AI  当协作者⽽⾮权威，质疑
每个变更
Token  成本约
束 循环运⾏消耗⼤量 token 设置 stop after N turn
s，⽤⼩模型评估器
条件模糊导致⽆
效循环
条件不够具体， AI  反复尝试但⽆
法满⾜
条件要写成" AI  ⾃⼰的输出能证
明"的形式
何时⽤哪种循环模式
有明确终态的实质性⼯作（迁移、重构、实现功能）
  → /goal
持续性监控和巡检（ CI 状态、 PR 审查、性能回归）
  → /loop
跨会话的⻓期定期任务（每⽇构建检查、每周代码审查汇总）
  → Automations
需要多⻆⾊协作的复杂任务（规划 + 执⾏ + 评审）
  → Team 模式  + /goal
⼋、总结
Loop  Engineering  的核⼼不是某个具体⼯具，⽽是⼀种系统设计思维：把 AI  当作循环中的执
⾏者，你设计循环的规则、验证标准和状态管理。 CodeBuddy  提供了完整的⼯具链来实现这
⼀范式：
/goal 是 Loop  的⼼跳——条件驱动，⾃动循环
/loop 是 Loop  的时钟——时间驱动，定期触发
Skills 是 Loop  的知识——固化经验，避免冷启动
MCP 是 Loop  的触⼿——连接真实⼯具链
Team  模式 是 Loop  的分身——对抗验证，多⻆⾊协作
Rules  + Memory 是 Loop  的记忆——状态外置，断点续跑
从"⼀问⼀答"到"设定⽬标、⾃动循环"，这是 AI  辅助开发从⼯具到伙伴的质变。⽽ Loop
Engineering  的实践者，正是这⼀质变的设计师。
````

## PDF 第 12 页

[原页](RAW.pdf#page=12)

````text
阅读 2 . 3 万
留⾔
还没有留⾔，来写⾸评
写留⾔
````

## 采集与转写核验记录（非原文）

以下说明由本次核验添加；上方逐页文本保持文本层原样，图片与布局以PDF为准。

- PDF物理页 7,8：模块迁移的 /goal 代码示例在PDF p.7跨页截断，p.8有条件释义；完整代码未恢复。
