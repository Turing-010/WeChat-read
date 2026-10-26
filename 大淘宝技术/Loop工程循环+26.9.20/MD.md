# Loop engineering：把 agent 放进工程循环：PDF文本转写

> 这是RAW.pdf的文本层转写，不是AI总结。页码为PDF物理页码；未恢复原版面、表格或代码缩进。文本框长行、缺图与未加载内容不能仅靠文字提取判定完整。

[原始PDF](RAW.pdf) · [外部AI总结](AI_Loop工程循环.md) · [来源与质量](META.json)

## PDF 第1页

[查看RAW.pdf第1页](RAW.pdf#page=1)

> 本页含2个PDF图像对象；图中内容未转写。文本层顺序、表格、代码缩进和视觉完整性待核对。

```text
Loop engineering：把 agent 放进⼯程循环
原创 会员技术团队 ⼤淘宝技术 2026年9⽉20⽇ 23:02 浙江 33⼈
本⽂探讨了“Loop engineering”这⼀理念，即⼯程师不再逐轮提示agent，⽽是设计包
含读取状态、判断任务、执⾏操作、验证结果、记录状态和判断停⽌条件的⾃动化循环系
统。⽂章详细拆解了⽀撑该系统的六⼤组件：负责唤醒的⾃动化机制、隔离并⾏的
worktrees、沉淀项⽬知识的skills、接⼊外部⼯具的插件、分离读写职责的⼦agent以及
确保状态持久化的记忆层。作者强调，loop engineering并⾮盲⽬追求全⾃动，⽽是通
过明确输⼊输出、严格权限分层与成本控制来保障⼯程可靠性。⼯程师的⻆⾊从单轮操作
者转变为循环机制的设计者与最终责任⼈，其核⼼价值在于利⽤可控的⾃动化杠杆加深对
系统的理解，⽽⾮单纯甩锅给AI以逃避责任。
摘要
最近，coding agent 圈⼦⾥有⼀句话传得很快：不要再只是提示 agent，要设计提示 agent
的 loop。
这句话容易被误读成⼀个新名词。其实它说的是⼀个⽼问题：当⼯具开始能⾃⼰读代码、改代
码、跑测试、开 PR 以后，⼯程师的⼯作重⼼会往哪⾥移？
过去的⽤法很直接。你写 prompt，agent 回答。你贴报错，agent 修改。你看 diff，继续追
问。⼈⼀直握着⽅向盘。
Loop engineering 处理的是另⼀层⼯作。你不再亲⾃推动每⼀轮，⽽是设计⼀个⼩系统，让
它按固定节奏发现任务、选择下⼀步、调⽤ agent、检查结果、记录状态，并决定是否继续。
⼈还在系统⾥，只是位置变了：从每⼀轮的操作者，变成循环机制的设计者和最后的责任⼈。
这个变化有⽤，但也很容易变成另⼀种⾃动化幻觉。
最近我看到在 HN 和 Reddit：有⼈在转 Addy 的⽂章，也有⼈直接问"loop engineering 是
不是⼜⼀个 buzzword"。这种怀疑不是坏事。loop engineering 如果只是给⾃动化换个名
字，确实没什么意思；只有当它把状态、验证、权限和停⽌条件都写进⼯程流程⾥，它才和普
通的"让 agent 多跑⼏轮"不⼀样。
```

## PDF 第2页

[查看RAW.pdf第2页](RAW.pdf#page=2)

> 本页含2个PDF图像对象；图中内容未转写。文本层顺序、表格、代码缩进和视觉完整性待核对。

```text
概念界定：先把 loop 说清楚
这⾥的 loop 不是 while true，也不是把⼀个 prompt 定时重放。
⼀个能⼯作的⼯程 loop ⾄少有六个动作：
1. 读取外部状态：CI、issue、PR、⽇志、⽤户反馈、代码 diff。
2. 判断下⼀步：哪些问题值得处理，哪些应该忽略，哪些需要⼈判断。
3. 执⾏任务：让 agent 查代码、改代码、写测试或更新⽂档。
4. 验证结果：运⾏测试、复现路径、浏览器检查、代码审查或安全扫描。
5. 写⼊状态：把结论、失败原因、已尝试⽅案和下⼀步写到对话之外。
6. 判断停⽌条件：继续、重试、换策略、升级给⼈，或者结束。
少了第 5 步，它只是⼀次会话。少了第 6 步，它就是烧 token 的定时器。
这也是为什么 Addy Osmani 在《Loop Engineering》[1]⾥把它放在 agent harness 之上。
Harness 解决的是⼀个 agent 在什么环境⾥运⾏；loop 解决的是这些 agent 什么时候被唤
醒、拿什么上下⽂、做哪类事、由谁检查、状态放在哪⾥。
这⾥还要补⼀层。Birgitta Böckeler 在 Martin Fowler ⽹站上的《Harness engineering
for coding agent users》 [2] 把 harness 拆 成 两 类 控 制 ： 事 前 的 guides， 事 后 的
sensors。前者把规则、架构约束、技能⽂档和上下⽂喂给 agent；后者⽤测试、lint、⽇志、
浏览器、review agent 或安全扫描让 agent ⾃我修正。放到 loop ⾥看，harness 是控制
件，loop 是调度和闭环。只有调度，没有控制件，就是定时犯错；只有控制件，没有循环，就
还是⼀次性⼯具。
图 1. Harness engineering overview。来源：Harness engineering for coding agent users [3]。
更直⽩地说：prompt engineering 关⼼⼀句话怎么写。context engineering 关⼼给模型什
么材料。harness engineering 关⼼⼯具、权限和运⾏环境。loop engineering 关⼼这些东
```

## PDF 第3页

[查看RAW.pdf第3页](RAW.pdf#page=3)

> 本页含2个PDF图像对象；图中内容未转写。文本层顺序、表格、代码缩进和视觉完整性待核对。

```text
⻄如何持续运转。
研究背景与相关⼯作：
为什么现在讨论 loop
因为产品能⼒正在凑⻬。
Codex app ⽂档⾥已经能看到 automations、worktrees、skills、plugins、MCP、
subagents、memories，以及 Goal mode。
Claude Code 也在往同⼀类⼯作流靠近：scheduled tasks 、 /loop 、 goals、hooks、
skills、subagents、worktrees 和 MCP。名字不同，形状很接近。
这不表示两个⼯具完全等价。权限、持久化、审计和执⾏环境的差异会影响能不能放到⽣产流
程⾥。但从⼯程模式看，⼤家都在往同⼀个⽅向⾛：agent 不再只是聊天框⾥的代码助⼿，它
开始被放进持续运⾏的⼯程流程。
OpenAI Cookbook ⾥的 agent improvement loop 也在讲类似思路：真实 traces 是输⼊证
据，⼈⼯和模型反馈负责诊断，eval 变成可复⽤验收，handoff artifact 把下⼀轮要改什么写
下来，最后再交给 Codex 修改 agent 或 harness。它有价值的地⽅不在"让 AI 改 AI"，⽽在
于把反馈、验证、状态和权限边界接到同⼀个流程⾥。
Amplitude 的 Ralph loop 实验[4]更激进。它把产品数据、机会⽣成、浏览器验证和
coding agent 接在⼀起：每轮先构建下⼀个 opportunity，再⽤浏览器点通新功能，⽣成新
的机会队列。作者还让 agent 给⾃⼰产出的功能埋点，下⼀轮就能看到哪些路径被⽤过、哪⾥
卡住；每个 PR 附⼀个浏览器录制的 GIF，当作验证证据。到后期，他只允许少数低⻛险机会
类型⾃动合并，涉及⽤户数据的改动仍然保留⼈⼯判断。
图 2. Ralph Loop。来源：What I Learned Pointing a Ralph Loop at My Product for a Week[5]。
```

## PDF 第4页

[查看RAW.pdf第4页](RAW.pdf#page=4)

> 本页含1个PDF图像对象；图中内容未转写。文本层顺序、表格、代码缩进和视觉完整性待核对。

```text
最近的研究也在拆这个问题。论⽂《Engineering Robustness into Personal Agents with
the AI Workflow Store》[6]盯着 on-the-fly agent loop 的弱点：agent 临场合成计划、
临场串⼯具，速度很快，但很容易跳过软件⼯程⾥那些麻烦却必要的步骤，⽐如迭代设计、严
格测试、对抗评估和分阶段发布。它的答案不是让 agent 更会即兴发挥，⽽是把可靠流程沉淀
成可复⽤、受约束的 workflow。
另⼀篇《EurekAgent》[7]说得更像⼯程实践：权限、artifact 、预算和 human-in-the-
loop 不只是配套设施，它们会直接改变 agent 做事的⽅式。这两篇都不是在说"loop 越⾃动
越好"，⽽是在说 loop 要能复⽤、能审计、能限制。
这组案例说明，loop engineering 的重点不是⾃动化程度，⽽是控制⾯。你设计的是任务⼊
⼝、判断标准、权限边界、记忆⽅式、验证机制和停⽌条件。
系统构成：六个组件
▐ 4.1 Automations：⼼跳，不是⼤脑
Automation 负责把 loop 唤醒。
Codex 的 automations 可以按计划在项⽬上运⾏，结果进⼊ Triage inbox；如果没有发现，
也可以⾃动归档。它还能结合 skills，把重复任务变成可维护的⼯作流。Claude Code 的
scheduled tasks[8] 和 /loop 则 适合在⼀个 session 内反复检查某件事，⽐如部署是否完
成、PR 是否有新评论、CI 是否变绿。
Hooks[9] 处在另⼀个位置。它不是定时器，⽽是⽣命周期事件上的确定性控制。Claude
Code 的 hooks 可以在编辑后格式化代码，在⼯具调⽤前阻断敏感⽂件修改，在需要输⼊时发
通知，也可以把上下⽂重新注⼊会话。放在 loop ⾥看，hooks 更像护栏：它不决定做什么任
务，但能限制 agent 在执⾏过程中不能越过哪些边界。
这⾥最容易犯的错，是把 automation 当成智能本身。它只负责把任务按时唤醒，不负责替你
定义判断标准。
所以 automation prompt ⾥最好同时写 feedforward 和 feedback。Feedforward 是
agent 开始前必须知道的约束：只看哪个 PR、不能碰哪些⽬录、什么⻛险必须停。Feedback
是它做完后必须接受的传感器：跑哪个测试、看哪个⽇志、贴哪个浏览器录制、让哪个
reviewer 读 diff。没有 feedforward，agent 会到处试；没有 feedback，它会把"我觉得可
以"当成完成。
```

## PDF 第5页

[查看RAW.pdf第5页](RAW.pdf#page=5)

> 本页含1个PDF图像对象；图中内容未转写。文本层顺序、表格、代码缩进和视觉完整性待核对。

```text
图 3. Change lifecycle。来源：Harness engineering for coding agent users[10]。
⼀个好的 automation prompt 应该写得像操作规程，⽽不是愿望清单：
1 读取最近 24 ⼩时失败的 CI。
2 只处理和当前 PR 相关的失败。
3 如果失败来⾃依赖下载或外部服务超时，记录为 infra-flake，不改代码。
4 如果失败能稳定复现，创建最⼩修复。
5 每轮最多修改 3 个⽂件。
6 测试通过后写⼊ loop-state.md。
7 遇到权限、数据迁移或安全相关变更，停⽌并交给⼈。
坏的写法通常是这样：
1 每天帮我检查项⽬，有问题就修⼀下。
这种写法把判断权交给模型猜。
▐ 4.2 Worktrees：并⾏之前先隔离
多个 agent 同时⼯作时，第⼀类失败不是推理失败，⽽是⽂件冲突。
Git worktree 给每个任务⼀个独⽴ checkout。Codex app 的 worktree ⽀持 也是围绕这个
⽬标设计的：让多个线程在同⼀个 repo 上做独⽴任务，不⼲扰本地⼯作。Claude Code 也⽀
持⽤ worktrees 隔离并⾏ session。
```

## PDF 第6页

[查看RAW.pdf第6页](RAW.pdf#page=6)

> 本页含0个PDF图像对象；图中内容未转写。文本层顺序、表格、代码缩进和视觉完整性待核对。

```text
但 worktree 只解决机械冲突。它不解决 review 带宽。
如果你每天让 8 个 agent 各开⼀个 PR，但你只能认真读两个 diff，那系统吞吐没有提升，
只是把瓶颈从"写代码"挪到了"理解代码"。更糟的是，这种瓶颈不⼀定⻢上报错。PR 都很
⼩，测试也可能是绿的，但你的⼼智模型已经落后。
所以 worktree 的设计原则应该是：并⾏只⽤于低耦合任务，合并仍然按⼈的理解能⼒限流。
▐ 4.3 Skills：把项⽬知识写到系统外⾯
没有 skills 的 loop，每次醒来都像新来的同事。它要重新猜测试命令，重新理解⽬录结构，
重新发现团队不喜欢哪种写法。
Skill 的价值不是让 prompt 更漂亮，⽽是把稳定知识移出对话上下⽂。Codex 官⽅把 skill
定义为可复⽤⼯作流的编写格式，⼀ 个 SKILL.md 可 以带 scripts、references 和
assets。Claude Code 也采⽤相近的 skills 机制。
适合写进 skill 的内容包括：
如何运⾏单元测试、端到端测试、lint 和类型检查
哪些⽬录不能碰
哪些改动必须加迁移脚本
PR 描述必须包含什么
遇到 flaky test 如何分类
哪些历史事故不能重演
别把所有东⻄塞进⼀个⼤ skill。⼀个好 skill 应该⼩⽽明确， ⽐如 triage-ci 、 fix-flaky-tes
t 、 review-pr 、 frontend-qa 、 security-check 。 描述要直⽩，因为 agent 是根据描述决定
是否加载它的。
这⾥有个很实际的收益：skills 省的不只是 token，还有误判。项⽬约定没有写下来时，
agent 会⽤开源世界的常⻅模式补空⽩。你的项⽬越特殊，这种补空⽩越危险。
▐ 4.4 Plugins 和 connectors：让 loop 接触真实⼯具
只看⽂件系统的 loop 很快就不够⽤了。真实⼯程状态分散在 GitHub、Linear、Slack、
Sentry、数据库、staging API、浏览器和 CI 系统⾥。
这⾥要分清三层东⻄。MCP 是⼯具和上下⽂接⼊协议。Connector 是⾯向某个外部系统的具
体连接，⽐如 GitHub、Linear、Slack、Sentry 或 Figma。Plugin 是某些产品⾥的分发打包
机制，可以把 skills、app integrations、MCP servers、配置和素材⼀起交给团队安装。
plugin 只是分发和启⽤⼊⼝，不等于权限、审计和审批都已经设计好了。把这三层混在⼀起
写，会误导团队以为装了⼀个包就等于有了完整控制⾯。
```

## PDF 第7页

[查看RAW.pdf第7页](RAW.pdf#page=7)

> 本页含0个PDF图像对象；图中内容未转写。文本层顺序、表格、代码缩进和视觉完整性待核对。

```text
这⼀步会把 loop 从"给出建议"变成"参与流程"：
1 发现 CI 失败
2 读取失败⽇志
3 定位相关 commit
4 在 worktree ⾥修复
5 运⾏测试
6 打开 PR
7 关联 Linear ticket
8 通知 Slack
9 把结果写回状态⽂件
能⼒变强以后，权限设计也要跟着变严格。能读⽇志和能改⽣产数据库不是同⼀种权限。能开
PR 和能⾃动 merge 也不是同⼀种权限。
我的建议是按⻛险分层：
observe：只读，允许总结和分类。
propose：允许⽣成 patch 或 PR，但不允许合并。
act with approval：可执⾏外部动作，但关键步骤需要⼈批准。
autonomous：只给低⻛险、可回滚、验证强的任务。
⼤多数团队不应该⼀开始就追求 autonomous。先把 observe 和 propose 做扎实，收益已经
很明显。
▐ 4.5 Sub-agents：maker 和 checker 分开
loop ⾥有⼀条很实⽤的经验：写的⼈和查的⼈要分开。
写代码的 agent 不适合做唯⼀裁判。它刚刚花了⼏轮说服⾃⼰这条路线成⽴，很容易继续相信
⾃⼰的结果。Codex subagents ⽂档也提到，⼦ agent 适合把探索、测试和⽇志分析这类嘈
杂⼯作移出主线程，避免 context pollution 和 context rot。
⼀个稳妥的分⼯是：
explorer 只读代码，定位问题和相关⽂件。
implementer 做最⼩修改。
verifier 复现问题、跑测试、检查验收条件。
reviewer 读 diff，找边界条件、回归⻛险和过度修改。
security reviewer 只处理权限、数据暴露、注⼊、依赖和密钥⻛险。
```

## PDF 第8页

[查看RAW.pdf第8页](RAW.pdf#page=8)

> 本页含1个PDF图像对象；图中内容未转写。文本层顺序、表格、代码缩进和视觉完整性待核对。

```text
不是每个任务都需要五个 agent。sub-agents 会增加 token 成本，也会增加协调成本。它们
适合⽤在两类地⽅：检查环节，以及可以并⾏的读多写少任务。
如果任务很⼩，⼀个 implementer 加⼀个 verifier 通常够了。
▐ 4.6 Memory：状态必须在对话之外
⻓期 loop 不能靠聊天记录活着。
上下⽂会压缩，线程会中断，模型会忘，agent 还会重复尝试同⼀条死路。外部状态层不是锦
上添花，是 loop 能不能接着跑的前提。
Memory 可以很简单：
1 loop-state.md
⾥⾯记录：
当前⽬标
已处理事项
已尝试⽅案
失败原因
已通过验证
需要⼈⼯判断的问题
下⼀轮⼊⼝
它 也 可 以 是 Linear board 、 GitHub labels 、 数 据 库 表 、 PR comment 或 Codex
memories。Codex memories 适合保存稳定偏好、项⽬约定和常⻅坑点，但强约束最好仍然
放在 repo ⽂档 、 AGENTS.md 或 skill ⾥。原因很简单：团队规则应该可 review、可版本
化、可共享。
⼀句话：模型可以忘，系统状态不能忘。
⽅法示例：⼀个真实可⽤的 loop
从⼀个低⻛险 loop 开始，不要从"全⾃动⼯程团队"开始。
⽐如 CI triage loop：
```

## PDF 第9页

[查看RAW.pdf第9页](RAW.pdf#page=9)

> 本页含0个PDF图像对象；图中内容未转写。文本层顺序、表格、代码缩进和视觉完整性待核对。

```text
1 每天 9:00 运⾏。
2 读取过去 24 ⼩时失败的 CI。
3 按失败类型分类：真实回归、flaky、infra、未知。
4 只处理真实回归中影响当前 PR 的失败。
5 每次最多修⼀个问题。
6 必须先写复现步骤，再改代码。
7 修复后运⾏对应测试。
8 测试通过则开 PR 或更新当前 PR。
9 测试不通过则记录失败原因。
10 涉及迁移、安全、权限、账务、⽣产配置时停⽌。
这个 loop 不性感，但能落地。它的好处是边界清楚、输⼊稳定、输出可 review、失败可解
释。
再往前⼀步，可以做 review comment loop：
1 定期读取 PR 上未解决的 review comments。
2 把评论分成机械修改、需要判断、⽆法处理三类。
3 机械修改直接提交 patch。
4 需要判断的评论整理成问题列表。
5 ⽆法处理的评论说明原因。
6 每次修改后运⾏最⼩相关测试。
这类 loop ⽐"帮我优化项⽬"可靠，因为⽬标和判断都没有交给模型⾃由发挥。
还有⼀种 loop 值得单独拎出来：harness maintenance loop。
1 每周读取最近合并的 agent PR 和 review comments。
2 找出重复出现的失败模式：误改公共 API、漏跑迁移、测试只覆盖 happy path、过度重构。
3 能⽤确定性⼯具拦住的，优先补 lint、类型检查、架构规则或测试夹具。
4 只能靠语义判断的，更新 review skill 或 verifier prompt。
5 每次只改⼀个 harness 控制件。
6 记录这个控制件拦住了什么问题，以及有没有带来误报。
这个 loop 不直接交付功能，但它会让后⾯的功能 loop 更稳。很多团队会先迷上"让 agent
写更多代码"，但更该先问的是：怎样让 agent 少犯同⼀种错。
```

## PDF 第10页

[查看RAW.pdf第10页](RAW.pdf#page=10)

> 本页含2个PDF图像对象；图中内容未转写。文本层顺序、表格、代码缩进和视觉完整性待核对。

```text
⾃动化判定标准：
判断⼀个 loop 是否值得⾃动化
我会⽤五个条件筛选：
1. 输⼊是否稳定。CI、issue、review comments、⽇志都可以；模糊战略问题不适合。
2. 输出是否可 review。PR、报告、状态⽂件、ticket 更新可以；隐式修改不⾏。
3. 验证是否明确。测试、复现步骤、schema 校验、浏览器路径可以；"看起来更好"不够。
4. 权限是否可控。默认只读或提案，逐步放开执⾏权限。
5. 失败是否可恢复。失败最多产⽣⼀个待审 patch，⽽不是破坏共享环境。
现在我会再加⼀个条件：这个 loop 的产物能不能沉淀。⼀次性的 agent 对话失败了，最多留
下聊天记录；⼀个好的 loop 失败了，应该能留下更好的 fixture、更明确的 rule、更⼩的
skill、更稳的脚本，或者⼀条以后能复⽤的 workflow。否则你只是在反复购买同⼀份现场发
挥。
不满⾜这些条件时，不要急着⾃动化。先把流程写清楚。
⻛险分析：loop 的⼏个失败模式
▐ 7.1 ⽬标函数太粗
"提升质量"、"优化体验"、"让项⽬更好"都不是合格⽬标。agent 会把它们翻译成⾃⼰能做的
动作，⽐如重构、改⽂案、加测试、删重复代码。动作看起来合理，但未必解决你的问题。
⽬标要写成可验证条件：
1 让 checkout.spec.ts 中的 3 个失败⽤例通过，不能修改测试断⾔，不能改⽀付⽹关 mock
▐ 7.2 验证被 agent ⾃⼰吞掉
很多 agent 会在⽇志很⻓时总结成"测试通过⼤部分，只剩少量⽆关问题"。这句话在 loop ⾥
应该直接判失败。
验证结果必须结构化。⾄少要记录命令、退出码、失败⽤例和是否满⾜停⽌条件。
```

## PDF 第11页

[查看RAW.pdf第11页](RAW.pdf#page=11)

> 本页含1个PDF图像对象；图中内容未转写。文本层顺序、表格、代码缩进和视觉完整性待核对。

```text
▐ 7.3 状态⽂件没⼈读
写状态⽂件只是第⼀步。下⼀轮 prompt 必须显式要求先读状态⽂件，并根据状态决定是否继
续。否则它就是⼀份没⼈看的⽇报。
▐ 7.4 并⾏制造理解债
并⾏ agent 很容易让⼈产⽣"产能翻倍"的错觉。合并后的系统你是否还理解，才是更难回答的
问题。如果你没有读 diff，只是看 summary，这个债会积累得很快。
▐ 7.5 成本没有上限
Loop 的 token 成本不是账单问题，⽽是架构问题。没有上限的 loop 最后⼀定会被成本、噪
⾳或误操作叫停。
每个 loop 都应该有预算：
每轮最多⼏次尝试
每天最多开⼏个 PR
sub-agents 只能在哪些任务启⽤
多久没有进展必须停⽌
什么时候必须交给⼈
⼯程责任：⼯程师还剩什么
loop 不会取消⼯程师的责任。它只是把责任挪到了更不容易偷懒的位置。
⼯程师仍然要决定什么值得⾃动化，哪些权限可以放开，哪些状态必须落盘，哪些 diff 必须⼈
⼯读。停⽌条件也不能留给模型临场发挥。写不清停⽌条件的任务，通常也不该⽆⼈值守运
⾏。
这也是 loop engineering 和"甩给 AI"的区别。
甩给 AI 的⼈会写：
1 帮我把项⽬维护好。
```

## PDF 第12页

[查看RAW.pdf第12页](RAW.pdf#page=12)

> 本页含2个PDF图像对象；图中内容未转写。文本层顺序、表格、代码缩进和视觉完整性待核对。

```text
做 loop engineering 的⼈会写：
1 每个⼯作⽇上午检查当前 PR 的 CI。
2 只处理可稳定复现的测试失败。
3 先定位失败⽤例和相关 diff。
4 修改范围不得超过失败相关模块。
5 运⾏对应测试。
6 把命令、结果和下⼀步写⼊ loop-state.md。
7 如果连续两次失败原因相同，停⽌并交给我。
前者是在购买安慰感。后者才是在设计系统。
结论
Loop engineering 不是⼀个新包装的 prompt 技巧。它更接近⼯程流程设计：节奏、上下
⽂、⼯具、权限、验证、记忆、停⽌条件。
它可能成为 coding agent 的主要使⽤⽅式。原因不是 agent 已经可靠到可以⽆⼈管理，⽽
是单次对话不适合承载复杂⼯程⼯作。只要 agent 开始跨多轮处理真实任务，状态、反馈和责
任边界就绕不开。
直接提示 agent 仍然有⽤。很多任务就该在⼀轮对话⾥解决。不要为了显得先进，把所有事都
做成 loop。
对于重复发⽣、边界清楚、验证明确、⻛险可控的⼯程任务，loop 值得做。
最后可以⽤⼀个很朴素的标准验收：这个 loop 是让你更理解系统，还是让你更少读代码、更
少判断、更少承担责任。前者是杠杆，后者只是更快地⽋债。
附录
[1] 《Loop Engineering》 :
https://addyosmani.com/blog/loop-engineering/
[2] 《Harness engineering for coding agent users》 :
https://martinfowler.com/articles/harness-engineering.html
```

## PDF 第13页

[查看RAW.pdf第13页](RAW.pdf#page=13)

> 本页含2个PDF图像对象；图中内容未转写。文本层顺序、表格、代码缩进和视觉完整性待核对。

```text
[3] Harness engineering for coding agent users :
https://martinfowler.com/articles/harness-engineering.html
[4] Ralph loop 实验：
https://amplitude.com/blog/ralph-loop
[5] What I Learned Pointing a Ralph Loop at My Product for a Week :
https://amplitude.com/blog/ralph-loop
[6] 《Engineering Robustness into Personal Agents with the AI Workflow Store》:
https://arxiv.org/abs/2605.10907
[7] 《EurekAgent》:
https://arxiv.org/abs/2606.13662
[8] scheduled tasks :
https://code.claude.com/docs/en/scheduled-tasks
[9] Hooks :
https://code.claude.com/docs/en/hooks-guide
[10] Harness engineering for coding agent users
https://martinfowler.com/articles/harness-engineering.html
团队介绍
本⽂作者苏雄，来⾃淘天集团-会员技术团队。业务上，我们负责 88VIP、天猫积分、省钱
卡、⼤会员、消费券等淘宝核⼼业务，同时⽀撑淘宝、千问、闪购等阿⾥业务的账号互联互
通。技术上，我们深耕 AI 与业务融合，为消费者带来全新体验，为业务创造新增量。
¤ 拓展阅读 ¤
3DXR技术 | 终端技术 | ⾳视频技术
服务端技术 | 技术质量 | 数据算法
⼤淘宝技术
⼤淘宝技术官⽅账号
```

## PDF 第14页

[查看RAW.pdf第14页](RAW.pdf#page=14)

> 本页含0个PDF图像对象；图中内容未转写。文本层顺序、表格、代码缩进和视觉完整性待核对。

```text
964篇原创内容
公众号
阅读 5585
留⾔
写留⾔
还没有留⾔，来写⾸评
```

