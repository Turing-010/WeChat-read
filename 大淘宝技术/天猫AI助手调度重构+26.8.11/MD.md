# 天猫AI助手：调度框架重构与AI Coding工程化实践：PDF文本转写

> 这是原始PDF文本层转写，不是学习摘要。页码为PDF物理页序；图表、代码版面和图片文字不能完整表达在此文本层。已查看图像的内容和质量问题见AI学习笔记及META.json。

[原文PDF](RAW.pdf) · [AI学习笔记](AI_天猫AI助手调度重构.md) · [处理与质量记录](META.json)

## PDF 第1页

[查看原页](RAW.pdf#page=1)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
天猫AI助手：调度框架重构与AI Coding工程化实
践
原创
天猫技术团队 2026年8月11日 19:12 浙江
大淘宝技术 10人
天猫AI助手 团队通过“调度框架重构”与“AI Coding工程化”双轮驱动，在两周内将底层
架构从硬编码升级为基于Reducer/Event的三层调度模型，实现了状态写入收敛、可观
测性独立通道及业务接入效率的大幅提升；同时建立包含范式
、Skill、Hook 及观测报
告的AI工程化闭环，将单业务接入成本从3.5–4.5人天降
至约0.7人天，验证了将隐性知
识显式化为组织工程能力对于应对业务泛化迭代及穿越模型代际更迭的核心价值。
前情提要
我们旧瓶装新酒，对天猫AI助⼿的调度框架做了⼀次较彻底的改造，同时把团队的 AI Coding
从"个⼈⽤ Agent 写代码"升级为"组织化的⼯程能⼒"
。两条线交叉推进，最终达成⼏个可量化结
果：
业务承载⼒：从单⼀讲价流程，扩展到 5+ ScheduleBizType / 5+ ProcessTemplate 共存，新
增业务接⼊压平到 < 1 天；
状 态 写 复 杂 度 ： 21 处 散 点 query + CAS + retry 收 敛 到 2 个 Reducer + 25 个
Event，单 process 终态写库次数从 4 次降到 2 次；
可观测性：从⼀份 assistShared.log ，拆成 monitor / bizStat / error 三通道独⽴采
样、独⽴降级；
AI Coding ⼯程化：4 份范式 + 13 个 Skill + 8 个 Hook + ⽉度观测报告形成闭环，单业务
接⼊从 3.5–4.5 ⼈/天压到 ~0.7 ⼈/天。
本⽂不是论⽂，是⼀次复盘，重点想分享三件事：
1. 状态写收敛这件事到底怎么落、为什么收益是⾮线性的；
2. AI Coding 在团队层⾯到底应该做成什么样，我们⾛的路⼦和数据；
3. 中间踩过的坑，希望对其他团队有借鉴价值。
```

## PDF 第2页

[查看原页](RAW.pdf#page=2)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
背景：业务快速迭代与泛化探索的诉求
业务泛化探索对底层框架提出了两个直接诉求：
诉求 1：业务能"快速迭代"
。
⼀个新业务从⽴项到上线的周期，不能再是"先排⼏周框架对⻬、
再写业务逻辑"
。理想状态是业务⽅拿到清晰的接⼊范式后，专注写⾃⼰的业务节点，框架层⾯
的状态管理、调度推进、可观测性这些事，不应该让业务侧重新发明⼀遍。
诉求 2：框架能"承载多形态"
。 不同业务的核⼼节点形态差异很⼤，但底层共享调度、状态机、
可观测性、灰度等能⼒。框架需要"既⽀持已知形态，也不堵死未知形态"
。
回到调度框架⾃身的现状，原来的实现是节点链硬编码在 process/v1/ ，节点状态靠⼿写
if-else 推进。这种实现在单⼀场景下跑了⼀年多没问题，但放到泛化探索的语境⾥，⼏个结构性
约束就开始显现：
状态写⼊散点化：service 模块⾥能数出 21 处对 scheduleBO / processBO 的写⼊，
每处⾃带 query → mutate → CAS → retry 。每接⼀个业务就要复刻⼀遍这套模
板，且并发场景下不同组件之间的写⼊容易互相覆盖；
业务边界不清：新业务接⼊要么改 v1（侵⼊⽼逻辑、引⼊回归），要么 fork ⼀份（复制粘
贴、⻓期分裂），缺⼀个让"业务彼此物理隔离、共享底层框架"的中间层；
可观测性靠 grep：所有⽇志糊在⼀份 assistShared.log ⾥，⼤促降级只能"全开/全
关"
，SLS 聚合也聚不起来；
隐性知识⻔槛⾼：框架的约定散在⽼员⼯脑⼦⾥——什么时候⽤ CAS、状态怎么流转、节点
结束后谁负责推进——没⽂档、没⼯具、没拦截，新业务接⼊第⼀周基本在"读⽼代码 + 问
范式"
。
这些约束指向的不是"⽼代码不好"
，⽽是"⽼代码是为单⼀场景优化的，不适合泛化"
。要让业务
能快速迭代、让框架能承载多形态，调度框架本身必须做⼀次结构性升级。
与此同时，我们还押注了第⼆件事——把团队的 AI Coding 从"个⼈⽤ AI Coding"升级为"组织
化的⼯程能⼒"
。这两件事天然耦合：泛化框架需要把"约定"显式化、范式化，⽽范式恰好是
Skill 的素材；反过来，Skill 加速业务接⼊⼜能验证范式是否真的好⽤。两条线必须⼀起推。
下⾯分两条线讲清楚我们做了什么。
系
统
线：从硬编码节点链到三层调度
+
Reducer/Event收敛
▐ 3.1 整体演进
```

## PDF 第3页

[查看原页](RAW.pdf#page=3)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
不是⼀次性推倒重来，⽽是分阶段⾮破坏性演进：
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
v1 (历史) 硬编码节点链，仅讲价场景使用
│
▼
pro (过渡期) │
▼
抽象 ProcessNode / Executor / Builder / Syncer，按业务分
framework (本次) ┌─ DAG 层：依
赖/取消/级联收敛
├─ State 层：Reducer + 25 Event 写收敛
├─ Log 层：三通道 + Observer 横切
└─ Skill 体系：范式 + Hook + 观测
⽼的 v1 流程仍在跑，不强推迁移；pro 是过渡期产物，新业务⼀律⾛ framework。这是关键决
策——我们没有为了"架构⼲净"去强⾏重写 v1 ⽼代码，因为⽼代码⻛险⼤、收益低，留⼀份"考
古证据"反⽽⽐重写划算。
▐ 3.2 三层调度模型
整个调度被划分成清晰的三层：
1
2
3
4
5
6
7
Schedule 层 ─ dispatch / cancel / 终态聚合
│
│
├─ DAG 层 ─ 初始化、
后继推进、失败级联、
取消广播
└─ Process 层 ─ ReAct 循环、Node 调度、Syncer 钩子
│
└─ Node 层 ─ 原子动作，返回 NodeResult(CONTINUE/SUSPEND)
每⼀层都
有⾃⼰的状态机： ScheduleBizStatus → ProcessBizStatus → Proce
ssNodeStatus 。粒度由外到内递减。
这 种 分 层 最 ⼤ 的 好处 是 业 务 侧 只 关
⼼ Node 层 —— 节点 是 个 原⼦ 动 作 ，输
是 NodeResult(CONTINUE/SUSPEND) ，永远不需要操⼼ schedule 怎
⼊是 BO，输 出
么终结、DAG
怎
么传播取消、
状态怎
么⼊库。这些事情上层框架统⼀处理。
```

## PDF 第4页

[查看原页](RAW.pdf#page=4)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
▐ 3.3 写收敛：本次改造的"压舱⽯"
这块是改造的核⼼，也是收益最⼤的部分。
⽼问题：
21 处散点写⼊，每处都⻓这样：
1
2
3
4
5
6
7
8
9
// 老代码风格（散点 CAS）
ProcessBObo= processDaoService.query(processId);
if (bo.getStatus() != EXPECTED
_
FROM) return;
bo.setStatus(NEW
_
STATUS);
bo.setSomeField(...);
booleanok= processDaoService.updateByCas(bo, expectedFrom);
if (!ok) {
// retry...重新 query 一次再 CAS
}
这种写法的问题，并不是"写得不好"，而是它把三件本应分开的事情糅在一起：
1. 前置条件校验（precondition）；
2. 字段变更（m
utation）；
3. 并发
冲突处理（retry）。
业务侧每次写新组
（比
如多个组
件时，都要重复实现这套模板，且每次写法都略有
件并发改同一
行
），CAS 失败的 retry 策略很容易踩
不同。一旦
坑。
新设计：Redu
cer
+
Event。
借鉴了 Redux 的思路，但落到 Java
+ 数据库的语境下：
冲突场景复杂
1
2
// 新代码风格
scheduleReducer.dispatch(scheduleId, newMaybeAdvanceToTerminalEvent(...
业务侧只表
达"我希望发生 X"，至于 X 在什么条件下能发生、和数据库当前状态如何对账、
CAS 失败要不要重试——全
部由 Redu
cer 内部统一处理。
收益不是线性而是结构性的：
```

## PDF 第5页

[查看原页](RAW.pdf#page=5)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
特别说明一下"单 process 终态写库次数从 4 次降到 2 次"。在 N 个子任务并发推进的场景
下，这是 N 倍放大效应——一个含 10 个子任务的主任务，旧框架下终态聚合可能要 40 次
写，新框架下只要 20 次。
▐ 3.4 25 个 Event 是不是太多了？
第一次看到这个数字时，团队内部也讨论过：是不是过度设计？
我们的判断
大体可以分成几类：
是：Event 数不是越少越好，而是要"覆盖所有有
意义
的状态跃迁"。25 个 Event
生命周期类（Initial / Terminal）：每种实体的初始化、终态推进；
业务驱动类（NodeFinish / ProcessSuspend / ProcessResu
me）：业务节点产生的状
态变化；
DAG 协同类（DagAdvance / DagCancelBroadcast / ContextReconcile）：DAG 层依
/取消/对账；
赖
聚合类（MaybeAdvanceToTerminal / Su
mmarizeAndAdvance）：跨实体的状态汇总。
每个 Event 都对应一个明确的语义
。如果硬把语义
个 Event 里塞各种 if-else 判断模式，反过来污
不同的事件合并，业务侧用起来反而要在一
Redu
cer。
写 收 敛 的 本 质 是 把 " 如 何 写 " 和 " 为 什 么 写 " 分 离 ——Redu
写 " （ precondition/m
utation/retry ） ， Event 描 述 " 为 什 么写 " 。 这 层 分 离 让 process 两块状态从此再没出过 P0 级问题。
cer 管 " 如 何
schedule /
染
▐ 3.5 一些关键的技术取舍
挑几个对外可借鉴的：
```

## PDF 第6页

[查看原页](RAW.pdf#page=6)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
取舍 1：DAG 调度内置在 framework，没用外部调度引擎。原因：业务节点深度依
赖
inline
ReAct（节点内多轮
调用 AI 模型），外部调度引擎的"任务粒度"太粗，且会引入额外的中间件
依
赖
。代价是要自己维护调度逻辑，但收益是灵活、可控、链路短。
取舍 2：取消是"同步闭环"而非"异步广播"。端侧 cancel 用户是立即点的，体验上必须秒
回。我们让 cancel 复用 dispatch 锁，做同步 CANCELLING → CANCELLED 闭环。代价是
cancel 和正在执
行
的节点会有锁竞争，但在我们的场景下节点都是短任务，竞争窗口可控。
取舍 3：日志三通道独立 logger，而不是 MDC 区分。最初想用 MDC 区分日志类型（一个
logger，多个 MDC tag），但 Async appender 下 MDC 传递在跨线程时不可靠，且无法
做"通道级"降
级
。最后决定拆成 3 个独立 logger，配 8 个 SwitchCenter 开关覆盖通道总开
/ eventType / bizType / 采样率四个维度。
取舍 4：横切关注点用 O
bserver 而不是装
饰器嵌套。Redu
审计、
灰度判断等横切逻辑。用装
饰器嵌套层数会爆炸，用 O
cer 的写入路径上有指标埋点、
bserver 模式让 Spring 自动收
集，新增观察者零侵入。代价是 O
bserver 抛异常需要单独隔离不污
染主流程。
▐ 3.6 可观测性：让 oncall 有数据可看
三通道日志规约：
schedule
_
monitor.log ：高 频
行
dag.advance / compensation.scan）
为日 志 （ dispatch / execute / cas /
schedule
biz
_
_
stat.log ： 业 务 结 果日 志 （ schedule.terminated /
process.complete / process.suspend）
schedule
_
error.log ： ERR
R
O
{syncer,observer}.failed 等 7 类）
+
堆 栈 （ 含 redu
cer.apply.error / notifier.
字段做了白名单约束，eventType 做了字典约束。这两个约束保证 SLS 能直接 grou
指标，不再依
赖
grep。
p by 出
落到 SLS 看板的关键指标：
schedule 终态时延 P50/P95/P99（按 bizType）
redu
cer CAS 重试率 / exhausted 计数
单 process 写库次数（迁移前后对比）
process.suspend 比例
+
payload 类型分布
oncall 从"凭经验 grep"升级到"看
理范畴的前提。
大盘做决策"，这一步是把稳定性从 P0/P1 升级到 SLO 治
AI 线：从"用 Agent 写代码"到
```

## PDF 第7页

[查看原页](RAW.pdf#page=7)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
"团队 AI Coding 工程化"
▐ 4.1 我们对 AI Coding 三种水位的判断
AI Coding 在团队
里的成熟度，可以粗略分成五个水位：
大 部 分 团 队 卡 在 L1 / L2 ： 每个人都在用 Agent ， 但团 队 没有 沉 淀 。 组里
prompt 不会传给新员工，反模式踩过就忘，下次换个人继续踩
。
资
深
我们这次想做的事情是：把团队的 AI Coding 推到 L3，并在 L3 稳定后向 L4 过渡。
员工 写 的
▐ 4.2 工程化飞轮
整个体系
是一个有反馈回路的飞轮：
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
设计文档 design/ ──┐
│ 抽出
研发范式 paradigm/ ──┐
Skill 矩阵 (.agent/skills/) ──┐
│ 编码进
│ 触发
agent 执
行
──┐
│ Hook 监听
.agent/hooks/* + logs/ ──┐
│ 跑分析
analyze-skill-usage ──┐
│ 反馈
docs/local/skill-usage-report.md ──┐
│ 调优
```

## PDF 第8页

[查看原页](RAW.pdf#page=8)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
15 回到 design / paradigm / skill ──┘
逐层拆解：
1. 设计文档（design/）
存放每个核心模块的"长
期决策"，比
如《调度框架设计文档》《日志设计方
案
》《Skill使
用观测设计》。这些文档不轻易改，是知
识资
产。
2. 研发范式（paradigm/）
"做 X 这件事的标准流程"，比
如《新增主任务研发范式》《新增子任务研发范式》。范式
= 步骤清单
反模式列表
+
+
标准锚点路径。范式是 Skill 的素材，但本身也是给人看的文
档。
3. Skill 矩阵（.agent/skills/）
范式被编码成 agent Code Skill，让 agent 在合适的场景下被自动触发，按范式执
行
。我
们沉淀
了 13 个 Skill，可以分成几类：
4. Hook 数据采集（.agent/hooks/）
Skill 是被触发
的
道。Hook 弥补这个缺口：
、prompt 是被发出的
commit 是落地的——这中间发生了什么我们不
知
SessionStart / UserPromptSubmit → 记录所有
prompt
PreToolUse / PostToolUse → 记录 Skill 调用、工具调用
Stop → 记录每次 session 结束、打 commit 快照
PreCompact → 记录上下文压缩
、
```

## PDF 第9页

[查看原页](RAW.pdf#page=9)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
8 个 Hook 落 到 .agent/logs/ 下四类日 志 ： skill-usage / prompts / commit-
snapshot / edits。Hook 这层是"数据基础设施"，没它就没有
后面所有
的度量。
5. 观测分析（analyze-skill-usage）
每月跑一次，输出 6 类报告：
§0 数据来源（按 hostname 聚合）
§1 使用频率（哪些 skill 真在用）
§2 意图触发（哪些 prompt 没触发到 skill）
§3 落地率（skill 启动后 6h 内是否产生 commit）
§4 绕过率（commit 改了 skill 锚定路径但没启动 skill）
§5 GAP（模型输出的 Edit/Write 是否落到 commit）
6.
反馈回路
报告中
暴露的问题反过来调 description / 调范式 / 加 hook，形成闭环。
▐ 4.3 落地数据：好的
、不好的
、
灰色的都
摊开讲
这是 ATA 复盘里最重要的部分——不
光讲成功，把数据真实
摊开来。
好的部分：
add-schedule-biz-type 和 add-process-template 是高频
高落地率的"健康
+
skill"。aiAddOn 接入这次实测，11 个骨架文件 5 分钟生成完毕（人工抄 findDiscount 至少
半天），且骨架里 12 个反模式 checklist 帮助 Code Review 提前拦住了 3 个潜在问题。
check-docs-sync 在最近一次发版前发现了 docs/design/调度框架设计文档.md 的 §6
章节锚点路径已
变更，避免了文档漂移。
不好的部分：
绕过率有 8 条记录，集中在 findDiscount/node/
系列。也就是说，开
发
者改了节点目
录下的文件，但没启动相应 skill。原因
有两个：
1. 这些 skill 的 description 写得不够"主动"——agent 没意识到要触发；
2. 部分修改是小改（改个常量、加个日志），开
发
者主观觉得没必要走 skill。
第一 个 问题是 description 优 化 的 事 ， 可 以 解 ； 第二 个 问题反 映 了一 个 深 层 trade-off——
range 太广 skill 会过度触发，range 太窄又会漏触发。我们当前的策略是"宁可漏触发也不
过度触发"，因为过度触发会让开
发
者烦，长
期反而降
低主动使用率。
灰色的部分：
GAP 指标上，最近一份报告显示有 10 个文件 agent Edit 过但 0 落 commit；commit 中又
有 8 个文件 0 来自 agent。展
开看，原因杂得很：
```

## PDF 第10页

[查看原页](RAW.pdf#page=10)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
agent 改对了但开
发
者本地手工又改了一版（重写）
agent 改了 90% 但最后 10% 开
发
者觉得快而手写
agent 完全错了，开
发
者放弃
这部分数据噪声很大，但它逼我们正视一个现实：模型输出 ≠ 实际落地，团队真正受益的代码
量，需要从 commit 角度反推，不能只看 agent 调用次数。
▐ 4.4 ROI 估算：一次新业务接入
抽一个真实
case 做 Fermi 估算（aiAddOn 接入这次为例）：
按业务接入频率估，年度节省 40–80 人/天。考虑到体系
本身的维护成本（月度 1–2 人/
天），R
OI 是正的。
但我们也想坦诚承认这里的不确定性：
度量本身有噪声（落地率受 prompt 复杂度影响）
Skill 维护是软成本，团队人员流动会冲击
范式过严会反向降
低主动使用率
R
OI 表上的数字是真实的，但它代表的是上限，而不是默认值——前提是范式被遵守、skill 被
触发、报告被复盘。
▐ 4.5 与上游能力的边界
很多人问过我："你们做这套不是和 agent Code 自己的能力重复吗？"
讲清楚边界很重要：
```

## PDF 第11页

[查看原页](RAW.pdf#page=11)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
上游（Anthropic / agent Code）能力：模型本身、tool use、prompt cache、Skill /
Hook / Plan Mode / Agent 这些原语、IDE 集成。这些我们不维护，跟着升级
。
我们的能力：业务范式
、Skill 内容、Hook 业务规则、观测分析、组织约定。这些必须我
们维护，没人替我们写。
类比一下：上游给的是"乐高零件"，我们组
装
的是"乐高城堡"。模型能力会持续涨，但组织知
识资
产是真正的壁垒——模型升级时，我们的范式
+
skill 是顺风车。
踩过的坑
文章不讲坑就不
完整。挑几个值得分享的：
坑 1：DagTerminationChecker 下线那次的"幽灵 CANCELLING"
第一版写收敛时，留了一个 DagTerminationChecker 做兜底——觉得"万一 Redu
没推进到终态，让 checker 来补"。结果上线
后偶发出现"主任务永久卡 CANCELLING"。
cer
排查发现，checker 和 redu
而引入了
竞争——两个组
cer 在某些时序下会互相覆盖对方的 m
件都觉得自己是终态聚合的最终决策者。
utation。本质是双兜底反
后来下线了 checker，统一走 MaybeAdvanceToTerminalEvent + SummarizeAndAd
vanceEvent ，问题消失。
教训：收敛要彻底，不要"先收敛
到兜底路径上去。
+
再加兜底"。兜底的存在会让收敛失效，因为业务侧总会绕
坑 2：Skill description 太宽 vs 太窄
最早写 analyze-grayconfig 时，description 写得偏窄："仅在用户提到 GrayConfig
时触发"。结果发现很多 PR 改了配置但触发不到。改宽后又陷入另一个极端——非配置改动也
偶尔被触发。
最后定下的规则是：description 写"什么场景该触发"
+
比堆关键词有
效。这条经验后来沉淀成了
skill-creator
"什么场景不该触发"两段，明确边界
的内置约束。
坑 3：Hook 数据隐私
Hook 会记录所有
prompt。最早实现时直接写文件
、没脱敏。后来内部 Code Review 时被
指出可能记录到敏感字段（虽然主要是技术 prompt，但偶尔会带 cookie/token）。最后给
Hook 加了简单
的脱敏规则
日志路径权限控制
。
+
教训：采集即责任
。任何动 telemetry 的项目，第一天就得想清楚数据治理。
```

## PDF 第12页

[查看原页](RAW.pdf#page=12)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
坑 4：范式过严反而降
低使用率
第一版 add-schedule-biz-type 范式列了 16 个反模式，每条都强校验。结果开
觉得"用 skill 比
手写还累"——因为骨架太严格，业务有点点偏离就要绕。
者
发
后来调整成"反模式分级"——P0 级（必须拦截，比
拦）
+
P2 级（仅在 review 时建议）。落地率明显回升。
如 Node 直推 GUI）
+
P1 级（提醒不强
教训：范式是给人用的，不是给人受罪的。"严"和"好用"是冲突的，需要持续微调。
可对外参考的方法论
如果你的团队也想做类似的事情，下面这些经验大概率有用：
▐ 6.1 系
统重构方面
1. 非破坏性演进 > 推倒重来。我们让 v1 / pro / framework 三代并存，新业务一律走最新
代，老代码留作"考古证据"。这种打法的关键是给老代码画清楚边界，避免"两
边都改"。
2. 写 收敛 是高 R
OI 病。Redu
cer
+
的 重 构方 向。 状 态 机 散 点 写、 CAS 散 点 retry Event 的范式
不需要新中间件，落地成本低，收益持续。
是大 部 分 成 熟系
统 的 通
3. 分层不是越多越好，是"每层有清晰职责"。我们的 Schedule / DAG / Process / Node
四层，每层只负责一类决策。判断分层是否合理的标准：每层的代码能否独立讲清楚。
4. 可观测性投入要前置。日志通道拆分、字段白名单、SLS 看板，这些在重构同期做最划算
——重构本身会大量改写日志点，不如顺手改成新规约。
▐ 6.2 AI Coding 方面
1. 范式先于 Skill。先把"做这件事的标准流程"写成 paradigm 文档，再编码成 Skill。直接
写 Skill 容易陷入"对模型说什么"，写范式逼你想清楚"对人说什么"。
2. Hook 是 telemetry 基础设施，越早做越好。没有数据就没有反馈回路，整个飞轮转不起
来。Hook 最便宜的实现就是"prompt + tool 调用
+
commit"三类日志，月度跑一次分
析。
3. Skill 的 description 是 70% 的工作。写 Skill 内容不难，难的是让 agent 在正确的场
景下"想到"用它。description 不是关键词堆叠，是边界声明——什么时候用 / 什么时候
不用都要明说。
```

## PDF 第13页

[查看原页](RAW.pdf#page=13)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
4. 观测 报 告 要敢
于 摊 开 数 据 。 落 地 率低
、 绕 过 率高
、 GAP 大 —— 这 些 数 据比"用 了 多 少 次
Skill"更有价值，因为它们暴露问题。月度复盘的 90% 价值在"不健康"的指标里。
5. 维护成本是真实的。Skill / Hook / 报告需要 owner。我们当前由 1 人兼职可承担，但要
清楚：没有 owner，飞轮一定会停。
▐ 6.3 双轮驱动的本质
回头
看，系
统重构和 AI Coding 工程化是同一件事的两面：
重构需要把"老员工脑子里的隐性知
识"变成"可执
的范式"；
行
AI Coding 工程化需要"可执
行
的范式"作为 Skill 的素材；
Skill 反过来加速业务接入，验证范式是否真的可执
；
行
业务接入产生的数据反向调优范式和重构。
如果只做重构不做 AI 工程化，范式会停留在文档上，新员工还是要 1 周看代码；如果只做 AI
工程化不做重构，Skill 编码的是"老代码的写法"，沉淀的是反模式。
两条线必须一起推。
已知
边界与下一步
诚实地讲，当前这套体系仍有
几个边界：
WAITING 子任务无超时机制
。长链阻塞需要主任务级 deadline 兜底，目前还没补；
su
mmarize 失败重试无上限。外部依
期
长
赖
不可用时会无限重试，准备加 retryCount 上
限；
completedProcessIds 等集合规模上限。单主任务 >100 子任务时需评估 JSON 体
积，目前业务还没到这个量；
Skill 触发率和开
发
者主观感受耦合。需要定期 1:1 收集主观
反馈，单纯看数据不够；
跨仓库 telemetry 聚合。当前 hook 数据落本地 / 团队内 telemetry repo，跨组复制时
需要平台化考虑。
下一步的路线
大致：
短 期 （ 3 个月 内 ） ： 稳 住 L3 体系 ，月 度 skill 报 告 固 化 ； 补 WAITING 超时 和
su
mmarize 上限。
中 期 （ 半 年 内 ） ： 推 到 L4—— 落 地 率 / 绕 过 率 SLO 化 ，反 向自 动调优 Skill
description。
中期：跨组复制 POC，验证范式
+
skill 体系
是否可被搬运（可能需要平台层抽象）。
```

## PDF 第14页

[查看原页](RAW.pdf#page=14)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
长
期：根据模型能力进展，评估是否能做"自动 Skill 生成 / 自动 PR 评审"这类 L5 能
力。
写在最后
这次改造的最大体会：AI Coding 不是个人生产力工具，是团队工程能力。
个人用 agent 写代码这件事，不需要
任何工程化——打开 IDE 装个插件就完事。但当一个团
队要让"AI Coding 的收益可度量、可复制
、可传承"时，就必须做工程化：把范式写下来、把
范式编码成 Skill、把 Skill 的使用观测起来、把观测数据反馈回去。
这套打法不复杂，但需要持续投入。比起买更贵
越模型代际更迭的核心壁垒。
的模型，让团队的隐性知
识沉淀下来，才是穿
如果你的团队也在思考"AI 怎
么真的帮到我们而不是只帮到个人"，希望本文有点用。欢迎交流
拍砖。
团队介绍
本文作者依凡，来自淘天集团—天猫APP技术团队。作为淘天集团的核心技术引擎，我们负责
天猫APP的全栈开
发与体验升级，支撑导购、
搜推、商详、购物车、下单等核心交易链路。我
们以极致的端侧性能与创
新的Agent架构，打造「AI导购」「AI助手」等面向C端的智能应用，
并探索端外场景合作，为千万级用户构建沉浸式
、个性化的购物体验，持续引领电商APP的技
术演进。
¤ 拓展阅读 ¤
3DXR技术 | 终端技术 | 音视频技术
服务端技术 | 技术质量 | 数据算法
大淘宝技术
大淘宝技术官方账号
966篇原创内容
公众号
```

## PDF 第15页

[查看原页](RAW.pdf#page=15)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
阅读 5487 修改于2026年8月11日
留言
写留言
还没有
留言，来写首评
```
