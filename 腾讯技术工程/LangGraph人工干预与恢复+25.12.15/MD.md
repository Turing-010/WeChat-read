# 破除AI Agent自主操控风险：万字解读LangGraph“人工干预”机制，附零基础实战

来源：[RAW.pdf](RAW.pdf)，capture-001。

这是PDF文本层按物理页码转写，不是AI总结。图片未嵌入；图内文字、截图、公式、表格及代码排版可能未提取或不可靠；源PDF中存在的右侧裁切不补写。实际复核范围详见META.json。

## PDF物理页 1

破除 AI Agent⾃主操控⻛险：万字解读       LangGraph“⼈ ⼯⼲预”机  制
，附零基础实战


原创 腾讯程序员  腾讯技术⼯程  2025年12⽉15⽇   02:18⼴东258⼈
















作者： yukixxwang



  随着⼤型语⾔模型（LLM）驱动的⾃主代理（Agent）从学术⾛向应⽤，如何确保其⾏为
  的可靠性、安全性与可控性，已成为决定其能否在真实世界关键任务中落地的核⼼挑战。
  ⼤语⾔模型能⼒虽然越来越强，但并⾮完美⽆缺，可能产⽣错误或不准确输出。当⼀个
  Agent 被授权执⾏⾼风险领域或敏感操作时，⼀个⼩⼩的错误也可能带来不可预知的风
  险。所以我们需要“⼈⼯⼲预”机制，在关键决策点让 Agent 停下来，将控制权交还给⼈
  类，让⼈类的智慧能够介⼊，弥补模型的不⾜。


 引⾔

随着⼤型语⾔模型（LLM）驱动的⾃主代理（Agent）从学术⾛向应⽤，如何确保其⾏为的可
靠性、安全性与可控性，已成为决定其能否在真实世界关键任务中落地的核⼼挑战。⼤语⾔模
型能⼒虽然越来越强，但并⾮完美⽆缺，可能产⽣错误或不准确输出。当⼀个 Agent 被授权
执⾏⾼风险领域或敏感操作时，⼀个⼩⼩的错误也可能带来不可预知的风险。所以我们需要
“⼈⼯⼲预”机制，在关键决策点让 Agent 停下来，将控制权交还给⼈类，让⼈类的智慧能够介
⼊，弥补模型的不⾜。
 全⽂概览

在介绍 Multi-agent的⼈⼯⼲预机制之前，我们先简单介绍Multi-Agent的基本概念：定义、主
流开发框架、⼈⼯⼲预。之后我们会着重以LangGraph为例，介绍LangGraph的⼈⼯⼲预机制
的核⼼原理、四⼤经典模式、      以及具体的案例实践。在案例实践中，我们除了介绍
LangGraph的四⼤经典模式案例之外，还通过  MCP协议提供的智能搜索⼯具（Venus MCP
server市场 - ⽹络综合搜索⼯具）搭建了真实案例来帮助⼤家理解  LangGraph的中断机制。



 什么是 Multi-Agent？

简单来说，Multi-Agent（多智能体）系统不是由⼀个“⽆所不知”的超级AI来解决所有问题，⽽
是由多个具有特定⾓⾊和能⼒的、相对简单的⾃主智能体（Agent）协同⼯作，共同完成⼀个

## PDF物理页 2

复杂任务的系统。这些智能体各⾃有⾃⼰的专长（通过不同的Prompt             、⼯具和知识库来定
义），它们之间可以沟通、协作、互相反馈、甚⾄辩论，最终合⼒交付⼀个⾼质量的成果。

核⼼特征：

● 分解 (Decomposition): 将⼀个宏⼤、模糊的任务分解成多个具体、可执                                                                                                            ⾏的⼦任务。

● 专长 (Specialization): 每个智能体都有明确的⾓⾊和擅长的技能（例如，⼀个智能体专门⽤
于⽹络搜索，另⼀个专门⽤于代码执⾏）                                                                                   。

● 协作 (Collaboration): 智能体之间通过信息交换（类似内部聊天）来协调⼯作。例如，程序
员写完代码后交给测试员。

● ⾃主性 (Autonomy): 每个智能体可以在其职责范围内独⽴做出判断和执⾏操作，⽆需⼈类每
⼀步都进⾏⼲预。



Multi-Agent主流开发框架

随着LLM（⼤型语⾔模型）的发展，多智能体框架也迎来了爆发式增长。它们封装了智能体定
义、通信、任务调度等复杂逻辑，让开发者能更专注于业务逻辑。⽬前主流的开发框架主要
有：LangGraph、AutoGen、CrewAI、MetaGPT和Magentic。



Multi-Agent中的⼈⼯⼲预

什么是⼈⼯⼲预

简单来说，就是让⼈类能够参与到机器的⼯作流程中，深⼊到AI的核⼼⼯作环节，让⼈类能够
实时审查、编辑甚⾄批准AI的决策和⾏动。尤其是在由⼤语⾔模型驱动的应⽤场景中，这种机
制显得尤为重要。因为LLM虽然很强⼤，但有时候也会犯错，或者需要⼀些额外的背景知识才
能做出正确的判断。这时候就需要⼈类来帮忙把关。













引⼊⼈⼯⼲预的必要性

⼤语⾔模型能⼒越来越强，写⽂章、写代码、翻译、做数学等，但并⾮完美⽆缺，可能产⽣错
误或不准确输出。当⼀个 Agent 被授权执⾏预订酒店、调⽤付费 API 、修改数据库、或遇到
法律、医疗这种⾼风险领域等敏感操作时，在拥有完全的⾃主性的情况下，甚⾄⼀个⼩⼩的错
误也可能带来不可预知的风险。

## PDF物理页 3

所以我们需要⼀种机制，需要⼀个“暂停按钮”，在关键决策点让 Agent 停下来，将控制权交还
给⼈类，让⼈类的智慧能够介⼊，结合⼈类的判断⼒、专业知识和经验给AI的⼯作加⼀道保
险，弥补模型的不⾜。⼈类还可以通过审核、修正、验证等操作，提⾼应⽤的准确性和可靠
性。在处理复杂或敏感任务时，⼈⼯⼲预能够提供更可靠的保障。



LangGraph中的⼈⼯⼲预

LangGraph 框架通过其强⼤的“⼈机协同（”Human-in-the-Loop）功能，提供了⼀套优雅⽽完
备的解决⽅案。本⽂接下来将深⼊剖析 LangGraph 如何通过持久化状态与动态中断机制，实
现灵活、可靠的⼈⼯⼲预，并详解其在实践中的四⼤核⼼设计模式。

LangGraph 框架通过其创新的 interrupt（中断）机制，使得构建需要⼈⼯审查、编辑和批准
的“⼈机协同（”Human-in-the-Loop）⼯作流成为可能。当⼯作流（Graph）执⾏到中断点时，
它会保存当前的所有状态，然后⽆限期暂停，直到接收到⼈类的输⼊指令后再从断点处继续。
这为构建可靠、安全且透明的    Agent 应⽤奠定了基⽯。

它允许⽤户在⼯作流的任何阶段进⾏⼲预。这对于⼤型语⾔模型驱动的应⽤程序尤其有⽤，因
为模型输出可能需要验证、更正或补充上下⽂。该功能包括两种中断类型：动态中断和静态中
断，允许⽤户暂停图执⾏并进⾏审查或编辑。此外，灵活的集成点使⼈类可以针对特定步骤进
⾏⼲预，例如批准   API 调⽤、更正输             出或引导对话。

作⽤及应⽤场景

● 对关键步骤（如外部  API 调⽤）进                ⾏⼈⼯批准/拒绝，防⽌错误执⾏。

● 纠正或补充模型输出，提升结果可靠性。

● 让业务⼈员在不阻塞整个系统的情况下提供上下⽂或修正。

核⼼能⼒

LangGraph 的⼈机协同能⼒构建于两                           ⼤基⽯之上：持久化的执⾏状态 和 灵活的中断机制。

持久化执⾏状态

这是实现异步、⽆时间限制⼈⼯审查的关键。LangGraph    在⼯作流（Graph）的每⼀步执⾏
后，都会利⽤其持久化层（Persistence Layer）来创建检查点（Checkpoint），完整地保存
当前 Graph 的所有状态。

这意味着，当⼀个⼯作流被中断时，它的全部上下⽂都被安全地保存下来。⼈类可以在任何时
候（⼏秒、⼏⼩时甚⾄⼏天后）回来处理这个中断，然后系统可以从中断点⽆缝恢复，继续执
⾏后续任务，⽽不会丢失任何信息。

灵活的中断机制

● 动态中断 (Dynamic Interrupts)

## PDF物理页 4

在特定节点内部根据当前状态暂停，这种⽅式就像在程序⾥设置了⼀个条件判断，当满⾜某个
特定条件时，就⾃动触发中断。例如，当你的LLM在⽣成⼀段⽂本后，你希望检查⼀下这段⽂
本是否符合某些特定的要求（是否有敏感词、信息是否准确等），如果发现不符合要求，就可
以动态触发中断，把⼯作流暂停下来，等待⼈⼯介⼊。这种⽅式⾮常灵活，可以根据实际情况
随时调整中断的条件，真正做到按需暂停。

● 静态中断 (Static Interrupts)

在预定义的节点前后固定设置。中断后图会暂停，状态持久化，等待⼈⼯操作后再         resume。

这种⽅式⽐较直接，它是在⼯作流设计阶段预先定义好的。你可以指定在某个特定的节点之前
或者之后，必须暂停⼯作流，等待⼈⼯⼲预。或者，在某个关键步骤之后，需要⼈⼯确认结果
是否正确，才能继续下⼀步。静态中断就像是在⼯作流中设置了⼏个固定的“关卡”，每到⼀个
关卡，就必须有⼈来检查⼀下，确保万⽆⼀失。

触发⽅式： 使⽤ interrupt_before 和 interrupt_after，在预定义的节点前后暂停。

适⽤场景：需要在固定流程节点进⾏⼈⼯审核或确认的场景。

⽰例：在 API 调⽤前使⽤ interrupt_before，确保 API 请求的合规性。

## PDF物理页 5

灵活的集成点

LangGraph的⼈⼯⼲预机制还有⼀个⾮常重要的特点，就是它的集成点⾮常灵活。也就是说，
你可以把⼈⼯⼲预的逻辑放在⼯作流的任何位置。你可以根据不同的需求，选择在不同的节点
进⾏⼈⼯⼲预。⽐如，你想让⼈类审批API调⽤，那就把中断点放在   API调⽤节点之前；你想
让⼈类纠正LLM的输出，那就把中断点放在LLM⽣成输出之后。这种灵活性使得我们可以根据
具体的业务场景，定制化地设计⼈⼯⼲预的流程，真正做到精准定位，避免不必要的⼲预。

典型模式

基于上述强⼤的功能，我们可以构建出各种各样的典型应⽤场景。

● 模式⼀：批准/拒绝

在⼯作流的关键步骤前暂停⼀下，让⼈类来审核⼀下，看看这个操作是不是应该执⾏。如果审
核通过，就继续执⾏；如果审核不通过，就可以拒绝这个操作，甚⾄可以采取⼀些替代⽅案。

## PDF物理页 6

● 应⽤场景：API调⽤前的审批、敏感操作确认（                                财务交易确认、订单确认）

● 价值：降低风险，防⽌错误操作，提⾼安全性。

● 模式⼆：编辑图状态

暂停后让⼈⼯修改状态后再继续。有时候，LLM在⽣成结果的过程中，可能会出现⼀些错误，
或者信息不够完整。这时候，我们就可以暂停⼯作流，让⼈类来审核当前的状态，并进⾏修
改。修改完成后，再把更新后的状态重新放回⼯作流中，让后续的步骤继续执⾏。这样就能保
证整个⼯作流的数据质量，避免因为错误的信息⽽导致后续步骤出现问题。











● 应⽤场景：纠正错误信息（纠正⽤户姓名拼写错误）                                                                                                              、补充缺失信息、更新上下⽂等。

● 价值：修正错误，完善信息，提升后续步骤的准确性。

● 模式三：审查⼯具调⽤

在 LLM 发出⼯具请求前让⼈⼯检查并可编辑。我们知道，LLM往往需要借助各种⼯具来完成
任务，⽐如搜索⽹络信息、查询数据库等。但是，LLM有时候可能会选错⼯具，或者调⽤⼯具
的参数设置不正确。为了避免这种情况，我们可以再LLM发起⼯具调⽤之前，先暂停⼯作流，
让⼈类来审核⼀下这个⼯具调⽤是否合理。⽐如，LLM可能想调⽤⼀个⽀付API来完成转账，
但是参数设置错了，导致⾦额输⼊错误。这时候，⼈类就可以介⼊，检查⼀下⼯具调⽤的参数
是否有错误，若有错误就及时纠正。











● 应⽤场景：审核  API请求参数、验证                                ⼯具选择的合理性等。

## PDF物理页 7

● 价值：确保⼯具调⽤的正确性和安全性，避免错误操作。

● 模式四：验证⼈⼯输⼊

在后续步骤前确认⼈⼯提供的信息有效。这个模式听起来好像有点反直觉，因为我⼀直在讲
“human-in-the-loop”，怎么⼜变成验证⼈类输⼊了呢？其实，这个模式主要是针对那些需要
⽤户输⼊信息的场景。⽐如，⽤户填写⼀个表单，或者在聊天机器⼈中输⼊⼀些指令。为了确
保⽤户输⼊的信息是有效的，我们可以利⽤⼈⼯⼲预机制，在系统处理⽤户输⼊之前，先暂停
⼀下，让⽤户⾃⼰确认⼀下输⼊的信息是否正确。如果⽤户确认⽆误，就继续执⾏；如果⽤户
发现输⼊有误，可以及时修改。










● 应⽤场景 ：⽤户输⼊验证、表单数据校验等。

● 价值：确保数据质量，防⽌⽆效或错误的输⼊影响后续流程。


      腾讯技术⼯程
      腾讯技术官⽅号。腾讯技术创新、前沿领域发布解读平台。
      690篇原创内容


 公众号


langGraph中的⼈⼯⼲预核⼼                                     ⼯作流

实现⼀次完整的⼈机交互闭环，       interrupt 的⼯作流遵循⼀个清晰的四步模式：

1. 配置持久化层   (Checkpointer)：中断的本质是状态的保存与恢复。因此，在编译        Graph
  时，必须为其指定⼀个      checkpointer，⽤于在每⼀步执⾏后⾃动保存状态。





 from langgraph.checkpoint.memory import InMemorySaver



 checkpointer = InMemorySaver()

 graph = graph_builder.compile(checkpointer=checkpointer)


2. 在节点中调⽤   interrupt()：在需要⼈⼯⼲预的节点函数中，调⽤     interrupt() 函数。此函数
  会⽴即暂停执⾏，并可以向⽤户传递⼀个          JSON 可序列化的对象，其中包含需要审查的数
  据。





 from langgraph.types import interrupt

## PDF物理页 8

  def human_review_node(state: State):

      # 中断执⾏，并将 state 中的摘要⽂本交给⽤户审查

      edited_data = interrupt({

          "task": "请审查并编辑下⾯的摘要",

          "summary_to_review": state["summary"]

      })

      # 恢复后，edited_data 将是⽤户输⼊的新内容

      return {"summary": edited_data["edited_summary"]}


3. 运⾏并触发中断       ：使⽤     invoke 或 stream ⽅法并传⼊                     唯⼀的 thread_id 来运⾏ Graph。当
   执⾏流遇到      interrupt() 时，Graph 会暂     停，并在返回结果中包含⼀个特殊
   的 interrupt 键，其中包含了中断的详细信息（如传递给⽤户的数据）                                                                                                                         。





  config = {"configurable": {"thread_id": "some-unique-id"}}

  result = graph.invoke({"summary": "初步⽣成的摘要..."}, config=config)



  # 检查中断信息

  print(result['__interrupt__'])

  # > [Interrupt(value={'task': '请审查...', 'summary_to_review': '...'}, id='...')]


4. 使⽤   Command 恢复执⾏       ：当⽤户完成审查并提供输⼊后，通过再次调⽤                        invoke 或
   stream，并传⼊⼀个        Command(resume=...) 对象来恢复       Graph 的执⾏。    resume 中包含的
   值将作为     interrupt() 函数的返回值。





  from langgraph.types import Command



  # ⽤户提供了编辑后的摘要

  user_input = {"edited_summary": "这是经过⼈⼯编辑的最终摘要。"}

  final_result = graph.invoke(Command(resume=user_input), config=config)


⚠  核⼼机制警⽰：恢复即重跑              (Resume Reruns the Node)

这是理解 interrupt 最关键的⼀点：恢复执⾏并⾮从 interrupt()                 函数调⽤的那⼀⾏代码继续，
⽽是从包含      interrupt() 的那个节点的开                                头重新执⾏整个节点。

在 重 跑 期 间，当执 ⾏ 流 再次遇到  interrupt()            时，它不会 再次暂 停，⽽ 是 直 接 返 回
Command(resume=...) 中提供的值。这个设计虽然巧妙，但也意味着任何位于 interrupt() 调⽤
之前的、具有副作⽤的操作（如 API 调⽤、数据库写⼊）都会被重复执⾏。因此，最佳实践
是将副作⽤操作放在          interrupt() 之后，     或置于⼀个独⽴的后续节点中。



langGraph实战模式           --interrupt的四⼤经典模式的应⽤

基于其核⼼机制，        interrupt 可以灵活        地实现多种强⼤的⼈机交互模式。

## PDF物理页 9

要在图中使⽤      interrupt，您需要：

1. 指定⼀个检查点来保存每个步骤后的图形状态。

2. interrupt()在适当的地⽅调⽤。

3. 使⽤线程    ID运⾏图，直到       interrupt命中     。

4. 使⽤  invoke/恢复执⾏    stream。

我们挑选了两个模式（模式⼀和模式三）                                         ，边运⾏边讲解执⾏过程。

模式⼀：审批或否决             (Approve or Reject)

在执⾏⾼风险操作前，强制要求⼈⼯批准。根据⽤户的决策，                             Graph 可以     ⾛向不同的分⽀。

步骤⼀：基本函数定义




  # ⽬标：中断图的执⾏，让⽤户做出决策（如批准/拒绝），然后根据决策跳转到不同的流程分⽀。



  from typing import Literal, TypedDict

  import uuid



  from langgraph.constants import END

  from langgraph.graph import StateGraph

  from langgraph.types import interrupt, Command

  from langgraph.checkpoint.memory import InMemorySaver



  # 1. 定义图的共享状态，包含⼀个 'decision' 字段来记录⼈类的决定

  class State(TypedDict):

      llm_output: str

      decision: str



  # 模拟⼀个⽣成内容的节点

  def generate_llm_output(state: State) -> State:

      print("\n--- 步骤1：AI⽣成内容 ---")

      return {"llm_output": "这是AI⽣成的⼀段需要审批的⽂本。"}



  # 2. 定义⼈⼯审批节点。注意：返回值类型是 Command，意味着此节点将发出控制指令。

  def human_approval(state: State) -> Command[Literal["approved_path", "rejected_path"]]:

      """

      此节点暂停并等待⼈类决策，然后根据决策返回⼀个带有 `goto` 指令的 Command，

      从⽽控制图的⾛向。

      """

      print("\n--- 暂停：等待⼈⼯审批 ---")

      # 3. 暂停图的执⾏，等待⼈类做出决策（例如，输⼊ "approve" 或 "reject"）。

      decision = interrupt({

          "question": "请审批以下内容，回复 'approve' 或 'reject'：",

          "llm_output": state["llm_output"]

## PDF物理页 10

      })



      # 4. 核⼼逻辑：根据⼈类的决策（'decision' 变量的值）进⾏判断。

      if decision == "approve":

          print("\n--- 决策：批准 ---")

          # 5. 如果批准，返回⼀个 Command 指令，强制图跳转到 'approved_path' 节点。

          #    'goto' 是实现条件路由的关键。'update' 是⼀个可选参数，⽤于同时更新状态。

          return Command(goto="approved_path", update={"decision": "approved"})

      else:

          print("\n--- 决策：拒绝 ---")

          # 6. 如果拒绝，则跳转到 'rejected_path' 节点。

          return Command(goto="rejected_path", update={"decision": "rejected"})



  # 批准后的流程节点

  def approved_node(state: State) -> State:

      print("--- 步骤2 (分⽀A): 已进⼊批准流程。---")

      return state



  # 拒绝后的流程节点

  def rejected_node(state: State) -> State:

      print("--- 步骤2 (分⽀B): 已进⼊拒绝流程。---")

      return state


步骤⼆：构建图




  builder = StateGraph(State)

  builder.add_node("generate_llm_output", generate_llm_output)

  builder.add_node("human_approval", human_approval)

  builder.add_node("approved_path", approved_node)

  builder.add_node("rejected_path", rejected_node)



  # 7. 设置图的⼊⼝和边，定义了基本的流程。

  #    注意，从 human_approval 节点出发的路径将由其返回的 Command(goto=...) 动态决定。

  builder.set_entry_point("generate_llm_output")

  builder.add_edge("generate_llm_output", "human_approval")

  builder.add_edge("approved_path", END) # 批准分⽀的终点

  builder.add_edge("rejected_path", END) # 拒绝分⽀的终点



  checkpointer = InMemorySaver()

  graph = builder.compile(checkpointer=checkpointer)


步骤三：⾸次运⾏，图会执⾏到                    human_approval 节点并暂停




  config = {"configurable": {"thread_id": f"thread-{uuid.uuid4()}"}}

  print("⾸次调⽤，启动审批流程...")

## PDF物理页 11

  result = graph.invoke({}, config=config)

  print("\n图已暂停，等待审批...")


运⾏结果：









步骤四：使⽤       Command(resume="approve") 恢复执⾏：




  #  "approve" 这个字符串会成为 interrupt() 的返回值，并赋给 'decision' 变量。

  #    你可以尝试将 "approve" 改为 "reject" 来测试另⼀条分⽀。

  print("\n--- 恢复执⾏：传⼊ 'approve' 决策 ---")

  final_result = graph.invoke(Command(resume="approve"), config=config)



  # 打印最终结果。由于我们 resume="approve"，流程会⾛ approved_path，最终状态会包含 'decision': 'ap

  print("\n流程执⾏完毕，最终状态如下:")

  print(final_result)


运⾏结果：








模式⼆：审查与编辑状态                (Review and Edit State)

允许⽤户审查并直接修改             Agent 在执⾏过程中⽣成的数据，如修正⼀篇                     AI ⽣成的⽂章草稿。





  # 模式⼆：编辑状态 (Edit State)

  # ⽬标：中断图的执⾏，让⽤户提供或修改数据，然后⽤该数据更新图的状态。



  # 导⼊所需库

  from typing import TypedDict

  import uuid



  from langgraph.constants import START, END

  from langgraph.graph import StateGraph

  from langgraph.types import interrupt, Command

  from langgraph.checkpoint.memory import InMemorySaver



  # 1. 定义图的状态（State）

## PDF物理页 12

# State 是⼀个 TypedDict，它定义了在整个图的执⾏过程中共享的数据结构。

# 把它想象成所有节点都可以读写的共享内存。

class State(TypedDict):

    summary: str



# 2. 定义图中的各个节点（Node）

# 每个节点都是⼀个函数，它接收当前状态作为输⼊，并返回⼀个字典来更新状态。



# 节点A：模拟AI⽣成摘要

def generate_summary(state: State) -> State:

    print("--- 步骤1: AI 正在⽣成摘要... ---")

    return {

        "summary": "The cat sat on the mat and looked at the stars."

    }



# 节点B：⼈⼯审查和编辑节点

def human_review_edit(state: State) -> State:

    print("--- 步骤2: 等待⼈⼯审查和编辑... ---")

    # 调⽤ interrupt() 来暂停图的执⾏。这是实现⼈机交互的关键。

    # 传⼊的字典会作为中断的有效负载（payload）发送给调⽤⽅（例如前端应⽤），

    # 以便向⽤户展示任务和当前数据。

    result = interrupt({

        "task": "Please review and edit the generated summary if necessary.",

        "generated_summary": state["summary"]

    })



    # 当图恢复执⾏时，interrupt() 的返回值 `result` 将会是稍后通过 Command(resume=...) 传⼊的数据

    # 节点返回⼀个新字典，⽤⼈类编辑后的内容来更新状态中的 'summary' 字段。

    return {

        "summary": result["edited_summary"]

    }



# 节点C：模拟使⽤编辑后摘要的下游任务

def downstream_use(state: State) -> State:

    print(f"--- 步骤3: 正在使⽤编辑后的摘要... ---")

    # 打印最终确认的摘要，证明状态已经被⼈⼯输⼊所更新。

    print(f"✅  Using edited summary: {state['summary']}")

    return state



# 3. 构建图（Graph）

builder = StateGraph(State)



# 将上⾯定义的函数注册为图中的节点

builder.add_node("generate_summary", generate_summary)

builder.add_node("human_review_edit", human_review_edit)

builder.add_node("downstream_use", downstream_use)

## PDF物理页 13

  # 设置图的流程：定义⼊⼝和节点之间的固定连接顺序。

  builder.set_entry_point("generate_summary")

  builder.add_edge("generate_summary", "human_review_edit")

  builder.add_edge("human_review_edit", "downstream_use")

  builder.add_edge("downstream_use", END) # END 表示流程结束



  # 4. 编译图

  # 设置⼀个内存检查点（checkpointing）。这是使⽤ interrupt 功能的必要条件，

  # 因为图需要⼀个地⽅来保存它暂停时的状态。

  checkpointer = InMemorySaver()

  graph = builder.compile(checkpointer=checkpointer)



  # 5. 执⾏图 - 第⼀次调⽤（触发中断）

  # 为本次运⾏创建⼀个唯⼀的线程ID（thread_id），⽤于追踪和恢复状态。

  config = {"configurable": {"thread_id": str(uuid.uuid4())}}

  print("--- 开始执⾏图 ---")

  # ⾸次调⽤图。执⾏将会在 'human_review_edit' 节点中的 interrupt() 处暂停。

  result = graph.invoke({}, config=config)



  # 当图被中断时，返回的结果会包含⼀个 '__interrupt__' 键，其值是中断时发送的数据。

  print("\n--- 图已暂停，等待输⼊ ---")

  print("中断信息:", result["__interrupt__"])



  # 6. 恢复图的执⾏ - 第⼆次调⽤（提供输⼊）

  # 模拟⼈类⽤户提供了编辑后的摘要。

  edited_summary = "The cat lay on the rug, gazing peacefully at the night sky."



  print("\n--- 恢复执⾏图 ---")

  # 使⽤ Command(resume=...) 来恢复图的执⾏。

  # 传⼊的数据（⼀个字典）会成为 'human_review_edit' 节点中 interrupt() 函数的返回值。

  # 注意：必须使⽤与第⼀次调⽤相同的 config（包含相同的 thread_id）来恢复正确的会话。

  resumed_result = graph.invoke(

      Command(resume={"edited_summary": edited_summary}),

      config=config
  )



  print("\n--- 图执⾏完毕 ---")

  # 打印图执⾏完毕后的最终状态，可以看到 'summary' 已经被更新。

  print("最终状态:", resumed_result)


模式三：审查⼯具调⽤               (Review Tool Calls)

这是保障 Agent 安全性的终极防线。可以在 Agent 决定调⽤某个⼯具时强制中断，等待⼈⼯
确认。下⾯会介绍如何在            agent内部通          过中断interrupt()实现⼈⼯⼲预。

环境安装

## PDF物理页 14

 pip install -U langgraph

 pip install -U langchain

 pip install -U langchain_openai


步骤⼀：先⽤     Venus AI平台初始化模型




 BASE_URL=" http://v2.xxxxxx.com/llmproxy"

 TOKEN=...

 MODEL_NAME=... # 可以填写模型名称（e.g. gpt-4o, deepseek-v3.1-terminus,外部模型如gpt-4o，需要单

 from langchain_openai import ChatOpenAI

 from langchain.chat_models import init_chat_model



 model = init_chat_model(
     model=MODEL_NAME,

     model_provider="openai",

     base_url=BASE_URL,

     api_key=TOKEN

     temperature=0,

 )


步骤⼆：定义酒店查询⼯具

这⾥定义了⼀个酒店查询⼯具，后⾯会再引⼊                        MCP 协议提供的智能搜索⼯具为例⽤
LangGraph实现中断





 def search_hotel(hotel_name: str):

    """根据酒店名称查询酒店信息"""

    return f"为您查询{hotel_name}."


注意：这个⼯具定义了⼀个参数              hotel_name，定义了⼯具描述：根据酒店名称查询酒店信
息，在步骤三和步骤四会被提到。

步骤三：定义可⼈⼯⼲预的通⽤的包装器：可为任何⼯具添加

通⽤包装器 add_human_in_the_loop：内部集成了interrupt()，这是个可以包装任何⼯具的函
数。它能在不修改原⼯具代码的情况下，⾃动为其增加⼈⼯审查层，极⼤地提升了代码的模块
化和复⽤性。

可以通过参数     tool和interrupt_conﬁg来直接使⽤。

具体参见下⾯的代码和注释。





 from typing import Callable

 from langchain_core.tools import BaseTool, tool as create_tool

## PDF物理页 15

from langchain_core.runnables import RunnableConfig

from langgraph.types import interrupt

from langgraph.prebuilt.interrupt import HumanInterruptConfig, HumanInterrupt



def add_human_in_the_loop(

    tool: Callable | BaseTool,

    *,

    interrupt_config: HumanInterruptConfig = None,

) -> BaseTool:

    """

    将⼀个⼯具封装起来，为其添加⼈⼯审核（Human-in-the-loop）功能。

    这是⼀个⾼阶函数，它接收⼀个⼯具，返回⼀个带有内置审批流程的新⼯具。

    参数:

        tool: 可以是⼀个普通的 Python 函数，也可以是⼀个继承⾃ BaseTool 的 LangChain ⼯具实例。

        interrupt_config: ⼀个可选的字典，⽤于配置⼈类审批界⾯的选项（如是否允许编辑、批准等）。

    返回:

        ⼀个新的 BaseTool 实例，这个新⼯具封装了原始⼯具并加⼊了⼈⼯审核功能。

    """

    # 步骤 1: 规范化输⼊⼯具

    # 检查传⼊的 `tool` 是否已经是 `BaseTool` 的实例。

    # 如果不是（例如，只是⼀个普通的 Python 函数），则使⽤ `create_tool` 将其转换为⼀个标准的 LangC

    # 这确保了后续代码可以统⼀处理 `tool` 对象。

    ifnot isinstance(tool, BaseTool):

        tool = create_tool(tool)



    # 步骤 2: 设置默认的⼈⼯交互配置

    # 如果⽤户没有提供 `interrupt_config`，则设置⼀个默认配置。

    # 默认允许⽤户：批准 (accept)、编辑 (edit) 或直接回应 (respond)。

    if interrupt_config isNone:

        interrupt_config = {

            "allow_accept": True,

            "allow_edit": True,

            "allow_respond": True,

        }



    # 步骤 3: 创建并返回⼀个新的、封装后的⼯具

    # 使⽤ `create_tool` 装饰器来创建⼀个新的⼯具。

    # 关键在于，这个新⼯具会继承原始⼯具的名称 (`name`)、描述 (`description`) 和参数结构 (`args_sc

    # 这使得调⽤此⼯具的 LLM 能够像使⽤原始⼯具⼀样看到它，⽽不知道其内部包含了⼈⼯审核逻辑。

    @create_tool(

        tool.name,

        description=tool.description,

        args_schema=tool.args_schema

    )

    def call_tool_with_interrupt(config: RunnableConfig, **tool_input):

        """这是新⼯具的具体实现函数，它包含了⼈⼯审核的逻辑。"""

## PDF物理页 16

        # 步骤 3.1: 构建中断请求

        # 构建⼀个 `HumanInterrupt` 类型的字典，这个字典将作为 `interrupt` 函数的参数。

        # 它包含了所有需要展示给⼈类审批者的信息：

        # - action_request: AI 想要执⾏的动作（⼯具名和参数）。

        # - config: 告诉前端界⾯应该显示哪些按钮（批准、编辑等）。

        # - description: 给⼈类审批者的提示信息。

        request: HumanInterrupt = {

            "action_request": {

                "action": tool.name,

                "args": tool_input

            },

            "config": interrupt_config,

            "description": "Please review the tool call"

        }



        # 步骤 3.2: 暂停图并等待⼈类输⼊

        # 调⽤ `interrupt` 函数，将请求打包成列表传⼊。

        # **这是图执⾏暂停的地⽅**。

        # 当图通过 `resume` 命令恢复时，`interrupt` 函数会返回⼀个响应列表，我们取第⼀个响应。

        response = interrupt([request])[0]



        # 步骤 3.3: 根据⼈类的响应采取⾏动

        # 如果⼈类审批者点击了“批准” (`accept`)

        if response["type"] == "accept":

            # 直接使⽤原始的参数调⽤原始⼯具。

            tool_response = tool.invoke(tool_input, config)

        # 如果⼈类审批者编辑了参数 (`edit`)

        elif response["type"] == "edit":

            # 从响应中获取新的参数，更新 `tool_input`。

            tool_input = response["args"]["args"]

            # 然后⽤新参数调⽤原始⼯具。

            tool_response = tool.invoke(tool_input, config)

        # 如果⼈类审批者选择直接回应 (`response`)，⽽不是执⾏⼯具

        elif response["type"] == "response":

            # 将其提供的反馈内容 (`user_feedback`) 直接作为⼯具的输出返回。

            # 这可以⽤来给 LLM 提供指导，例如：“不要搜索这个，请先总结⼀下已有信息。”

            user_feedback = response["args"]

            tool_response = user_feedback

        else:

            # 处理未知的响应类型，增加代码的健壮性。

            raise ValueError(f"Unsupported interrupt response type: {response['type']}")



        # 返回最终结果。这个结果将作为⼯具的执⾏输出，返回给调⽤它的 LLM。

        return tool_response



    # `add_human_in_the_loop` 函数返回这个被完全封装好的、带有新功能的新⼯具。

    return call_tool_with_interrupt

## PDF物理页 17

步骤四：定义可⼈⼯⼲预的预订酒店                 agent

使⽤  步骤三创建的包装器          add_human_in_the_loop和步骤⼆定义的           search_hotel⼯具

search_tools





  from langgraph.checkpoint.memory import InMemorySaver

  from langgraph.prebuilt import create_react_agent

  # 1. 初始化检查点

  # 同样，因为要使⽤中断功能，必须提供⼀个检查点来保存和恢复 Agent 的状态。

  checkpointer = InMemorySaver()



  # 2. 带⼈机交互的agent定义⽅法：

  search_agent = create_react_agent(

      # 指定 Agent 使⽤的 LLM 模型

      model=model,

      # 为 Agent 提供⼯具列表

      tools=[

          # 关键点：我们没有直接传⼊ `search_tool`，

          # ⽽是传⼊了 `add_human_in_the_loop(search_tool)` 的返回结果。

          # 这意味着 Agent 拿到的 `search_hotel` ⼯具已经是被封装过的、带有⼈机交互逻辑的版本。

          # 上⼀节中定义的封装函数

          add_human_in_the_loop(search_hotel),

      ],

      # 将检查点与 Agent 关联起来

      checkpointer=checkpointer,

      name="search_assistant",

      prompt="你是⼀个酒店查询⼯具"

  )


步骤五：配置并运⾏          agent

Turn0:

输⼊  query：我要查酒店，        llm判断会⽤到步骤⼆定义的            search_hotel⼯具





  # 配置并运⾏ Agent

  # 为本次对话创建⼀个唯⼀的线程 ID，以便状态可以被正确保存和恢复。

  config = {"configurable": {"thread_id": "1"}}



  # 使⽤ `stream` ⽅法来运⾏ Agent，这样我们可以观察到每⼀步的中间输出。

  # 这对于理解 Agent 的思考过程和中断发⽣的位置⾮常有帮助。

  # Run the agent

  for chunk in agent.stream(

      {"messages": [{"role": "user", "content": "我要查酒店"}]},

## PDF物理页 18

     config

 ):

     print(chunk)

     print("\n")

 # 注意：此代码运⾏后会暂停，等待下⼀次 `invoke` 或 `stream` 调⽤来恢复。

 # 要完成整个流程，你需要像之前的例⼦⼀样，捕获中断信息，然后⽤ Command(resume=...) 再次调⽤ agent。


此时没有中断，⽽是要求输⼊酒店名称                   hotel_name, 这个是因为我们在步骤⼆定义
search_hotel这个⼯具的时候定义了hotel_name参数，只有当⼯具定义的参数信息都完备时
才具体触发⼯具调⽤前的中断逻辑

运⾏结果：












Turn1:

输⼊ query：帮我查下北京瑰丽酒店的                                           信息





 # 配置并运⾏ Agent

 # 为本次对话创建⼀个唯⼀的线程 ID，以便状态可以被正确保存和恢复。

 config = {"configurable": {"thread_id": "1"}}



 # 使⽤ `stream` ⽅法来运⾏ Agent，这样我们可以观察到每⼀步的中间输出。

 # 这对于理解 Agent 的思考过程和中断发⽣的位置⾮常有帮助。

 # Run the agent

 for chunk in agent.stream(

     {"messages": [{"role": "user", "content": "帮我查下北京瑰丽酒店的信息"}]},

     config
 ):

     print(chunk)

     print("\n")

 # 注意：此代码运⾏后会暂停，等待下⼀次 `invoke` 或 `stream` 调⽤来恢复。

 # 要完成整个流程，你需要像之前的例⼦⼀样，捕获中断信息，然后⽤ Command(resume=...) 再次调⽤ agent。


llm判断会⽤到步骤⼆定义的search_hotel⼯具，且识别出⼯具要求的参数hotel_name=北京瑰
丽酒店，⼯具要求的信息已经完备，此时触发中断

运⾏结果：

## PDF物理页 19

步骤六：     Command根据⼈⼯输⼊恢复                                     代理以继续。




  from langgraph.types import Command



  for chunk in agent.stream(

      Command(resume=[{"type": "accept"}]),

      config

  ):

      print(chunk)

      print("\n")


运⾏结果：















模式四：验证⽤户输⼊                 (Validate Human Input)

在需要⽤户提供特定格式的输⼊时，可以使⽤循环来反复请求，直到输⼊有效为⽌。





  # 导⼊所需库

  from typing import TypedDict

  import uuid



  from langgraph.constants import START, END

  from langgraph.graph import StateGraph

  from langgraph.types import interrupt, Command

  from langgraph.checkpoint.memory import InMemorySaver



  # 1. 定义图的状态

  # State 定义了在整个图的执⾏过程中共享的数据结构。

  class State(TypedDict):

## PDF物理页 20

    age: int



# 2. 定义图中的节点



# 节点A：获取并验证⽤户输⼊的年龄

# 这个节点展示了⼀个⾮常实⽤的模式：在节点内部循环，直到获得有效的⼈类输⼊。

def get_valid_age(state: State) -> State:

    # 初始化第⼀次向⽤户展示的提示信息

    prompt = "Please enter your age (must be a non-negative integer)."



    # 使⽤⼀个⽆限循环来不断请求输⼊，直到输⼊有效为⽌

    whileTrue:

        # 核⼼：调⽤ interrupt() 来暂停图的执⾏，并向⽤户显示提示信息。

        # 当图恢复时，`resume` 命令传⼊的值将成为 `user_input`。

        user_input = interrupt(prompt)



        # 验证⽤户的输⼊

        try:

            age = int(user_input)

            if age < 0:

                raise ValueError("Age must be non-negative.")

            break# 如果输⼊有效（是正整数），则跳出循环

        except (ValueError, TypeError):

            # 如果输⼊⽆效（例如，是字符串或负数），则更新提示信息，

            # 准备在下⼀次循环中向⽤户显示带有错误反馈的新提示。

            prompt = f"'{user_input}' is not valid. Please enter a non-negative integer f



    # 只有在获得有效输⼊并跳出循环后，此节点才会返回结果，更新图的状态。

    return {"age": age}



# 节点B：使⽤验证后的年龄

def report_age(state: State) -> State:

    # 打印最终确认的年龄，证明状态已成功更新。

    print(f"✅  Human is {state['age']} years old.")

    return state



# 3. 构建图

builder = StateGraph(State)

builder.add_node("get_valid_age", get_valid_age)

builder.add_node("report_age", report_age)



# 设置图的执⾏流程

builder.set_entry_point("get_valid_age")

builder.add_edge("get_valid_age", "report_age")

builder.add_edge("report_age", END)



# 4. 编译图

## PDF物理页 21

  # 创建⼀个内存检查点，这是使⽤ interrupt 功能的必要条件。

  # 它负责保存图在暂停时的完整状态（包括在哪个节点的哪⼀⾏）。

  checkpointer = InMemorySaver()

  graph = builder.compile(checkpointer=checkpointer)



  # 5. 执⾏图 - 分步演示



  # 为本次运⾏创建⼀个唯⼀的会话ID

  config = {"configurable": {"thread_id": str(uuid.uuid4())}}



  # 第⼀次调⽤：图启动并⽴即在 get_valid_age 节点内暂停

  print("--- 第⼀次调⽤：请求输⼊ ---")

  result = graph.invoke({}, config=config)

  print("中断信息:", result["__interrupt__"])  # 输出: "Please enter your age..."



  # 第⼆次调⽤：模拟⽤户输⼊⼀个⽆效的字符串

  print("\n--- 第⼆次调⽤：模拟⽆效输⼊ (字符串) ---")

  result = graph.invoke(Command(resume="not a number"), config=config)

  print("中断信息:", result["__interrupt__"])  # 输出: 带有验证失败信息的提示



  # 第三次调⽤：模拟⽤户输⼊⼀个⽆效的负数

  print("\n--- 第三次调⽤：模拟⽆效输⼊ (负数) ---")

  result = graph.invoke(Command(resume="-10"), config=config)

  print("中断信息:", result["__interrupt__"])  # 输出: 带有验证失败信息的提示



  # 第四次调⽤：提供有效的输⼊

  print("\n--- 第四次调⽤：提供有效输⼊ ---")

  final_result = graph.invoke(Command(resume="25"), config=config)

  print("\n--- 图执⾏完毕 ---")

  print("最终状态:", final_result)  # 应该包含有效的年龄并打印出报告


⾼级主题与注意事项

●  并⾏中断与批量恢复：如果                 Graph 并⾏执⾏了多个包含中断的节点，可以通过
graph.get_state(conﬁg).interrupts 获取所有中断的列表，并构造⼀个映射                  resume_map =
{interrupt_id_1: value_1, ...}，通过 Command(resume=resume_map) ⼀次性恢复所有中断。

● ⼦图中的中断：当中断发⽣在⼦图中时，恢复操作会从⽗图中调⽤该⼦图的节点开头，以及
⼦图中包含中断的节点开头同时重跑。

● 调试利器：静态中断：除了⽤于⼈机交互的动态中断，LangGraph 还⽀持在编译时设置静
态中断（interrupt_before, interrupt_after）。这相当于在特定节点前后设置了断点，是单步调
试和检查     Graph 状态的绝佳⼯具，但不推荐⽤于⽣产环境的⼈机交互流程                                                                                                                            。


        腾讯技术⼯程
        腾讯技术官⽅号。腾讯技术创新、前沿领域发布解读平台。
        690篇原创内容

## PDF物理页 22

 公众号



langGraph实战案例        --引⼊  MCP协议实现真实⼯具的中断

本⽰例将实现⼀个通过MCP协议提供的智能搜索⼯具的中断：该⼯具是⼀个综合⽹络搜索插
件，⽀持通⽤⽹络搜索、酒店机票查询、学术检索、新闻咨询、图⽚搜索等功能，需要先在
Venus MCP server市场 - ⽹络综合搜索⼯具创建实例，然后获取访问sse链接后使⽤。该⼯具
均已实现   MCP标准化接⼝，可直接被          Agent调⽤。

步骤⼀：先⽤      Venus AI平台初始化                     模型




 BASE_URL="  http://v2.xxxxxx.com/llmproxy"

 TOKEN=...

 MODEL_NAME=... # 可以填写模型名称（e.g. gpt-4o, deepseek-v3.1-terminus,外部模型如gpt-4o，需要单

 from langchain_openai import ChatOpenAI

 from langchain.chat_models import init_chat_model



 model = init_chat_model(

     model=MODEL_NAME,

     model_provider="openai",

     base_url=BASE_URL,

     api_key=TOKEN

     temperature=0,

 )

步骤⼆：在     Venus MCP server市场     - ⽹络综合搜索⼯具创建实例                             ，然后获取访问
sse链接后使⽤

创建实例：




















独⽴部署实例     -->确认：

## PDF物理页 23

实例 -->使⽤⽅式：














SSE连接 --> sse_url





















步骤三：引⼊    venusMCPserver市场的智能搜多⼯具

## PDF物理页 24

以Venus MCP server市场 - ⽹络综合                搜索⼯具为例⽤      LangGraph实现中断

将步骤⼀的      sse_url赋值给下⾯的         url





  from langchain_mcp_adapters.client import MultiServerMCPClient

  from langgraph.prebuilt import create_react_agent



  search_client = MultiServerMCPClient(
      {

          "other_search": {

              "url": url, # 创建实例后填⼊实例⽣成的sse链接

              "headers": {

                  "Authorization": f"Bearer {TOKEN}" # venus token，结尾有⼀个@XXX，XXX是应⽤组

              },

              "transport": "sse"}

        }

  )

  search_tools = await search_client.get_tools()


步骤四：定义可⼈⼯⼲预的通⽤的包装器：可为任何⼯具添加

由于要调⽤的⼯具是异步的，因此这个通⽤包装器实现过程中也要注意异步实现。与之前定义
的 add_human_in_the_loop不同，有两处需要注意：

 1. call_tool_with_interrupt函数的定义：

async    def    call_tool_with_interrupt(conﬁg:    RunnableConﬁg,    **tool_input):    #    <---    1. 改 为
async def

 2. invoke改为   ainvoke：

tool_response = await tool.ainvoke(tool_input, conﬁg) # <--- 2. 改为      await tool.ainvoke

完整实现见下⾯的代码：





  # 异步

  from typing import Callable

  from langchain_core.tools import BaseTool, tool as create_tool

  from langchain_core.runnables import RunnableConfig

  from langgraph.types import interrupt

  from langgraph.prebuilt.interrupt import HumanInterruptConfig, HumanInterrupt



  def add_human_in_the_loop(

      tool: Callable | BaseTool,

      *,

      interrupt_config: HumanInterruptConfig = None,

## PDF物理页 25

) -> BaseTool:

    """

    将⼀个⼯具封装起来，为其添加⼈⼯审核（Human-in-the-loop）功能。

    这是⼀个⾼阶函数，它接收⼀个⼯具，返回⼀个带有内置审批流程的新⼯具。

    参数:

        tool: 可以是⼀个普通的 Python 函数，也可以是⼀个继承⾃ BaseTool 的 LangChain ⼯具实例。

        interrupt_config: ⼀个可选的字典，⽤于配置⼈类审批界⾯的选项（如是否允许编辑、批准等）。

    返回:

        ⼀个新的 BaseTool 实例，这个新⼯具封装了原始⼯具并加⼊了⼈⼯审核功能。

    """

    # 步骤 1: 规范化输⼊⼯具

    ifnot isinstance(tool, BaseTool):

        tool = create_tool(tool)



    # 步骤 2: 设置默认的⼈⼯交互配置

    if interrupt_config isNone:

        interrupt_config = {

            "allow_accept": True,

            "allow_edit": True,

            "allow_respond": True,

        }



    # 步骤 3: 创建并返回⼀个新的、封装后的⼯具

    @create_tool(

        tool.name,
        description=tool.description,

        args_schema=tool.args_schema

    )

    asyncdef call_tool_with_interrupt(config: RunnableConfig, **tool_input):# <--- 1. 改为

        """这是新⼯具的具体实现函数，它包含了⼈⼯审核的逻辑。"""



        # 步骤 3.1: 构建中断请求

        request: HumanInterrupt = {

            "action_request": {

                "action": tool.name,

                "args": tool_input

            },

            "config": interrupt_config,

            "description": "Please review the tool call"

        }



        # 步骤 3.2: 暂停图并等待⼈类输⼊

        response = interrupt([request])[0]



        # 步骤 3.3: 根据⼈类的响应采取⾏动

        if response["type"] == "accept":

            # 直接使⽤原始的参数异步调⽤原始⼯具。

## PDF物理页 26

              tool_response = await tool.ainvoke(tool_input, config) # <--- 2. 改为 await to

          elif response["type"] == "edit":

              # 从响应中获取新的参数，更新 `tool_input`。

              tool_input = response["args"]["args"]

              # 然后⽤新参数异步调⽤原始⼯具。

              tool_response = await tool.ainvoke(tool_input, config) # <--- 2. 改为 await to

          elif response["type"] == "response":

              # 将其提供的反馈内容 (`user_feedback`) 直接作为⼯具的输出返回。

              user_feedback = response["args"]

              tool_response = user_feedback

          else:

              raise ValueError(f"Unsupported interrupt response type: {response['type']}")



          # 返回最终结果

          return tool_response



      return call_tool_with_interrupt


步骤五：定义可⼈⼯⼲预的搜索                      agent

使⽤  步骤四创建的包装器              add_human_in_the_loop      和 步骤三定义的⼯具            search_tools  ，为
search_tools 中的每⼀个⼯具添加中断功能





  from langgraph.checkpoint.memory import InMemorySaver

  from langgraph.prebuilt import create_react_agent

  # 1. 初始化检查点

  # 同样，因为要使⽤中断功能，必须提供⼀个检查点来保存和恢复 Agent 的状态。

  checkpointer = InMemorySaver()





  # 为 search_tools 中的每⼀个⼯具添加中断功能

  wrapped_search_tools = [add_human_in_the_loop(tool) for tool in search_tools]



  # 2. 带⼈机交互的agent定义⽅法：

  agent = create_react_agent(

      # 指定 Agent 使⽤的 LLM 模型

      model=model,

      # 为 Agent 提供⼯具列表

      tools=wrapped_search_tools,

      # 将检查点与 Agent 关联起来

      checkpointer=checkpointer,

      name="search_assistant",

      prompt="你是⼀个能搜索各种信息的助⼿，⽀持通⽤⽹络搜索、酒店机票查询、学术检索、新闻咨询、图⽚搜索等

  )

步骤六：配置并运⾏              agent

## PDF物理页 27

输⼊  query：查明天北京的天⽓





  import asyncio



  # 将调⽤ agent 的代码封装在⼀个 async 函数中

  async def run_agent():

      config = {"configurable": {"thread_id": "2"}}



      # 使⽤ astream 进⾏异步迭代

      async for chunk in agent.astream(

          {"messages": [{"role": "user", "content": "查明天北京的天⽓"}]},

          config

      ):

          print(chunk)

          print("\n")


运⾏结果如下，触发中断：









步骤七：       Command根据⼈⼯输⼊                           恢复代理以继续





  import asyncio

  from langgraph.types import Command



  # 将调⽤ agent 的代码封装在⼀个 async 函数中

  asyncdef run_response():

      config = {"configurable": {"thread_id": "2"}}





      print("--- Resuming with 'accept' ---")

      asyncfor chunk in agent.astream(

          Command(resume=[{"type": "accept"}]),

          config

      ):

          print(chunk)

          print("\n")



  #run

  await run_response()

## PDF物理页 28

⼈⼯同意之后，运⾏结果，输出检索到的天⽓情况：












总结

LangGraph的“⼈⼯⼲预”为我们提供了⼀种⾮常强⼤且灵活的⽅式来将⼈类的智慧融⼊到AI的
⼯作流程中。  LangGraph通过interrupt机制，将“暂停-保存-恢复-重执⾏”的流程⽆缝集成到
Agent 的⼯作流中，它为开发者提供了前所未有的控制⼒，使得我们能够构建出既能发挥⼤模
型强⼤能⼒，⼜能在关键时刻接受⼈类智慧指导的复杂、可靠且安全的智能代理。通过运⽤持
久化执⾏状态、动态及静态中断、以及灵活的集成点，我们可以实现各种各样的应⽤场景，⽐
如审批与拒绝、编辑图状态、审查⼯具调⽤、验证⼈类输⼊等功能。这些模式可以帮助我们提
⾼LLM应⽤的可靠性、安全性和准确性                                   ，让AI真正成为我们的好帮⼿。

参考⽂献

Overview



























     腾讯技术⼯程
     腾讯技术官⽅号。腾讯技术创新、前沿领域发布解读平台。
     690篇原创内容


 公众号

## PDF物理页 29

阅读 6429





留⾔


写留⾔





                        还没有留⾔，来写⾸评
