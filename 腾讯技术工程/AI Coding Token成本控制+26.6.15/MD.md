# 原文逐页转写

文本来自本次 PDF 文本层；不补写图片、截断内容或代码。图片和布局请打开每页 PDF 链接核对。AI 解释另见学习笔记。

## PDF 第 1 页

[原页](RAW.pdf#page=1)

````text
⼀篇搞懂 AI  Coding  Agent  的 Token  成本控制
Jun  15 , 2026 , 2 : 27  AM⼴东腾讯技术⼯程 160  listened
作者：devinyzeng
⽉初看账单，吓⼀跳。
也没问多少问题，Token 怎么烧成这样？
后来认真拆了⼀轮，才发现⼀个反直觉的事实：
你问的那句话，在每次请求⾥可能连  1% 都不到。
真正的成本⼤头藏在别的地⽅。这篇⽂章，就是把这个 “ 别的地⽅ ” 讲清楚，然后给⼀套从⽇
常使⽤习惯、模型路由，到⼯具层、代码图谱、多  Agent 协作的完整优化⽅法。
第⼀章  账单都花在哪了
很多⼈⼀上来先优化提问⽅式：把句⼦写短⼀点，把形容词删掉⼀点，把问题问得更 “ 像
Prompt Engineer ⼀点 ” 。
⽅向不算错，但经常抓错重点。
因为在  AI Coding Agent ⾥，真正决定账单的，通常不是你⼿⾥敲进去那⼏⼗个字，⽽是系
统为了让模型 “ 看起来懂上下⽂ ” ，⾃动帮你带上的那⼀⼤坨东⻄。
先把⼀轮请求拆开看清楚，再谈优化。否则你会⼀直在省零钱，漏掉⼤头。
1.1 你问的那句话，其实最便宜
适⽤： CodeBuddy 、 Cursor 、 Codex 、 Gemini CLI 等这类  AI Coding Agent 。
读完你会得到三样东⻄：⼀个正确的⼼智模型、⼀份今天就能做的⾏动清单、⼏套继续
往下压成本的⼯程⽅法。
````

## PDF 第 2 页

[原页](RAW.pdf#page=2)

````text
先看⼀个典型的请求结构：
System Prompt         5K
项⽬说明⽂档           10K
Skill 定义             20K
Tool / MCP 定义        30K
历史会话              100K
代码⽂件               50K
⽤户问题                0.1K
这不是所有产品都⼀样的精确账单，⽽是⼀种很常⻅的分布。
它传递的信息很明确：
很多⼈本能地把优化⽅向定为 “ 怎么把问题写短点 ” 。这当然不是坏事，但它抓不到主要⽭
盾。因为模型真正收到的，不是 “ 你的问题 ” ，⽽是 “ 带着整包上下⽂的问题 ” 。
可以把⼀轮请求近似理解成这个公式：
总成本  ≈ 固定前缀  + 会话历史  + 运⾏时检索  + ⼯具往返  + 模型输出
这⾥⾯有三层东⻄：
固定前缀： System Prompt 、 Skill 定义、 Tool / MCP 定义、稳定背景⽂档
半固定上下⽂：项⽬说明、 Repo Map 、 Memory 、⻓期约束
动态上下⽂：聊天历史、代码⽚段、检索结果、⼯具返回、你这轮新问题
你那句提问，往往只是最后⼀撮 “ 点⽕器 ” 。它负责触发任务，但通常不是成本主体。
这个结构可以画成⼀张很直观的图：
这也是为什么很多⼈会产⽣错觉：
我明明只问了⼀句话，怎么这么贵？
答案是：你只问了⼀句话，但系统替你背了⼀整⻋背景。
当你理解这⼀点，后⾯很多优化动作就会突然变得合理：为什么要开新会话，为什么要压缩
历史，为什么要少装  Skill ，为什么要做代码图谱。这些动作看上去分散，本质都在做同⼀件
贵的是系统塞进去的东⻄，不是你写的那句话。
````

## PDF 第 3 页

[原页](RAW.pdf#page=3)

````text
事：
减少重复上下⽂。
1.2 “ 它明明记得 ” 只是⼀种幻觉
AI Coding Agent ⽤久了，很容易产⽣⼀种感觉：
它好像⼀直记得我们聊过什么
但实际上，⼤模型本身通常是⽆状态的。
真正 “ 记得 ” 的，不是模型，⽽是包在模型外⾯的  Agent / CLI / 平台层。它在每⼀轮请求前，
把历史、规则、⼯具、代码、⽂档重新拼起来，再发给模型。所谓 “ 记忆 ” ，很多时候只是
“再次传⼊ ” 。
这个过程可以简化成：
````

## PDF 第 4 页

[原页](RAW.pdf#page=4)

````text
这件事为什么重要？因为它直接决定了成本结构。
第⼀，会话越⻓，后续每⼀轮越贵。因为历史不是 “ 存在那⾥等模型⾃⼰想起来 ” ，⽽是很可
能在每轮都要重新带过去。
第⼆，⼯具越多，常驻定义越重。⼀个  Tool / MCP 不只是 “ 多⼀个按钮 ” ，⽽是多⼀段要让模
型理解的说明、参数模式和调⽤约束。
第三，⼯具调⽤会形成回路。模型先读⼀⼤包上下⽂，再调⽤⼯具；⼯具返回⼀段结果；结
果⼜被塞回上下⽂，再进⼊下⼀轮。于是⼀次任务，不是⼀次计费，⽽是⼀连串 “ 请求 — 返
回 — 再请求 ” 的链条。
所以  AI Agent 最怕的不是问题复杂，⽽是：
会话越滚越⻓
⼯具越堆越多
背景越塞越满
每次都从零找信息
输出不合格反复重试
很多⼈说 “ 它明明记得 ” 。更准确的说法其实是：
1.3 五种成本，不⽌是 “ 输⼊字数 ”
做成本优化，先别把  Token 理解成 “ 字数 ” 。
Agent 场景⾥⾄少有五类开销，要分开来看：
成本类型 它是什么 为什么会放⼤
输⼊  Token 系统提示词、历史消息、代码⽚段、
检索结果、⼯具定义
每轮都可能重复携带，是最
⼤头
输出  Token 模型最终回答的⽂字 回答越⻓、越啰嗦、越容易
失控
推理  Token / thinking
budget 模型内部⽤于思考和规划的预算 简单任务如果⾛⾼推理档
位，会明显溢价
⼯具往返成本 ⼯具描述、调⽤参数、返回结果进⼊
上下⽂
⼀次⼯具调⽤，常常⽐原问
题还⻓
重试成本 第⼀次做错后重新来⼀轮 每修⼀次，都可能把整包上
下⽂再付⼀遍
不是它记得，⽽是系统在⼀遍遍提醒它。
````

## PDF 第 5 页

[原页](RAW.pdf#page=5)

````text
这⾥最容易被低估的，往往是后两项。
⼯具往返成本的问题在于：你以为⾃⼰只是 “ 让它查个⽂件 ” ，但模型其实经历的是：理解⼯
具定义  →  ⽣成参数  →  接收返回值  →  再结合返回值继续思考。对⼈来说只是⼀个动作，对
系统来说可能是多段上下⽂交换。
重试成本更隐蔽。真正烧钱的，常常不是第⼀次调⽤太⻓，⽽是第⼀次不合格 —— 格式不
对、结构错、找错⽂件、推理过度 —— 于是⼜来⼀轮。
第⼀次没答对
→ 重新描述问题
→ 重新附带历史
→ 重新拉代码或⼯具结果
→ 再跑⼀轮模型
所以很多 “ 看起来只补了⼀句话 ” 的修正，实际含义是：
错误的第⼀次调⽤
+
第⼆、第三次修正调⽤
=
整包上下⽂被反复付款
这也是为什么 “ 减少重试 ” 本身就是⼀种⾮常硬的成本优化⼿段。格式约束更清楚、任务边界
更明确、上下⽂给得更准，省下来的不只是⼀次输出，⽽是整条失败链路。
1.4 Prompt Cache ：为什么它是所有优化的基础
理解了成本结构，就能理解为什么  Prompt Cache  这么重要。
很多⼈第⼀次听到缓存，会以为它缓存的是 “ 答案 ” 。其实更接近的理解是：缓存的是稳定前
缀的处理结果。也就是 —— 如果两次请求前半段⼏乎⼀样，服务端就不必每次都从头处理那
⼀⼤段相同内容。 [1] 、 [2]
原理可以先粗略理解成：
固定前缀  → 缓存命中  → 不⽤每次都从头处理
最容易被缓存的内容，通常是这些：
System Prompt
Tool / MCP 定义
Skill 定义
````

## PDF 第 6 页

[原页](RAW.pdf#page=6)

````text
⻓⽂档背景
稳定的  few-shot 前缀
为什么官⽅⽂档总在强调 “ 静态内容放前⾯，动态内容放后⾯ ” ？因为缓存命中的对象通常是
前缀，不是整段任意位置的拼图。
看这张图就很容易懂：
这⾥有三个很关键的推论。
第⼀， Prompt Cache 省的不是⾸次成本，⽽是重复成本。  第⼀次发送⻓前缀时，通常还是
要正常付费；价值在第⼆次、第三次、后续很多次复⽤时才会体现出来。
第⼆，缓存不是 “ 写短 ” ，⽽是 “ 写稳 ” 。  你天天改系统提示词、天天调  Skill Prompt ，那缓存
理论上存在，实践⾥也很难命中。
第三，缓存优化和上下⽂治理是⼀回事。  减少前缀抖动、把稳定内容前置、把变化内容后
置，本质都在提升 “ 可复⽤⽐例 ” 。
所以  Prompt Cache 本质上不是让模型更聪明，⽽是让你别为同⼀段前缀反复买单。官⽅数
据也说明了这⼀点： OpenAI 与  Anthropic  都提到，⻓前缀命中缓存后，输⼊成本和延迟都
可能显著下降。 [1] 、 [2]
（缓存的具体配置⽅法，会在后⽂⼯具层详细展开。）
1.5 ⼀张全图：五层模型
梳理完成本来源后，再看优化路径就会清楚很多。
Token 优化重点，不是把提示词写短，⽽是把前缀写稳。
````

## PDF 第 7 页

[原页](RAW.pdf#page=7)

````text
这篇⽂章核⼼框架分五层：
它们不是并列的⼩技巧，⽽是⼀条从便宜到贵、从易到难的升级路径。
使⽤习惯解决的是 “ ⽆意义的历史和废  Token”
模型路由解决的是 “ 贵模型⼲便宜活 ”
Context ⼯程解决的是 “ 同样前缀重复发送 ”
代码图谱解决的是 “ 每次都从零找代码 ”
Agent 架构解决的是 “ 所有任务都塞给同⼀个⼤上下⽂ ”
这五层背后其实只有⼀个总⽬标：
让模型少看⽆关内容
让便宜模型多⼲标准活
让贵模型只做⾼价值推理
还有⼀条贯穿全⽂的线：观测与预算治理。
没有数据，优化就会变成体感。你觉得⾃⼰ “ 省了 ” ，但不知道省在哪，也不知道是不是⽤质
量换的。这个话题会在后⽂继续展开。
到这⾥，第⼀章真正想建⽴的⼼智模型可以浓缩成⼀句话：
````

## PDF 第 8 页

[原页](RAW.pdf#page=8)

````text
⼀旦你脑⼦⾥有了这张图，第⼆章那些 “ 看起来很琐碎 ” 的使⽤习惯，就不再是经验技巧，⽽
会变成⾮常⾃然的⼯程动作。
第⼆章  使⽤习惯：最便宜也是最被低估的优化
如果你现在就想开始省  Token ，最先动的不是架构，不是知识图谱，⽽是使⽤习惯。
这层⼏乎零⼯程投⼊，却经常拿到第⼀波最⼤收益。接下来的九个习惯，都是今天就能改
的。
2.1 ⼀个  Session ，⼀件事
很多⼈把  AI Agent 当成永不关闭的⻓会话：上午修  Bug ，下午写⽂档，晚上聊架构，第⼆天
接着来。
体验很顺，成本是灾难。
原因很简单： Session 越⻓  →  继承的历史越多  →  每⼀轮越贵。
修  Bug 开⼀个，做重构开⼀个，写⽂章开⼀个，查线上问题开⼀个。别混着来。
Topic 切分就是最便宜的  Context 管理。
2.2 ⻓会话不压缩，就是负债
很多⼈舍不得清历史，觉得 “ 越完整越稳 ” 。
模型不需要你的完整试错过程。它需要的是：
现在要⼲什么
做完了什么
哪条路不通
卡在哪了
下⼀步怎么做
AI Coding Agent 的成本，本质上不是 “ 你问了什么 ” ，⽽是 “ 系统为了回答你，重复搬运
了多少上下⽂ ” 。
⼀个  Session 只服务⼀个⽬标。
````

## PDF 第 9 页

[原页](RAW.pdf#page=9)

````text
/compact 做的，本质上是这⼀件事：
1 把完整历史
2 压成可继续⼯作的状态
对话记录不是资产，未压缩的⻓对话是负债。它让后续每⼀轮都背着越来越重的历史包袱。
2.3 聊天记录不是数据库
很多团队把背景、决策、约束、待办全挂在会话⾥，指望  Agent ⼀路记到底。
后果：会话越来越⻓，状态越来越难提炼，成本越来越⾼。
真正该⻓期保留的信息，外置出去：
项⽬⽂档
Summary ⽂件
Memory ⽂件
Repo Map / Knowledge Graph
任务清单
让会话只承载 “ 当前⼯作状态 ” ，⽽不是全部项⽬历史。
2.4 少说废话，也是省  Token
很多⼈优化只盯输⼊，忘了输出⼀样贵。
编码场景最浪费的回答不是 “ 错 ” ，是 “ 废 ” ：先复述⼀遍问题，再讲⼀段众所周知的背景，然
后⼀堆礼貌性铺垫，最后才给结论。
如果你只需要  diff 、步骤、结论、表格、 JSON—— 直接要求它这么给。
这类约束值钱，因为它同时省两类：
1. 输出更短
2. 结果更可⽤  →  重试更少
在很多⽇常任务⾥，⼀句指令就够了：
直接给结论，不要复述问题，必要时再展开
Caveman 这类思路受欢迎，不是 “ 简陋 ” ，⽽是直接打掉⾼频废  Token 。
````

## PDF 第 10 页

[原页](RAW.pdf#page=10)

````text
2.5 Skill ≠ 免费能⼒
Skill 有价值，但也背成本。
每个  Skill 都带着  Description 、 Instructions 、 Examples 、触发逻辑。这些信息如果常驻，就
会进上下⽂。
问题不是 “ 装不装 ” ，⽽是：
⾼频、稳定、通⽤的  Skill 常驻。低频、⻓说明、低复⽤的按需触发。
和后端服务治理同理：常驻能⼒要尽量少⽽精。
2.6 MCP 越多，不⼀定越强
MCP 的最⼤诱惑是让  Agent “ 什么都能接 ” 。
但从成本看，每多⼀个  MCP ，就多⼀份  Tool Deﬁnition 、多⼀层选择成本。
很多⼈装了  GitHub 、 Notion 、 Jira 、 Slack 、 Browser 、 Filesystem 、 Kubernetes 、Docker 和
各种内部系统。看起来很强，实际⾼频⽤的就两三个。
⼯具太多不只是 “ ⽂档⻓ ” 的问题：
选择空间变⼤  →  决策变慢
错误调⽤概率变⾼
每轮携带定义更重
所以⼯具治理和依赖治理⼀样：关键不是能不能装，是有没有必要常驻。
2.7 CLI 优先于  MCP
这是⼀个有点尖锐但很实⽤的原则：
1 能  CLI 解决  → 尽量  CLI
2 能脚本解决  → 尽量脚本
3 最后才考虑  MCP
很多操作已经有⾮常成熟的  CLI ：gh pr create、kubectl get pods、docker ps、git
diff。
AI 直接⾛命令更轻，不需要额外拉⼀整套⼯具说明。
哪些常驻，哪些按需加载。
````

## PDF 第 11 页

[原页](RAW.pdf#page=11)

````text
对于国内常⻅的研发平台，也有专⻔为  AI Agent 优化的  CLI ⼯具可以直接⽤：
**tapd-ai-cli** ：腾讯  TAPD 的  AI Agent 专⽤  CLI ，⽀持需求、缺陷、任务的查询和更
新。直接⽤ tapd story list、tapd bug create 之类的命令操作  TAPD ，⽐拉⼀套
MCP 轻得多，还能⽤ tapd skill init ⼀键⽣成  SKILL.md 配置。
**gongfeng-cli** ：腾讯⼯蜂代码托管的  AI Agent 专⽤  CLI ，专⻔针对  Agent 的认知模式
优化了输出格式（ Markdown + JSON 混合），⽀持  PR 创建、代码评审、项⽬管理等完
整⼯作流， Token 消耗显著低于同等  MCP ⽅案。
这两个⼯具的共同思路值得借鉴：专为  Agent 设计，⽽不是给⼈看的  UI 套了个  CLI 壳。输
出格式、信息密度、命令发现机制，都针对  AI 的调⽤模式做了优化。
MCP 的价值在：跨系统编排、结构化返回、权限统⼀收敛、内部业务能⼒包装。
所以不是 “CLI 永远优于  MCP” ，⽽是：
2.8 引⽤⽂件时带完整路径
这是⼀个极其容易忽视的⼩习惯，但省的  Token 实实在在。
很多⼈引⽤⽂件时习惯只写⽂件名：
1 看⼀下  config.go 的问题
2 帮我修改  utils.py
AI 收到这类请求，往往要先搜索整个项⽬找这个⽂件在哪，有时候还会搜到同名⽂件或路径
不确定，再次搜索确认。这些搜索调⽤和返回结果，全部计⼊  Token 。
更直接的做法：
1 看⼀下  src/config/config.go 的问题
2 帮我修改  @/Users/yourname/project/utils.py
⽤ @ 符号加上相对路径或绝对路径， Agent 直接定位读取，不需要搜索任何中间步骤。
这个习惯对⼤型项⽬更显著 —— 项⽬越⼤，搜索代价越⾼，⽬录层级越深，搜索越容易绕
弯。
1 只写⽂件名  → 搜索  → 可能多次确认  → 读取
2 完整路径    → 直接读取
已有成熟命令链路时，不要为了看起来⾼级⽽过度⼯具化。
````

## PDF 第 12 页

[原页](RAW.pdf#page=12)

````text
⼀个 @ 路径 节省的，是⼀整条搜索链路。
2.9 把意图⼀次说完，别聊天式拆碎
AI Agent 的使⽤场景⾥，有⼀种很常⻅的低效模式：
表⾯上看，这是 “ 正常沟通 ” 。实际上，每⼀轮来回都在消耗  Token ：重新组装上下⽂、重新
带⼊历史、重新确认状态。四轮对话的成本，往往是⼀次完整表达的好⼏倍。
更省的做法是⼀次把意图说清楚：
1 看  @src/order/service.go 的  CreateOrder 函数，
2 找出潜在的  bug ，修复，并为修复后的函数写单测。
这不是要求你写得⻓，⽽是要求你把⽬标说完整。⼀次对话， Agent ⼀次性跑完整个任务，
省去了所有中间确认的来回成本。
越具体、越完整的指令，浪费的轮次越少。这和程序员提  Issue 的逻辑是⼀样的：把背景、
期望、验收条件都写清楚，沟通成本才不会⽐写代码还贵。
第三章  模型路由：别让贵模型⼲便宜活
习惯层做好之后，下⼀步收益最⾼的，是模型路由。
很多⼈⼀上来就犯⼀个错：所有环节默认最强模型。看起来稳，实际上最烧钱。
3.1 匹配优先，不是便宜优先
````

## PDF 第 13 页

[原页](RAW.pdf#page=13)

````text
模型路由不是 “ ⼀律⽤便宜的 ” ，⽽是先把任务类型分对：
复杂任务  →  强模型
简单任务  →  便宜模型
重复任务  →  稳定模型
架构设计需要⻓链路推理，该⽤贵的就⽤。写单测、补注释、⽣成提交信息的，便宜模型完
全够⽤。⼤规模批量分类和摘要，适合低单价模型或离线批处理。
3.2 ⼀张表说清楚
任务 推荐模型档位 理由
写  UT 便宜模型 模式稳定、模板化
写  commit 便宜模型 输出短、⻛险低
Code Review 中⾼档模型 需要语义理解
架构设计 强模型 ⻓链路推理
复杂  Bug 分析 强模型 多步假设和验证
批量分类 / 摘要 低价或  Batch 规模⼤、成本敏感
选模型不是凭喜好，是按任务需要的能⼒。
3.3 先过便宜模型，再升级
很多任务不需要⼀上来就最贵模型。
更省的模式可以简化成⼀条升级链路：
1 便宜模型先跑
2 ↓
3 判断复杂度
4 ↓
5 需要才升级
例如：先让便宜模型分类（重构？ Bug ？⽂档？），先做初筛（ PR 有没有⾼⻛险？），先做
摘要（ 20 ⻚  →  1 ⻚），再交给强模型做推理。
这种级联⼯作流，既省钱，⼜让贵模型花在⼑刃上。
3.4 不只换模型，也要调预算旋钮
现在很多模型提供成本旋钮：
````

## PDF 第 14 页

[原页](RAW.pdf#page=14)

````text
reasoning effort
thinking budget
verbosity
max output tokens
它们影响的，其实是同⼀组东⻄：
想多深、答多⻓、花多少钱
Google Gemini 的  thinkingBudget 允许按任务控制思考  Token ，简单任务甚⾄可以压到  0
（关闭思考）。 OpenAI 也建议很多⼯作负载从 low 的  reasoning effort 起步。
3.5 Skill / Agent / Command 都应该绑定模型
模型路由不该只存在于 “ 主对话框 ” 的⼼智⾥，要落实到执⾏单元。
Skill 绑定模型：写  UT 、 commit 、格式修复、样板代码，明确绑定便宜模型。
以  CodeBuddy 为例， SKILL.md ⽂件头部可以直接声明模型和上下⽂策略：
---
context: fork
model: deepseek-v4-pro
---
model 字段指定该  Skill 使⽤的模型，context: fork 表示把这类固定流程放到独⽴执⾏上
下⽂⾥，适合任务边界清晰、可单独完成的  Skill 。这样⼀来，低复杂度的  Skill 就能⾃动⾛
便宜模型，也不必把主会话的全部历史都带进去。
斜杠命令（ Slash Command ）和  Agent 同样⽀持 model参数绑定，在定义时就固化好模型
选择。这样团队⾥每个⼈⽤ /commit、/gen-ut 这类命令时，都默认⾛便宜模型，不需要
依赖个⼈记得切换。
Agent 绑定模型：
Planner  → 中⾼档
Coder    → 中档  / 便宜
Reviewer → 强
不是所有任务都要深度思考，也不是所有任务都要⻓答案。 让⼀个模型⽤⾼推理档位
做分类、摘要、提交说明，本质上是在拿推⼟机扫地。
````

## PDF 第 15 页

[原页](RAW.pdf#page=15)

````text
Command 绑定模型：很多命令本身就是固定模板，适合预设便宜模型。这类设计⼀旦固
化，成本治理就从 “ 靠⼈记得切 ” 变成 “ 系统默认更省 ” ，前三章解决的是两件事：先减少⽆意
义上下⽂，再别让贵模型⼲便宜活。
下⾯开始进⼊⼯具层和架构层：
先把⾼频进出上下⽂的内容压下来
再让  Agent 少⾛盲搜链路
最后把多  Agent 的职责边界拆清楚
第四章  上下⽂压缩：先把⾼频上下⽂压下来
如果说前⾯三章解决的是 “ 少带⽆关上下⽂ ” ，这⼀层解决的就是另⼀件事：把那些⼀定会进
上下⽂的内容，尽量压短。
这四个⼯具⽅向不同，但可以叠加。你不⼀定要⼀次装全，但只要装上⼀个，通常就能⽴刻
看到收益。
4.1 RTK ：终端输出才是真正的  Token ⼤杀⼿
很多⼈把  Token 浪费归因于 “ 聊太多轮 ” ，但忽略了⼀个隐性⼤户：终端命令的冗余输出。
CodeBuddy 执⾏cargo test，成千上万⾏测试⽇志、警告、进度条、 ANSI 颜⾊码全部涌
进上下⽂。
实测： 30 分钟开发会话对⽐（中等规模  TypeScript/Rust 项⽬估算）：
场景 Token 消耗
不⽤  RTK ~118,000
⽤  RTK ~23,900
节省 80%
按命令类别的典型压缩率：
命令类别 原始  tokens RTK 后 节省
cargo test / npm test 25,000 2,500 -90%
pytest 8,000 800 -90%
vitest run 102,199 字符 377 字符 -99.6%
ls / tree 2,000 400 -80%
grep / rg 16,000 3,200 -80%
git status 3,000 600 -80%
git diff 10,000 2,500 -75%
````

## PDF 第 16 页

[原页](RAW.pdf#page=16)

````text
命令类别 原始  tokens RTK 后 节省
cat / read 40,000 12,000 -70%
RTK 的四层过滤策略
1. 智能过滤：剔除注释、空⾏、 ANSI 颜⾊码、进度条、⽆关警告
2. 分组聚合：同类输出合并展示（搜索结果按⽂件分组、错误按类型归类）
3. 智能截断：按信息密度取样，保留关键⽚段，砍掉重复⻓尾
4. 去重合并：「连接超时」重复  10 次  →  「连接超时（ ×10 ）」
5 分钟安装
# macOS （推荐）
brew install rtk
# Linux / WSL
curl -fsSL https://raw.githubusercontent.com/rtk-ai/rtk/master/install.sh | sh
注意：安装后⽤ rtk gain 验证。如果命令不存在，可能装了同名的  Rust Type Kit ，需卸载
重装。
# 全局启⽤  CodeBuddy （推荐）
rtk init -g --agent codebuddy
# 仅启⽤  Hook ，不修改  CODEBUDDY.md
rtk init -g --hook-only
重启  CodeBuddy 后⾃动⽣效，所有命令透明经过  RTK 过滤，开发者⽆感知。
# 常⽤命令
rtk gain                 # 查看节省统计
rtk gain --history       # 带命令历史
rtk discover             # 扫描哪些命令还没⽤  RTK
# Git （压缩率  60-80% ）
rtk git status
rtk git diff
说明：这张表混合了  token 和字符两种统计⼝径。前⼏⾏是  token ，vitest run  这⼀
⾏是字符⻓度，⽤来说明压缩幅度，不能和  token ⾏直接横向⽐较。
````

## PDF 第 17 页

[原页](RAW.pdf#page=17)

````text
# 测试（压缩率  90-99.6% ）
rtk test cargo test
rtk vitest run
4.2 Caveman ：压缩输出端的废话
RTK 压缩的是命令输出（输⼊  Token ）， Caveman 压缩的是  AI 回复（输出  Token ）。两者⽅
向不同，可以叠加。
核⼼数据（来⾃  arXiv:2604.00025 ）：
任务类型 正常输出 Caveman 节省
解释  React bug 118 tokens 15 tokens 87%
配置  PostgreSQL 234 tokens 38 tokens 84%
Docker 多阶段构建 104 tokens 29 tokens 72%
Code Review PR 67 tokens 39 tokens 41%
平均 — — 65-75%
Caveman 有四种模式，按压缩程度递增：
/caveman lite：删填充词，保留冠词，专业⻛格（适合正式输出）
/caveman（ full 默认）：删冠词，碎⽚句，平衡压缩
/caveman ultra：极度压缩，⽤ A→B→C 箭头因果链
/caveman wenyan：⽂⾔⽂模式（理论上  token 效率最⾼的书⾯语）
实际效果示例（ full 模式）：
问：为什么  React 组件不断重渲染？
普通输出（ 69 tokens ）：
"The reason your React component is re-rendering is likely because you're
creating a new object reference on each render cycle..."
Caveman 输出（ 19 tokens ）：
"New object ref each render. Inline object prop = new ref = re-render.
Wrap in useMemo."
安装
git clone https://github.com/studyzy/caveman
cd caveman && ./install.sh 
# 选中  [2] CodeBuddy Code 确定即可
````

## PDF 第 18 页

[原页](RAW.pdf#page=18)

````text
安装后在  CodeBuddy ⾥输⼊ /caveman 即可激活。模式在会话内持续⽣效，输⼊ stop c
aveman 关闭。
4.3 headroom ：压 “ 进上下⽂的所有内容 ”
RTK 压的是命令输出， Caveman 压的是  AI 回复。 headroom 压的是第三个⽅向：所有读进
上下⽂的内容—— ⽂件内容、⼯具调⽤返回值、会话历史。
先看⼀张图，理解  headroom 在整个链路中的位置和它内部做了什么：
这张图解释了三件事：
1. headroom ⾸先是代理层，不只是压缩器——Agent 不直接连  LLM ，⽽是先经过本地的
headroom 代理⼊⼝。提示词、⼯具输出、⽇志、 RAG 结果、⽂件等上下⽂，都会先在
这⾥被接住、处理、再转发。
2. 代理层内部是⼀条处理流⽔线—— 先由  CacheAligner 稳定前缀，帮助  Prompt Cache 命
中；再由  ContentRouter 判断内容类型，把  JSON 、代码、⽂本分别交给  SmartCrusher 、
CodeCompressor 、 Kompress-base 。
3. CCR 负责 “ 可逆压缩 ”—— 原始数据全部保留在本地，模型只收到压缩版；需要细节时再
通过  headroom_retrieve  按需取回。不是删掉信息，⽽是延后加载细节。
实测效果（真实  Agent ⼯作负载）：
说明： Caveman 官⽅⽬前还没有⽀持 CodeBuddy 所以使⽤  studyzy Fork 版（已增加
CodeBuddy ⽀持）。
````

## PDF 第 19 页

[原页](RAW.pdf#page=19)

````text
场景 压缩前 压缩后 节省
代码搜索（ 100 条结果） 17,765 1,408 92%
SRE 故障排查 65,694 5,118 92%
GitHub Issue 分类 54,174 14,761 73%
代码库探索 78,502 41,254 47%
更重要的是，压缩后的准确率没有下降。在  GSM8K （数学推理）、 TruthfulQA （事实准确
性）等标准基准上，压缩前后的得分基本持平甚⾄略优。
安装
pip install "headroom-ai[all]"
接⼊  CodeBuddy
# 基础接⼊
headroom wrap codebuddy
# 推荐：同时开启跨  session 记忆  + 代码图谱集成
headroom wrap codebuddy --memory --code-graph
之后正常⽤  CodeBuddy ， headroom 在后台透明处理压缩，⽆感知。
也⽀持  MCP Server 模式
如果不想⽤  wrap ⽅式，可以⾛  MCP ：
headroom mcp install
安装后在  CodeBuddy ⾥⾃动注册三个⼯具：headroom_compress、headroom_retriev
e、headroom_stats。
与  RTK 的区别
说明：如需在  CodeBuddy 中使⽤，可使⽤  studyzy Fork 版（已增加  CodeBuddy ⽀
持）。
````

## PDF 第 20 页

[原页](RAW.pdf#page=20)

````text
RTK headroom
压缩对象 终端命令的输出 所有进上下⽂的内容
⼯作⽅式 过滤  + 截断 可逆压缩  + 按类型路由  + 按需还原
安装⽅式 brew / curl pip + wrap 命令
典型节省 89% 47–92%
两者⽅向不同， Headroom 甚⾄还集成了  RTK ，可以叠加使⽤。如果只装⼀个， RTK 解决最
⼤的单点问题（终端输出）；如果追求更全⾯的压缩覆盖，再加上  headroom 。
4.4 context-mode ：⼯具输出不再撑爆上下⽂
context-mode 解决的是⼀个具体痛点：MCP ⼯具调⽤的返回值太⼤。
⼀次  Playwright 快照  56 KB ，⼆⼗条  GitHub issue 59 KB ，⼀份访问⽇志  45 KB 。⽤  30 分
钟， 40% 上下⽂就没了。然后  /compact  ⼀压缩， CodeBuddy 忘了在改哪些⽂件、任务进⾏
到哪了。
context-mode 是⼀个  MCP server 插件，四层能⼒⼀起上：
能⼒⼀： Sandbox ⼯具输出（ 98% 压缩）⼯具调⽤结果先沙箱化，不直接进上下⽂。 315
KB →  5.4 KB 。 LLM 按需取回原始数据，不是真的删掉。
能⼒⼆：跨  compact 会话连续性所有⽂件编辑、 git 操作、任务进度、错误信息全部记录到
本地  SQLite 。/compact  之后不丢失现场 ——context-mode ⽤  FTS5 全⽂索引按相关性取回，
⽽不是把所有历史重新塞回去。
能⼒三：⽤代码代替读⽂件ctx_execute()  ⼯具让  CodeBuddy 写脚本处理数据，⽽不是读  50
个⽂件进上下⽂：
// Before: 47 次  Read() = 700 KB
// After: 1 次  ctx_execute() = 3.6 KB
ctx_execute("javascript", `
  const files = fs.readdirSync('src').filter(f => f.endsWith('.ts'));
  files.forEach(f => {
    const lines = fs.readFileSync('src/' + f, 'utf8').split('\\n').length;
    console.log(f + ': ' + lines + ' lines');
  });
`);
CodeBuddy ⽣成并运⾏脚本，只把结果（⼏⾏⽂字）放进上下⽂，⽽不是把  47 个⽂件的内
容全部读进来。
````

## PDF 第 21 页

[原页](RAW.pdf#page=21)

````text
能⼒四：不⼲预输出格式context-mode 只管数据往哪⾛，不管  CodeBuddy 怎么回答。如果
你同时装了  Caveman ，两者各管各的，不冲突。
安装（ CodeBuddy 插件市场直装）
npm install -g context-mode
重启  CodeBuddy 后⽣效。
验证
/context-mode:ctx-doctor
所有项显示 [x] 即正常。
常⽤命令
/context-mode:ctx-stats    # 查看节省统计，按⼯具分类
/context-mode:ctx-insight  # 打开本地分析看板（ 90 个指标）
四个压缩⼯具⼀览
⼯具互补，不互斥。从左到右压缩复杂度递增：
⼯具 压缩什么 典型节省 装法
RTK 终端命令输出  →  上
下⽂ 89%
brew install rtk
 + rtk init -g（ CodeBuddy
⽤  Fork 版）
Caveman AI 回复输出 65–75% install.sh
（ CodeBuddy ⽤  Fork 版）
headroom 所有进上下⽂的内容47–92%
pip install headroom-ai
[all]
  （ CodeBuddy ⽤  Fork 版）
context-mo
de
MCP ⼯具结果  + 会话
连续性
98% （⼯具输
出）
npm install -g context-
mode
（ CodeBuddy ⽤  Fork 版）
最低成本起点：先装  RTK + Caveman ，五分钟，⽴即⻅效。有时间再评估  headroom 和
context-mode 。
说明：如需在  CodeBuddy 中使⽤，可使⽤  studyzy Fork 版（已增加  CodeBuddy ⽀
持）。
````

## PDF 第 22 页

[原页](RAW.pdf#page=22)

````text
第五章  代码图谱：让  AI 不再盲搜
前⼀层压的是 “ 已经进来的东⻄ ” 。这⼀层解决的是另⼀类浪费：本来就不该读进来的东⻄。
5.1 真正贵的是 “ 找代码 ” ，不是 “ 读代码 ”
上下⽂窗⼝够⼤，不代表不需要图谱。
项⽬越⼤， AI 越容易陷⼊⼀个循环：
grep ⼀圈找⼊⼝
→ 读⼏个⽂件找关系
→ 发现漏了⼀个
→ 再  grep ⼀圈
→ 反复⼏轮才定位到
这个过程消耗⼤量  Tool Call 和上下⽂，⽽且结果还不⼀定准确。
代码图谱解决的是：让  AI 在动⼿读⽂件之前，就知道该读哪⾥。
5.2 Graphify ：把代码库变成可查询的知识地图
Graphify 在  2026 年  4 ⽉发布，短时间内  GitHub stars 超过  22k 。
核⼼机制：⽤  Tree-sitter 解析代码构建知识图谱， AI 查图⽽不是反复读⽂件。
官⽅数据：⽐直接读⽂件减少  71.5 倍  Token 消耗。
安装和使⽤
# 安装
uv tool install graphifyy
# 或
pipx install graphifyy
# 注册到  CodeBuddy
graphify install --platform codebuddy
# 或
graphify codebuddy install
在  CodeBuddy ⾥执⾏ /graphify，⾃动扫描项⽬并⽣成三份产物：
> /graphify
````

## PDF 第 23 页

[原页](RAW.pdf#page=23)

````text
Building knowledge graph...
  Parsed 247 files (TS/Prisma)
  Found 1,832 symbols, 4,217 edges
  Detected 14 communities (clusters)
  Generated:
    - graphify-out/graph.html           ←  交互式可视化
    - graphify-out/GRAPH_REPORT.md     ←  ⾃然语⾔报告
    - graphify-out/graph.json           ←  AI 查询⽤的数据
后续问跨⽂件问题时， AI 读 graphify-out/graph.json，⽽不是反复  grep 源码：
> 我想在  /api/v1/comments 加⼀个  PATCH 接⼝。
> 列出会受到影响的所有中间件、 Prisma model 、和测试⽂件。
影响分析（基于知识图谱）：
中间件链：
  - middleware/auth.ts → optionalAuth → requireAuth
  - middleware/rate-limit.ts （ commenting 路径  30/min 限制）
Prisma model ：
  - Comment （直接修改）
  - User （通过  authorId 关联）
  - Mention （通过  commentId 关联， PATCH 后需要重算）
测试：
  - tests/comments.test.ts
  - tests/integration/registration.test.ts （间接依赖）
不⽤图谱时，同样问题经常要靠多轮  grep 和补读⽂件来兜底，遗漏关键路径并不少⻅。⽤
图谱后，定位和影响分析会稳定得多，尤其适合跨⽂件问题。
⽀持范围
30+ 种语⾔： Python 、 TypeScript 、 Go 、 Rust 、 Java 、 C/C++ 、 Ruby 、 C# 、 Kotlin 等
多模态： SQL schema 、 Markdown ⽂档、 PDF 、图⽚（通过  LLM 提取语义）
增量更新： git hook 触发，每次  commit ⾃动重建
与  CodeGraph 的区别
CodeGraph 是另⼀个⽅向的⼯具，基于  MCP Server + 持久化图数据库（ Neo4j/KuzuDB ），
对  7 个真实开源仓库做了完整  benchmark （ Claude Opus 4.8 ， 2026-06-02 验证）：
平均数据： 16% 更低成本、 47% 更少  Token 、 58% 更少  Tool Call 、 22% 更快。
分仓库明细：
````

## PDF 第 24 页

[原页](RAW.pdf#page=24)

````text
代码库 语⾔ 成本 Tokens ⼯具调⽤
VS Code TypeScript -18% -64% -81%
Excalidraw TypeScript 持平 -25% -40%
Tokio Rust 持平 -38% -57%
Django Python -8% -60% -77%
Gin Go -19% -23% -44%
OkHttp Java -25% -54% -50%
Alamoﬁre Swift -40% -64% -58%
注意：收益和项⽬规模、语⾔强相关。 Rust/TypeScript ⼤型项⽬收益最显著， Java/Go 较⼩
项⽬收益相对有限。
CodeGraph 安装：
# npm 安装
npm i -g @colbymchenry/codegraph
# 初始化项⽬
cd your-project
codegraph init -i
⼿动配置  CodeBuddy ：
// ~/.codebuddy/.mcp.json
{
  "mcpServers": {
    "codegraph": {
      "type": "stdio",
      "command": "codegraph",
      "args": ["serve", "--mcp"]
    }
  }
}
核⼼⼯具：
codegraph_context：找⼊⼝点和关键符号（第⼀跳）
codegraph_trace：追调⽤路径（含动态派发）
codegraph_impact：重构前影响分析
选哪个：个⼈项⽬、快速上⼿  →  Graphify （ Skill 形态，零配置）。团队、⼤型仓库、需要
持久化查询  →  CodeGraph （ MCP 服务器，功能更完整）。
````

## PDF 第 25 页

[原页](RAW.pdf#page=25)

````text
第六章  多  Agent 协作：边界清晰时， CodeBuddy 会更省  Token
前两层解决的是 “ 单个上下⽂怎么更省 ” 。这⼀层继续往前⾛：别让所有任务都挤进同⼀个上
下⽂。
换句话说，前⾯讲的是 “ 单个会话怎么省 ” ，这⾥讲的是：多个  Agent 怎么分⼯协作，才能在
任务边界清晰时更省。
CodeBuddy 本身就⽀持  subagent 调度、 worktree 隔离、 Skill 绑模型 —— 不需要⾃⼰写
Orchestrator ，⽤好内置能⼒就够了。
6.1 单  Agent 为什么越⽤越贵
复杂项⽬⾥，单  session 很容易演变成这样：
规划、写代码、跑测试、 Code Review 全在⼀个会话
上下⽂越积越⻓（所有历史都往⼀个  session ⾥塞）
所有任务⽤同⼀个模型配置，便宜活也⽤最贵模型
职责越混，上下⽂越胖，成本越⾼。
6.2 subagent ：任务隔离的最低成本⽅式
CodeBuddy 的  Skill ⾥可以直接调⽤  Agent tool ，把⼦任务分发出去：
1 使⽤  Agent tool 分析这个  PR 的影响范围，
2 然后把结果返回给我，不需要读具体实现⽂件。
每个  subagent 都应该有独⽴的上下⽂边界 —— 它只看到⾃⼰需要的内容，主  session 只看到
结果。前提是⼦任务真的能拆开；如果每个  Agent 都要重复读同⼀批背景，拆得越多，反⽽
越贵。
典型分⼯：
1 主  session （规划  + 决策）
2   ├── subagent A ：影响分析（只看图谱，不读源码）
3   ├── subagent B ：写实现（只看相关⽂件）
4   └── subagent C ：跑测试  + ⽣成报告
与前⽂  3.5 的连接： subagent 可以单独绑定便宜模型。规划⽤强模型，执⾏⽤便宜模型，两
者在不同  session ⾥，互不⼲扰。
````

## PDF 第 26 页

[原页](RAW.pdf#page=26)

````text
6.3 Orchestrator-Worker 模式：把多  Agent 协作变成⼯程
前⾯⼏节讲的是 " 怎么给单个  Agent 减负 " 。这⼀节讲更进⼀步的思路：⽤  Orchestrator-
Worker 模式，把⼀个臃肿的⻓任务变成⼀个有分⼯的流⽔线。
核⼼思路：
Orchestrator （协调器  Agent ）
  ├── 负责规划、拆解、调度、汇总
  ├── 不亲⾃读⼤量⽂件，不亲⾃跑命令
  └── 只负责决策
Worker （⼦  Agent ，按需派遣）
  ├── 每个  Worker 只做⼀件事
  ├── 只看⾃⼰需要的上下⽂
  └── 做完了把结果交回
为什么这个模式能省  Token ？
⼀个单  Agent 处理复杂任务时，它必须同时承载规划、代码阅读、⼯具调⽤、⽣成、验证的
所有上下⽂ —— 哪怕它当前正在做的只是 " 改⼀个函数 " 。 Orchestrator-Worker 模式的本质，
是让每个  Agent 只看和当前步骤相关的内容，⽽不是把整个任务的所有背景都塞进每⼀次调
⽤。
⼀个典型的成本对⽐：
单  Agent 全程跑：
  System Prompt(5K) + 历史 (120K) + 规划 (10K) + 代码 (50K) + ⼯具结果 (30K)
  = 215K tokens × N 轮
Orchestrator + Worker 分⼯：
  Orchestrator 轮次： System Prompt(5K) + 任务状态 (2K) + 规划 (3K) = 10K tokens
  Worker A 轮次：⽬标 (1K) + 相关⽂件 (8K) + ⼯具结果 (5K) = 14K tokens
  Worker B 轮次：⽬标 (1K) + 测试⽂件 (6K) + 前步结果 (3K) = 10K tokens
  同样完成任务，每轮成本压缩  5-10 倍
具体分⼯的⼀个真实例⼦ ——" 修复  API 层  Bug + 补测试  + 写变更说明 " ：
Orchestrator （强模型）
  ├── 分析任务，⽣成⼯作计划到  .agent/plan.json
  ├── 派出  Worker A ：定位  Bug （只给图谱和⼊⼝⽂件）
  ├── 派出  Worker B ：修复代码（只给有  Bug 的那⼏个⽂件）
  ├── 派出  Worker C ：补单测（只给修复后的⽂件  + 现有测试）
  └── 派出  Worker D ：写  changelog （只给  git diff + 模板）
每个  Worker ：
````

## PDF 第 27 页

[原页](RAW.pdf#page=27)

````text
  - 独⽴上下⽂，完成即销毁
  - 绑定便宜模型（如  DeepSeek ）
  - 并⾏执⾏（ C 和  D 可以同时跑）
  - 结果写⼊共享⽂件， Orchestrator 汇总
在  CodeBuddy ⾥，这个模式可以通过  Agent tool 直接实现 ——Orchestrator 在主  Skill 或会话
⾥运⾏，通过 Agent tool 分发⼦任务：
使⽤  Agent tool 执⾏以下⼦任务，上下⽂独⽴，不需要继承当前历史：
⽬标：定位  src/api/order.go ⾥的  CreateOrder Bug
上下⽂：只读  src/api/order.go 和  src/model/order.go
输出：把  Bug 描述和⽂件⾏号写⼊  .agent/findings.md
6.4 上下⽂隔离之后，数据怎么流转
这是  Orchestrator-Worker 模式最绕不开的问题：
答案：通过共享外置⽂件，不通过会话历史。
会话历史是每个  Agent 私有的，不同  Agent 的历史⽆法互通。但⽂件系统是共享的。这意味
着上下⽂隔离和信息共享可以同时成⽴：
Agent A 完成⼯作
  → 把结果写⼊⽂件（ .agent/step1_result.json ）
  → 上下⽂销毁
Agent B 开始⼯作
  → 读取⽂件（ .agent/step1_result.json ）
  → 只看这个⽂件，不看  A 的历史
  → 把⾃⼰的结果写⼊  .agent/step2_result.json
这个模式有⼏个关键设计原则。
原则⼀：输出格式要结构化。  ⾃然语⾔在  Agent 之间传递时容易产⽣歧义，也难以精确定
位所需信息。结构化的  JSON 更紧凑、更可靠，下游  Agent 只需要读它关⼼的字段：
// .agent/findings.md → 改为  .agent/findings.json
{
"task": "locate-bug",
"status": "completed",
"findings": [
上下⽂既然隔离了， Agent 之间怎么传递信息？
````

## PDF 第 28 页

[原页](RAW.pdf#page=28)

````text
    {
      "file": "src/api/order.go",
      "line": 142,
      "issue": " 并发场景下  inventory.Lock() 未释放 ",
      "severity": "high"
    }
  ],
"next_step": "fix-bug",
"context_needed": ["src/api/order.go:120-165", "src/model/inventory.go:30-55"]
}
下游  Agent 收到的指令⾥只需要包含：
读取  .agent/findings.json ，针对其中的  findings 数组修复代码。
修复完成后将结果写⼊  .agent/fix_result.json ，格式参考  .agent/findings.json 。
原则⼆：⽤进度⽂件追踪状态。 复杂任务⾥， Orchestrator 需要知道每个步骤是否完成、是
否失败、是否需要重试。这个状态本身也应该外置：
// .agent/progress.json
{
"task_id": "fix-order-bug-20260609",
"created_at": "2026-06-09T10:00:00Z",
"steps": [
    {
      "id": "step-1-locate",
      "status": "completed",
      "worker": "investigator",
      "output_file": ".agent/findings.json",
      "completed_at": "2026-06-09T10:02:30Z"
    },
    {
      "id": "step-2-fix",
      "status": "in_progress",
      "worker": "implementer",
      "started_at": "2026-06-09T10:02:35Z"
    },
    {
      "id": "step-3-test",
      "status": "pending",
      "depends_on": "step-2-fix"
    },
    {
      "id": "step-4-changelog",
      "status": "pending",
      "depends_on": "step-2-fix"
````

## PDF 第 29 页

[原页](RAW.pdf#page=29)

````text
    }
  ]
}
Orchestrator 每次唤醒时，只需要读这⼀个⽂件就能知道任务进展。不需要回放任何  Agent
的历史会话。
原则三：每个  Worker 的  context 包精⼼裁剪。  新开⼀个  Worker 时， Orchestrator 应该明确
告诉它 " 只读哪些东⻄ " ，⽽不是让  Worker ⾃⼰去探索：
# Orchestrator 派遣  Worker 时的指令模板
任务：为  CreateOrder 修复编写单元测试
上下⽂：
  - 修复内容：读  .agent/fix_result.json 中的  diff 字段
  - 现有测试⻛格：读  src/api/order_test.go （前 50 ⾏）
  - 不需要读其他⽂件
输出：
  - 新增测试写⼊  src/api/order_test.go
  - 把测试覆盖情况写⼊  .agent/test_result.json
约束：
  - 只修改  order_test.go ，不动其他⽂件
  - 测试不超过  80 ⾏
这个指令本身很短（约  150 tokens ），但它让  Worker 的上下⽂精准到最⼩必要集合。
原则四：临时⽂件及时清理。.agent/ ⽬录是临时⼯作区，任务完成后可以归档或删除：
# 任务完成后归档
mv .agent/ .agent-archive/fix-order-bug-20260609/
# 或直接清理
rm -rf .agent/
这样不会污染代码仓库，也不会把旧任务的上下⽂意外带⼊新任务。
6.5 并⾏执⾏：时间和成本同时压
Orchestrator-Worker 模式的另⼀个收益是并⾏。
独⽴的⼦任务可以同时启动，不需要等待。 CodeBuddy 的  Agent tool ⽀持在⼀次  tool call ⾥
发出多个并⾏指令：
````

## PDF 第 30 页

[原页](RAW.pdf#page=30)

````text
同时启动以下两个独⽴任务（使⽤  Agent tool 并⾏调⽤）：
任务  A ：为修复后的代码写单元测试
  - 读  .agent/fix_result.json
  - 读  src/api/order_test.go
  - 输出  .agent/test_result.json
任务  B ：⽣成本次变更的  changelog 条⽬
  - 读  .agent/fix_result.json 中的  diff 字段
  - 参考  CHANGELOG.md 的格式
  - 输出  .agent/changelog_entry.md
两个  Worker 同时跑，各⾃只看⾃⼰需要的⽂件，没有上下⽂重叠。时间上并⾏，成本上独
⽴，互不⼲扰。
实际加速效果取决于任务数量和独⽴性：
并⾏  Worker 数 实际加速倍数
2 个 1.5–1.8 倍
3 个 2.2–2.6 倍
4 个 2.8–3.4 倍
理论上  N 个并⾏就是  N 倍，实际略低，原因是  Orchestrator 本身有启动 / 汇总开销，以及
Worker 间有时有轻微的  I/O 竞争。但即便  50% 的并⾏效率，也意味着  4 个任务只花不到  2
个串⾏任务的时间。
什么样的任务适合并⾏：
✅  适合并⾏：
  - 不同模块的  Bug 修复（改的⽂件没有交集）
  - 代码  + 测试  + ⽂档（三者可以同时⽣成）
  - 多个⽂件的格式化 / 重构（⽆依赖关系）
  - 影响分析  + 实现⽅案设计（可以同时推进）
❌  不适合并⾏：
  - 有顺序依赖的步骤（先定位  Bug 才能修复）
  - 修改同⼀个⽂件的多个任务（会产⽣冲突）
  - 依赖上⼀步输出的任务（需要等待）
6.6 完整的编排流程：⼀个端到端示例
把上⾯三节串起来，看⼀个完整的端到端示例。
场景：给⼀个中型  Go 项⽬做  API 层重构 —— 把分散的错误处理统⼀改成标准  Error
Wrapper ，同时补充缺失的单测，⽣成⼀份重构报告。
````

## PDF 第 31 页

[原页](RAW.pdf#page=31)

````text
如果⽤单  Agent ：
整个任务在⼀个  session ⾥跑
→ 随着轮次推进，历史越来越⻓
→ 到第  10 轮已经带着  150K+ 的历史
→ 每⼀轮都重新处理同⼀批背景
→ 中途如果  /compact ，现场信息丢失
→ 总成本：约  800K–1.2M tokens
⽤  Orchestrator-Worker 编排：
阶段  0 ：初始化
  Orchestrator 读  graph.json ，分析影响范围
  → ⽣成  .agent/plan.json （步骤、⽂件列表、依赖关系）
  → Orchestrator 本轮消耗： ~8K tokens
阶段  1 ：分析（并⾏）
  Worker A ：扫描每个  API ⽂件，找出⾮标准错误处理，结果写  .agent/audit.json
  Worker B ：读现有测试，评估覆盖率缺⼝，结果写  .agent/test_gap.json
  → 两个  Worker 同时跑，各⾃消耗： ~12K tokens
  → 总消耗（并⾏）： ~12K tokens ，耗时约  1 个  Worker 的时间
阶段  2 ：实现（可并⾏）
  Worker C ：按  .agent/audit.json 逐⽂件替换  Error Wrapper （每次只处理⼀个⽂件）
  → 每次消耗： ~6K tokens × ⽂件数
阶段  3 ：补测（串⾏，依赖阶段  2 ）
  Worker D ：读修改后的⽂件  + .agent/test_gap.json ，补测试
  → 消耗： ~10K tokens
阶段  4 ：汇总（并⾏）
  Worker E ：⽣成重构报告（读  .agent/audit.json + git diff ）
  Worker F ：⽣成  PR 描述（读  .agent/plan.json + .agent/ 各结果⽂件）
  → 两个  Worker 同时跑： ~8K tokens
总消耗估算：约  100K–150K tokens （⽐单  Agent 节省  70-85% ）
成本差异来源很直接：
1. 每个  Worker 只看当前步骤的相关内容，不带全程历史
2. 便宜模型处理执⾏任务，强模型只⽤于规划和决策
3. 并⾏减少时间成本，等待时间从串⾏叠加变成并⾏中最⻓的那个
4. 进度⽂件替代会话历史， Orchestrator 不需要回放所有轮次
````

## PDF 第 32 页

[原页](RAW.pdf#page=32)

````text
到这⾥，这篇⽂章真正想建⽴的⼼智模型其实也可以浓缩成⼀句话：不要只想着把单次回答
压短，更要想办法让系统少把同⼀批背景反复搬进来。
第七章  误区：很多 " 优化 " 其实在加成本
误区⼀：上下⽂越多越好。上下⽂越多不⼀定越准，但通常越贵。噪⾳越多，模型越容易分
神。该读哪个⽂件，⽐读多少⽂件更重要。
误区⼆： MCP 越多越强。⼯具堆得越多，选择空间越⼤、决策越慢、错误调⽤概率越⾼。
低频⼯具⻓期挂载，贡献的更多是成本。
误区三：所有  Agent 都上最强模型。这不叫优化质量，叫放弃路由。每个环节默认最贵模
型，系统⾥就没有 “ 资源分配 ” ，只有 “ 直接烧钱 ” 。
误区四：聊天记录当⻓期记忆。⻓会话⽅便，但不是记忆系统。⻓期依赖会话承载全部背
景，最终成本越来越⾼，关键信息越来越难提取。
误区五：只看单价不看总成本。便宜模型如果导致更多重试、更多搜索、更多上下⽂回填，
总成本未必更低。真正该看的是完成⼀次任务的总成本。
误区六： Prompt 越短越好。压缩时丢掉了必要的  few-shot 或格式说明，导致第⼀次输出不
合格，反复重试。压缩要精准，不是⼀味缩短。
第⼋章  结语
全⽂核⼼只有⼀句话：
AI Agent 成本优化
本质不是让你少问⼀句话
⽽是让系统少重复做⽆效⼯作
压成公式：
更低成本
=
更少重复上下⽂（ RTK 、 Caveman 、 headroom 、 context-mode 、会话管理）
+ 更合理模型路由（任务匹配、 Skill 绑模型）
+ 更精准代码检索（ Graphify 、 CodeGraph ）
+ 更清晰  Agent 分⼯（ subagent 隔离、 worktree 并发、记忆外置）
⾏动清单
今天就能做
````

## PDF 第 33 页

[原页](RAW.pdf#page=33)

````text
/clear 切断⽆关历史，⼀个  Session ⼀件事
⻓会话及时  /compact，别让历史变包袱
指定输出格式，减少废话和重试
清点  Skill 和  MCP ，低频的卸掉或按需加载
能  CLI 就先  CLI ，别过度⼯具化
引⽤⽂件时⽤  @ 路径，不要只写⽂件名让  AI 去搜索
意图⼀次说完，避免聊天式拆碎指令
这周能做
按任务给模型分档：复杂任务⽤强模型，简单任务⽤便宜模型
给常⽤  Skill 、 Agent 、命令绑定默认模型
安装  RTK ，先压测试、 git 、搜索这类⾼频命令输出
需要更短回复时启⽤  Caveman ，压掉输出端废  Token
评估  Graphify 或  CodeGraph ，先让  Agent 知道该读哪⾥
这个⽉能做
把稳定前缀做成缓存友好结构，减少前缀抖动
评估  headroom 或  context-mode ，控制更⼤规模的上下⽂输⼊
建代码图谱、 Summary 、 Memory 等外置记忆层
把规划、实现、验证、 Review 拆成边界清晰的多  Agent ⼯作流
⽤  Orchestrator-Worker 模式处理复杂任务：协调器负责规划，⼦  Agent 只看当前步骤所
需上下⽂
建⽴ .agent/ ⽬录约定：⽤结构化  JSON ⽂件传递  Agent 间数据，⽤  progress.json 
追踪任务进度识别可并⾏的独⽴⼦任务，利⽤  Agent tool 并⾏调⽤压缩时间成本
给  Token 、成本、重试率、⼯具调⽤次数建观测⾯板
参考资料
[1] OpenAI ，《提示词缓存  | OpenAI API 》
[2] Anthropic ，《 Token-saving updates on the Anthropic API 》
````

## PDF 第 34 页

[原页](RAW.pdf#page=34)

````text
阅读 1 . 3 万
[3] OpenAI ，《使⽤  GPT-5.5 | OpenAI API 》
[4] Google AI for Developers ，《 Thinking 》
[5] Anthropic ，《 Prompt caching 》
[6] RTK （ Rust Token Killer ） GitHub
[7] Caveman GitHub
[8] Caveman 论⽂： Brevity Constraints Reverse Performance Hierarchies
[9] Graphify GitHub
[10] CodeGraph GitHub
[11] headroom GitHub
[12] context-mode GitHub
留⾔
写留⾔
````

## PDF 第 35 页

[原页](RAW.pdf#page=35)

````text
还没有留⾔，来写⾸评
````

