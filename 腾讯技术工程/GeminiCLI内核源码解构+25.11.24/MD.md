# 深入AI Agent内核: Google gemini-cli 源码深度解构

来源：[RAW.pdf](RAW.pdf)，capture-001。

这是PDF文本层按物理页码转写，不是AI总结。图片未嵌入；图内文字、截图、公式、表格及代码排版可能未提取或不可靠；源PDF中存在的右侧裁切不补写。实际复核范围详见META.json。

## PDF物理页 1

深⼊AI  Agent内  核: Google  gemini-cli 源码深度解构


原创 腾讯程序员   腾讯技术⼯程    2025年11⽉24⽇  01:38⼴东  714⼈
















作者：  wenconglin



  随着⼤语⾔模型与开发⼯具链的深度融合，命令⾏终端正被重塑为开发者的AI协作界⾯。
  本⽂以 Google gemini-cli 为范本，通过源码解构，系统性分析其 Agent 内核、ReAct ⼯
  作流、⼯具调⽤与上下⽂管理等核⼼模块的实现原理。为希望构建终端                  Agent 的开发
  者，提供⼯程实现的系统化参考。


  一、引言

命令⾏终端是开发者的核⼼⼯作区，也是许多开发者完成⼯作的⾸选⼯具。当前，⼤语⾔模型
正在重塑命令⾏终端的能⼒，使终端不仅能完成命令执⾏，还能让开发者与智能体共同完成命
令的协作、创造。

近  期 ，Google 开  源  了  其  官  ⽅  实  现 的命  令  ⾏    AI ⼯  作  流  ⼯  具——gemini-cli
（   https://github.com/google-gemini/gemini-cli ），旨在将 AI 能⼒深度融⼊开发者的⽇常。它能
分析庞⼤的代码库、⾃动化处理复杂的 Shell 指令和 Git 操作，还⽀持多模态交互。同时，它
也是⼀个⾼度可扩展的平台，积极拥抱了模型上下⽂协议（            MCP）、A2A等拓展协议。

本⽂的⽬标将不⽌于⼯具使⽤，我们将深⼊ gemini-cli 的源码，重点分析其整体架构，并解析
其命令分发、⼯具调⽤和上下⽂管理等关键模块的实现原理，分析其AI Agent 的整体构建思
路。

我们希望这次源码层⾯的分析，能为那些对 AI Agent 内部机制感到好奇，或是希望构建类似
终端 agent的开发者，提供⼀份务实且                                                           有价值的技术参考。



  二、核心能力演示

在深⼊源码之前，让我们通过⼏个真实的场景，直观地感受 gemini-cli 如何将⾃然语⾔转化为
实实在在的⽣产⼒。

2.1 场景⼀：⾃动化系统任务       —— 批量处理⽂件

## PDF物理页 2

这是最能体现命令⾏⼯具本质的场景。gemini-cli 可以将你⽤⾃然语⾔描述的复杂⽂件操作，
直接翻译成可执⾏的命令。

上下⽂：  你的⼀个⽬录下堆满了     jpg图⽚⽂件。

⽤户输⼊：gemini > 将这个⽬录⾥的所有图⽚转换为 png 格式，并根据照⽚的 EXIF 数据⾥的
拍摄⽇期来重命名它们。

gemini-cli的决策与执⾏路径：展⽰了 gemini-cli，是⼀个能够规划、编码、诊断、并从失败
中学习和迭代的    AI Agent。















1.规划与编码：将任务拆解为四步计划，读取图⽚，转换格式，重命名新⽂件，删除原始⽂
件。它没有直接⽣成复杂的 Shell 指令，判断出运⽤Python 脚本来解决问题。调⽤WriteFile，
在本地创建了⼀个    convert_images.py 脚本。

2.环境准备与⾃我纠错：在执⾏前，它预判到需要           Pillow 库，并尝试⽤ pip 安装。命令失败
后，它能理解错误并    ⾃动切换到   pip3 重试，展现了环境适应能⼒

3.诊断与迭代：⾸次运⾏脚本时，因图⽚缺少 EXIF 数据⽽失败。gemini-cli 捕获并理解了这个
错误。它没有⽌步于此，⽽是启动了代码修复流程：它⽤ ReadFile 读取了⾃⼰刚写的代码，
然后 WriteFile 进⾏了代码重构，增加了⼀个   “使⽤⽂件修改时间作为                        备⽤⽅案”的逻辑。

4.最终执⾏与验证：最后，它运⾏了更新后的脚本，成功完成了图⽚格式转换与重命名。并通
过 ReadFolder 命令验证了最终结果，形成了⼀个的闭环。

2.2 场景⼆：快速理解新项⽬       —— 深⼊分析代码库

⾯对⼀个陌⽣的代码库，它可以迅速帮助我们理清脉络。

上下⽂：  克隆了  gemini-cli 源代码⾄本地⽂件                                     夹中

⽤户输⼊：gemini > 本⽂件中有gemini-cli的源码，帮我梳理gemini-cli的整体架构。关键的⽬
录和它们的作⽤分别是什么？

gemini-cli的决策与执⾏路径： 这个交互展⽰了    gemini-cli 作为信息分                     析助⼿的智能⼯作流。

## PDF物理页 3

1.环境了解与信息收集： 由于是全新会话，它⾸先意识到⾃⼰缺乏对当前环境的了解。它的
第⼀步是 调⽤  ReadFolder ⼯具，扫描当前⽬                                     录，获取⼀份完整的⽂件和⽂件夹“地图”。

2.模式识别与策略制定： 在获取⽂件列表后，它利⽤内置的软件⼯程知识进⾏模式识别。当
看到 docs/architecture.md 这个路径时，它迅速将⽤户的关键词“架构”与之关联，并制定出⼀
条最⾼效的策略：  优先读取官⽅⽂档   ，⽽⾮盲⽬分析代码。

3.执⾏与信息提取： 策略确定后，它⽴刻调⽤ ReadFile ⼯具，读取 docs/architecture.md 的
内容。

4.整合与结构化呈现： 它没有直接返回⽂档原⽂，⽽是完成了信息整合。它将从⽂档中提取
的信息与第⼀步查看的实际⽬录结构进⾏交叉验证和补充，最终⽣成了⼀份逻辑清晰、结构化
的项⽬架构分析。

2.3 场景三：跨越模态的创造⼒      —— 从设计图到代码

这个场景将突破传统命令⾏的⽂本限制，理解视觉信息并将其转化为可执⾏的⼯作流。

上下⽂：  你的项⽬⽂件夹⾥有⼀张产品经理给的登录页⾯截图         login-mockup.png。

⽤户输⼊：gemini > 这是我们的登录页⾯设计图 (login-mockup.png)，帮我⽣成对应的 HTML
和 CSS 代码，并⽤浏览器打开预览编码结果。

gemini-cli的决策与执⾏路径： 这是从视觉到代码，再到预览的⾃动化⼯作流。










1.任务拆解与规划： 它⾸先将⽤户的复合指令拆解为三步计划：分析图⽚、⽣成⽂件、打开
浏览器预览 ，展现了清晰的逻辑规划能⼒。

2.视觉理解与代码翻译： 它通过 ReadFile 加载图⽚，其多模态模型解析出设计图中的布局、
组件和样式，然后基于这些视觉信息     编写结构化的    HTML 和 CSS 代码。

3.遵循最佳实践的⽂件操作：     它将结构和样式分离，通过两次WriteFile  调⽤，分别创建了
index.html 和 style.css 两个⽂件，遵循了前端开发的基本规范。

4.⽆缝的⼯具链调⽤： 最后，它调⽤ Shell ⼯具执⾏ open 命令，⾃动在浏览器中打开了⽣成
的页⾯ ，完成了从⼀个创意原型到可交互预览的完整闭环。

## PDF物理页 4

通过这三个场景，我们看到 gemini-cli 扮演了三个关键⾓⾊：能够⾃我纠错的 AI Agent、⾼效
的代码分析师，以及理解视觉的创意开发者。它的能⼒已远超传统命令⾏终端的范畴，不只是
简单的命令执⾏者，⽽是能将⽤户的复杂意图⽆缝转化为实际⼯作流的智能伙伴。

那么，这⼀切强⼤能⼒的背后，究竟是怎样的架构设计在⽀撑呢？


     腾讯技术⼯程
     腾讯技术官⽅号。 腾讯技术创新、 前沿领域发 布解读平台。
     690篇原创内 容


 公众号


 三、架构设计与核心源码解析

3.1 核⼼架构与⼯作流程
























如图所⽰，gemini-cli的架构分为⽤户交互层、逻辑层、⼤模型服务与⼯具层。整体上围绕⼀
个动态的推 理 与 ⾏动（ReAct ）⼯ 作 流 构 建 。 其 实 现 逻 辑 分布在 两 个 核 ⼼包中：
packages/core 负责提供与⼤模型通信、执⾏⼯具等原⼦能⼒，⽽   packages/cli 作为上层协
调者，负责驱动整个任务流程。

具体来说，整个  ReAct循环由cli包驱动。当接收到⽤户指令后，它⾸先调⽤      core 包进⾏“推
理”，core 则将模型制定的⾏动计划返回给 cli。收到计划后，cli 再指令 core 执⾏⼯具，并通
过回调函数回收执⾏结果。cli 随即发起携带新上下⽂的下⼀轮“推理”，如此循环往复，直⾄
任务完成。

这种由 cli 驱动、core 执⾏的协作模式，既保证了核⼼ AI 逻辑的可复⽤性，也赋予了界⾯层
精细控制任务每⼀步状态的能⼒。

3.2 推理与⾏动循环

## PDF物理页 5

如图，Gemini CLI 的核⼼是⼀个由      packages/cli 驱动、packages/core执⾏的“推理-⾏动”
（ReAct）循环。这个循环并⾮简单的函数递归，⽽是通过⼀系列精⼼设计的 Hooks和回调函
数闭合的异步流程。让我们从源码的视⾓，⼀步步拆解这个循环的实现机制。

3.2.1 “⽤户输⼊”到“模型推理  ”

在     交     互     模     式     下  ，每     ⼀  次⽤     户     提     交     输     ⼊  ，都     会  触发
packages/cli/src/ui/hooks/useGeminiStream.ts 中的 submitQuery 函数。这是整个 ReAct 循
环的⼊⼝。

1.预处理与分发：submitQuery   ⾸先会调⽤    prepareQueryForGemini 函数。这是⼀个关键的
预处理器，它负责解析⽤户输⼊，处理 @⽂件引⽤和 /命令等前端指令。如果指令可以在本地
处理（如   /clear），流程就此终⽌；否则，它会将处理后的查询内容打包，准备发往模型。

## PDF物理页 6

2.发    起    推    理：拿  到处理    好  的查询    后  ，submitQuery       会  调⽤
geminiClient.sendMessageStream()，与 Gemini⼤模型建⽴⼀个流式连接。这标志着“推理”阶
段的开始。

3.2.2 “⾏动计划”到“⼯具执⾏   ”

模 型 在 “推 理  ”后，可 能 会 返 回 ⼀ 个包含 ⾏动计 划的响 应，即 ⼯ 具调⽤ 请 求
（ToolCallRequest）。

1.接收与调度：useGeminiStream  中的 processGeminiStreamEvents 函数负责监听事件流。
当它收到 ToolCallRequest事件时，会将这些请求收集起来，并调⽤               scheduleToolCalls 函
数。

2.UI  层           的           调           度           桥           梁：scheduleToolCalls 来           ⾃
packages/cli/src/ui/hooks/useReactToolScheduler.ts。这个 Hook不直接执⾏⼯具，它实例化
了来⾃   core 包的 CoreToolScheduler 类，并将⼯具请求转发给它。

3.Core层    的    执    ⾏    核    ⼼：真    正  的⼯    具  调度    和    执    ⾏    逻    辑    位    于
packages/core/src/core/coreToolScheduler.ts 的 CoreToolScheduler 类中。它的 schedule⽅
法执⾏的关键步骤：

排队 ：确保同⼀时间只处理⼀批⼯具调⽤。

验证 ：检查⼯具是否存在、参数是否合法。

确认：对于敏感操作（如写⽂件）                            ，会挂起并等待⽤户在 UI 层⾯确认。

执⾏ ：调⽤⼯具⾃⾝的      execute() ⽅法，真                正执⾏⽂件读写、命令运⾏等操作。

到此，  cli 包成功地将 “⾏动”指令委托          给了 core 包去执⾏，并可以执⾏本地⼯具

3.2.3 “观察”结果到再次  “推理 ”

⼯具执⾏完毕后，结果需要被送回模型，以完成“观察”并开启下⼀轮“推理”。这个递归流程是
通过回调链实现的。

1.执 ⾏ 完 成  ：CoreToolScheduler 在 所 有 ⼯ 具 执 ⾏ 完毕后，会调⽤ ⼀ 个 名 为
onAllToolCallsComplete 的回调函数，          并将所有⼯具的执⾏结果作为参数。

2.逐层返回：这个回调函数会穿透 useReactToolScheduler，最终在 useGeminiStream hook
中被⼀个名为     handleCompletedTools 的函数接收。

3.闭合循环：handleCompletedTools 函数是整个循环的闭合点。它将所有⼯具的返回结果打
包成模型需要的格式，然后——也是最关键的⼀步——再次调⽤                    submitQuery 函数，并将⼯
具结果作为新的查询内容，也是新⼀轮“观察”阶段的结束和新⼀轮“推理”的开始模型会根据⼯
具的执⾏结果，决定是给出最终答案，还是规划下⼀步新的“⾏动” 。这个由回调驱动的循环
会持续进⾏，直⾄最终任务完成。

3.3 ⼯具调⽤与扩展

## PDF物理页 7

上⼀节我们看到，ReAct 循环的其中⼀个关键点在于模型能够决定何时调⽤⼯具。本节将深⼊
探讨⼯具调⽤，以及     gemini-cli 是如何          实现并安全执⾏它们的。整体逻辑可参考下图：
































3.3.1 ⼯具的声明与实现

以 read_ﬁ    le ⼯具为例（位于packages/core/src/tools/read-ﬁle.ts）。

声明 : ⼯具⾸先需要向⼤模型进⾏⾃我介绍。这是通过⼀个符合 JSON Schema 规范的配置对
象完成的。它详细定义了⼯具的名称（如read_ﬁ    le）、功能描述（⽤于读取⽂件内容），以及最
重要的——参数（如 absolute_path、oﬀset等）。这份介绍是模型理解并决定如何使⽤该⼯具
的依据。

实现 : 当模型决定调⽤该⼯具后，其实际的执⾏逻辑则被封装在⼀个 Invocation 类中。该类的
execute()⽅法包含了真正的功能代码                             ，例如调⽤⽂件系统 API 来读取⽂件。

3.3.2 统⼀的“⼯具注册表 ”

所有内置或外部的⼯具，会被⼯具注册表ToolRegistry      （位于  packages/core/src/tools/tool-
registry.ts）来管理。

在应⽤启动时，Conﬁg模块会负责创建所有内置⼯具的实例，并逐⼀注册到表中。当需要与⼤
模型交互时，系统会从注册表中提取所有⼯具的“声明”信息，统⼀提交给模型，让模型知道它
当前拥有哪些可⽤的能⼒。同样，当模型请求执⾏某个⼯具时，调度器也会通过注册表来查找
并执⾏它。

3.3.3 安全执⾏的确认机制

对于 run_shell_command （实现位于packages/core/src/tools/shell.ts）这类可能造成风险的
执⾏⼯具，gemini-cli 建⽴了⼀套安全确认机制，其决策逻辑位于 core 包，⽽ UI 交互则由 cli

## PDF物理页 8

包呈现。

1.决策点 ： 当⼀个⾼危⼯具被请求执⾏时，CoreToolScheduler     会⾸先调⽤该⼯具的
shouldConﬁrmExecute() ⽅法，以确定⼯具能否被执⾏。

2.检查: 以shell⼯具为例，shouldConﬁrmExecute() 会进⾏检查：该命令是否在⽤户本次会话
中已经授权过？

3.请求确认: 如果授权检查未通过， CoreToolScheduler 会暂停执⾏，并发送信号⾄cli层。cli
包接收到这个信号后，会渲染⼀个对话框，展⽰待执⾏的命令，并让⽤户做出是否确认执⾏的
决定。

这套机制确保敏感操作都在⽤户的明确授权下进⾏，同时通过会话内⽩名单等⽅式避免了不必
要的重复确认。

3.3.4 MCP拓展：连接外部⼯具

gemini-cli通过⽀持“模型上下⽂协议（”MCP），可以与任何外部⼯具服务器进⾏交互，从⽽获
得扩展能⼒。

gemini-cli启动时，gemini-cli 会连接在配置中指定的 MCP服务器，并请求对⽅提供其⽀持的
⼯具列表。MCP服务器返回⼯具的声明信息后，gemini-cli     会将它们作为   MCP⼯具注册到⾃
⼰的ToolRegistry 中。 （代码位于packages/core/src/tools/ ⽬录下的 mcp-client-manager.ts）

当模型决定调⽤⼀个MCP外部⼯具时，其执⾏流程与内置⼯具不同是 execute()⽅法，它通过
初始化阶段建⽴的连接，将参数转发给MCP服务器。它会等待服务器返回执⾏结果，再将其
递交给模型。            （代码位于packages/core/src/tools/ ⽬录下的 mcp-client.ts 、 mcp-tool.ts ）

通过这种⽅式，   gemini-cli 将MCP⼯具整合进了⾃⾝的 ReAct循环中。

3.4 上下⽂管理机制

在前两节中，我们分析了      gemini-cli 的推理循环与⼯具执⾏能⼒。要让这些能⼒发挥最⼤价
值，其管理和利⽤上下⽂的能⼒必不可少。gemini-cli 通过多层次上下⽂管理机制，实现了短
期会话记忆、长期知识注⼊，确保了交互的连贯性。

## PDF物理页 9

3.4.1 会话历史

基础的会话历史，保证了模型能记住你和它之间的对话。

1.UI 层 : useGeminiStream hook **(位于 packages/cli/src/ui/hooks/useGeminiStream.ts)**负责
管理⼀个⽤于界⾯渲染的历史记录数组。当⽤户或模型产⽣新消息时，它会更新这个数组，让
⽤户能在屏幕上看到对话流。

2.core层: 模型记忆维护在调⽤Gemini的客户端代码 GeminiClient (位于       packages/core/src/co
re/client.ts) 及其内部的 GeminiChat 对象 (位于 packages/core/src/core/geminiChat.ts) 中。
GeminiChat 内部维护着⼀个需要发送给 API 的、完整的对话历史。当它处理⼀个新的⽤户请
求时，其  sendMessageStream ⽅法会执⾏对历史会话的      “读-写”操作：

1.写⼊⽤户输⼊: 在向模型发送请求前，它⾸先将⽤户的最新输⼊追加到其内部历史记录的末
尾。

2.发送完整历史   : 它将这个包含了最新输⼊的完整历史发送给模型。

3.写⼊模型回复   : 在接收到模型的完整回复      后，它再将模型的回复追加到历史记录中。

通过这种⽅式，利⽤GeminiChat 这个有状态的对象，每⼀轮对话都建⽴在完整的历史上下⽂
之上，实现了连贯的交互。

3.4.2 系统提⽰词

在⼤模型推理中，我们需要模型在整个会话中都记住⼀些核⼼背景信息，gemini cli除了内置
的系统提⽰词（    system prompt），还⽀持可选的⽤户⾃定义的上下⽂信息                                                                                      。

⽤户⾃定义的上下⽂，可通过          context.ﬁleName 属性（配置⽂件   .gemini/conﬁg.yaml）来配
置，可将⽤户提供的⽂件内容，与gemini-cli内置的系统提⽰词（system prompt）合并，形成
⼀个在整个会话中保持不变的预设指令。在 gemini-cli 启动时，loadCliConﬁg 函数 (位于            pac
kages/cli/src/config/config.ts) 会 读 取context.ﬁleName指定的⽂ 件 内 容，并将 其 作 为
userMemory 属性，存⼊   Conﬁg 对象     中。

## PDF物理页 10

在创建聊天会话时，GeminiClient 会调⽤ getCoreSystemPrompt 函数 **(位于 packages/core/s
rc/core/prompts.ts)**来构建完整的系统提⽰词（system prompt）。这个函数执⾏了如下逻辑：

1.加载基础系统提⽰词（system prompt）: 它⾸先会加载⼀个内置的字符串 basePrompt。
这个  basePrompt 就是 gemini-cli 的原⽣系统提⽰，它详细定义了AI 助⼿的核⼼职责、⼯作
流程、⾏为准则等。

2.追加⽤户上下⽂: 它会检查 userMemory（即您⽂件中的内容）是否存在。如果存在，它会
将其⽤分隔符（   ---）追加到 basePrompt 的末尾。

这个合并了原⽣指令和⽤户⾃定义知识的、完整的系统提⽰词（system prompt），会在API 请
求上下⽂中被发送。模型会基于这个上下⽂来进⾏推理和⾏动。

3.4.3 即时引⼊上下⽂

为了让⽤户能灵活地、即时地引⼊⽂件作为上下⽂，gemini-cli 提供了 @ 引⽤功能。这套机制
是⼀个在请求发送前的预处理器中完成。

1.输⼊检测、解析: ⽤户输⼊会被useGeminiStream hook (位于 packages/cli/src/ui/hooks/useGe
miniStream.ts)检测输⼊中的  @ 符号，并将其交给      handleAtCommand 处理器（位于
packages/cli/src/ui/hooks/atCommandProcessor.ts）。

2.复⽤存量⼯具: handleAtCommand 会解析出所有⽂件路径，然后调⽤上⽂提到的内置的⽂
件读取⼯具，来读取这些⽂件的内容。

3.组装上下⽂ : 它将读取到的⽂件内容，连同⽤户的原始提问，⼀起组装成⼀个完整              prompt。

4.模型推理: 最后，这个包含了“即时上下⽂”的查询被发送给模型。这使得模型可以在当前这
⼀轮对话中，精准地针对特定⽂件内容进⾏回答。

3.4.4 会话持久化

默认情况下，对话历史是存在于内存中的，关闭即消失。为了能跨越多次启动来保留对话，
gemini-cli 提供了快照功能。

该功能通过   /chat save和 /chat resume命令来触发。

具体实现是通过Logger类（位于 packages/core/src/core/logger.ts）提供了 saveCheckpoint
和 loadCheckpoint ⽅法。通过读写本                地⽂件实现上下⽂存储和读取。

通过这四种机制的协同⼯作，使得gemini-cli能处理流畅的即时对话，加载长期的背景知识、
引⽤临时的⽂件内容，并能按需持久化和恢复整个对话，为⽤户提供了强⼤⽽灵活的上下⽂管
理能⼒。



  四、架构思想与新范式

上⼀节，我们深⼊源码的细节，揭⽰了 gemini-cli 的⼯作原理，同时也能逐步窥见代码背后⼀
系列深思熟虑的架构决策。本章节将尝试对具体的技术实现进⾏梳理和提炼，分享对gemini-

## PDF物理页 11

cli架构思想和技术选型的⼀些思考。

我们将主要探讨以下⼏个⽅⾯：

  gemini-cli 是如何通过分层设计，构建                                                           其可移植的 Agent 内核的？

  ⼤模型在其运⾏时扮演了怎样的动态调度⾓⾊？

  系统是如何通过指令确认机制，来构建⼈机协作模式的？

  它⼜是如何通过开放协议，来构想其未来的⼯具⽣态的？

通过对这些问题的探讨，希望能够揭⽰其设计背后的决策考量，为构建同类 AI Agent 的开发
者提供⼀份有价值的架构参考。

4.1 可复⽤的 Agent 内核架构

gemini-cli 在架构上对项⽬模块进⾏了明确的职责划分，将核⼼AI逻辑与前端交互界⾯彻底分
离，其⽬的是构建⼀个与特定运⾏时环境解耦、可独⽴复⽤的                Agent内核。

这⼀模式体现在     packages ⽬录下两个                     关键模块的划分上：

  packages/core (内核层): 此模块封装了所有与    AI Agent 相关的     原⼦能⼒和核⼼逻辑。它
  包含了与   Gemini API 的通信客户端  (GeminiChat)、⼯具的定义与注册机制
  (ToolRegistry)、⼯具调度的执⾏器  (CoreToolScheduler)，以及会话⽇志与快照功能
  (Logger)。内核层不包含任何与⽤户界⾯       (UI) 相关的代码，其   API 设计与具体应⽤⽆关
  的。

  packages/cli (应⽤交互层): 此模块是 core 内核的⼀个具体应⽤                     ，负责将其能⼒适配到命
  令⾏终端这个特定的运⾏环境中。它的职责包括：解析命令⾏参数、使⽤                    Ink 库渲染终端
  UI、管理⽤户交互状态      (Node.js，基于Hooks和回调的事件驱动⾮阻塞      I/O 模型)，以及调
  ⽤ core 模块提供的   API 来驱动整个  ReAct ⼯作流。

在我们前⽂的源码分析中，两个模块的职责边界很清晰：

  ReAct 循环的实现  ：主逻辑   useGeminiStream Hook 存在于 cli 交互层，⽽调⽤的
  sendMessageStream 等核⼼通信逻辑是由    core 内核层提供。

  安全确认机制    ：需要⽤户确认的决策由       core 内核层  的 CoreToolScheduler 做出，但应⽤
  渲染确认框的     UI 逻辑则由 cli交互层实                现。

  上下⽂处理   ：cli 交互层负责解析   @ 符号这类特定                     于终端的便捷语法，并将解析出的⽂件内
  容，传递给    core 来构建最终的请求上                                           下⽂。

可复⽤的Agent 内核带来了较强的可移植性，作为⼀个独⽴的模块，可以被应⽤在任何项⽬
中，如构建    web 服务、桌⾯应⽤等，它是可供开发者在不同场景下构建                 AI Agent的核⼼
SDK。

4.2 LLM作为动态调度器的开发范式

在传统应⽤中，程序控制流由开发者通过 if/else 等逻辑硬编码。⽽这⾥gemini-cli展⽰了⼤模
型时代的编程范式，它将⼤语⾔模型作为应⽤的计划器、调度器。

## PDF物理页 12

开发者负责通过 ToolRegistry 声明式地注册⼀系列原⼦化的⼯具，但不编写具体的业务流程代
码，⽽如何组合这些⼯具的决策权，交给了 LLM。当⽤户输⼊复杂指令时，LLM 在运⾏时动
态⽣成⼀个执⾏计划，由具体代码（      coreToolScheduler.ts）完成执⾏。

这种模式带来了两⼤优势：

  能⼒的涌现  ：由于执⾏计划是   LLM动态⽣成的，   agent能够执⾏开发者从未明确编码过                                   的
  ⾏为，甚⾄⾃主决定编写并执⾏⼀个脚本来完成任务。

  业务逻辑复杂度降低：    开发者只需不断增加原⼦能⼒⼯具，复杂的业务编排逻辑交给            LLM
  来决定，整体代码复杂度得以降低。

gemini-cli 将 LLM 作为动态调度器的设计，是当前  AI Agent 领域的核⼼实现范式。⽆论是
LangChain、LlamaIndex 等框架，还是 OpenAI、Grok 等模型提供商的官⽅⼯具调⽤功能，
其底层逻辑都是⼀致的，即，     将LLM做为⼀个主动的任务规划与函数                                   调⽤引擎。

此架构范式让应⽤的能⼒上限不再受限于开发者预设的控制流，⽽是取决于 AI 在运⾏时对可
⽤⼯具的动态组合与调⽤，为实现能处理复杂、多步任务，并具备⼀定⾃主性的通⽤ AI agent
提供了可参考的实现路径。

4.3 指令确认与安全执⾏的⼈机共创模式

当 LLM 成为动态调度器，具备⾃主规划和执⾏任务的能⼒时，问题也随之⽽来：如何确保AI
的⾏为可控？

被业界⼴泛认可的解决⽅法是利⽤Human-in-the-Loop设计模式来构建⾃动化流程。HITL 强
调在 AI 系统的关键决策点上，引⼊⼈类的监督、审核或最终授权，完成流                                                                           程闭环。

gemini-cli 提供了将HITL理念⼯程化的范例。实现⽅案上并不是直接限制 AI模型本⾝的能⼒，
⽽是通过指令确认与安全执⾏机制，在终端环境中实现了⼀种⼈机共创的协作模式。即，AI
负责提议与规划，⼈类保留最终的决策与执⾏权。

从源码层⾯看，为了保留⼈的决策权，CoreToolScheduler   在执⾏  run_shell_command 等⾼
风险⼯具前，会暂停     ReAct 循环并向 cli 应⽤层发起授权请求。代码设计上做了职责分离：
core 内核负责决策，cli层负责交互，利⽤了nodejs的事件驱动模型，实现了⾮阻塞式的确认
流程。

另外，在上下⽂管理机制中，gemini-cli 允许我们使⽤ @ﬁle 实时引⽤⽂件，可以为 AI 注⼊明
确的上下⽂信息，为⼈保留了更多的上下⽂控制权限、个⼈知识库信息的主导权。

可以说，为了实现HITL的设计理念，gemini-cli的采⽤的⼯程化⼿段，给了开发者构建⼈机协
同的 AI Agent 提供了有价值的设计参                                           考。

4.4 从⼯具到agent协作的开放协议⽣态

gemini-cli 在扩展性上拥抱了开放协议MCP、A2A，在拓展性上不限于官⽅与开发者⾃建的插
件⼯具。

## PDF物理页 13

  MCP ，实现能⼒即插即⽤：通过       MCP协议将  ⼯具解耦为可通过⽹络调⽤的独⽴服务。在
  gemini-cli 的实现中，McpClientManager 在启动时会向配置的MCP服务器查询并加载⼯
  具的元信息，将其注册进本地的         ToolRegistry。当 LLM 决定调⽤时，将请求转发  给对应
  MCP 服务，  为gemini-cli 提供各类第三⽅能⼒集成的可能。

  A2A ，将gemini-cli的能⼒服务化以⽀                                     持智能体间的协作：近期gemini-cli开源了对A2A的
  ⽀持，在   packages/a2a-server 中的实现。它将 gemini-cli 的核⼼能⼒封装成了⼀套可通
  过A2A协议调⽤的服务。尽管      A2A整体⽣态尚处于早期阶段，但该实现对未来          gemini-cli成
  为分布式  Agent协作⽹络中的⼀部分，                                           提供了可能性。

gemini-cli 通过⽀持 MCP 和 A2A 这两⼤开放协议，展⽰了⼀种双向的扩展模式：既能作为客
户端使⽤外部⼯具服务，也能作为服务端为其他应⽤提供 Agent 能⼒。开发者可以⽤任意语
⾔构建⼯具或应⽤与     gemini-cli ⽆缝集     成，共同组成⼀个更加开放和强⼤的  AI Agent ⽣态。



  五、总结与展望

从直观的能⼒演⽰到深⼊的源码剖析，我们⼀同拆解了 gemini-cli 的内部构造，并探讨了其背
后的架构思想。⾄此，我们可以清晰地看到，gemini-cli 不⽌是⼀个功能丰富的命令⾏⼯具，
它更是⼀个关于如何构建      AI Agent 、有价值且可供参考的⼯程范例。

回顾全⽂，其核⼼设计亮点，可总结为如下四点：

  代码架构：   通过 “核⼼层 -交互层 ”的分离，提供了⼀个可移植的内核        sdk，提供了易于复⽤
  与拓展的⼯程范例。

  运⾏模式：   基于 ReAct框架，将  LLM 作为⼤脑，                实现了agent能⼒的“涌现”。

  ⼈机协作：   遵循了 HITL设计理念，在    AI 的⾃主性与⼈的主导权间取得平衡，构建可信的
  共创模式。

  拓展⽣态：   通过拥抱开放协议，⽀持⼯具能⼒的拓展，提供多            agent间协作的⽆限潜⼒。

展望未来，以   gemini-cli为代表的终端Agent 可能往⼏个⽅向的发展：

  与操作系统、桌⾯应⽤的深度集成联动：          终端 Agent可能打破终端本⾝的限制，                                                      通过与操
  作系统   API、被安装的各类应⽤的深度                                                           集成，理解屏幕交互信息，模拟⼈的操作，驱动任
  意桌⾯应⽤，执⾏跨系统应⽤⼯作流。

  更强⼤的长期记忆：     随着模型能⼒持续进化，结合向量检索等技术，           Agent 将建⽴更⼤规
  模的长期记忆能⼒，能基于对整个项⽬的全局上下⽂理解，做出更优的决策与执⾏。

  从单⼀智能体到分布式多智能体协作         ：随着 A2A 等协议的成熟，更加繁荣的       Agent ⽣态将
  会出现。⼀个复杂的开发任务可能会被分发给多个专⽤              Agent 协作完成，发展为从命令执
  ⾏、代码开发逐步拓展到⾃动化测试、         CI/CD流程、安全扫描等⼯业化⽣产要素完备的⾃
  动化研发  Agents团队。

最终，开发者终端agent将不再孤⽴，⽽是⼀个由 AI Agents驱动的、⾼度协同的智能开发环
境。开发者的⾓⾊也将从代码开发、执⾏者，转变为与             AI agents协同共创的架构师。

## PDF物理页 14

 六、参考⽂献

1. gemini-cli 官⽅    GitHub 仓库     :https://github.com/google-gemini/gemini-cli

2. Gemini API 函数调⽤官⽅⽂档               : https://ai.google.dev/gemini-api/docs/function-calling?hl=zh-

  cn&example=meeting

3. [论⽂  ]Yao, S., Zhao, J., Yu, D., Du, N., Shafran, I., Narasimhan, K., & Cao, Y. (2022). ReAct:

  Synergizing Reasoning and Acting in Language Models. ArXiv,

  abs/2210.03629.https://arxiv.org/abs/2210.03629

4. [论⽂  ]Madaan, A., Tandon, N., Gupta, P., Hallinan, S., Gao, L., Wiegreﬀe, S., Alon, U., Dziri, N.,

  Prabhumoye, S., Yang, Y., Welleck, S., Majumder, B., Gupta, S., Yazdanbakhsh, A., & Clark, P. (2023).

  Self-Reﬁne: Iterative Reﬁnement with Self-Feedback. ArXiv,

  abs/2303.17651. https://arxiv.org/abs/2303.17651

5. [论⽂  ]Schick, T., Dwivedi-Yu, J., Dessì, R., Raileanu, R., Lomeli, M., Zettlemoyer, L., Cancedda, N., &

  Scialom, T. (2023). Toolformer: Language Models Can Teach Themselves to Use Tools. ArXiv,

  abs/2302.04761.https://arxiv.org/abs/2302.04761

6. 模型上下⽂协议           (MCP) 规范：       https://github.com/modelcontextprotocol

7. Agent-to-Agent (A2A) 通信协议：            https://github.com/a2aproject/A2A

8. ⼈机回路       (Human-in-the-Loop, HITL) 概念：          https://en.wikipedia.org/wiki/Human-in-the-loop

9. 六边形架构        (端⼝与适配器         ): https://alistair.cockburn.us/hexagonal-

  architecture/  https://alistair.cockburn.us/hexagonal-architecture


























           腾讯技术⼯程
           腾讯技术官⽅号。 腾讯技术创新、 前沿领域发 布解读平台。
           690篇原创内 容

## PDF物理页 15

  公众号




















阅读 1.4万




留⾔  6


写留⾔


   EasonFeng5…北京2025年11⽉24⽇                                   4
   拆解的再深⼊⼀些会更好


   孙振强+AI进…  陕⻄ 2025年11⽉24⽇                                   1
   从⾃然语⾔指令到⾃动化⼯作流，Google gemini-cli展示了终端AI Agent的完整实现。⽆论是
   批量处理⽂件还是解析代码库，其⾃我纠错与规划能⼒让⼈印象深刻。


   瑾⾔ 上海  2025年11⽉24⽇                                         1
   不错


   ⻛筝 四川  2025年11⽉24⽇                                         1
   虽然看不懂，但是感觉很厉害


   Ty⼭东 2025年11⽉24⽇                                           1
   好⽂章


   陈浩能  ⼴东 2025年11⽉24⽇
   难得好⽂

## PDF物理页 16


