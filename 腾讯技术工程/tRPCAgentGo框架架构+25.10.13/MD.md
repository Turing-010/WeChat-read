# tRPC-Agent-Go：构建智能AI应用的Go语言Agent框架

来源：[RAW.pdf](RAW.pdf)，capture-001。

这是PDF文本层按物理页码转写，不是AI总结。图片未嵌入；图内文字、截图、公式、表格及代码排版可能未提取或不可靠；源PDF中存在的右侧裁切不补写。实际复核范围详见META.json。

## PDF物理页 1

tRPC-Agent-Go：构建智能         AI应⽤的    Go语⾔   Agent框架

腾讯技术⼯程    2025年10⽉13⽇   02:36⼴东   16⼈





                               导语


tRPC是腾讯 内部  覆盖 最⼴ 的RPC 开发框架  ， 覆盖 了 腾讯 ⼤多数微  服务  ，服务 了 如QQ，  腾讯 视
频， 腾讯 ⾳乐 ，QQ浏览器   ，腾讯 新闻 ， 元宝 ， 电脑 、⼿机管家   ，腾讯 云等  业务 。其中tRPC -Go
是使⽤ 最⼴ 的， 累计 覆盖 将近 200w+节点  ，5w+服务 。


2023年起，LLM  发展迅速，⽽A gent开发框架成为连接A I能⼒与业务应⽤的重要基础设施。为了

便于⽤户更好的开发A gent应⽤    ， 并⽅便 和tRPC 微服务 结合 提供  ⾼性能 ， ⾼可⽤ 的服务  ，tRPC-
Go在 25  年 持   续   深   耕  A gent能 ⼒建   设   ，   本   ⽂   将  为 你   全   ⾯   解 读trpc-agent-
go(https://github.com/trpc-group/trpc-agent-go)如何构建智能A I应⽤。







                        ⼀、技术选型和      定位


1.业界框架技术路线分析


⽬前A I A gent 应⽤开发框架主要分为两⼤技术路线：      ⾃主多A gent框架 和编排式框架   。


1.1 ⾃主多Agent框架


⾃主多A gent框架体现了真正的A gent（A utonomous A gent）理念，每个A gent都具备环境感

知、⾃主决策和动作执⾏能⼒。多个A gent通过消息传递和协商机制实现分布式协作，能够根据环
境变化动态调整策略，展现出智能涌现特性。


●AutoGen（M  icrosoft）: 多A gent协作系统，⽀持A gent⻆⾊专业化和动态协商


●ADK（Google Agent Development Kit）: 提供完整的A gent⽣命周期管理和多A gent编

排能⼒


●CrewAI： ⾯向任务的多A gent协作平台，强调⻆⾊定义和责任链模式


●Agno: 轻量级⾼性能A gent框架，专注于多模态能⼒和团队协作

## PDF物理页 2

1.2 编排式框架


编排式框架采⽤⼯作流思维，通过预定义的流程图或状态机来组织LLM 调⽤和组件交互。虽然整个
系统表现出"智能"特征，但其执⾏路径是确定性的，更像是"智能化的⼯作流"，             ⽽⾮真正的⾃主
A gent。


●LangChain：基于Chain抽象的组件编排框架，通过预定义执⾏链路构建LLM   应⽤


●LangGraph：有向⽆环图（D A G）状态机框架，提供确定性状态转换和条件分⽀




2.两种框架类型技术对  ⽐


























3.tRPC-Agent-Go技术定位


⾏业与⽣态现状  ：随着LLM   能⼒的持续突破，A gent开发框架正成为A I应⽤开发的重要趋势。当前
主流的⾃主多A gent框架（如A utoGen、CrewA I、A D K、A gno等）主要基于Python⽣态构建，
为Python开发者提供了丰富的选择。然⽽，Go语⾔凭借其卓越的并发性能、内存安全和部署便利
性，在微服务架构中占据重要地位。⽬前较为成熟的Go 语⾔A I开发框架          ⼤多数专注于编排式架

构，主要适⽤于结构化业务流程，       现代LLM  在复杂推理、动态决策⽅⾯能⼒显著提升，⾃主多
A gent框架相⽐编排式框架具有以下特征：


●⾃适应性  ：A gent基于上下⽂动态调整决策策略和执⾏路径


●协作涌现  ：多A gent通过消息传递实现去中⼼化协商和任务分解


●认知集成  ：深度整合LLM  的推理、规划、反思能⼒形成智能决策链路

## PDF物理页 3

在我们 的业务  调研 中， 腾讯 的业务 对上⾯  的特性有较强的需求    。


因此 tRPC-A gent-Go框架选型偏向于⾃主多A gent协作  的模式和架构。但⼜存在如下       问题


1，对于明确  的场景和流程，   A I⼯作流更 合适 ，能够 给 出更 稳定 的输出


2，腾讯 内部 已有⼤量的A I⼯作流   ，基于tRPC 的开发经验  ， 需要 对存量进⾏   兼容


基于上⾯  的原因 ，tRPC-A gent-Go的核⼼架构是基于⾃主多A gent协作     的框架  ，同时⼜提供   ⼯
作流 编排 的能⼒。






                   ⼆、  tRPC-Agent-Go框架总览


tRPC-A gent-Go（https://github.com/trpc-group/trpc-agent-go ） 框架集成了LLM  、
智能规划器、会话管理、可观测性和丰富的⼯具⽣态系统。⽀持创建⾃主A gent和半⾃主A gent，
具备推理能⼒、⼯具调⽤、⼦A gent协作和⻓期状态保持能⼒，为开发者提供构建智能应⽤的完整
技术栈。


1.整体架构图


1.1 模块图






























●A gent: 核⼼执⾏单元，负责处理⽤户输⼊并⽣成响应，提供智能推理引擎和任务编排能⼒，
tRPC A gent⽀ 持单A gent（ GraphA gent， LLM  A gent） 和M  ulti-A gent（ ChainA gent，
ParallelA gent，CycleA gent），并⽀持基于muti-agent-system进⾏串联。

## PDF物理页 4

●Runner: A gent 的执⾏器，负责管理A gent的⽣命周期管理、会话状态维护和事件流处理，串
联 Session/M  emory Service 等能⼒


●M  odel: M  odel模块提供了统⼀的LLM   接⼝抽象，⽀持OpenA I兼容的A PI调⽤。通过标准化的
接⼝设计，开发者可以灵活切换不同的模型提供商，实现模型的⽆缝集成和调⽤。该模块主要⽀持
了OpenA I like接⼝的兼容性，已验证公司内外⼤多数接⼝。


●Tool:Tool模块提供了标准化的⼯具定义、注册和执⾏机制，使A gent能够与外部世界进⾏交
互。⽀持同步调⽤（CallableTool）和流式调⽤（StreamableTool）两种模式，满⾜不同场景

的技术需求， 提供各种⼯具能⼒FunctionTool、M  CP、D uckD uckGo 等


●Session: Session模块提供了会话管理功能，⽤于维护A gent与⽤户交互过程中的对话历史和
上下⽂信息。会话管理模块⽀持多种存储后端，包括内存存储和Redis存储


●M  emory: 记录⽤户的⻓期记忆和个性化信息


●Knowledge: 知识管理核⼼组件，它实现了完整的RA G（检索增强⽣成）能⼒。该模块不仅提
供了基础的知识存储和检索功能，还⽀持多种⾼级特性：


●知识源管理：⽀持本地⽂件（M  arkdown、PD F、TXT等）、⽬录批量导⼊、⽹⻚抓取，智能
识别输⼊类 型 。向量存储 ：提供 内存存储 （ 开 发测 试 ） 、PostgreSQL 、pgvector、
ElasticSearch。Embedding：集成OpenA I Embedding、Gemini Embedding，⽀持⾃定义

模型，优化异步批处理性能。智能检索：语义相似度搜索，⽀持多轮对话上下⽂，结果重排序提升
相关性。


●Planner: Planner模块为A gent提供智能规划能⼒，通过不同的规划策略增强A gent的推理和
决策能⼒。⽀持内置思考模型、React结构化规划和⾃定义显式规划指导三种模式，使A gent能够
更好地分解复杂任务和制定执⾏计划


●CodeExecutor：CodeExecutor模块为A gent提供代码执⾏能⼒，⽀持在本地环境或D ocker
容器中执⾏Python、Bash代码，使A gent具备数据分析、科学计算、脚本⾃动化等实际⼯作能
⼒。


●Observability：集成OpenTelemetry标准，在A gent执⾏过程中⾃动记录详细的telemetry
数据，⽀持全链路追踪和性能监控，内置诸多指标。





1.2 tRPC Agent整体交互流程设计

## PDF物理页 5

整个tRPC Agent框架采⽤分层设计实现    ：


● Runner模块是A gent的执⾏器和运⾏环境，负责A gent的⽣命周期管理、会话状态维护和事
件流处理，对接外部web服务


● Event模块负责A gent执⾏过程中的状态传递和实时通信。通过统⼀的事件模型，实现A gent
间解耦通信和透明执⾏监控。


●tRPC A gent沿⽤tRPC的插件化设计，所有组件都能做插件化集成，tRPC A gent有内置的组
件，也做了各种⽣态组件的集成。


●tRPC A gent的Callbacks模块还提供了⼀套完整的回调机制，允许在A gent执⾏、模型推理
和⼯具调⽤的关键节点进⾏拦截和处理。通过回调机制，可以实现⽇志记录、性能监控、内容审核
等功能。





1.3 时序图：


下⾯展示⼀个完整的⽤户和 A gent 对话的完整时序图，展示了runner、service，A gent，
LLM  Flow，M  odel，Tool之间的关系。

## PDF物理页 6



## PDF物理页 7

                           三、核⼼模块详解


1.M    odel模块 - ⼤  语⾔模型抽象层


M  odel模块提供了统⼀的LLM   接⼝抽象，⽀持OpenA I兼容的A PI调⽤。通过标准化的接⼝设计，
开发者可以灵活切换不同的模型提供商，实现模型的⽆缝集成和调⽤。该模块主要⽀持了OpenA I
like接⼝的兼容性，已验证公司内外⼤多数接⼝。


1.1 核⼼接⼝设计



  1 // Model是所有语⾔模型必须实现的接⼝
  2 type Model interface {
  3     // ⽣成内容，⽀持流式响应
  4     GenerateContent(ctx context.Context, request *Request) (<-chan *Res
  5
  6     // 返回模型基本信息
  7     Info() Info
  8 }
  9
 10 // 模型信息结构
 11 type Info struct {
 12     Name string // 模型名称
 13 }

## PDF物理页 8

1.2 OpenAI兼容实现


框架提供了完整的OpenA I兼容实现，⽀持连接各种OpenA I-like接⼝：


  1  // 创建 OpenAI模型
  2  model := openai.New("gpt-4o-mini" ,
  3      openai.WithAPIKey("your-api-key"),
  4      openai.WithBaseURL("https://api.openai.com/v1"), //  可⾃定义   BaseURL
  5  )
  6
  7  // ⽀持⾃定义配置
  8  model := openai.New("custom-model" ,
  9      openai.WithAPIKey("your-api-key"),
 10      openai.WithBaseURL("https://your-custom-endpoint.com/v1" ),
  11     openai.WithChannelBufferSize( 512),
 12      openai.WithExtraFields(map[string]interface{}{
 13          "custom_param": "value",
 14      }),
 15  )






1.3 ⽀持的模型平台


当前框架⽀持所有提供OpenA I兼容A PI的模型平台，包括但不限于：


●OpenAI - GPT-4o、GPT-4、GPT-3.5等系列模型


●腾讯云    - D eepSeek， Hunyuan 系列


●其他云⼚商      - 提供OpenA I兼容接⼝的各类模型，如D          eepSeek， Qwen 等


M  odel模块的详细  介绍  详⻅：  https://trpc-group.github.io/trpc-agent-go/zh/model/




2.Agent模块 - Agent执⾏引擎


A gent模块是tRPC-A gent-Go的核⼼组件，提供智能推理引擎和任务编排能⼒。该模块具备以
下核⼼功能：


●多样化Agent类型     ：⽀持LLM  、Chain、Parallel、Cycle、Graph等不同执⾏模式


●⼯具调⽤与集成      ：提供丰富的外部能⼒扩展机制

## PDF物理页 9

●事件驱动架构    ：实现流式处理和实时监控


●层次化组合    ：⽀持⼦A gent协作和复杂流程编排


●状态管理   ：确保⻓对话和会话持久化


A gent模块通过统⼀接⼝标准实现⾼度模块化，为开发者提供从智能对话助⼿到复杂任务⾃动化的
完整技术⽀持。


2.1 核⼼接⼝设计



  1 type Agent interface {
  2     // 执⾏ Agent调⽤，返回事件流
  3     Run(ctx context.Context, invocation *Invocation) (<-chan *event.Eve
  4
  5     // 返回 Agent可⽤的⼯具列表
  6     Tools() []tool.Tool
  7
  8     // 返回 Agent的基本信息
  9     Info() Info
 10
 11     // 返回⼦ Agent列表，⽀持层次化组合
 12     SubAgents() []Agent
 13
 14     // 根据名称查找⼦    Agent
 15     FindSubAgent(name string) Agent
 16 }






2.2 多种Agent类型


2.21 LLM  Agent - 基础智能Agent


核⼼特点  : 基于LLM  的智能A gent，⽀持⼯具调⽤、流式输出和会话管理。


●执⾏⽅式   : 直接与LLM 交互，⽀持单轮对话和多轮会话


●适⽤场景   : 智能客服、内容创作、代码助⼿、数据分析、问答系统


●优势  : 简单直接、响应快速、配置灵活、易于扩展



 1  agent := llmagent.New(
 2      "assistant",

## PDF物理页 10

 3      llmagent. WithModel(openai.New("gpt-4o-mini" )),
 4      llmagent. WithInstruction("你是⼀个专业的     AI助⼿  "),
 5      llmagent. WithTools([]tool.Tool{calculatorTool, searchTool}),
 6  )







2.22 ChainAgent - 链式处理Agent


核⼼特点   : 流⽔线模式，多个A gent按顺序执⾏，前⼀个的输出成为后⼀个的输⼊。


●执⾏⽅式    : A gent1 → A gent2 → A gent3 顺序执⾏


●适⽤场景    : ⽂档处理流⽔线、数据ETL、内容审核链条


●技术优势    : 专业分⼯、流程清晰、易于调试



  1 chain := chainagent.New(
 2      "content-pipeline",
 3      chainagent.WithSubAgents([]agent.Agent{
 4          planningAgent,    // 第⼀步：制定计划
 5          researchAgent,    // 第⼆步：收集信息
 6          writingAgent,     // 第三步：创作内容
 7      }),
 8  )







2.23 ParallelAgent - 并⾏处理Agent


核⼼特点   : 并发模式，多个A gent同时执⾏相同任务，然后合并结果。


●执⾏⽅式    : A gent1 + A gent2 + A gent3 同时执⾏


●适⽤场景    : 多专家评估、多维度分析、决策⽀持


●技术优势    : 并发执⾏、多⻆度分析、容错性强



  1 parallel := parallelagent.New(
 2      "multi-expert-evaluation" ,
 3      parallelagent.WithSubAgents([]agent.Agent{
 4          marketAgent,      //  市场分析专家
 5          technicalAgent,   //  技术评估专家
 6          financeAgent,     //  财务分析专家

## PDF物理页 11

 7     }),
 8 )







2.24 CycleAgent - 循环迭代Agent


核⼼特点  : 迭代模式，通过多轮"执⾏     →评估  →改进"循环，不断优化结果。


●执⾏⽅式   : 循环执⾏直到满⾜条件或达到最⼤轮次


●适⽤场景   : 复杂问题求解、内容优化、⾃动调试


●技术优势   : ⾃我改进、质量提升、智能停⽌



 1 cycle := cycleagent.New(
 2     "problem-solver",
 3     cycleagent.WithSubAgents([]agent.Agent{
 4         generatorAgent,  // ⽣成解决⽅案
 5         reviewerAgent,   // 评估质量
 6     }),
 7     // 设置最⼤迭代次数为    5，防⽌⽆限循环
 8     cycleagent.WithMaxIterations(5),
 9 )







2.25 GraphAgent - 图⼯作流Agent


核⼼特点  : 基于图的⼯作流模式，⽀持条件路由和多节点协作的复杂任务处理。


设计⽬的: 为了满⾜和兼容腾讯内部之前⼤多数的A I A gent应⽤是基于图编排框架进⾏开发的，⽅
便存量⽤户迁移，保留已有的开发习惯。


●执⾏⽅式   : 按图结构执⾏，⽀持LLM 节点、⼯具节点、条件分⽀和状态管理


●适⽤场景   : 复杂决策流程、多步骤任务协作、动态路由处理、存量图编排应⽤迁移


●技术优势   : 灵活路由、状态共享、可视化流程、兼容现有开发模式



  1 // 创建⽂档处理⼯作流
  2 stateGraph := graph.NewStateGraph(graph.MessagesStateSchema())
  3
  4 // 创建分析⼯具

## PDF物理页 12

   5  complexityTool := function.NewFunctionTool(
   6      analyzeComplexity,
   7      function.WithName("analyze_complexity"),
   8      function.WithDescription(    "分析⽂档复杂度       "),
   9  )
  10  tools :=  map[ string]tool.Tool{"analyze_complexity": complexityTool}
  11
  12  // 构建⼯作流图
  13  g, err := stateGraph.
  14      AddNode("preprocess"   , preprocessDocument).               //  预处理节点
  15      AddLLMNode("analyze"   , model,
  16          " 分析⽂档复杂度，使⽤         analyze_complexity⼯具     ", tools). // LLM  分析节点
  17      AddToolsNode(  "tools" , tools).                            //  ⼯具节点
  18      AddNode("route_complexity", routeComplexity).               //  路由决策节点
  19      AddLLMNode("summarize", model, "     总结复杂⽂档      ", nil ).  // LLM总结节点
  20      AddLLMNode("enhance"   , model,   "提升简单⽂档质量       ",  nil). // LLM  增强节点
  21      AddNode("format_output", formatOutput).                     //  格式化节点
  22      SetEntryPoint(  "preprocess").                              //  设置⼊⼝
  23      SetFinishPoint("format_output").                            //  设置出⼝
  24      AddEdge("preprocess"   , "analyze"  ).                   //     连接节点
  25      AddToolsConditionalEdges(    "analyze",   "tools" , "route_complexity"   ).
 26       AddConditionalEdges(   "route_complexity", complexityCondition, map[s
  27          "simple"  :  "enhance"  ,
 28           "complex"  : "summarize",
 29       }).
 30       AddEdge("enhance"   , "format_output").
  31      AddEdge("summarize",     "format_output"  ).
  32      Compile()
 33
 34   // 创建  GraphAgent 并运⾏
 35   graphAgent, err := graphagent.New("document-processor", g,
 36       graphagent.WithDescription("     ⽂档处理⼯作流      "),
  37      graphagent.WithInitialState(graph.State{}),
 38   )
 39
 40   runner := runner.NewRunner("doc-workflow"      , graphAgent)
  41  events, _ := runner.Run(ctx, userID, sessionID,
 42       model.NewUserMessage(    "处理这个⽂档内容       "))



A gent详细介绍：     https://trpc-group.github.io/trpc-agent-go/zh/agent/





2.3 M  ulti-Agent System - 多Agent协作系统


tRPC-A gent-Go采⽤SubA gent机制构建多A gent系统，⽀持多个A gent协作处理复杂任务。

## PDF物理页 13

   1 // 创建专业领域     Agent
  2  marketAnalyst := llmagent.  New("market-analyst",
  3      llmagent.WithModel (model),
  4      llmagent.WithInstruction(  "你是市场分析专家      "),
  5      llmagent.WithTools ([]tool.Tool{marketDataTool}))
  6
  7  techArchitect := llmagent.  New("tech-architect",
  8      llmagent.WithModel (model),
  9      llmagent.WithInstruction(  "你是技术架构专家      "),
  10     llmagent.WithTools ([]tool.Tool{techAnalysisTool}))
  11
  12 // 串⾏协作：市场分析        → 技术评估
  13 planningChain := chainagent.New("product-planning",
 14      chainagent. WithSubAgents([]agent.Agent{
  15         marketAnalyst, techArchitect,
 16      }))
  17
 18  // 并⾏协作：多专家同时评估
 19  expertPanel := parallelagent.  New("expert-panel",
 20      parallelagent. WithSubAgents([]agent.Agent{
  21         marketAnalyst, techArchitect,
 22      }))
 23
 24  // 执⾏多  Agent协作
 25  events, err := expertPanel.Run  (ctx, &agent.Invocation{
 26      Message: model. NewUserMessage ("分析市场，设计产品⽅案        "),
 27  })






3.Event模块 - 事件驱动  系 统


Event模块是tRPC-A gent-Go的事件系统核⼼，负责A gent执⾏过程中的状态传递和实时通信。
通过统⼀的事件模型，实现A gent间解耦通信和透明执⾏监控。


3.1 核⼼特性


●异步通信    ：A gent通过事件流进⾏⾮阻塞通信，⽀持⾼并发执⾏


●实时监控    ：所有执⾏状态通过事件实时传递，⽀持流式处理


●统⼀抽象    ：不同类型A gent通过相同事件接⼝交互


●多Agent协作    ：⽀持分⽀事件过滤和状态追踪

## PDF物理页 14

3.2 核⼼接⼝



  1 // Event代表  Agent执⾏过程中的⼀个事件
 2  type Event struct  {
 3      *model.Response        // 嵌⼊LLM 响应的所有字段
 4      InvocationID  string   // 本次调⽤的唯⼀标识
 5      Author        string   // 事件发起者（    Agent 名称）
 6      ID            string   // 事件唯⼀标识
 7      Timestamp    time.Time // 事件时间戳
 8      Branch        string   // 分⽀标识（多    Agent 协作）
 9  }






3.3 主要事件类型


●chat.completion  - LLM  对话完成事件


●chat.completion.chunk - 流式对话事件


●tool.response - ⼯具响应事件


●agent.transfer - A gent转移事件


●error - 错误事件





3.4 Agent.Run()与事件处理


所有A gent都通过   Run()⽅法返回事件流，实现统⼀的执⾏接⼝：



   1 // Agent 接⼝定义
  2  type Agent  interface {
  3      Run(ctx context.Context, invocation *Invocation) (<-chan *    event.Ev
  4  }
  5
  6  // 创建  Agent并处理事件流
  7  agent := llmagent.New("assistant",
  8      llmagent.WithModel(model),
  9      llmagent.WithTools(tools))
  10

## PDF物理页 15

  11  events, err := agent.Run(ctx, &agent.Invocation{
  12      Message: model.NewUserMessage(       "计算   2+3 等于多少     "),
  13  })
  14
  15  // 实时处理事件流
  16  for  event := range events {
  17       switch  event .Object {
  18       case "chat.completion.chunk":
  19          fmt.Print(event    .Choices[0].Delta.Content)
  20       case "tool.response":
  21          fmt.Printf(    "\n[%s]  ⼯具执⾏完成      \n" , event .Author)
  22       case "chat.completion"    :
  23           if  event .Done {
  24              fmt.Printf(    "\n[%s]   最终答案    : %s\n" ,
  25                     event.Author,    event .Choices[0  ].Message.Content)
  26          }
  27       case "error"  :
  28          fmt.Printf(    "错误  : %s\n" , event  .Error.Message)
  29           return   event .Error
  30      }
  31       if event .Done { break }
  32  }






3.5 多Agent协作中的事件流



   1  chainAgent := chainagent.New("chain",
   2      chainagent.WithSubAgents([]agent.Agent{
   3          analysisAgent, solutionAgent,
   4      }))
   5
   6  events, err := chainAgent.Run(ctx, invocation)
   7  if err != nil {
   8       return err
   9  }
  10
  11  for  event := range events {
  12       switch  event.Object {
  13       case "chat.completion.chunk":
  14          fmt.Print(event    .Choices[0].Delta.Content)
  15       case "chat.completion"    :
  16           if  event.Done {
  17              fmt.Printf(    "[%s] 完成   : %s\n",   event.Author,
  18                     event.Choices[   0].Message.Content)

## PDF物理页 16

  19         }
 20       case "tool.response":
  21         fmt.Printf(   "[%s] ⼯具执⾏完成     \n" , event.Author)
 22       case "error":
 23          fmt.Printf(   "[%s] 错误  : %s\n",  event.Author,   event.Error.Message
 24      }
 25  }





4.Invocation - Agent执⾏上下⽂


Invocation是A gent执⾏的核⼼上下⽂对象，封装了单次调⽤所需的所有信息和状态。它作为
A gent.Run()⽅法的参数，⽀持事件追踪、状态管理和A gent间协作。


4.1 核⼼结构



   1 type  Invocation  struct  {
   2          Agent             Agent                    //       要调⽤的   Agent实例
  3           AgentName           string                   // Agent名称
  4           InvocationID        string                   //     调⽤唯⼀标识
  5           Branch              string                   //     分⽀标识符（多      Agent
  6           EndInvocation       bool                      //    是否结束调⽤
   7          Session           *session.Session         //       会话状态
  8           Model             model.Model              //       语⾔模型
  9           Message           model.Message            //       ⽤户消息
  10          EventCompletionCh <-chan    string            // 事件完成信号
  11          RunOptions        RunOptions               //       运⾏选项
  12          TransferInfo      *TransferInfo            // Agent转移信息
  13          AgentCallbacks    *Callbacks               // Agent回调
  14          ModelCallbacks    *model.Callbacks         //       模型回调
  15          ToolCallbacks     *tool.Callbacks          //       ⼯具回调
  16 }
  17
  18 type  TransferInfo  struct {
  19          TargetAgentName string    // ⽬标  Agent名称
 20           Message         string    // 转移消息
  21          EndInvocation   bool      // 转移后是否结束
 22  }






4.2 主要功能

## PDF物理页 17

●执⾏上下⽂     ：A gent标识、调⽤追踪、分⽀控制


●状态管理    ：会话历史、模型配置、消息传递


●事件控制：异步通信、执⾏选项


●Agent协作   ：控制权转移、回调机制





4.3 使⽤示例



  1  // 创建   Invocation 对象（⾼级⽤法）
  2  invocation := agent.NewInvocation(
  3      agent.WithInvocationAgent(r.agent),                               /
  4      agent.WithInvocationSession(&session.Session{ID:     "session-001"}), /
  5      agent.WithInvocationEndInvocation(   false),                         /
  6      agent.WithInvocationMessage(model.NewUserMessage(    "User input" )),  /
  7      agent.WithInvocationModel(modelInstance),                         /
  8  )
  9
 10  // 直接调⽤    Agent （⾼级⽤法）
  11 ctx := context.Background()
 12  eventChan, err := llmAgent.Run(ctx, invocation)
 13  if err !=  nil {
 14      log.Fatalf( "执⾏   Agent 失败  : %v", err)
 15  }








4.4 最佳实践


●优先使⽤Runner⾃动创建Invocation


●框架会⾃动填充M  odel、Callbacks等字段


●使⽤transfer⼯具实现A gent转移，避免直接设置TransferInfo






5.Planner模块 - 智能规划引擎

## PDF物理页 18

Planner模块为A gent提供智能规划能⼒，通过不同的规划策略增强A gent的推理和决策能⼒。⽀
持内置思考模型、React结构化规划和⾃定义显式规划指导三种模式，使A gent能够更好地分解复
杂任务和制定执⾏计划。其中React模式通过"思考-⾏动"循环和结构化标签，                        为普通模型提供显
式的推理指导，确保A gent能够系统性地处理复杂任务。


5.1 核⼼接⼝设计




  1  // Planner接⼝定义了所有规划器必须实现的⽅法
  2  type Planner interface {
  3      // 构建规划指令，为     LLM请求添加规划相关的系统指令
  4      BuildPlanningInstruction(
  5          ctx context.Context,
  6          invocation *agent.Invocation,
  7          llmRequest *model.Request,
  8      ) string
  9
 10      // 处理规划响应，对     LLM的响应进⾏后处理和结构化
 11      ProcessPlanningResponse(
 12          ctx context.Context,
 13          invocation *agent.Invocation,
 14          response *model.Response,
 15      ) *model.Response
 16  }








5.2 内 置规划策略



5.21 Builtin Planner - 内置思考规划器


适⽤于具有原⽣思考能⼒的模型，通过配置模型参数启⽤内部推理机制：



  1  // 为OpenAI o系列模型配置推理强度
  2  builtinPlanner := builtin.New(builtin.Options{
  3      ReasoningEffort: stringPtr("medium"), // "low", "medium", "high"
  4  })
  5
  6  // 为Claude/Gemini模型启⽤思考模式
  7  builtinPlanner := builtin.New(builtin.Options{
  8      ThinkingEnabled: boolPtr(true),
  9      ThinkingTokens:  intPtr(1000),

## PDF物理页 19

 10 })







5.22 React Planner - 结构化规划器


React（Reasoning and A cting）Planner是⼀种A I推 理 模式， 通 过 结构化 标 签引导 模 型 进
⾏"思考-⾏动"循环。它将复杂问题分解为四个标准化阶段：制定计划、推理分析、执⾏⾏动、提
供答案。这种显式的推理过程让A gent能够系统性地处理复杂任务，同时提⾼决策的可解释性和错
误检测能⼒。






5.3 集成到 Agent



React Planner可以⽆缝集成到任何LLM  A gent中，为A gent提供结构化的思考能⼒。集成后，
A gent会⾃动按照React模式的四个阶段来处理⽤户请求，确保每个复杂任务都能得到系统性的处

理。



  1 // 创建带规划能⼒的    Agent
  2 agent := llmagent.New(
  3     "planning-assistant",
  4     llmagent.WithModel(openai.New("gpt-4o")),
  5     llmagent.WithPlanner(reactPlanner), // 集成规划器
  6     llmagent.WithInstruction("你是⼀个善于规划的智能助⼿    "),
  7 )
  8
  9 // Agent将⾃动使⽤规划器来：
 10 // 1. 为复杂任务制定步骤化计划（      PLANNING阶段）
 11 // 2. 在执⾏过程中进⾏推理分析（      REASONING阶段）
 12 // 3. 调⽤相应⼯具执⾏具体操作（      ACTION阶段）
 13 // 4. 整合所有信息提供完整答案（      FINAL_ANSWER阶段）



实际应⽤效果   ： 使⽤React Planner的A gent在处理复杂查询时，会展现出明显的结构化思考特
征。例如，当⽤户询问"帮我制定⼀个旅⾏计划"时，A gent会⾸先分析需求（PLA NNING），然
后推理最佳路线（REA SONING），接着查询具体信息（A CTION），最后提供完整的旅⾏建议
（FINA L_A NSWER ）。这种⽅式不仅提⾼了回答质量，还让⽤户能够清楚地看到A gent的思考过
程。







5.4 ⾃定义规划器

## PDF物理页 20

开发者可以实现⾃定义规划器来满⾜特定需求：



   1 // ⾃定义   Reflection 规划器示例
  2  type ReflectionPlanner struct    {
  3      maxIterations   int
  4  }
  5
  6  func  (p *ReflectionPlanner) BuildPlanningInstruction(
   7     ctx context.Context,
  8      invocation *agent.Invocation,
  9      llmRequest *model.Request,
  10 ) string {
  11     return  `请按以下步骤进⾏反思式规划：
  12 1. 分析问题并制定初始计划
  13 2. 执⾏计划并收集结果
  14 3. 反思执⾏过程，识别问题和改进点
  15 4. 基于反思优化计划并重新执⾏
  16 5. 重复反思-    优化过程直到达到满意结果         `
  17 }
  18
  19 func  (p *ReflectionPlanner) ProcessPlanningResponse(
 20      ctx context.Context,
  21     invocation *agent.Invocation,
 22      response *model.Response,
 23  ) *model.Response {
 24      // 处理反思内容，提取改进建议
 25      // 实现反思逻辑      ...
 26      return  response
 27  }
 28
 29  // 使⽤⾃定义规划器
 30  reflectionPlanner := &ReflectionPlanner{maxIterations: 3     }
  31 agent := llmagent.New(
 32      "reflection-agent"  ,
 33      llmagent.WithModel(model),
 34      llmagent.WithPlanner(reflectionPlanner),     // 使⽤⾃定义规划器
 35  )



Planner   模   块  的  详   细   介   绍   请   参   阅   ：  https://trpc-group.github.io/trpc-agent-

go/zh/planner/





6.Tool模块 - ⼯具调⽤框架

## PDF物理页 21

Tool模块提供了标准化的⼯具定义、注册和执⾏机制，使A gent能够与外部世界进⾏交互。⽀持
同步调⽤（CallableTool）和流式调⽤（StreamableTool）两种模式，满⾜不同场景的技术需
求。



6.1 核⼼接⼝设计




  1  // 基础⼯具接⼝
  2  type Tool  interface {
  3      Declaration() *Declaration  // 返回⼯具元数据
  4  }
  5
  6  // 同步调⽤⼯具接⼝
  7  type CallableTool   interface {
  8      Call(ctx context.Context, jsonArgs []    byte) (any,  error)
  9      Tool
 10  }
  11
 12  // 流式⼯具接⼝
 13  type StreamableTool interface    {
 14      StreamableCall(ctx context.Context, jsonArgs []byte) (*tool.StreamR
 15      Tool
 16  }







6.2 ⼯具创建示例




   1 //  计算器⼯具
   2 calculatorTool := function.   NewFunctionTool (
  3       func(ctx context.Context, input struct {
  4          Expression string `json:"expression"`
   5     }) (struct {
  6          Result float64 `json:"result"`
   7     }, error) {
  8          result, err :=   evaluateExpression(input.Expression)
  9          return struct{Result float64}{result}, err
  10     },
  11     function .WithName("calculator"),
  12     function .WithDescription("  执⾏数学计算     "),
  13 )
  14
  15  type weatherInput struct {

## PDF物理页 22

16      Location string `json:"location"      `
17    }
18
19   type weatherOutput struct {
20      Weather string `json:    "weather"`
21   }
22
23  // 2.  实现流式⼯具函数
24   func getStreamableWeather(input       weatherInput) *tool   .StreamReader {
25       stream := tool.NewStream     (10 )
26       go func() {
27          defer stream.Writer.Close      ()
28
29          // 模拟逐步返回天⽓数据
30          result :=    "Sunny, 25°C in " + input.Location
31          for i :=    0; i  < len(result); i++ {
32              chunk := tool.StreamChunk{
33                  Content: weatherOutput{
34                      Weather: result[i : i+1],
35                  },
36                  Metadata: tool.Metadata{CreatedAt: time.          Now ()},
37              }
38
39              if closed := stream.Writer.Send(chunk, nil); closed {
40                  break
41              }
42              time.Sleep(10     *  time .Millisecond  ) // 模拟延迟
43          }
44      }()
45
46      return stream   .Reader
47  }
48
49  // 3.  创建流式⼯具
50      weatherStreamTool :=           function.NewStreamableFunctionTool[w
51          getStreamableWeather,
52          function.   WithName ("get_weather_stream"),
53          function.   WithDescription   ("流式获取天⽓信息        "),
54      )
55
56  // 创建多⼯具     Agent
57  agent := llmagent.   New (
58      "multi-tool-assistant",
59      llmagent.  WithModel(model),
60      llmagent.  WithTools([]tool.Tool{
61          calculatorTool,

## PDF物理页 23

  62          weatherStreamTool,
  63          duckduckgo.NewTool    (),
 64       }),
  65  )







6.3 MCP⼯具集成



框架⽀持各种mcp⼯具调⽤，提供多种连接⽅式：



   1  // STDIO mcp  ⼯具
   2  mcpToolSet := mcp.NewMCPToolSet     (
   3      mcp.ConnectionConfig{
   4           Transport:   "stdio" ,
   5           Command :    "python" ,
   6           Args :      []string  {"-m",   "my_mcp_server"  },
   7           Timeout :    10 * time.Second,
   8      },
   9  )
  10
  11  // SSE mcp⼯具
  12  mcpToolSet := mcp.NewMCPToolSet     (
  13      mcp.ConnectionConfig{
  14           Transport:   "sse",
  15           ServerURL:   "http://localhost:8080/sse"     ,
  16           Timeout :    10 * time.Second,
  17           Headers : map[string  ]string  {
  18                "Authorization"  : "Bearer your-token",
  19          },
  20      },
  21  )
  22  // streamable mcp⼯具
  23  mcpToolSet := mcp.NewMCPToolSet     (
  24      mcp.ConnectionConfig{
  25           Transport:   "streamable_http",  //     注意：使⽤完整名称
 26            ServerURL:   "http://localhost:3000/mcp"     ,
  27           Timeout :    10 * time.Second,
 28       },
 29   )
 30
  31  agent := llmagent.New("mcp-assistant",
  32      llmagent.WithModel(model),

## PDF物理页 24

 33      llmagent.WithToolSets([]tool.ToolSet{mcpToolSet}))



Tool 模块的详细介绍请参阅：https://trpc-group.github.io/trpc-agent-go/zh/tool/





7.CodeExecutor模块 - 代码执⾏引擎


CodeExecutor模 块 为A gent提供 代 码执⾏ 能⼒， ⽀ 持 在本 地 环 境或D ocker容器 中执⾏
Python、Bash代码，使A gent具备数据分析、科学计算、脚本⾃动化等实际⼯作能⼒。



7.1 核⼼接⼝设计




  1  // CodeExecutor 是代码执⾏的核⼼接⼝
  2  type CodeExecutor  interface {
  3      ExecuteCode(context.Context, CodeExecutionInput) (CodeExecutionResu
  4      CodeBlockDelimiter() CodeBlockDelimiter
  5  }
  6
  7  // 代码执⾏输⼊和结果
  8  type CodeExecutionInput struct   {
  9      CodeBlocks  []CodeBlock
 10      ExecutionID string
  11 }
 12
 13  type CodeExecutionResult   struct {
 14      Output      string   // 执⾏输出
 15      OutputFiles []File  // ⽣成的⽂件
 16  }







7.2 两种执⾏器实现



7.21 LocalCodeExecutor - 本地执⾏器


直接在本地环境执⾏代码，适⽤于开发测试和可信环境：



  1  // 创建本地执⾏器
  2  localExecutor := local. New (
  3      local. WithWorkDir("/tmp/code-execution"),

## PDF物理页 25

  4      local. WithTimeout(  30*time.Second),
  5      local. WithCleanTempFiles(true),
  6  )
  7
  8  //  集成到  Agent
  9  agent := llmagent.  New(
 10      "data-analyst"  ,
  11     llmagent.WithModel   (model),
 12      llmagent.WithCodeExecutor    (localExecutor), //   集成代码执⾏器
 13      llmagent.WithInstruction(    "你是数据分析师，可以执⾏          Python代码   "),
 14  )







7.22 ContainerCodeExecutor - 容器执⾏器


在隔离的D ocker容器中执⾏代码，提供更⾼安全性，适⽤于⽣产环境：



   1 //  创建容器执⾏器
  2  containerExecutor, err := container.New(
  3      container.  WithContainerConfig  (container.Config{
  4          Image:   "python:3.11-slim"  ,
  5      }),
  6      container.WithHostConfig(container     .HostConfig {
  7          AutoRemove:  true,
  8          NetworkMode: "none",  //     ⽹络隔离
  9          Resources: container.Resources{
 10              Memory: 128 *    1024  * 1024 ,  // 内存限制
  11         },
 12      }),
 13  )
 14
 15  agent := llmagent.  New(
 16      "secure-analyst",
  17     llmagent.WithModel   (model),
 18      llmagent.WithCodeExecutor    (containerExecutor), //    使⽤容器执⾏器
 19  )







7.3 ⾃动 代码块识别



框架⾃动从A gent回复中提取markdown代码块并执⾏：

## PDF物理页 26

 1  // Agent回复包含代码块时会⾃动执⾏：
 2  // ```python
 3  // import statistics
 4  // data = [1, 2, 3, 4, 5]
 5  // print(f"平均值  : {statistics.mean(data)}")



⽀持 python和bash代码



  1
  2  #### 使⽤示例
  3
  4  ```go
  5  // 数据分析   Agent
  6  dataAgent := llmagent.New(
  7      "data-scientist",
  8      llmagent.WithModel(model),
  9      llmagent.WithCodeExecutor(local.New()),
 10      llmagent.WithInstruction("你是数据科学家，使⽤       Python标准库进⾏数据分析       "),
  11 )
 12
 13  // ⽤户提问，   Agent⾃动⽣成并执⾏代码
 14  runner := runner.NewRunner("analysis" , dataAgent)
 15  events, _ := runner.Run(ctx, userID, sessionID,
 16      model.NewUserMessage("分析数据   : 23, 45, 12, 67, 34, 89"))
  17
 18  // Agent⾃动：
 19  // 1. ⽣成 Python分析代码
 20  // 2. 执⾏代码获取结果
 21  // 3. 解读分析结果



CodeExecutor模块使A gent从纯对话升级为具备实际计算能⼒的智能助⼿，⽀持数据分析、脚本
⾃动化、科学计算等应⽤场景。后续⽀持更多的remote代码执⾏器




8.Runner模块 - Agent执⾏器


Runner模块是A gent的执⾏器和运⾏环境，负责A gent的⽣命周期管理、会话状态维护和事件流
处理。



8.1 核⼼接⼝

## PDF物理页 27

  1 type Runner    interface  {
  2     Run(
 3          ctx context.Context,
 4          userID string    ,           //    ⽤户标识
 5          sessionID string     ,        //   会话标识
 6          message model.Message,         //  输⼊消息
  7         runOpts ...agent.RunOption,        // 运⾏选项
 8      ) (<-  chan  *event.Event,   error)   //   返回事件流
 9  }







8.2 使⽤示例




   1  // 步骤  1: 创建  Agent
   2  agent := llmagent.New(
   3      "customer-service-agent",
   4      llmagent.WithModel(openai.New(     "gpt-4o-mini")),
   5      llmagent.WithInstruction(    " 你是专业的客服助⼿        "),
   6  )
   7
   8  // 步骤  2: 创建  Runner并绑定    Agent
   9  r := runner.NewRunner(
  10      "customer-service-app"    ,  // 应⽤名称
  11      agent,                       // 绑定   Agent
  12  )
  13  ctx := context.Background()
  14  userMessage := model.NewUserMessage("      你好！   ")
  15  eventChan, err := r.Run(ctx,     "user1",   "session1"  , userMessage)
  16  if err !=  nil {
  17      panic(err)
  18  }
  19  for event := range    eventChan {
 20       if  event.Error !=   nil  {
  21          fmt.Printf(   "错误  : %s\n", event.Error.Message)
  22          continue
 23       }
 24       if  len(event.Choices) >0 {
 25           fmt.Print(event.Choices[0     ].Delta.Content)
 26       }
  27  }

## PDF物理页 28

Runner   模    块   的  详    细    介    绍    请    参    阅    ：https://trpc-group.github.io/trpc-agent-
go/zh/runner/




9.Memory模块 - 智能记忆系 统


M  emory模块为A gent提供持久化的记忆能⼒，使A gent能够跨会话记住和检索⽤户信息，提供个
性化的交互体验。



9.1 ⼯作原理



A gent通过内置的记忆⼯具⾃动识别和存储重要信息，⽀持主题标签分类管理，并在需要时智能检
索相关记忆。通过 A ppName+UserID  实现多租户隔离，确保⽤户数据安全。







9.2 应⽤场景



适⽤于个⼈助⼿、客服机器⼈、教育辅导、项⽬协作等需要跨会话记忆⽤户信息的场景，如记住⽤
户偏好、追踪问题解决进度、保存学习计划等。






9.3 核⼼接⼝




   1 type Service interface {
  2      // 添加新记忆
  3      AddMemory(ctx context.Context, userKey UserKey, memory string    , top
  4      // 更新现有记忆
  5      UpdateMemory(ctx context.Context, memoryKey Key, memory string    , to
  6      // 删除指定记忆
  7      DeleteMemory(ctx context.Context, memoryKey Key) error
  8      // 清空⽤户所有记忆
  9      ClearMemories(ctx context.Context, userKey UserKey) error
  10     // 读取最近记忆
  11     ReadMemories(ctx context.Context, userKey UserKey, limit    int) ([]*
  12     // 搜索记忆
  13     SearchMemories(ctx context.Context, userKey UserKey, query string    )
  14     // 获取记忆⼯具
  15     Tools() []tool.Tool
  16 }

## PDF物理页 29

  17
  18  // 数据结构
  19  type Entry  struct {
 20       ID        string       `json:"id"`
  21      AppName   string       `json:"app_name"`
  22      UserID    string       `json:"user_id"`
 23       Memory    *Memory      `json:"memory"`
 24       CreatedAt time.Time    `json:"created_at"`
 25       UpdatedAt time.Time    `json:"updated_at"`
 26   }
  27
 28   type Memory  struct {
 29       Memory        string       `json:"memory"`
 30       Topics      []string       `json:"topics,omitempty"`
  31      LastUpdated *time.Time     `json:"last_updated,omitempty"`
 32   }







9.4 快速集成




   1 llmAgent := llmagent.   New (
  2       "memory-assistant",
  3      llmagent.  WithTools(memoryService.Tools     ()), //  ✅  步骤  1：注册⼯具
  4  )
  5
  6  runner := runner.   NewRunner(
  7       "app" ,
  8      llmAgent,
  9      runner.WithMemoryService    (memoryService), // ✅      步骤  2：设置服务
 10  )
  11







9.5 内 置记忆⼯具



           ⼯具名称                         默认状态                        功能描述

         memory_add                      ✅  启⽤                   添加新的记忆条⽬

        memory_update                    ✅  启⽤                   更新现有记忆内容

## PDF物理页 30

       memory_search             ✅  启⽤              根据关键词搜索记忆

       memory_load               ✅  启⽤              加载最近的记忆记录

       memory_delete             ❌  禁⽤               删除指定记忆条⽬

       memory_clear              ❌  禁⽤               清空⽤户所有记忆







9.6 使⽤示例




  1 // Agent会⾃动调⽤记忆⼯具：
  2
  3 // 记录信息  : "我叫张三，住在北京     "
  4 // → memory_add("张三住在北京   ", ["个⼈信息 "])
  5
  6 // 查询信息  : "我住在哪⾥？   "
  7 // → memory_search("住址") → 返回相关记忆
  8
  9 // 更新信息  : "我搬到上海了   "
 10 // → memory_update(id, "张三住在上海  ", ["个⼈信息  "])



M  emory   模   块  的 详   细   介   绍   请   参   阅   ：  https://trpc-group.github.io/trpc-agent-
go/zh/memory/





10.Session模块 - 会 话管理系 统


Session模块提供了会话管理功能，⽤于维护A gent与⽤户交互过程中的对话历史和上下⽂信息。
会话管理模块⽀持多种存储后端，包括内存存储和Redis存储，后续会根据⽤户需求补⻬M  ySql、

PgSql等存储后端，为A gent应⽤提供了灵活的状态持久化能⼒。


10.1 核⼼特性



●会话持久化    ：保存完整的对话历史和上下⽂


●多存储后端    ：⽀持内存存储和Redis存储，内⽹版本可⽆缝接⼊tRPC Redis插件


●事件追踪   ：完整记录会话中的所有交互事件

## PDF物理页 31

10.2 会 话层次结构




  1 Application (  应⽤  )
 2  ├── User   Sessions  (⽤户会话)
 3  │   ├── Session    1 (会话1  )
 4  │   │   ├── Session    Data  (会话数据    )
 5  │   │   └── Events (   事件列表    )
 6  │   └── Session    2 (会话2  )
  7 │       ├── Session    Data  (会话数据    )
 8  │       └── Events (   事件列表    )
 9  └── App Data   (应⽤数据    )







10.3 核⼼接⼝




   1  // Service定义会话服务的核⼼接⼝
   2  type Service interface    {
   3  // CreateSession creates a new session.
   4           CreateSession(ctx context.Context, key Key, state StateMap, op
   5
   6  // GetSession gets a session.
   7           GetSession(ctx context.Context, key Key, options ...Option) (*
   8
   9  // ListSessions lists all sessions by user scope of session key.
  10           ListSessions(ctx context.Context, userKey UserKey, options ...O
  11
  12  // DeleteSession deletes a session.
  13           DeleteSession(ctx context.Context, key Key, options ...Option)
  14
  15  // AppendEvent appends an event to a session.
  16           AppendEvent(ctx context.Context, session *Session, event *even
  17
  18  // Close closes the service.
  19           Close()  error
 20   }







10.4 存储后端⽀持

## PDF物理页 32

  1  // 内存存储（适⽤于开发测试）
  2  sessionService := inmemory.NewSessionService()
  3
  4  // Redis存储（适⽤于⽣产环境）
  5  sessionService, err := redis.NewService(
  6      redis.WithURL( "redis://localhost:6379/0"),
  7  )
  8
  9  // 内⽹版本使⽤     tRPC Redis插件，同样的⽅式，只需额外引⼊内⽹的              redis 包，即可使⽤    tRP
 10  import _ "git.woa.com/trpc-go/trpc-agent-go/trpc/storage/redis"
  11
 12  sessionService, err := redis.NewService(
 13      redis.WithURL( "redis://localhost:6379/0"),
 14  )







10.5 与 Runner集成




  1 // 创建  Runner并配置会话服务
 2  runner := runner.NewRunner(
 3      "my-agent",
 4      llmAgent,
 5      runner.WithSessionService(sessionService),    // 集成会话管理
 6  )
 7
 8  // 使⽤  Runner进⾏多轮对话
 9  eventChan, err := runner.Run(ctx, userID, sessionID, userMessage)



Session   模   块  的 详   细   介   绍   请   参   阅   ：  https://trpc-group.github.io/trpc-agent-
go/zh/session/





11.Knowledge模块 - 知识管理系 统


Knowledge模块是trpc-agent-go中的知识管理核⼼组件，它实现了完整的RA G（检索增强⽣
成）能⼒。该模块不仅提供了基础的知识存储和检索功能，还⽀持多种⾼级特性：


（1） 知识源管理


a. ⽀持多种格式的本地⽂件（M  arkdown、PD F、TXT等）

## PDF物理页 33

b. ⽀持⽬录批量导⼊，⾃动处理⼦⽬录


c. ⽀持⽹⻚抓取，可直接从URL加载内容


d. 智能识别输⼊类型，⾃动选择合适的处理器


（2）向量存储


a. 内存存储：适⽤于开发和⼩规模测试


b. PostgreSQL + pgvector：适⽤于⽣产环境，⽀持持久化


c. TcVector：云原⽣解决⽅案，适合⼤规模部署


（3）Embedding


a. 默认集成OpenA IEmbedding模型


b. ⽀持⾃定义  Embedding模型接⼊


c. 异步批处理优化性能


（4） 智能检索


a. 基于语义的相似度搜索


b. ⽀持多轮对话历史上下⽂


c. 结果重排序提升相关性







11.1 核⼼接⼝设计




  1  // Knowledge是知识管理的主要接⼝
  2  type Knowledge interface {
  3      // Search执⾏语义搜索并返回相关结果
  4      Search(ctx context.Context, req *SearchRequest) (*SearchResult, er
  5  }
  6
  7  // SearchRequest代表带上下⽂的搜索请求
  8  type SearchRequest struct {
  9      Query     string                  // 搜索查询⽂本
 10      History   []ConversationMessage   // 对话历史⽤于上下⽂

## PDF物理页 34

  11      UserID    string                 // ⽤户标识
  12      SessionID string                 // 会话标识
  13  }
  14
  15  // SearchResult  代表知识搜索的结果
  16  type SearchResult   struct {
  17      Document *document.Document //      匹配的⽂档
  18      Score    float64                // 相关性分数
  19      Text     string                 // ⽂档内容
 20   }







11.2 与 Agent集成




   1  // 创建知识库
   2  kb := knowledge.New(
   3      knowledge.WithVectorStore(inmemory.New()),
   4      knowledge.WithEmbedder(openai.New()),
   5      knowledge.WithSources([]source.Source{
   6          file.New([]   string{ "./docs/llm.md"  }),
   7          url.New([]string{"https://wikipedia.org/wiki/LLM"         }),
   8      }),
   9  )
  10
  11  // 加载知识库
  12  kb.Load(ctx)
  13
  14  // 创建带知识库的      Agent
  15  agent := llmagent.New(
  16      "knowledge-assistant",
  17      llmagent.WithModel(model),
  18      llmagent.WithKnowledge(kb), //      ⾃动添加    knowledge_search⼯具
  19      llmagent.WithInstruction("    使⽤  knowledge_search   ⼯具搜索相关资料来回答问题
 20   )



Knowledge  模   块  的 详   细   介   绍   请   参   阅   ：  https://trpc-group.github.io/trpc-agent-
go/zh/knowledge/





12.Observability模块 - 可观测性系 统

## PDF物理页 35

Observability模块集成OpenTelemetry标准，在A gent执⾏过程中⾃动记录                    详细的telemetry
数据，⽀持全链路追踪和性能监控。框架复⽤OpenTelemetry标准接⼝，⽆⾃定义抽象层。



12.1 快速启动




   1 import (
   2     agentmetric   "trpc.group/trpc-go/trpc-agent-go/telemetry/metric"
  3      agenttrace   "trpc.group/trpc-go/trpc-agent-go/telemetry/trace"
  4  )
   5
  6  func  main()  {
   7     ctx := context.Background()
  8
  9       // 启动  telemetry收集
  10     cleanupTrace, _ := agenttrace.Start(ctx)        // 默认  localhost:4317
  11     cleanupMetric, _ := agentmetric.Start(ctx) //        默认 localhost:4318
  12      defer cleanupTrace()
  13      defer cleanupMetric()
  14
  15      // Agent 执⾏过程将⾃动记录        telemetry数据
  16     agent := llmagent.New(    "assistant",
  17         llmagent.WithModel(openai.New(     "gpt-4o-mini")))
  18
  19     runner := runner.NewRunner(    "app", agent)
 20      events, _ := runner.Run(ctx, "user-001",       "session-001"  ,
  21         model.NewUserMessage("    你好  "))
 22  }







12.2 ⾃动 记录的    Trace链路



框架⾃动创建以下Span层次结构：



   1 invocation                                   # 对话顶层    span
  2  ├── call_llm                                # LLM API调⽤
  3  ├── execute_tool calculator                 # ⼯具调⽤
  4  ├── execute_tool search                     # ⼯具调⽤
  5  └── execute_tool (merged)                   # 并⾏⼯具调⽤合并
  6
  7  # GraphAgent  执⾏链路
  8  invocation

## PDF物理页 36

  9  └── execute_graph
 10      ├── execute_node preprocess
  11     ├── execute_node analyze
  12     │   └── run_model
 13      └── execute_node format







12.3 主要  Span属性



●通⽤属性      ： invocation_id, session_id, event_id


●LLM   调⽤  ： gen_ai.request.model, llm_request/response JSON


●⼯具调⽤      ： gen_ai.tool.name, tool_call_args, tool_response JSON


●Graph节点     ： node_id, node_name, node_description






12.4 配置选项



12.41 ⾃定义端点配置



  1  cleanupTrace, _ := agenttrace.     Start (ctx,
 2       agenttrace.  WithEndpoint   ("otel-collector:4317"    ))







12.41 ⾃定义M  etrics



  1  counter, _ := metric.Meter.     Int64Counter  ("agent.requests.total"    )
  2  counter. Add (ctx, 1 , metric.  WithAttributes  (
 3       attribute.String   ("agent.name",    "assistant"  )))



Observability 模  块 的详  细  介  绍  请  参  阅  ：   https://trpc-group.github.io/trpc-agent-
go/zh/observability/

## PDF物理页 37

13.Debug Server - 调试服务器


D ebug Server提供HTTP调试服务，兼容A D K Web UI，⽀持A gent执⾏的可视化调试和实时监
控。



13.1 快速启动




  1  // 步骤  1: 准备 Agent实例
  2  agents := map[string]agent.Agent{
  3      "chat-assistant": llmagent.New  (
  4          "chat-assistant",
  5          llmagent.WithModel  (openai.New ("gpt-4o-mini")),
  6          llmagent.WithInstruction(  "你是⼀个智能助⼿       "),
  7      ),
  8  }
  9
 10  // 步骤  2: 创建 Debug Server
  11 debugServer := debug.New(agents)
 12
 13  // 步骤  3: 启动HTTP  服务器
 14  http.Handle ("/", debugServer. Handler())
 15  log.Fatal(http. ListenAndServe (":8080" , nil))




D ebug  Server  的 详   细   介   绍   请   参   阅   ：https://trpc-group.github.io/trpc-agent-
go/zh/debugserver/





14.Callbacks模块 - 回调机  制


Callbacks模块提供了⼀套完整的回调机制，允许在A gent执⾏、模型推理和⼯具调⽤的关键节点
进⾏拦截和处理。通过回调机制，可以实现⽇志记录、性能监控、内容审核等功能。






14.1 回调类型



14.11 M  odelCallbacks（模型回调）



  1          _ = model.NewCallbacks().

## PDF物理页 38

  2                    RegisterBeforeModel(func   (ctx context.Context, req *mode
  3                             fmt.Printf("🌐    Global BeforeModel: processing %
  4  return  nil , nil
  5                    }).
  6                    RegisterAfterModel(func(ctx context.Context, req *model
  7  if modelErr !=   nil  {
  8                                      fmt.Printf("🌐    Global AfterModel: erro
  9                             }  else {
 10                                      fmt.Printf("🌐    Global AfterModel: proce
  11                            }
 12  return  nil , nil
 13                    })
 14



a. BeforeM  odel：模型推理前触发，可⽤于输⼊拦截、⽇志记录


b. A fterM  odel：每个输出块后触发，可⽤于内容审核、结果处理






14.12 ToolCallbacks（⼯具回调）



   1          _ = tool.NewCallbacks().
  2                    RegisterBeforeTool(func(ctx context.Context, toolName s
  3                             fmt.Printf("🌐    Global BeforeTool: executing %s\
  4  return  nil , nil
  5                    }).
  6                    RegisterAfterTool(   func(ctx context.Context, toolName st
  7  if runErr != nil {
  8                                      fmt.Printf("🌐    Global AfterTool: %s fai
  9                             }  else {
 10                                      fmt.Printf("🌐    Global AfterTool: %s com
  11                            }
 12  return  nil , nil
 13                    })
 14



a. BeforeTool：⼯具调⽤前触发，可⽤于参数验证、结果模拟


b. A fterTool：⼯具调⽤后触发，可⽤于结果处理、⽇志记录






14.13 AgentCallbacks（Agent回调）

## PDF物理页 39

  1          _ = agent.NewCallbacks().
  2                   RegisterBeforeAgent(func (ctx context.Context, invocatio
  3                           fmt.Printf("🌐   Global BeforeAgent: starting %s\
  4  return nil , nil
  5                   }).
  6                   RegisterAfterAgent(func(ctx context.Context, invocation
  7  if runErr != nil {
  8                                    fmt.Printf("🌐   Global AfterAgent: execu
  9                           }  else {
 10                                    fmt.Printf("🌐   Global AfterAgent: execu
  11                          }
 12  return nil , nil
 13                   })
 14  )
 15



a. BeforeA gent：A gent执⾏前触发，可⽤于权限检查、输⼊验证


b. A fterA gent：A gent执⾏后触发，可⽤于结果处理、错误处理






14.2 使⽤场景



（1） 监控和⽇志    ：记录模型调⽤、⼯具使⽤和A gent执⾏过程


（2） 性能优化    ：监控响应时间和资源使⽤情况


（3） 安全和审核     ：过滤输⼊内容，审核输出内容


（4） ⾃定义处理     ：格式化结果，重试错误，增强内容







14.3 集成示例




  1  // 创建带回调的Agent
  2  agent := llmagent. New(
  3      "callback-demo" ,
  4      llmagent.WithModel (model),
  5      llmagent.WithModelCallbacks(modelCallbacks),
  6      llmagent.WithToolCallbacks  (toolCallbacks),

## PDF物理页 40

  7      llmagent.WithAgentCallbacks(agentCallbacks),
  8  )
  9
 10  // 创建  Runner并执⾏
  11 runner := runner.NewRunner  (
 12      "callback-app" ,
 13      agent,
 14      runner. WithSessionService (sessionService),
 15  )
 16
 17  // 执⾏对话
 18  events, err := runner.  Run(ctx, userID, sessionID,
 19      model. NewUserMessage( "Hello"))



Callbacks模块通过提供灵活的回调机制，使得A gent的⾏为更可控、更透明，同时为监控、审
核、定制化等需求提供了强⼤的⽀持。




15.A2A集成 - Agent间通信


A 2A  (A gent-to-A gent) 模块提供A gent间通信能⼒，⽀持将tRPC-A gent-Go的A gent快速集
成到A 2A协议中，实现多A gent协作以及对外暴露能⼒。


15.1 快速启动




   1 // 步骤  1: 创建  Agent
  2  agent := llmagent.New(
  3      "my-agent",
  4      llmagent.WithModel(openai.New(   "gpt-4o-mini")),
  5      llmagent.WithInstruction("   你是⼀个智能助⼿      "),
  6  )
  7
  8  // 步骤  2: 创建  A2A服务器
  9  a2aServer, err := a2a.New(
  10     a2a.WithAgent(agent,true),              // 绑定  Agent
  11     a2a.WithHost("localhost:8080"), // 设置监听地址
  12 )
  13 if err != nil {
  14     log.Fatal(err)
  15 }
  16
  17 // 步骤  3: 启动服务器
  18 ctx := context.Background()

## PDF物理页 41

 19 if err := a2aServer.Start(ctx); err != nil {
 20     log.Fatal(err)
 21 }
 22
 23 log.Println("A2A服务器已启动 : localhost:8080")







                           四、业务实践


tRPC-Agent-Go在内部 ⽤诸多 应⽤  ，在这⾥介绍下   四个业务   场景：


1. 元宝-深度写作


业务通过GraphA gent编排⾃动化写作流⽔线。A 2A A gent先⾏调⽤搜索服务获取素材，随后LLM
Node⽣成XM  L⼤纲并流式处理，最后循环调⽤Writer LLM 节点按⼤纲逐步⽣成内容。


2. 腾讯体育-体育⼤ 聪明


战报⽣成：LLM  A gent通过M  CP⼯具获取数据，并以其“思考模式”分步⽣成回顾、摘要与标题。


体育搜索：GraphA gent驱动业务流程：LLM 节点先改写查询，Planner节点规划  M  CP⼯具调⽤
获取信息，最终输出并流式解析为前端卡⽚。


多轮助⼿：GraphA gent实现路由，通过A 2A A gent调度体育类请求⾄专属A gent，⾮体育类问题
则路由⾄联⽹SubA gent  。


3. AMS⼴告营销-报表Agent


GraphA gent是核⼼：其LLM   Node结合tRA G分析意图，流式⽣成“⾏动模板”并推送前端。随后
根据模板调⽤M  CP⼯具获取业务数据，最终组装成图表、表格等组件化报表。


4. 腾讯视频海外-翻译Agent


基于trpc-agent框架快速构建了四个专业LLM  A gent（剧情提取、术语提取、术语翻译、字幕翻
译）形成⼯作流。框架的封装回调机制将复杂逻辑内聚，对外提供简洁接⼝，⾼效完成从原始字幕
到多语⾔终稿的转换。

## PDF物理页 42

                             五、写在最后


特别感谢腾讯各业务单元，包括腾讯元宝、腾讯视频、腾讯新闻、IM  A  和 QQ ⾳乐的宝贵⽀持和
⽣产环境验证推动框架发展。


感谢优秀的开源框架如 A D K、A gno、CrewA I、A utoGen 等的启发，       让tRPC -A gent-Go得以
站在巨⼈的肩膀上快速前⾏！        🙏


tRPC-Agent-Gogithub：https://github.com/trpc-group/trpc-agent-go


欢迎star！


除此之外  tRPC的Go A I⽣态还 提供 了 A2A（https://github.com/trpc-group/trpc-a2a-go）
和M  CP框 架的开发能⼒（https://github.com/trpc-group/trpc-mcp-go ）  也 欢 迎⼤家  使
⽤。






                            关注 腾 讯开 源公 众号
                       获 取更 多最 新 腾讯 官⽅ 开源 信 息！

       腾讯开源
       腾讯官⽅开源动态、开发经验分享
       91篇原创内容


 公众号




                    加⼊微信群即可了解更多“      腾讯开源新动态”


















阅读 2648





留⾔


写留⾔

## PDF物理页 43

还没有留⾔，来写⾸评
