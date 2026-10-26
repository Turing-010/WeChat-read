# 从一次 LLM 调用到完整 Harness，Agent 到底经历了什么？

> 来源：[RAW.pdf](RAW.pdf)；公众号：腾讯技术工程；作者：ivanxxie、davoszhang。
> 本文件为PDF文本层转写，按物理页码排列；保留提取字符。图片未嵌入，表格与代码布局可能有损失，请对照各页PDF。缺失、裁切及附件问题不会根据上下文补写；转写完成不代表原文完整核验通过。

> 原始材料已记录的质量问题：
> - PDF原文地址、采集时间和显示时间的时区未确认；外部事实及在线原文一致性未核查。；核验状态：unverified

## PDF第1页

[查看原始页面](RAW.pdf#page=1)

从⼀次 LLM 调⽤到完整 Harness，Agent 到底经历了什么？

原创 腾讯程序员 腾讯技术⼯程 Sep 7, 2026, 2:36 AM ⼴东 1063 listened

作者：ivanxxie、davoszhang

今天的 Agent 系统看起来很像⼀套⼩型操作系统：它们管理⼦ Agent 进程，维护长期记忆⽂
件，通过⼯具驱动接触外部世界，还要处理权限、隔离、恢复和观测。可它们的起点并不宏
⼤。最初，开发者⼿⾥只有⼀个把输⼊映射为输出的语⾔模型。

复杂性并不是⼀次设计出来的。每当模型试图越过⼀次调⽤的边界，系统就必须在模型外⾯增
加⼀个新部件：模型不知道此前聊了什么，于是出现上下⽂；模型⽆法改变世界，于是出现⼯
具；⼀次⼯具调⽤解决不了任务，于是出现循环；上下⽂装不下历史，于是出现记忆；循环开
始产⽣真实副作⽤，于是出现权限与沙箱；⼀个循环不够并⾏，于是出现⼦ Agent...

从⼀次模型调⽤到 Agent

LLM

最朴素的⼤语⾔模型接⼝可以被看成⼀个函数：输⼊⼀段 token，输出另⼀段 token。它可以
在参数中编码世界知识，却不会天然记住某个⽤户上⼀轮说过什么，也不知道⾃⼰刚刚输出的
命令是否被执⾏。

### 2020 年，GPT-3 展⽰了⼤规模语⾔模型仅通过⽂本提⽰完成多种任务的能⼒；2022 年底，
GPT-3.5 成为 ChatGPT 背后的模型；2023 年 2 ⽉，Meta 发布 LLaMA，推动开放权重模型
进⼊主流研究与本地部署。GPT、LLaMA 以及后来出现的 Claude、Gemini、Qwen 等模型虽
然能⼒不同，但在应⽤看来仍然共享同⼀个基本形态：接收上下⽂，predict next token。
`````text

   answer = LLM(question)
`````

> 本页含图像对象，未嵌入转写文件；图内文字及版面细节请查看本页PDF。

## PDF第2页

[查看原始页面](RAW.pdf#page=2)

最初的系统只有⼀次前向调⽤。模型负责⽣成⽂本，应⽤只负责把问题送进去、把答案显⽰出
来。模型参数⾥的知识来⾃训练；⼀次对话中的名字、偏好和任务状态，则必须由应⽤在每次
调⽤时重新提交。模型本⾝并没有⼀个不断增长的⽤户档案。

Q&A Bot

Q&A Bot 的第⼀项⼯程进步，不是换了⼀个更聪明的模型，⽽是在模型前⾯增加⼀个上下⽂
装配层。它把系统指令、⽤户当前输⼊和对话历史拼成⼀次请求。

在 GPT-3 时代，许多应⽤仍然把模型包装成单轮问答接⼝；2022 年 11 ⽉，ChatGPT 把多轮
对话带给⼤众，开发者开始普遍维护 System Prompt、User Prompt 和 Chat History。模型没
有突然获得跨轮记忆，是聊天应⽤在每次请求前重新装配了历史。
`````text

  working_context = [
    system_prompt,
    recent_chat_history,
    user_prompt
  ]

  answer = LLM(working_context)
`````

Working Memory 不是长期存储，⽽是这⼀轮真正提交给模型的全部上下⽂。

这⼀步看似只是字符串的拼接，却奠定了后⾯所有 Harness 的核⼼原则：模型看见的⼀切，
都是运⾏时系统为它构造出来的。运⾏时选择哪些历史进⼊上下⽂、哪些指令拥有更⾼优先

> 本页含图像对象，未嵌入转写文件；图内文字及版面细节请查看本页PDF。

## PDF第3页

[查看原始页面](RAW.pdf#page=3)

级、哪些内容必须被裁剪，都会改变 Agent 的⾏为。

ReAct

Bot 只需要回答⼀次，但 Agent 必须根据⾏动结果继续决策。2022 年提出的 ReAct 执⾏架构
把推理轨迹与动作交错起来：模型形成下⼀步意图，执⾏外部动作，接收 Observation，再把
观察送回下⼀轮推理。

ReAct 论⽂于 2022 年 10 ⽉公开，并在 ICLR 2023 发表。它把此前分别讨论的 Chain-of-
Thought 与外部⾏动连接成 Thought → Action → Observation 循环。2023 年⼤量早期 Agent
项⽬沿⽤了这⼀模式，Agent 也由“⼀种提⽰词技巧”逐渐变成了⼀个需要程序持续驱动的执⾏
循环。

Agent 真正的分⽔岭不是“会思考”，⽽是建⽴了 模型 → 动作 → 环境 → 观察 → 模型 的闭
环。
`````text

  while not finished:
      response = model(context)
      if response.has_action:
          observation = environment.execute(response.action)
          context.append(response.action, observation)
      else:

          return response.answer
`````

这个 while 循环就是最早的 Agent Runtime。模型仍然只⽣成 token，真正负责“继续运⾏”
的是模型外⾯的程序。它必须解析模型输出、判断是否结束、调⽤环境并把结果重新写⼊上下
⽂。

今天许多模型把内部推理隐藏起来，但这不改变系统结构，运⾏时仍然需要识别模型给出
的动作、执⾏动作，并把环境反馈送回模型。

> 本页含图像对象，未嵌入转写文件；图内文字及版面细节请查看本页PDF。

## PDF第4页

[查看原始页面](RAW.pdf#page=4)

Tool Calling

早期 Agent 常让模型输出类似 Search\[Wikipedia\] 的⽂本，再由程序⽤正则表达式解析。这种
⽅式很灵活，也很脆弱，格式可能漂移，参数可能缺失，模型还可能把解释⽂字混进命令。

### 2022 年的 ReAct 主要依赖约定格式表达动作；2023 年 6 ⽉，OpenAI 发布 Function
Calling，⼯具名和参数开始成为模型 API 的结构化输出；2024 年 11 ⽉，Anthropic 发
布 MCP，进⼀步尝试标准化 Agent 与外部数据源、⼯具服务之间的连接。

结构化 Tool Calling 改变了这件事。⼯具通过 schema 注册，模型输出带有⼯具名、调⽤ ID
和参数的结构化对象；运⾏时验证参数、选择实现、执⾏调⽤，再把结果以 Tool Result
Message 的⾝份放回上下⽂。2023 年 OpenAI 的 Function Calling 是这⼀机制⾛向主流 API
的重要节点。

Tool Router 把“模型想做什么”翻译为确定的程序调⽤；Tool Result Message 再成为下⼀轮模
型输⼊的⼀部分。

Tool Schema：描述⼯具名称、⽤途、参数类型与约束，让模型知道动作空间。

Tool Router：根据名称找到实现，验证参数，并把⼀次模型输出变成⼀次程序调⽤。

Tool Result：携带调⽤ ID、状态与返回值，保证观察可以准确对应到原始动作。

从这⼀刻开始，Agent 不再只是“⽣成看起来像命令的⽂本”，⽽是获得了⼀套可验证、可路
由、可审计的动作协议。后来的⽂件⼯具、终端、浏览器、数据库、MCP，本质上都在扩展
这个协议。

Memory

Agent Loop 解决了“如何连续⾏动”，却没有解决“如何跨会话积累”。完整历史会越来越长，
⽽上下⽂窗⼝始终有限。系统不得不把过去拆成两个空间：⼀个是本轮模型可见的 Working
Memory，另⼀个是模型外部可持久化、可检索的 Long-term Memory。

### 2020 年的 RAG 已经清楚地区分了模型参数中的知识与外部可检索知识；2023 年
的 MemGPT ⼜借⽤操作系统的分层存储思想，在有限上下⽂与外部存储之间调度信息。此

> 本页含图像对象，未嵌入转写文件；图内文字及版面细节请查看本页PDF。

## PDF第5页

[查看原始页面](RAW.pdf#page=5)

后，记忆从“检索⼏段⽂档”逐渐扩展到摘要、⽤户偏好、会话归档、技能⽂件和后台知识整
理。

这是⼀张逻辑化能⼒图。不同 Harness 会采⽤⽂件、数据库、全⽂检索、向量检索或摘要等
不同组合，⽽不是都实现完全相同的模块。

程序记忆（Procedural）：技能、习惯、操作流程和⽤户约定，典型载体是规则⽂件或 SKIL
L.md 。

语义记忆（Semantic）：稳定事实、概念、偏好与项⽬知识，常通过摘要、全⽂索引或向量检
索进⼊上下⽂。

情景记忆（Episodic）：某次任务发⽣了什么、采取了哪些动作、结果如何，通常来⾃会话⽇
志与事件轨迹。

这⾥真正困难的不是存储，⽽是写⼊与读取策略：什么值得保存？何时合并重复事实？怎样处
理互相冲突的记忆？检索多少条才不会挤压当前任务？错误记忆如何被纠正？因此，记忆系统
很快⼜会长出提炼、整合、门控与反思流程。

当能⼒变多，Agent 外⾯出现了 Harness

> 本页含图像对象，未嵌入转写文件；图内文字及版面细节请查看本页PDF。

## PDF第6页

[查看原始页面](RAW.pdf#page=6)

到这⾥，我们已经拥有上下⽂、循环、⼯具和记忆。但只要系统开始承担真实⼯作，⼀批新的
⼯程问题就会同时出现。

2023 年的许多 Agent 原型仍把 Prompt、Loop 和 Tools 写在⼀个应⽤⾥；2024 年，MCP 开
始统⼀外部连接协议；到 2025 年，Claude Code 和开源的 Codex CLI 把终端 Agent 推向真
实软件⼯程场景。随着任务变长、副作⽤变强、客户端变多，Agent Loop 外围的会话、权
限、沙箱、事件和扩展机制逐渐凝结成独⽴的 Harness 层。

会话能否恢复：程序崩溃或⽤户退出之后，循环必须从⼀致的状态重新开始。

副作⽤是否安全：命令、写⽂件、⽹络访问不能只依赖模型“⾃觉”。

上下⽂如何压缩：长任务需要保留关键事实，同时释放上下⽂窗⼝。

客户端如何连接：TUI、IDE、桌⾯端、Web 与 SDK 需要观察同⼀个运⾏状态。

扩展如何装配：⼯具、MCP、Skills、Hooks 和配置需要确定的发现与加载机制。

任务如何并⾏：⼦ Agent 要拥有隔离的上下⽂、权限、历史与⽣命周期。

于是 Agent Loop 不再直接⾯对所有东西。它被包进⼀个更⼤的运⾏时，由这个运⾏时负责装
配资源、管理会话、约束⼯具、持久化事件、暴露 API，并在多个 Agent 之间调度任务。这⼀
层就是本⽂所说的 Agent Harness。

Agent 决定下⼀步做什么；Harness 决定这⼀步在什么上下⽂、权限、⽣命周期与持久
化规则下发⽣。

下⾯的四个项⽬共享 Agent Loop、Tool Calling 和 Context Assembly 这些基本能⼒，却选择
了不同的演化⽅向。我将把它们依次展开，可以看到 Harness 的设计空间。

Pi：先把最⼩ Harness 看清楚

同⼀个模型，只是换了⼀套 Harness，结果能差多少？测评机构 Composio 把 DeepSeek V4
Flash 分别放进 Pi Agent、Prime Agent、Deep Agents 和 Hermes Agent，跑了同⼀批 30 个
Agentic Tasks。Pi 的通过率是 66.7%，中位任务成本只有 0.012 美元。在这组测试⾥，它完
成得最多，也花得最少。

## PDF第7页

[查看原始页面](RAW.pdf#page=7)

模型没有换，Harness ⼀换，模型能看到的上下⽂、⾛过的⼯具路径、循环的轮数和停⽌条件
都会跟着变。

Databricks 的内部基准 ⼜把这个问题放进更接近⽣产环境的坐标系。他们从⼯程师真实 PR 构
造任务，在覆盖 Python、Go、TypeScript、Scala 等语⾔的数百万⾏代码库上，⽐较单任务
平均成本和整体通过率。图⾥的红⾊虚线是 Pareto 前沿，Pi 占据多段。Opus 4.8 搭配 Pi 的
xhigh 设置接近 90%，GLM 5.2 搭配 Pi 也进⼊最⾼能⼒梯队。更有意思的是，部分同模型、
同推理强度换到 Pi 后，质量基本不变，单任务成本却能相差两倍以上。Databricks 追踪发
现，Pi 每轮送⼊的上下⽂约少三倍，⼯作集更紧，也⽤更少轮次完成任务。

> 本页含图像对象，未嵌入转写文件；图内文字及版面细节请查看本页PDF。

## PDF第8页

[查看原始页面](RAW.pdf#page=8)

Pi 为什么能⼀边压低成本，⼀边把任务做对？Databricks 的运⾏轨迹给出的证明，是它尽量
不让模型反复阅读⽆关内容。Pi 默认只暴露 read 、 write 、 edit 、 bash 四个⼯具，
Resource Loader 显式装配当前会话启⽤的指令、Skills 和 Prompt Templates，Session
Manager 再⽤活动分⽀和 Compaction 把完整会话投影成更紧的 Working Memory。这样⼀
来，每轮请求携带的上下⽂更少，历史噪声和⼯具描述也更少，模型便能⽤更少 token、更少
循环抵达结果。极简在这⾥不只是⼀种代码审美，它直接变成了任务成本和执⾏效率。

当然，⼩也有代价。Pi 当前不内置限制⽂件系统、进程、⽹络或凭证访问的权限系统，默认
继承启动它的⽤户权限。要把它放进⾼风险环境，还得⽤容器或外部沙箱补上边界。Pi 让我
们第⼀次看到从 Agent Loop 到极简 Harness 的跨越，它也是很多开源 Harness 框架魔改的
起点。

Resource Loader：在运⾏前装配资源

> 本页含图像对象，未嵌入转写文件；图内文字及版面细节请查看本页PDF。

## PDF第9页

[查看原始页面](RAW.pdf#page=9)

SYSTEM.md 、 AGENTS.md 、Skills 与 Prompt Templates 并不是由模型⾃⼰去磁盘⾥“感
知”的。Resource Loader 负责发现、解析并装配这些资源，再形成当前 Session 可使⽤的系
统上下⽂。资源加载因此成为⼀种显式的启动过程。

OpenCode：事件驱动的服务

在 OpenCode ⾥，⽤户看到的⼀段回复，在存储层并不是⼀整块⽂本。⼀次 Assistant
Message 下⾯可以同时挂着 Reasoning、Text、Tool、Step Start、Step Finish、Patch 和
Compaction 等 Part 组成的轨迹数据。模型想了什么、⼯具何时开始、补丁改了哪些⽂件、
上下⽂何时被压缩，都有各⾃的结构和⽣命周期。

为什么要把⼀轮回答拆得这么碎？OpenCode 保存的对象是 Agent 运⾏过的全过程。只要过程
可以被结构化记录，退出界⾯便不等于丢失现场，恢复 Session 也不再依赖重放终端字符。

这套运⾏从 Agent Profile 开始。源码中的 Agent.Info 不只包含 Prompt，还把模型、
Mode、Permission、步数与⽣成参数放进同⼀个配置对象。Build 和 Plan 是主 Agent，
General 和 Explore 是⼦ Agent，Compaction、Title、Summary 则是⽤户看不见的后台
Agent。同⼀个 Agent Loop 因⽽可以装载不同⾝份，每个⾝份拥有不同的⼯具边界与职责。

Agent Profile 决定此刻是谁在⼯作，Session Events 记录它做过什么，Compaction 决定
哪些过去还要继续被模型看见。

Profile 决定⾏为，Session Events 负责留下事实。Message 与 Part 的更新会驱动
Projector，把 Session、Message、Part 分别投影进 SQLite。长会话接近上下⽂上限时，隐
藏的 Compaction Agent 汇总较早的历史，并在 token 预算内保留近期 turns；旧⼯具输出还
可以被裁剪，压缩摘要与近期消息再组成下⼀轮 Working Memory。OpenCode 的记忆管理更
接近⼀条可重建的上下⽂管线，⽽不是额外外挂⼀个向量知识库。

在 2025 年前后的 Coding Agent 浪潮⾥，TUI、Web、桌⾯端和 SDK 开始共享同⼀套运⾏
时。OpenCode 的多客户端并⾮最关键的创新，它们是结构化状态带来的结果。不同界⾯只
需要提交请求并消费事件流，Agent 的⾝份、历史与执⾏进度仍由服务端 Session 统⼀管理。

这套设计也带来代价。⼀次看似简单的回复，现在需要维护 Agent 配置合并、权限组合、事
件顺序、数据库投影和压缩边界；Compaction、Title、Summary 还会引⼊额外的模型调⽤。
OpenCode ⽤更复杂的状态⼯程，换来 Session 可恢复、⾏为可审计、⼦ Agent 可隔离，以
及同⼀运⾏时被多种界⾯消费的能⼒。

## PDF第10页

[查看原始页面](RAW.pdf#page=10)

Agent Profile：同⼀个循环装载不同⾝份

Profile 不是⼀段换⽪ Prompt。它同时保存名称、描述、Prompt、模型、Mode、
Permission、⽣成参数与最⼤步数，决定 Agent 能看到什么、能调⽤什么⼯具、何时需要向
⽤户申请许可。

Build 与 Plan 以 primary 模式直接承担⽤户任务，⼆者最明显的差别落在权限边界上。
General 与 Explore 以 subagent 模式被 Task Tool 调度，Explore 只开放搜索、读取与受限命
令等探索能⼒。Compaction、Title、Summary 标记为隐藏 Agent，分别负责压缩上下⽂、⽣
成标题和汇总变更。前台⾓⾊与后台服务由同⼀种 Profile 机制表达。

Codex：安全执⾏和 Thread ⽣命周期

在 Codex ⾥，⽤户点下允许，并不等于模型拿到了整台电脑。Approval 只决定某个动作是否
获准，Sandbox Policy 仍然约束命令可以写到哪⾥、能否访问⽹络、可以触碰哪些系统资
源。⼀次会触碰系统的⼯具调⽤真正执⾏之前，要连续穿过这两道边界。

为什么需要两层？Q&A Bot 的错误只结束在屏幕上，但Coding Agent 的错误可能变成被覆盖
的⽂件、错误执⾏的命令，或者⼀次越过⼯作区边界的访问。模型能⼒越强，运⾏时越不能只
靠 Prompt 提醒它⼩⼼。Codex 真正要解决的，是怎样让⼀个并不完全可靠的模型，安全、
连续、可恢复地操作真实计算机。

这套⼯程并不便宜。独⽴测评项⽬ OpenBench 在 2026 年 7 ⽉把同⼀个 gpt-5.6-sol 放进 7
套 Coding Agent Harness，并只⽐较各组都完整跑过的 42 个任务。Codex 完成了 31 个，通
过率 73.8%；它的中位耗时是 94.6 秒，每个成功任务平均消耗 117,107 个新 token，都是这
组测试⾥最重的⼀档。

> 本页含图像对象，未嵌入转写文件；图内文字及版面细节请查看本页PDF。

## PDF第11页

[查看原始页面](RAW.pdf#page=11)

这张表不是通⽤排⾏榜，任务只有 42 个，不同长度、不同环境的任务也可能改变结果。但它
确实把 Codex 的 Harness 成本展现了出来。如果测试只关⼼⼀次短任务能不能做完，线程⽣
命周期、审批、沙箱、事件、持久化与恢复机制，很多时候都只会被算成额外开销。Codex
选择的不是最轻的路，⽽是让长任务真正可以被监督、中断、恢复和并⾏管理的路。

### 2025 年，开源的 Codex CLI 与云端 Codex 相继出现，使⽤⼊⼝随后扩展到 IDE、Web、App
和 SDK。⼊⼝越来越多只是表⾯变化，更深的⼀层是任务不能再依附某个终端进程。App
Server 提供统⼀协议，让不同客户端⾯对同⼀套任务⽣命周期、审批请求和流式事件。

这套协议的⾻架是 Thread、Turn 与 Item。Thread 承载⼀个可以持续多轮的任务，Turn 表⽰
⽤户推动任务向前⾛的⼀次过程，Item 则把模型消息、Reasoning、命令执⾏、⽂件修改、⼯
具调⽤和审批拆成可观察单元。任务可以 Start、Resume、Fork、Interrupt，正在运⾏的
Turn 也可以被 Steer。Codex 保存的不只是聊天记录，⽽是⼀棵能够继续⽣长的任务状态。

把这套⽣命周期真正运转起来的，是 Thread Manager。它维护⼀张以 Thread ID 为索引的活
跃任务表，让 App Server 能找到已经在跑的任务，继续投递 Turn 与操作。如果任务已经离开
内存，Thread Manager 才会从 Thread Store 或 Rollout 装回历史，重建⼀个可运⾏的
CodexThread。它不是另⼀层记忆库，也不亲⾃完成模型推理，更像⼀个把协议请求、运⾏实
例和持久化历史接在⼀起的任务控制平⾯。

Thread 负责长期⽣命周期，每次模型采样还需要⼀个更短暂、更严格的执⾏现场。源码中的
StepContext 会引⽤当前 TurnContext，并捕获这⼀刻选中的环境、Capability Roots、MCP
Binding、Tool Router 与 AGENTS.md 。后台配置即使发⽣变化，已经开始的这⼀步仍然⾯
对⼀套⾃洽的⼯具和环境。

当模型准备制造真实副作⽤时，Approval Policy 与 Sandbox 开始接管。前者判断什么情况下
必须停下来询问⽤户，App Server 会把请求绑定到具体的 Thread、Turn 和 Item；后者把允
许写⼊的⽬录、⽹络访问和操作系统能⼒落实为技术限制。⽤户接受⼀次命令，并不会⾃动取

> 本页含图像对象，未嵌入转写文件；图内文字及版面细节请查看本页PDF。

## PDF第12页

[查看原始页面](RAW.pdf#page=12)

消剩余限制。这⾥的安全不是模型答应会谨慎，⽽是执⾏路径中存在模型⽆法⾃⾏跨过的边
界。

Codex 对过去也分了不同层次。当前模型看到的是经过装配和压缩的上下⽂，Rollout 与
Thread Store 保存的是可以恢复的任务轨迹，SQLite 为 Thread 状态和元数据提供查询⼊⼝。
启⽤ Memory 后，后台管线还会读取历史 Rollout，先提取每个 Thread 中稳定的事实和经
验，再交给专门的整合 Agent 更新 ~/.codex/memories/ 。恢复⼀次任务与从许多任务中学
习，在这⾥是两条不同的管线。

Multi-agent 继续沿⽤同⼀套抽象。⼦ Agent 不是塞进主循环的⼀段特殊逻辑，⽽是由 Thread
Manager 派⽣出的⼦ Thread。它可以从⽗任务已经持久化的历史 fork，拥有⾃⼰的上下⽂、
⼯具运⾏时和 Rollout，再把状态与结果送回⽗任务。

这个抽象现在已经直接长到了产品界⾯上。图中，同⼀个主任务派⽣了 Newton、Franklin、
Dirac 和 Peirce 4 个后台 Agent，⽤户还可以⽤ @ 继续向某个 Agent 追加请求。看上去有
点像⼀个 Agent 群聊，但它们并不是 4 段推理挤在同⼀份上下⽂⾥，⽽是 4 个由 Thread
Manager 维护的独⽴⼦ Thread。

> 本页含图像对象，未嵌入转写文件；图内文字及版面细节请查看本页PDF。

## PDF第13页

[查看原始页面](RAW.pdf#page=13)

Thread Manager：把协议请求接到运⾏实例

App Server 暴露的是 thread/start 、 thread/resume 、 thread/fork 与 turn/start 这些协议操
作，真正把它们接到内部运⾏时的是 Thread Manager。它⽤⼀个内存中的 HashMap\<ThreadI
d, Arc\<CodexThread\>\> 记录活跃 Thread，再通过 Thread ID 查找实例、投递操作，并让 App
Server 继续读取对应的运⾏事件。结束的 Thread 会从表中移除，没有完成关闭的实例则保留
下来，便于重试或继续检查。

启动新任务时，Thread Manager 会先根据配置、初始历史、环境与⼯具能⼒创建 Session。
它等到第⼀个 SessionConfigured 事件后，才把 Session 包装成 CodexThread 并注册到活跃
表。如果 Resume 指向⼀个仍在运⾏的 Thread，它会直接返回现有实例，避免同⼀份历史启
动两套 Agent Loop。只有冷 Thread 才需要从 Thread Store 或 Rollout 读取历史，再重建新
的运⾏实例。

被管理的任务状态仍然遵循 Thread、Turn 与 Item 三层结构。Thread 是长期容器，Turn 是⽤
户推动任务的⼀次过程，Item 则把⽤户输⼊、Agent Message、Reasoning、命令执⾏、⽂件
变更、⼯具调⽤和审批拆成可观察单元。
`````text

  Thread
  └── Turn
      ├── User Input Item
      ├── Reasoning / Agent Message Item
      ├── Command Execution / File Change Item
      ├── Tool Call / Approval Item
      └── Turn Completed
`````

Fork 也不是复制⼏段聊天⽂字。Thread Manager 会按指定的持久化快照裁切历史，⽣成新的
Thread ID 与独⽴运⾏实例。派⽣⼦ Agent 时，它还会先要求⽗ Thread 物化并刷新尚未落盘

> 本页含图像对象，未嵌入转写文件；图内文字及版面细节请查看本页PDF。

## PDF第14页

[查看原始页面](RAW.pdf#page=14)

的 Rollout，再从稳定快照创建⼦ Thread。所以 Thread Manager 管的不只是⼀列会话，还有
任务之间的谱系与运⾏边界。

turn/start 与 turn/steer 会把新操作送给正确的 CodexThread，运⾏过程再通过 item/starte
d 、增量事件、 item/completed 和 turn/completed 向外暴露。Thread Manager 本⾝不执⾏
每⼀步推理，它负责保证每个协议请求都落到正确的任务、正确的历史和唯⼀的运⾏实例上。

Hermes：⾃进化

Pi 关⼼的是如何⽤尽量少的 Harness tax 完成眼前这次任务，Hermes 把问题往后推了⼀步，
Agent 第⼆次遇到类似任务时，能不能少⾛⼀遍弯路？这需要 Harness 不只保存聊天记录，
还要判断⼀次经历⾥哪些是稳定事实，哪些是可复⽤流程，哪些旧知识⼜应该被新的修正覆
盖。

到 2026 年 8 ⽉，这个问题有了⼀套专门的测试。PAST-Bench 不再把每个任务当成彼此隔离
的⼀次考试，⽽是安排了 26 个场景、204 个跨会话 Episode。早期 Episode 给 Agent 留下偏
好、流程或修正，后续 Episode 清空当前上下⽂，再分别测试 Memory、Procedural
Reuse、Information Gathering 和 Update。每组实验还会关掉持久化能⼒重跑⼀次，尽量把
模型本⾝的能⼒与历史经验带来的增益拆开。

固定 MiniMax-M2.7 后，Hermes 是现有基线⾥唯⼀在四类能⼒上全部获得正向增益的框架。
开启持久化后，它的总体增益是 +0.13 。更有意思的是，PAST-Bench 还检查了⽇志中的
Memory 写⼊、Skill 创建、Session Search 和后续读取，确认 Agent 是否真的⾛完了「写
⼊、检索、正确应⽤」这条路径。Hermes 的机制证据分是 0.64 ，同样取得 +0.13 增益的
nanobot 只有 0.57 。

再回头看 Hermes Agent 的架构，前台 Agent Loop 解决当前任务，Session Archive 留下原始
经历，Memory 和 Skills 分别承载稳定事实与可复⽤流程，Background Review 再决定哪些

> 本页含图像对象，未嵌入转写文件；图内文字及版面细节请查看本页PDF。

## PDF第15页

[查看原始页面](RAW.pdf#page=15)

经验值得影响未来。Hermes 所说的⾃我改进，是在模型外部维护⼀层会随使⽤逐渐变化的认
知系统。

Persistent Runtime：任务可以由时间⽽⾮⽤户触发

Terminal、Browser、MCP、任务分派和 Skill 管理构成 Agentic Tools；Cronjob 让 Harness
能够在没有即时⽤户输⼊时触发⼯作。Agent 因⽽从“打开终端才存在的进程”变成⼀个长期在
线的个⼈运⾏时。

总结

回到开头，今天的 Agent 看起来像⼀套⼩型操作系统，并不是因为有⼈⼀开始就想造⼀套⼩
型操作系统。每⼀层都是模型撞上边界以后，⼯程系统不得不补上的回答。记不住，就装配上
下⽂；碰不到世界，就接⼊⼯具；⼀步做不完，就启动循环；历史装不下，就分出长期记忆；
真实副作⽤越来越多，就继续长出会话、权限、沙箱、事件和⼦ Agent。

Agent 做决策，Harness 让这些决策可以持续、可控、可恢复地发⽣。模型决定下⼀步⾏动，
Harness 管理它看见什么、能够调⽤什么、动作在哪⾥执⾏、过程怎样留下记录，以及失败之
后如何重新开始。

Pi、OpenCode、Codex 和 Hermes 并没有给出同⼀道题的标准答案。Pi 把核⼼收得尽可能
⼩，OpenCode 把⾝份与历史组织成 Profile 和 Event，Codex 围绕 Thread 与安全边界完成
⼯程化，Hermes 则把注意⼒延伸到下⼀次任务。不同路线交换的是成本、控制⼒、可恢复性
和长期学习能⼒，选择哪⼀种，取决于 Agent 最终要进⼊怎样的真实环境。

> 本页含图像对象，未嵌入转写文件；图内文字及版面细节请查看本页PDF。

## PDF第16页

[查看原始页面](RAW.pdf#page=16)

模型还会继续变强，但 Harness 不会因此消失。模型越能⾏动，外⾯的运⾏时越不能含糊。
未来的分⽔岭，未必只是谁的模型更聪明，也是谁能为同⼀个模型搭出更好的上下⽂、更稳的
循环、更清晰的边界，以及⼀套不会在长期使⽤中越学越乱的记忆。

Agent 是怎样长出 Harness 的，答案就在这些⼀层层补上的边界⾥。

腾讯技术⼯程
腾讯技术官⽅号。腾讯技术创新、前沿领域发布解读平台。
685篇原创内容

公众号

阅读 4.0万

留⾔

写留⾔

> 本页含图像对象，未嵌入转写文件；图内文字及版面细节请查看本页PDF。

## PDF第17页

[查看原始页面](RAW.pdf#page=17)

还没有留⾔，来写⾸评

