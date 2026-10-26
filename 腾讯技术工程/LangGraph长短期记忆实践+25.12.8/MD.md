# 让AI智能体拥有像人类的持久记忆：基于LangGraph的长短期记忆管理实践指南

来源：[RAW.pdf](RAW.pdf)，capture-001。

这是PDF文本层按物理页码转写，不是AI总结。图片未嵌入；图内文字、截图、公式、表格及代码排版可能未提取或不可靠；源PDF中存在的右侧裁切不补写。实际复核范围详见META.json。

## PDF物理页 1

让AI智能体拥有像⼈类的持久记忆：基于              LangGraph的⻓短期记忆
管理实践指南


原创 腾讯程序员  腾讯技术⼯程   2025年12⽉8⽇   01:36⼴东620⼈
















作者： adacyang



  如何让AI智能体（Agent）像⼈类⼀样拥有持久的记忆，从⽽在复杂的连续任务中保持上
  下⽂感知和深度理解？这已成为构建⾼级智能体的核⼼挑战。本⽂将深⼊探讨              Agent
  Memory的核⼼概念，并聚焦于LangGraph框架下的长短期记忆实现，详解短期会话与长
  期知识的存储、管理、语义检索等技巧。更进⼀步地，我们将通过⼀个引⼊MCP协议的
  实战案例，⼿把⼿带你构建⼀个真实的融合长记忆机制的Multi-Agent     系统，直观展⽰中
  断、记忆与协作的融合。



基于⼤语⾔模型（LLM）的智能体（Agent）系统中，记忆机制是实现持续、连贯和个性化交
互的核⼼基⽯，通过记忆，可以让Agent记住过往的交互，保持上下⽂的⼀致性，并能从反馈
中学习，适应⽤户的偏好。

本⽂核⼼要点概述：

1.介绍Agent Memory的基本情况

2.LangGraph长短期记忆详解及案例说明：包含短期记忆实现、管理⽅法，长期记忆的实现⽅
法，以及搭建了融合postgres数据库、集成Embedding服务进⾏语义搜索等可⽤于⽣产环境的
真实案例。

3.引⼊MCP协议构建真实的Agent 长记忆应⽤：搭建⼀个基于     supervisor架构，集成中断机
制、长短期记忆机制的   multi-agent系统。



  记忆机制介绍

Agent Memory是什么？

## PDF物理页 2

上图中（来源于Mem0[1]），左边是没有Memory的agent，右边是有Memory的agent，后者可
以根据⽤户的过往信息（素⾷主义者、不喜欢乳制品）给出更合理的响应（不含乳制品的素⾷
菜单） ，⽽前者的回答显然是不合适的。

简单来说，Memory是赋予Agent记忆能⼒的技术和架构，能够让Agent像⼈⼀样记住过去的交
互、学到的知识、执⾏过的任务及未来的计划，是将⼀个LLM转变为能够执⾏复杂、长期任务
的真正 ”智能体  “的核⼼所在。

关于 Agent Memory我们需要考虑什么？

如何获取记忆：通过和⽤户交互、环境交互           ...

怎么组织记忆：模型参数、模型上下⽂、数据库

怎么利⽤记忆：    RAG、Few-shot...

有哪些  Memory类型？

关于 Memory的分类，有许多种分类体系，这⾥我们只讨论最常见及最易于                                                                                                                                       理解的。

正如⼈类利⽤长短期记忆进⾏有效的交互和学习⼀样，Agent的记忆机制通常划分为短期记忆
（short-term memory）和长期记忆 (long-term memory)，短期记忆决定了 Agent在微观任务上
的即时表现，⽽长期记忆则作为持久知识库，决定了Agent在宏观时间尺度上的智能深度和个
性化⽔平，通过两者配合，       Agent才能     表现出连贯性、上下⽂感知能⼒，才会显得更智能。

Agent Memory如何⼯作？

Agent通常通过以下⼏步来有效地管理                                                                      记忆，使得每次于⽤户的交互都更加精准智能：

1. 记忆存储：通过设计⼀系列策略来存储重要的交互信息，这些信息可能来源于对话内容、
  历史数据或任务要求等等。

2. 记忆更新：记忆会随着交互的发⽣，不断地进⾏更新，例如⽤户的偏好、最新的近况等
  等。记忆更新使得     Agent能够不断优化                           其响应。

## PDF物理页 3

3. 记忆检索： Agent根据当下的需求，去                                           记忆中检索需要的记忆内容，从⽽提供更加智能的
  回复。

Agent Memory怎么实现？

1. 物理外挂：即外置数据库和      RAG，需要检索当前   query相关的内容，例如：   Mem0、
  ACE。好处是即插即⽤，坏处是不够       end-to-end

2. Memory as Reasoning / Tool：通过训练Reasoning或Tool的⽅式动态更新context，例
  如：MemAgent、memory-R1。好处是更接近   end-to-end，但不是很灵活。

3. 参数更新： LLM本⾝就是⼀个   Memory体，所有参数都是它的     Memory，通     过更新参数来更
  新记忆，这种⽅式是最本质的，但也是最难实现的。



 LangGraph中的记忆管理

LangGraph[2]作为⼀款⾯向多智能体协作与状态管理的框架，其设计了巧妙的记忆管理系
统，旨在为Agent提供在不同交互中存储、检索和利⽤信息的能⼒。它区分了两种主要的记忆
类型：短期记忆和长期记忆。在实际使⽤中，通过这两种记忆协同，既能保障实时任务的⾼效
执⾏，⼜⽀持了跨任务、跨周期的经验复⽤。

● short-term memory（通过Checkpointer实现）：针对单个对话线程，核⼼价值在于保障对话
的临时性，使得   Agent能够跟踪会话中                的多轮对话，可以在该线程内的任何时刻被回忆。

● long-term memory（通过Store实现）：可以跨对话线程共享，可以在任何时间，任何线程
中被回忆，⽽不像短期记忆局限于单个对话。



























通过下表，可以更清晰的看到两者的区别：

## PDF物理页 4

LangGraph记忆的架构基础

要想更好的理解   LangGraph中的记忆                机制，⾸先需要理解其⽀持双轨记忆系统的核⼼概念。

Checkpointer

LangGraph有⼀个内置的持久化（Persistence）层，通过checkpointer实现，能够持久化存储
图状态，这使得开发记忆功能和⼈类⼲预功能成为可能。

当使⽤检查点编译⼀个图时，检查点会在每个             super-step保存图状态的checkpoint，这些
checkpoint被保存到⼀个thread中，可以在图执⾏后访问。因为threads允许在执⾏后访问图
的状态，所以可以实现记忆、⼈机协作、时间旅⾏、容错等多种强⼤的功能。

















⼯作流程：





 ⽤户输⼊ → [节点 1] → 💾 保存状态 → [节点 2] → 💾 保存状态 → 输出

 ↓  ↓

 Checkpoint 1   Checkpoint 2


Thread

为了管理多个独⽴的对话，LangGraph使⽤了thread的概念。thread_id是由checkpointer保存
的每个 checkpoint的唯⼀id，是激活和区分不同对话线程的唯⼀          key。在调⽤图的invoke  或
stream⽅法时，通过conﬁgurable字典传⼊⼀个thread_id，就代表这次操作属于thread_id这个
特定的对话。

Store

## PDF物理页 5

如上所述，图状态可以由checkpointer在每个super-step写⼊线程，从⽽实现状态的持久化。
但是，如果想在多个线程之间保留⼀些信息的话，那么就需要⽤到Store。Store本质上是⼀个
暴露给图节点和⼯具的键值数据库，与checkpointer的⾃动化快照不同，Store需要显式和主
动的进⾏操作。

























Namespace

Store中的数据通常通过更持久的标识来组织。            user_id是最常见的，⽤于关联⽤户的所有信
息，此外，namespace提供了⼀种数据隔离机制，例如，使⽤使⽤ (“memories”, user_id)           这
样的元组作为命名空间，可以将⽤户的记忆与其他类型的数据（如⽤户偏好                        (“preferences”,
user_id)）清晰地分离开来，避免数据                                冲突，保持知识库的整洁有序。

短期记忆详解

InMemorySaver内存会话临时存储

对于开发、原型设计和测试阶段，最简单快捷的⽅式是使⽤InMemorySaver。它将所有的对话
状态存储在内存中的⼀个       Python字典⾥。

1.设置记忆管理检查点





 from langchain_openai import ChatOpenAI

 from langchain.chat_models import init_chat_model

 from langgraph.checkpoint.memory import InMemorySaver

 from langgraph.prebuilt import create_react_agent



 # 初始化检查点保存器

 checkpointer = InMemorySaver()


2.定义⼤模型并创建    agent

## PDF物理页 6

  BASE_URL=""

  TOKEN=""

  MODEL_NAME=""



  model = init_chat_model(

      model=MODEL_NAME,

      model_provider="openai",

      base_url=BASE_URL,

      api_key=TOKEN,

      temperature=0,
  )



  agent = create_react_agent(

      model=model,

      tools=[],

      # 传⼊检查点，是将持久化能⼒“注⼊”图的关键步骤。编译后的graph对象现在具备了状态管理的能⼒。

      checkpointer=checkpointer

  )


如  果  是 底层  ⾃ 定义              api 在  图  构  建  阶  段 传⼊  检  查 点的代码  是                        graph      =
builder.compile(checkpointer=checkpointer)。

3.短期记忆     -内存后端





  config = {"configurable": {"thread_id": "1"}}  # 激活记忆机制的核⼼。如果没有提供thread_id，每次



  response = agent.invoke(

      {"messages": [{"role": "user", "content": "你好，我叫ada！"}]},

      config

  )



  print(f"thread1_bot_answer：{response['messages'][-1].content}")



  response = agent.invoke(

      {"messages": [{"role": "user", "content": "你好，请问你还记得我叫什么名字么？"}]},

      config

  )



  print('------------线程1------------------')

  print(f"thread1_bot_answer：{response['messages'][-1].content}")



  new_config = {"configurable": {"thread_id": "2"}}

  response = agent.invoke(

      {"messages": [{"role": "user", "content": "你好，请问你还记得我叫什么名字么？"}]},

      new_config

  )

## PDF物理页 7

 print('------------线程2------------------')

 print(f"thread2_bot_answer：{response['messages'][-1].content}")


执⾏上⾯代码，可以看到输出如下：





 thread1_bot_answer：你好，Ada！很⾼兴认识你！😊



 这是⼀个很美的名字呢！有什么我可以帮助你的吗？⽆论是想聊聊天，还是有任何问题需要解答，我都很乐意为你提供帮

 ------------线程1------------------

 thread1_bot_answer：当然记得！你刚才告诉我你叫 Ada～很⾼兴再次和你打招呼！😊
 ------------线程2------------------

 thread2_bot_answer：你好！很抱歉，我⽆法记住之前对话中的个⼈信息，⽐如你的名字。这是为了保护你的隐私，


短期记忆与线程相关，在对话时，需要在配置中传⼊thread_id。通过上⾯的结果我们可以看
到，当我们传⼊相同的thread_id时，agent就可以记住⽤户的名字，然⽽当我们更换thread_id
时，agent就不记得⽤户的名字了。

需要注意的是，InMemorySaver将所有状态都保存在内存中，⼀旦程序终⽌，那么所有对话
历史都会消失。

数据库持久化存储

可以发现，上⾯⼀⼩节的代码在应⽤程序结束后再启动，记忆就⼜消失了。这是因为
InMemorySaver仅仅是把记忆保存在内存中，应⽤程序结束后释放内存记忆就消失了。在⽣产
环境中常常使⽤数据库⽀持的检查点记录器持久化保存记忆，以保证数据的可靠性和服务的连
续性。

这⾥我们以   postgres数据库为例来说明，怎么持久化地保存记忆数据。

1.⾸先安装以下依赖：





 pip install -U "psycopg[binary,pool]" langgraph-checkpoint-postgres


2.安装 postgres数据库，具体的安装⽅法可以参考：Linux             下安装   PostgreSQL_linux安装
postgresql-CSDN博客。这⾥选择以源码的⽅式进⾏安装，安装包从官⽹（PostgreSQL:
Downloads）下载，选择最新的     postgresql-18.0.tar.gz。

3.安装数据库成功后，编码如下代码。

DB_URI是  数  据  库  连  接 的URL 。  想  要  ⾃ 动保 存在  数  据  库  中 的State 需  要  在
PostgresSaver.from_conn_string(DB_URI)上下⽂中操作。





 from langchain.chat_models import init_chat_model

 from langgraph.graph import StateGraph, MessagesState, START

## PDF物理页 8

from langgraph.checkpoint.postgres import PostgresSaver



BASE_URL=""

TOKEN=""

MODEL_NAME=""



model = init_chat_model(

    model=MODEL_NAME,

    model_provider="openai",

    base_url=BASE_URL,

    api_key=TOKEN,

    temperature=0,

)



DB_URI = "postgresql://postgres:postgres@localhost:5432/postgres?sslmode=disable"



with PostgresSaver.from_conn_string(DB_URI) as checkpointer:

    checkpointer.setup()  # 第⼀次调⽤时必须要setup()



    def call_model(state: MessagesState):

   response = model.invoke(state["messages"])

   return {"messages": response}



    builder = StateGraph(MessagesState)

    builder.add_node(call_model)

    builder.add_edge(START, "call_model")



    graph = builder.compile(checkpointer=checkpointer)



    config = {

   "configurable": {

"thread_id": "1"

   }

    }



    response = graph.invoke(

   {"messages": [{"role": "user", "content": "你好，我叫ada！"}]},

   config

    )



    print(response['messages'][-1].content)



    response = graph.invoke(

   {"messages": [{"role": "user", "content": "你好，请问你还记得我叫什么名字么？"}]},

   config

    )



    print(response['messages'][-1].content)

## PDF物理页 9

运⾏⼀次上述代码后，关闭应⽤程序后重启，再次运⾏上述代码，            print结果如下：





 bot_answer_1：你好，Ada！很⾼兴再次⻅到你！😊



 你的名字真动听！今天有什么我可以帮你解答或者想聊的话题吗？

 bot_answer_2：当然记得！你告诉我你叫 **Ada**。很⾼兴再次和你打招呼！😊


可以看到，记忆已经被保存了。我们检查数据库可以发现，          postgres数据库中出现了四个表：













上述表中，checkpoints表是”状态快照“表，每当程序执⾏⼀个step时，它就会在这张表中创
建⼀条新记录，这条记录就是⼀个检查点的快照。查询该表，可以得到如下结果：

































接下来，我们来分析每⼀列的含义：

## PDF物理页 10

理解了上⾯checkpoints表后，那么不禁会问，真正的消息内容被存到了哪⾥呢？真正的消息
内容存储在 checkpoint_writes表中，如下：



























除了PostgreSQL之外，LangGraph还⽀持MongoDB、Redis等数据库。

⼦图中的记忆

当构建复杂的、由多个⼦图嵌套⽽成的应⽤时，需要更灵活的记忆管理策略。

● 记忆继承（默认）：默认情况下，⼦图会继承其⽗图的checkpointer。这意味着整个嵌套图
共享同⼀个对话状态，数据可以在⽗⼦图之间⽆缝流动。这对于将⼀个⼤型任务分解为多个模
块化⼦任务⾮常有⽤。

● 记忆隔离：在某些场景下，例如构建多智能体系统，希望每个智能体（由⼀个⼦图表⽰）拥
有⾃⼰独⽴的内存空间，互不⼲扰。此时，可以在编译⼦图时设置         checkpointer=True。

如下代码，可以在⼦图中直接使⽤⽗图的短期记忆：

## PDF物理页 11

  from langgraph.graph import START, StateGraph

  from langgraph.checkpoint.memory import InMemorySaver

  from typing import TypedDict



  class State(TypedDict):
      foo: str



  # ⼦图

  def subgraph_node_1(state: State):

      return {"foo": state["foo"] + "bar"}



  subgraph_builder = StateGraph(State)
  subgraph_builder.add_node(subgraph_node_1)

  subgraph_builder.add_edge(START, "subgraph_node_1")

  subgraph = subgraph_builder.compile()



  # ⽗图

  builder = StateGraph(State)

  builder.add_node("node_1", subgraph)

  builder.add_edge(START, "node_1")



  checkpointer = InMemorySaver()

  graph = builder.compile(checkpointer=checkpointer)


如果⼦图希望使⽤⾃⼰的短期记忆，那么需要在编译⼦图时，显⽰传⼊⼦图的检查点：





  subgraph_builder = StateGraph(...)

  subgraph = subgraph_builder.compile(checkpointer=True)


⼯具中的记忆交互

在⼯具中读取状态：

LangGraph允许⼯具直接访问和读取                           当前的图状态，使其具备上下⽂感知能⼒。

核⼼机制：state: Annotated[CustomState, InjectedState]          ，InjectedState   的作⽤是在调⽤这
个⼯具时，将当前的完整状态对象作为第⼀个参数传递到⼯具中，使得这个⼯具能根据当前状
态来执⾏更智能的操作。





  from typing import Annotated

  from langchain.chat_models import init_chat_model

  from langgraph.prebuilt import InjectedState, create_react_agent

  from langgraph.prebuilt.chat_agent_executor import AgentState



  BASE_URL=""

## PDF物理页 12

  TOKEN=""

  MODEL_NAME=""



  model = init_chat_model(

      model=MODEL_NAME,

      model_provider="openai",

      base_url=BASE_URL,

      api_key=TOKEN,

      temperature=0,

  )


  class CustomState(AgentState):

      user_id: str



  def get_user_info(

      state: Annotated[CustomState, InjectedState]

  ) -> str:

      """查询⽤户信息"""

      user_id = state["user_id"]

      return"ada"if state["user_id"] == "user_ada"else"Unknown"



  agent = create_react_agent(
      model=model,

      tools=[get_user_info],

      state_schema=CustomState,

  )



  agent.invoke({

      "messages": "查询⽤户信息",

      "user_id": "user_ada"

  })


返回结果如下：





  根据查询结果，您的⽤户信息显示⽤户名为：**ada**\n\n这是您的⽤户信息查询结果。如果您需要了解其他信息或有


在⼯具中写⼊状态：

如果要在⼯具执⾏期间修改图的记忆，那么可以直接从⼯具返回状态更新。这对于持久化中间
结果、传递信息给后续⼯具等⾮常有⽤。

核⼼机制：⼯具返回Command对象。此时，LangGraph会将其返回值解释为对状态的直接修
改指令。Command(update={...})中的字典定义了要更新的状态字段及其新值。这允许⼯具在
完成其主要任务的同时，将结果写回智能体的短期记忆中，从⽽影响后续的决策。

## PDF物理页 13

from typing import Annotated

from langchain_core.tools import InjectedToolCallId

from langchain_core.runnables import RunnableConfig

from langchain_core.messages import ToolMessage

from langgraph.prebuilt import InjectedState, create_react_agent
from langgraph.prebuilt.chat_agent_executor import AgentState

from langgraph.types import Command



class CustomState(AgentState):

    user_name: str



def update_user_info(

    tool_call_id: Annotated[str, InjectedToolCallId],

    config: RunnableConfig
) -> Command:

    """查询并更新⽤户信息"""

    user_id = config["configurable"].get("user_id")

    name = "ada"if user_id == "user_123"else"Unknown user"

    return Command(update={

   "user_name": name,

   # 更新消息历史记录

   "messages": [

ToolMessage(

    "成功查询到⽤户信息",

    tool_call_id=tool_call_id
)

   ]

    })



def greet(

    state: Annotated[CustomState, InjectedState]

) -> str:

    """找到⽤户信息后，使⽤此⽅式向⽤户问好。"""

    user_name = state["user_name"]

    return f"你好 {user_name}！"



agent = create_react_agent(
    model=model,

    tools=[update_user_info, greet],

    state_schema=CustomState

)



agent.invoke(

    {"messages": [{"role": "user", "content": "向⽤户打招呼"}]},

    config={"configurable": {"user_id": "user_123"}}

)

## PDF物理页 14

输出结果如下：

















      腾讯技术⼯程
      腾讯技术官⽅号。 腾讯技术创新、 前沿领域发 布解读平台。
      690篇原创内 容


 公众号

长期记忆详解

LangGraph中的长期记忆允许系统在不同对话中保留信息，是跨对话线程共享的，可以在任何
时间、任何线程中被回忆。与短期记忆不同，长期记忆保存在⾃定义的命名空间中，每个记忆
都组织在⼀个⾃定义的   namespace和⼀个唯⼀的 key下。

记忆存储：LangGraph将长期记忆存储为JSON⽂档，使⽤Store进⾏管理，允许存储结构化和
⾮结构化的数据。

记忆更新时机  ：

● 热路径（Hot Path）：在应⽤程序逻辑运⾏时实时创建记忆（store.put()  ），优点是实时更
新，但可能增加程序复杂性、延迟等问题。

● 后台（Background）：作为单独的异步任务创建记忆（store.put()），优点是避免主应⽤延
迟、逻辑分离，难点在于确定更新频率和触发时机。

记忆检索 ：

● store.get()：根据命名空间和键精确                                                      获取记忆。

● store.search()：在指定命名空间内实现灵活记忆检索，不但可以通过命名空间和标识符，更
可以通过语义检索到记忆内容。通常需要      Store配置⼀个embed来⽀持语义搜索。

记忆的应⽤ ：

● 语义记忆：存储事实和概念。分为以下两种情况：Proﬁle：将关于⽤户、组织或代理⾃⾝的
特定信息存储为⼀个持续更新的JSON⽂档，需要模型来⽣成新的Proﬁle或更新已有JSON          档
案；Collection：将记忆存储为⼀组独⽴的⽂档，易于⽣成，但检索和更新较为复杂，且可能

## PDF物理页 15

难以捕获记忆间的完整上下⽂。在应⽤时，可以将检索到的记忆作为上下⽂或系统指令的⼀部
分传递给    LLM，⽤于个性化响应和回答                                                事实性问题。

● 情景记忆：存储过去的事件或⾏为经验。通常通过few-shot example prompt来实现，以指
导模型完成任务。

● 程序记忆：存储执⾏任务的规则或指令。通常通过修改代码⾃⾝的prompt来实现，将其应
⽤于  LLM。

InMemoryStore

与 Checkpointer类似，InMemoryStore⽤于快速开发和原型验证。它将所有数据存储在内存
中。





  from langchain.chat_models import init_chat_model

  from langchain_core.runnables import RunnableConfig

  from langgraph.store.memory import InMemoryStore

  from langgraph.config import get_store

  from langgraph.prebuilt import create_react_agent



  store = InMemoryStore()



  BASE_URL=""

  TOKEN=""

  MODEL_NAME=""



  model = init_chat_model(

      model=MODEL_NAME,

      model_provider="openai",

      base_url=BASE_URL,

      api_key=TOKEN,

      temperature=0,

  )



  store.put(

      ("users",),  # 命名空间：元组类型，类⽐⽂件系统中的⽂件夹，⽀持分层组织结构

      "user_123",  # 键: 字符串，是命名空间内的唯⼀标识符，⼀般推荐使⽤uuid库⽣成唯⼀标识符

      {

     "name": "ada",

     "language": "中⽂",

      }  # 值：Python字典类型，⽐如保存公共⻆⾊资料时可以是包含姓名、偏好等键值对的字典

  )



  def get_user_info(config: RunnableConfig) -> str:

      """查找⽤户信息的函数，可以查看⻓期记忆中储存的⽤户信息"""

      store = get_store()  # 获取上下⽂中可⽤的store实例

      user_id = config["configurable"].get("user_id")

## PDF物理页 16

      user_info = store.get(("users",), user_id)  # 输⼊命名空间和键进⾏精确查询

      return str(user_info.value) if user_info else"Unknown user"



  agent = create_react_agent(

      model=model,

      tools=[get_user_info],

      # 传⼊store

      store=store

  )



  response = agent.invoke(

      {"messages": [{"role": "user", "content": "帮我查找⻓期记忆中储存的⽤户信息"}]},

      config={"configurable": {"user_id": "user_123"}}

  )



  print(response['messages'])


输出结果如下，可以看到在⼯具函数中成功调⽤                          store查找到了保存的⽤户信息：











数据库持久化存储

为了让记忆真正         ”长期   “，⽣产环境必须使⽤数据库⽀持的Store                     ，LangGraph    ⽬前主要⽀持
PostgresStore和RedisStore。我们以        PostgresStore为例来进⾏说明。

 1. ⾸先，先安装对应的包：





  pip install -U "psycopg[binary,pool]" langgraph-checkpoint-postgres


 2. Postgres数据库的安装，请参考上⽂。


 3. 接下来进⾏⽰例说明。整体过程与Checkpointer类似，关键区别在于Store是怎样在节点内
   部被访问和使⽤的。





  import uuid

  from langchain.chat_models import init_chat_model

  from langchain_core.runnables import RunnableConfig

  from langgraph.graph import StateGraph, MessagesState, START

  from langgraph.store.base import BaseStore
  from langgraph.store.postgres import PostgresStore

  from langgraph.checkpoint.postgres import PostgresSaver

## PDF物理页 17

BASE_URL=""

TOKEN=""

MODEL_NAME=""



model = init_chat_model(

    model=MODEL_NAME,

    model_provider="openai",

    base_url=BASE_URL,

    api_key=TOKEN,

    temperature=0,

)



DB_URI = "postgresql://postgres:postgres@localhost:5432/postgres?sslmode=disable"



with (

    PostgresStore.from_conn_string(DB_URI) as store,

    PostgresSaver.from_conn_string(DB_URI) as checkpointer,
):

    store.setup()  # 第⼀次调⽤时必须要setup()

#checkpointer.setup()



    # 声明store参数

    def call_model(

   state: MessagesState,

   config: RunnableConfig,

   *,

   store: BaseStore,  # 在节点中访问store的标准⽅式，需要在函数签名上，加⼀个store

    ):

   # 从store中读取记忆

   user_id = config["configurable"]["user_id"]

   namespace = ("memories", user_id)

   memories = store.search(namespace, query=str(state["messages"][-1].content))

   info = "\n".join([d.value["data"] for d in memories])

   system_msg = f"你是⼀个与⼈类交流的⼩助⼿，⽤户信息: {info}"



   # 向store中写⼊记忆

   last_message = state["messages"][-1]

   if"记住"in last_message.content.lower():

memory = "⽤户名字是ada"

store.put(namespace, str(uuid.uuid4()), {"data": memory})



   response = model.invoke([{"role": "system", "content": system_msg}] + state["messages"

   return {"messages": response}


    builder = StateGraph(MessagesState)

    builder.add_node(call_model)

    builder.add_edge(START, "call_model")

## PDF物理页 18

      graph = builder.compile(checkpointer=checkpointer, store=store)  # agent同时配备了短期记



      # 第⼀次对话，告诉agent⽤户的名字

      config = {

     "configurable": {

  "thread_id": "3",

  "user_id": "1",

     }
      }



      response = graph.invoke(

     {"messages": [{"role": "user", "content": "你好，我叫ada！记住这个名字呦~"}]},

     config

      )



      print(response['messages'][-1].content)



      # 第⼆次对话，新线程，询问agent记不记得⽤户的名字

      config = {

     "configurable": {

  "thread_id": "4",

  "user_id": "1",

     }

      }



      response = graph.invoke(

     {"messages": [{"role": "user", "content": "我的名字是什么?"}]},

     config

      )

      print(response['messages'][-1].content)


输出结果如下：





  # ------------------第⼀次对话----------------------

  你好ada！很⾼兴认识你～我已经记住你的名字啦！✨


  有什么我可以帮你的吗？

  # ------------------第⼆次对话----------------------

  你的名字是ada


在第⼀次对话时，对话线程id为3，agent被要求记住⽤户的名字，并且根据代码逻辑，⽤户名
字信息是通过store.put()写⼊数据库的。第⼆次对话时，线程id为4，当被问起⽤户的名字时，
agent通过store.search()办法从数据库中检索到了这个信息，并成功回答，这展⽰了Store的跨
记忆存储能⼒。

## PDF物理页 19

长期知识赋能⼯具

在⼯具中读取长期记忆：

参考上⽂中，长期记忆              -InMemoryStore中的⽰例。

其中，核⼼在于store = get_store() ，这个函数是⼀个上下⽂感知的辅助函数，能够在⼯具执
⾏时，⾃动获取并返回              compile或create_react_agent中传⼊的           store实例。

在⼯具中写⼊长期记忆：





  from typing_extensions import TypedDict


  from langchain.chat_models import init_chat_model

  from langgraph.config import get_store

  from langchain_core.runnables import RunnableConfig

  from langgraph.prebuilt import create_react_agent

  from langgraph.store.memory import InMemoryStore



  store = InMemoryStore()



  BASE_URL=""

  TOKEN=""

  MODEL_NAME=""



  model = init_chat_model(

      model=MODEL_NAME,

      model_provider="openai",

      base_url=BASE_URL,

      api_key=TOKEN,

      temperature=0,

  )



  class UserInfo(TypedDict):

      name: str



  def save_user_info(user_info: UserInfo, config: RunnableConfig) -> str:

      """将⽤户信息保存到store"""

      store = get_store()

      user_id = config["configurable"].get("user_id")

      store.put(("users",), user_id, user_info)

      return"成功保存了⽤户信息"



  agent = create_react_agent(

      model=model,

      tools=[save_user_info],

      store=store

  )

## PDF物理页 20

 agent.invoke(

     {"messages": [{"role": "user", "content": "我叫ada！请你记住我的名字"}]},

     config={"configurable": {"user_id": "user_123"}}

 )


⾸先需要定义要存储的数据内容，即UserInfo，它为LLM提供了⼀个清晰的结构化输出格式，
当LLM决定调⽤    save_user_info的⼯具时，会⾃动⽣成⼀个包含         name字段的字典。然后调⽤
store.put()⽅法，将数据存储下来。





















 store.get(("users",), "user_123").value



 # 输出：{'name': 'ada'}


语义搜索

Store最强⼤的功能之⼀是⽀持语义搜索，这能将Store从⼀个简单的键值数据库，转变为⼀个
功能完备的向量数据库。智能体不再只能通过精确的关键词来检索记忆，⽽是能够根据概念的
相似性来查找相关信息。        这实际就是⼀套     RAG流程   。

下⾯我们将基于⾃定义部署的Embedding服务，来演⽰如何进⾏长期记忆语义搜索。特别说
明的是，代码仅供演⽰使⽤，实际使⽤可以参考下⾯代码，编写更规范的代码。

1.⾸先我们需要⾃⼰     部署⼀个   Embedding服务  ，这⾥我们以     Qwen3-Embedding-4B为例。

2.创建⾃定义Embedding类，这个类需要继承⾃langchain.embeddings.base.Embeddings，
这个类的作⽤是负责与       Embedding服务进⾏通信。





 import requests
 from typing import List, Optional, Dict

 from langchain.embeddings.base import Embeddings



 class SelfAPIEmbeddings(Embeddings):

     """

     ⼀个⾃定义的 Embedding 类，⽤于调⽤⾃部署的 embedding API 服务。

     """

     def __init__(self):

    """

## PDF物理页 21

   初始化函数。

   """

   self.token = ""

   self.url = ""

   self.model_id = ""



    def _call_api(self, texts: List[str]) -> List[List[float]]:

   """

   内部⽅法，⽤于调⽤ API。

   *** 您需要根据您⾃⼰服务的实际 API 格式来修改这部分 ***

   """

   try:

payload = {

    'model': self.model_id,

    'input': texts

}


headers = {

    'Content-Type': 'application/json',

    'Authorization': f'Bearer {self.token}'

}



response = requests.post(self.url, headers=headers, data=json.dumps(payload))



# 判断是否异常

if response.status_code != 200:

    print(response.json())

    exit()



res = response.json()

return res['data']

   except requests.exceptions.RequestException as e:

print(f"Error calling embedding API: {e}")

# 可以选择返回空列表或重新抛出异常

raise e



    def embed_documents(self, texts: List[str]) -> List[List[float]]:

   """

   为⽂档列表⽣成 embeddings。

   """

   if not texts:

return []

   # 为了避免请求体过⼤，可以分批处理

   # 这⾥为了简单起⻅，⼀次性发送所有⽂本

   new_texts = []

   for i in texts:

i = eval(i)

## PDF物理页 22

  new_texts.append(i['text'])



     res = self._call_api(new_texts)
     new_res = []

     for i in res:

  new_res.append(i['embedding'])

     return new_res



      def embed_query(self, text: str) -> List[float]:

     """

     为单个查询⽂本⽣成 embedding。

     """

     if not text:

  return []

     result = self._call_api([text])

     return result[0]['embedding']


3.将⾃定义的       Embedding类集成到⼯作                           流中，通过在Store中配置index来启⽤语义                搜索。





  from langchain.embeddings import init_embeddings

  from langgraph.store.memory import InMemoryStore



  custom_embeddings = SelfAPIEmbeddings()

  store = InMemoryStore(

      index={

     "embed": custom_embeddings,

     "dims": 2560,

      }

  )


4.语义查询测试        。





  store.put(("user_123", "memories"), "1", {"text": "我喜欢吃披萨"})

  store.put(("user_123", "memories"), "2", {"text": "我是⼀名程序员"})


  items = store.search(

      ("user_123", "memories"), query="我肚⼦饿了", limit=1

  )


输出如下，尽管查询没有”披萨“这个词，但是通过Embedding模型计算，知道披萨和饿了是相
近的语义，因此成功检索出了相关的记忆。

## PDF物理页 23

 [Item(namespace=['user_123', 'memories'], key='1', value={'text': '我喜欢吃披萨'}, created_



      腾讯技术⼯程
      腾讯技术官⽅号。 腾讯技术创新、 前沿领域发 布解读平台。
      690篇原创内 容


 公众号


短期记忆管理策略

随着对话的进⾏，短期记忆（对话历史）会不断增长，可能会超出LLM的上下⽂窗⼝，导致请
求调⽤失败，或者使LLM反应变慢、变差。这时，就需要对记忆进⾏管理了。常见的解决办法
有：

● 修剪消息（trim messages）：移除前 N  条或后 N  条消息（在调⽤     LLM 之前）。最简单直
接，但信息丢失严重，适合短期任务、⽆状态问答机器⼈、近期上下⽂最重要的应⽤。

● 删除消息（delete messages）：从LangGraph状态中永久删除消息。可以精确的控制移除内
容，但需要⾃定义逻辑来判断哪些消息需要删除，适合⽤于移除不再需要的冗余系统消息、⼯
具输出或错误信息。

● 总结消息（summarize messages）：汇总历史记录中的早期消息并将其替换为摘要。保留
了核⼼语义信息，但计算成本⾼，实现相对复杂，适合⽤于长期连续对话、需要维持深度长期
上下⽂的智能体。

● ⾃定义策略：例如消息过滤等。

修剪消息

管理对话历史的⼀个重要概念是限制传递给模型的消息数量，trim_messages就是LangChain
提供的⼀个实⽤函数，它根据指定的策略、token限制、模型要求以及是否包含系统消息等来
裁剪消息列表，它的主要⽬的是确保对话历史不会超出模型的上下⽂窗⼝⼤⼩。

它的解决策略是：当消息历史过长时，从开头或结尾丢弃⼀部分消息，以确保总长度符合限
制。





 from langchain_core.messages.utils import (

     trim_messages,

     count_tokens_approximately
 )

 from langchain.chat_models import init_chat_model

 from langgraph.checkpoint.memory import InMemorySaver

 from langgraph.graph import StateGraph, START, MessagesState



 BASE_URL=""

 TOKEN=""

## PDF物理页 24

MODEL_NAME=""



model = init_chat_model(
    model=MODEL_NAME,

    model_provider="openai",

    base_url=BASE_URL,

    api_key=TOKEN,
    temperature=0,

)



summarization_model = model.bind(max_tokens=128)



def call_model(state: MessagesState):

    # 保留最近消息，总 token ≤ 128

    messages = trim_messages(

   state["messages"],

   strategy="last",  # 保留最后的消息

   token_counter=count_tokens_approximately,
   max_tokens=128,

   start_on="human",  # 确保第⼀条消息（不包括系统消息）是从human消息开始保留

   end_on=("human", "tool"),  # 保留到human或tool消息为⽌

   allow_partial=False,  # 不允许分割消息内容

   include_system=True  # 保留system prompt

    )

    # --- 在这⾥打印传⼊模型的内容 ---

    print("-" * 20)

    print(f"Messages being sent to the model (trimmed to <= 128 tokens): {len(messages)}"

    for msg in messages:

   print(f"  [{msg.type.upper()}]: {msg.content}")

    print("-" * 20)

    response = model.invoke(messages)

    return {"messages": [response]}



checkpointer = InMemorySaver()

builder = StateGraph(MessagesState)

builder.add_node(call_model)

builder.add_edge(START, "call_model")

graph = builder.compile(checkpointer=checkpointer)



# 如果需要在agent中修剪，那么需要将pre_model_hook和trim_messages结合使⽤

"""

def call_model(state)

    messages = trim_messages(...)



agent = create_react_agent(

 model,

 tools,

 pre_model_hook=call_model,

## PDF物理页 25

   checkpointer=checkpointer,

  )

  """


发起请求如下：





  config = {"configurable": {"thread_id": "1"}}



  graph.invoke({"messages": "你好，我叫ada"}, config)

  graph.invoke({"messages": "请写⼀⾸诗，关于⼩狗的"}, config)

  graph.invoke({"messages": "再写⼀⾸关于⼩猫的"}, config)

  final_response = graph.invoke({"messages": "我叫什么名字呢？"}, config)


输出打印如下：





  --------------------

  Messages being sent to the model (trimmed to <= 128 tokens): 1

    [HUMAN]: 你好，我叫ada
  --------------------



  --------------------

  Messages being sent to the model (trimmed to <= 128 tokens): 3

    [HUMAN]: 你好，我叫ada

    [AI]: 你好，Ada！很⾼兴认识你！😊



  这是⼀个很美的名字呢！有什么我可以帮助你的吗？⽆论是想聊天、有问题需要解答，还是需要任何形式的帮助，我都很

    [HUMAN]: 请写⼀⾸诗，关于⼩狗的
  --------------------



  --------------------

  Messages being sent to the model (trimmed to <= 128 tokens): 5

    [HUMAN]: 你好，我叫ada

    [AI]: 你好，Ada！很⾼兴认识你！😊



  这是⼀个很美的名字呢！有什么我可以帮助你的吗？⽆论是想聊天、有问题需要解答，还是需要任何形式的帮助，我都很

    [HUMAN]: 请写⼀⾸诗，关于⼩狗的

    [AI]: 好的，Ada！为你写⼀⾸关于⼩狗的可爱⼩诗，希望你喜欢：


  **《⼩狗的约定》**

  .....  （此处省略诗的内容）

  这⾸诗捕捉了⼩狗的活泼、忠诚和它们带给我们的温暖。你觉得怎么样？😊

    [HUMAN]: 再写⼀⾸关于⼩猫的

  --------------------



  --------------------

  Messages being sent to the model (trimmed to <= 128 tokens): 3

## PDF物理页 26

   [HUMAN]: 再写⼀⾸关于⼩猫的

   [AI]: 好的，Ada！这⾸关于⼩猫的诗，希望同样能带给你⼀丝轻盈与温柔：



 **《⼩猫的遐想》**

 .....  （此处省略诗的内容）

 希望你喜欢这⾸⼩诗！🐾

   [HUMAN]: 我叫什么名字呢？

 --------------------


模型最终的输出为：















可以看出，传递给模型的消息内容已经被裁剪，修剪的过程为：

1.保留系统消息，     include_system=True

2.strategy="last"，反转消息列表，以                                           便从最新的消息开始处理

3.累积 token数量，当达到max_tokens限制，那么进⾏修剪

4.修剪时，由于allow_partial=False，因此，保留的消息都是完整的；且start_on="human"，
所以修剪后第⼀条⾮       system prompt是⽤户消息

虽然对传递给模型的历史消息进⾏了裁剪，但是查询state可以发现，历史记录仍被完整的保
留在内存中，没有被删除。





 print("\n" + "="*30)

 print("  查看 thread_id='1' 的完整对话历史")

 print("="*30)



 current_state = graph.get_state(config)

 conversation_history = current_state.values["messages"]



 for message in conversation_history:

     print(f"[{message.type.upper()}]: {message.content}")


删除消息

这种⽅法允许从状态中永久移除特定的消息。要删除消息，不能直接从状态的messages列表
中移除，⽽是使⽤RemoveMessage         函数，从graph state中直接删除消息来管理对话历史。

## PDF物理页 27

为了让      RemoveMessage        ⽣效，需要使⽤带有                   add_messages  reducer        的状态键，例如
MessagesState。

删除特定消息：





  from langchain_core.messages import RemoveMessage

  from langchain.chat_models import init_chat_model

  from langgraph.checkpoint.memory import InMemorySaver

  from langgraph.graph import StateGraph, START, MessagesState



  BASE_URL=""

  TOKEN=""

  MODEL_NAME=""



  model = init_chat_model(

      model=MODEL_NAME,

      model_provider="openai",

      base_url=BASE_URL,
      api_key=TOKEN,

      temperature=0,

  )



  def delete_messages(state):

      messages = state["messages"]

      if len(messages) > 2:

     # 删除最早的两条消息

     return {"messages": [RemoveMessage(id=m.id) for m in messages[:2]]}



  def call_model(state: MessagesState):

      response = model.invoke(state["messages"])

      return {"messages": response}



  builder = StateGraph(MessagesState)

  builder.add_sequence([call_model, delete_messages])

  builder.add_edge(START, "call_model")



  checkpointer = InMemorySaver()

  app = builder.compile(checkpointer=checkpointer)

  config = {"configurable": {"thread_id": "1"}}



  for event in app.stream(

      {"messages": [{"role": "user", "content": "你好，我是ada"}]},

      config,

      stream_mode="values"

  ):

      print([(message.type, message.content) for message in event["messages"]])

## PDF物理页 28

  for event in app.stream(

      {"messages": [{"role": "user", "content": "我叫什么名字"}]},

      config,

      stream_mode="values"

  ):

      print([(message.type, message.content) for message in event["messages"]])


输出如下，当请求完成时，如果消息数量                            >2，那么最早的两条消息会被删除。














清空所有消息：





  from langgraph.graph.message import REMOVE_ALL_MESSAGES


  def clear_messages(state):

      return {"messages": [RemoveMessage(id=REMOVE_ALL_MESSAGES)]}



  builder = StateGraph(MessagesState)

  builder.add_sequence([call_model, clear_messages])

  builder.add_edge(START, "call_model")



  checkpointer = InMemorySaver()

  app = builder.compile(checkpointer=checkpointer)

  config = {"configurable": {"thread_id": "1"}}



  for event in app.stream(

      {"messages": [{"role": "user", "content": "你好，我是ada"}]},

      config,

      stream_mode="values"

  ):

      print([(message.type, message.content) for message in event["messages"]])



  for event in app.stream(

      {"messages": [{"role": "user", "content": "我叫什么名字"}]},

      config,

      stream_mode="values"

  ):

      print([(message.type, message.content) for message in event["messages"]])

## PDF物理页 29

输出如下，请求完成后，会⽴即删除所有消息记录。











总结消息

通过修剪、删除来管理历史消息，会有丢失信息的问题。为了避免这个问题，可以进⾏消息总
结，也就是通过调⽤LLM对历史对话进⾏摘要，并将摘要作为新的上下⽂传⼊，以在减少消息
数量的同时保留关键信息。



















1.⾸先，安装LangMem，这是⼀个由LangChain维护的库，提供了⽤于在agent中管理记忆的
⼯具。





  pip install -U langmem


2.langmem库提供了⼀个预构建的           SummarizationNode，可以极⼤地简化实现过程：





  import tiktoken

  from typing import Any, TypedDict



  from langchain.chat_models import init_chat_model

  from langchain_core.messages import AnyMessage, BaseMessage, SystemMessage

  from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

  from langgraph.graph import StateGraph, START, MessagesState

  from langgraph.checkpoint.memory import InMemorySaver

  from langmem.short_term import SummarizationNode, RunningSummary


  summary_prompt = ChatPromptTemplate.from_messages(

      [

     MessagesPlaceholder(variable_name="messages"),

## PDF物理页 30

   # 使⽤ HumanMessage 模拟⽤户在最后发出总结指令

   ("human", "请根据以上对话，⽣成⼀段简洁、连贯的中⽂摘要，注意不要丢失细节"),

    ]

)



update_summary_prompt = ChatPromptTemplate.from_messages(

    [

   MessagesPlaceholder(variable_name="messages"),

   # 使⽤ HumanMessage 模拟⽤户在最后发出总结指令

   ("human", "以下是⽬前为⽌的对话摘要：{existing_summary}\n\n请根据以上新消息扩展此摘要："),

    ]

)



BASE_URL=""

TOKEN=""

MODEL_NAME=""



model = init_chat_model(

    model=MODEL_NAME,

    model_provider="openai",

    base_url=BASE_URL,

    api_key=TOKEN,

    temperature=0,

)
summarization_model = model.bind(max_tokens=128)



# count_tokens_approximately更适合英⽂分词，中⽂这⾥使⽤tiktoken来计算token数量

encoding = tiktoken.get_encoding("cl100k_base")



def count_tokens_accurately(messages: list[BaseMessage]) -> int:

    """使⽤ tiktoken 精确计算消息列表的 token 总数"""

    # 注意：langmem 的 token_counter 期望的输⼊是消息列表

    text_content = " ".join([msg.content for msg in messages if isinstance(msg.content, s

    return len(encoding.encode(text_content))



class State(MessagesState):

    context: dict[str, RunningSummary]


class LLMInputState(TypedDict):

    summarized_messages: list[AnyMessage]

    context: dict[str, RunningSummary]



summarization_node = SummarizationNode(

#token_counter=count_tokens_approximately,

    token_counter=count_tokens_accurately,  # 更换为⾃定义的token计算⼯具

    model=summarization_model,

    max_tokens=256,

    max_tokens_before_summary=256,

    max_summary_tokens=128,

## PDF物理页 31

      initial_summary_prompt=summary_prompt,  # 使⽤⾃定义prompt，默认为英⽂

      existing_summary_prompt=update_summary_prompt

  )


  def call_model(state: LLMInputState):

      response = model.invoke(state["summarized_messages"])

      return {"messages": [response]}



  checkpointer = InMemorySaver()

  builder = StateGraph(State)

  builder.add_node(call_model)

  builder.add_node("summarize", summarization_node)

  builder.add_edge(START, "summarize")

  builder.add_edge("summarize", "call_model")

  graph = builder.compile(checkpointer=checkpointer)



  # Invoke the graph

  config = {"configurable": {"thread_id": "1"}}

  graph.invoke({"messages": "你好，我叫ada"}, config)

  graph.invoke({"messages": "请写⼀⾸诗，关于⼩狗的"}, config)

  graph.invoke({"messages": "再写⼀⾸关于⼩猫的"}, config)

  final_response = graph.invoke({"messages": "我叫什么名字？"}, config)



  final_response["messages"][-1].pretty_print()

  # 检查摘要是否⽣成

  if"running_summary"in final_response["context"]:

      print("\n⽣成的摘要:", final_response["context"]["running_summary"].summary)

  else:

      print("\n对话较短，尚未⽣成摘要。")


输出如下：








如果需要在        agent 中实现的话，那么将               SummarizationNode    传⼊   pre_model_hook    即可。
SummarizationNode会⾃动检查历史消息的长度，当token数量超过阈值时，触发⼀次总结，
然后将”摘要 + 最新消息“的组合传递给model。其中，initial_summary_prompt⽤于第⼀次⽣
成摘要时的prompt         模板，existing_summary_prompt          ⽤于更新现有摘要的prompt                模板，
ﬁnal_prompt是将摘要与剩余的消息合                                                      并后的prompt模板。

State中的context字段⽤于存储运⾏中                     的摘要信息，   避免在每次调⽤时都重复总结。

检查点管理

## PDF物理页 32

对有状态的agent的记忆进⾏检查、管理和重置，对于监控agent和提⾼⽤户使⽤体验都必不可
少，LangGraph提供了以下的⼀些⼯                                           具，⽤来对检查点进⾏管理。

查看最近的短期记忆，也就是最近的检查点的状态：





 graph.get_state(config=config)


查看线程的所有短期记忆，会按时间顺序返回这个线程所有的历史检查点：





 graph.get_state_history(config=config)


删除⼀个线程的所有短期记忆，⼀般⽤于重启对话场景：





 checkpointer.delete_thread(thread_id)

引⼊ MCP协议构建真实的      Agent长记忆应⽤

本节将介绍如何基于     Model Context Protocol（MCP）协议，使⽤LangGraph-Supervisor框
架构建⼀个实⽤的、集成中断机制、有长记忆的多Agent系统。MCP是⼀种社区共建的AI开放
协议，它标准化了应⽤向      AI提供上下⽂的⽅式，极⼤简化了⼯具集成过程。

接下来，我们从头开始搭建multi-agent系统，模拟⼀个⽤户去进⾏旅游信息查询，并进⾏酒
店预定，然后酒店管理侧可以查询⽤户的预定信息。整个Demo我们将展⽰Supervisor框架的
搭建、⼈⼯介⼊、长短期记忆的应⽤等。















我们将逐步构建    multi-agent⼯作流的每个组件，它包含三个⼦智能体，三个专门的 ReAct
（推理和⾏动）⼦智能体，然后它们将组合起来创建⼀个包含额外步骤的多智能体⼯作流。

我们的⼯作流从以下开始：

1.human_input:⽤户输⼊;admin_input:管理员输⼊

2.supervisor协调三个⼦agent，根据input内容，选择合适的  agent进⾏⼯作

3.当supervisor选择调⽤search_assistant的时候，那么查询信息,并将结果返回

## PDF物理页 33

4.当supervisor选择调⽤      hotel_assistant的时候，那么把⽤户的预定信息                  ,更新到   Store中

5.当supervisor选择调⽤       booking_info_assistant，会先进⾏       verify_info，中断图的执⾏以请求
管理员ID,当输⼊管理员ID后，接着判断管理员ID是否符合要求，如果不符合,那么不进⾏记忆
查询，如果符合，则查询记忆                ,并返回。

步骤⼀：环境准备与安装




  pip install langchain-mcp-adapters

步骤⼆：模型初始化




  BASE_URL=""

  TOKEN=""

  MODEL_NAME=""



  from langchain_openai import ChatOpenAI

  from langchain.chat_models import init_chat_model



  model = init_chat_model(

      model=MODEL_NAME,

      model_provider="openai",

      base_url=BASE_URL,

      api_key=TOKEN,

      temperature=0,

  )

步骤三：初始化长短期记忆




  from langgraph.store.memory import InMemoryStore

  from langgraph.checkpoint.memory import InMemorySaver


  store = InMemoryStore()

  checkpointer = InMemorySaver()

步骤四：⼯具与助⼿配置

搜索助⼿




  from typing import List

  from typing_extensions import TypedDict



  from langchain_core.messages import BaseMessage

  from langchain_core.runnables import RunnableConfig

  from langchain_mcp_adapters.client import MultiServerMCPClient

## PDF物理页 34

  from langgraph.prebuilt import create_react_agent

  from langgraph.config import get_store



  from langgraph.graph import StateGraph, END

  from langgraph.types import interrupt

  from langchain_core.messages import AIMessage, ToolMessage, HumanMessage



  # 搜索功能

  url = ''

  TOKEN = ''

  search_client = MultiServerMCPClient(
      {

     "other_search": {

  "url": url,

  "headers": {

      "Authorization": f"Bearer {TOKEN}"

  },

  "transport": "sse"

     }

      }
  )

  search_tools = await search_client.get_tools()

  search_agent = create_react_agent(

      model,

      search_tools,

      name="search_assistant",

      prompt="你是⼀个能搜索各种信息的助⼿。"

  )





          腾讯技术⼯程
          腾讯技术官⽅号。 腾讯技术创新、 前沿领域发 布解读平台。
          690篇原创内 容


  公众号

酒店预定助⼿

定义图节点之间流动的共享数据结构，将需要存储的记忆格式化。





  class UserInfo(TypedDict):

      user_id: str

      hotel_name: str

      date: str

      num_guests: int

## PDF物理页 35

定义预定酒店⼦智能体，并将⽤户预定历史存储下来。





  def book_hotel(user_info: UserInfo, config: RunnableConfig):

      """处理酒店预订并更新⻓期记忆"""

      user_id = config["configurable"].get("user_id")

      print(user_info)



      hotel_name = user_info.get("hotel_name")

      date = user_info.get("date")

      num_guests = user_info.get("num_guests")



      # 存储⽤户个⼈预订历史

      namespace = ("user_bookings",)



      user_bookings = store.get(namespace, user_id) or []

      user_bookings.append(user_info)

      store.put(namespace, user_id, user_bookings)



      # 更新总预订计数

      namespace = ("total_hotel_bookings",)

      total_bookings = store.get(namespace, 'total_bookings_num') or 0

      store.put(namespace, 'total_bookings_num', total_bookings + 1)



      return f"成功为⽤户 {user_id} 预订了 {hotel_name}，⼊住⽇期：{date}，⼊住⼈数：{num_guests}



  book_hotel_agent = create_react_agent(

      model=model,

      tools=[book_hotel],

      store=store,

      name="hotel_assistant",

      prompt="你是⼀个酒店预定助⼿。不需要⽤户ID、身份证号码、姓名和联系⽅式，就可以预定，请直接预定！"

  )


查询助⼿

⽤户的预定信息都是需要保密的，只有特定的管理员才可以进⾏查询，因此，需要设计中断机
制，审核请求查询⽤户的权限是否符号要求，即：在正式查询前，先中断⼀下，要求输⼊管理
员ID信息；等输⼊后，接着执⾏图，再去判断管理员ID信息是否符合要求；只有符合才能正常
进⾏⽤户信息查询。

1.查询⼯具定义：





  def query_booking_from_store(config: RunnableConfig) -> str:

      """根据⽤户ID从存储中查询酒店预订信息。"""

      store = get_store()

## PDF物理页 36

      user_id = config["configurable"].get("user_id")

      booking_info = store.get(("user_bookings",), user_id)



      if booking_info and booking_info.value:

     return f"已找到预订信息：{str(booking_info.value)}"

      else:

     return "未找到该⽤户的预订信息"


2.定义⼦图的状态：





  class SubgraphState(TypedDict):

      messages: List[BaseMessage]


3.创建新的图节点，负责中断和验证：





  def authentication_and_query_node(state: SubgraphState, config: RunnableConfig):

      """

      这个节点⾸先中断图的执⾏以请求管理员ID，

      然后在恢复后验证ID，并调⽤⼯具查询信息。

      """

      # 核⼼：调⽤ interrupt() 来暂停图的执⾏

      admin_input = interrupt("请输⼊管理员id，如需退出查询，请输⼊exit")



      # 当图被恢复时，admin_input 将会获得传⼊的值

      if admin_input == "exit":

     result = "⽤户已退出查询。"

      elif admin_input == "admin_123":

     # 验证成功，调⽤真正的查询⼯具

     result = query_booking_from_store(config)

      else:

     # 验证失败

     result = f"没有权限查询：admin_id 不匹配 (输⼊为: '{admin_input}')"



      return {"messages": [AIMessage(content=result)]}


4.构建包含中断节点的⼦             agent：





  query_workflow = StateGraph(SubgraphState)

  query_workflow.add_node("auth_and_query", authentication_and_query_node)

  query_workflow.set_entry_point("auth_and_query")

  query_workflow.add_edge("auth_and_query", END)

## PDF物理页 37

  booking_query_subgraph = query_workflow.compile(checkpointer=checkpointer, store=store)



  # 为⼦图命名，以便Supervisor可以调⽤它

  booking_query_subgraph.name = "booking_info_assistant"


步骤五：      Supervisor架构构建

基于上述组件，我们将构建⼀个完整的                      Supervisor架构⼯作流。





  from langgraph_supervisor import create_supervisor



  workflow = create_supervisor(

      [search_agent, book_hotel_agent, booking_query_subgraph],
      model=model,

      prompt=(

     "您是团队主管，负责管理信息搜索助⼿、酒店预订助⼿、以及⽤户信息查询助⼿。"

     "如需搜索各种信息，请交由 search_assistant 处理。"

     "如需预定酒店，请交由 hotel_assistant 处理。"

     "如需查询⽤户的酒店预定信息，请交由 booking_info_assistant 处理。"

     "**注意**，你每次只能调⽤⼀个助理agent！"

      ),

  )


  supervisor = workflow.compile(checkpointer=checkpointer, store=store)

步骤六：系统运⾏

第⼀次交互：        查询北京⽕锅店




  config = {"configurable": {"thread_id": "1", "user_id": "user_123"}}



  print("--- 第⼀次交互 ：查询北京⽕锅店---")

  async for chunk in supervisor.astream(

      {"messages": [("user", "北京最出名的⽼北京⽕锅是哪家？")]},

      config

  ):

      # 打印每个数据块的内容

      for key, value in chunk.items():

     print(f"Node: '{key}'")

     if value:

  print("  value:")

  print(value)

      print("----")


输出：

## PDF物理页 38

  北京最出名的⽼北京⽕锅有很多家，其中⽐较有名的包括：\n\n1. **东来顺**：东来顺是北京最著名的⽼北京涮⽺⾁


第⼆次交互：根据上⼀步推荐的⽕锅店查询酒店




  print("--- 第⼆次交互 ：根据上⼀步推荐的⽕锅店查询酒店---")

  async for chunk in supervisor.astream(

      {"messages": [("user", "那第⼀个推荐的⽕锅店附近有哪些酒店呀")]},

      config

  ):

      # 打印每个数据块的内容

      for key, value in chunk.items():

     print(f"Node: '{key}'")

     if value:

  print("  value:")

  print(value)

      print("----")


输出：





  东来顺⽕锅店位于北京市东城区东华⻔⼤街。以下是东来顺⽕锅店附近的⼀些酒店推荐：\n\n1. **北京王府井希尔顿


可以看到，     supervisor记得上⽂中提到                           过的第⼀个推荐的⽕锅店，这是短期记忆的典型应⽤。

第三次交互：预定酒店




  print("--- 第三次交互 ：预定酒店---")



  async for chunk in supervisor.astream(

      {"messages": [("user", "帮我预定北京王府井希尔顿酒店酒店，预定⽇期：2025-11-13到2025-11-14，⼊

      config

  ):

      for key, value in chunk.items():

     print(f"Node: '{key}'")

     if value:

  print("  value:")

  print(value)

      print("----")


输出：





  已成功为您预订了北京王府井希尔顿酒店，⼊住⽇期为2025年11⽉13⽇⾄2025年11⽉14⽇，⼊住⼈数为1⼈。祝您旅途

## PDF物理页 39

成功调⽤预定酒店助⼿，并完成酒店预定。

第四次交互：管理员查询预定信息




  print("--- 第四次交互 ：管理员查询预定信息---")

  config = {"configurable": {"thread_id": "2", "user_id": "user_123"}}  # 更换管理员操作线程



  interrupt_data = None
  interrupt_input = None

  print("--- 第⼀次运⾏，将会触发中断 ---")

  async for chunk in supervisor.astream(

      {"messages": [("user", "查询⽤户预定酒店信息")]},

      config,

  ):

      for key, value in chunk.items():

     print(f"Node: '{key}'")

     if value:

  print("  value:")

  print(value)



     if key == "__interrupt__":

  print("\n======= 图已成功中断！=======")

  interrupt_data = value[0]

  print(f"中断信息: {interrupt_data.value}")

  break



      if interrupt_data:

     break

      print("----")





  if interrupt_data:

      # 模拟管理员输⼊正确的密码

      interrupt_input = Command(resume="admin_123")

      # 如果想测试错误的密码，可以使⽤下⾯这⾏

  #interrupt_input = Command(resume="wrong_password")



      print(f"\n--- 接收到中断输⼊ '{interrupt_input}'，继续执⾏图 ---")

      # 恢复图的执⾏

      async for chunk in supervisor.astream(

     interrupt_input,

     config,

      ):

     for key, value in chunk.items():

  print(f"Node: '{key}'")

  if value:

## PDF物理页 40

     print("  value:")

     print(value)

    print("----")


第⼀次运⾏，触发中断并输出：





 请输⼊管理员id，如需退出查询，请输⼊exit


接着，程序模拟管理员输⼊正确的ID后，继续执⾏图，booking_info_assistant查询到长期记
忆，并输出：





 已找到预订信息：[{'user_id': 'user_123', 'hotel_name': '北京王府井希尔顿酒店', 'date': '2025-11


最终， supervisor返回最终的结果：





 ⽤户预定的酒店信息如下：\n- ⽤户ID: user_123\n- 酒店名称: 北京王府井希尔顿酒店\n- 预定⽇期: 2025-11

未来⼯作

更智能的记忆管理策略

在上述的⽰例（预定酒店）中，我们仅将⽤户预定信息直接进⾏存储、检索，但对于
supervisor来说，记住和不同⽤户的过往交互是⾮常重要的，在后续的交互中，才能针对不同
的⽤户，给出更合适的回应。让Agent能⾃主决定记忆的存储、遗忘、更新和检索优先级，才
能真正模拟⼈类的记忆过程。因此，未来需要改进设计更智能的记忆管理策略。

记忆驱动的多智能体系统架构选择

在上述⽰例（预定酒店）中，我们选择了Supervisor架构进⾏实现，但这显然存在缺陷，管理
员系统不应该和⽤户系统使⽤同⼀个中央智能体，当系统功能越来越完善时，这样的设计会使
得supervisor⾮常繁杂、且难以维护，Supervisor架构更适合需要明确控制流程和集中决策的
场景。融合记忆功能的Multi-Agent  系统可以根据应⽤场景选择更合适的架构，例如
Hierarchical架构，可以⽤于不同层级的记忆服务于不同⽬的（个体、团队、全局）的场景；
Custom架构，预先定义好各个   Agent的记忆⾛向，构建更灵活的系统。



                        腾讯⼩  Q介绍

⼩Q是官⽅QQ助⼿，集成了腾讯混元、DeepSeek等前沿⼤模型技术，具备强⼤的多模态交互
与复杂任务处理能⼒。

## PDF物理页 41



## PDF物理页 42



## PDF物理页 43

参考⽂献


[1] Chhikara P, Khant D, Aryan S, et al. Mem0: Building production-ready ai agents with scalable long-

term memory[J]. arXiv preprint arXiv:2504.19413, 2025.


[2]  Langchain Docs




                                                福利时刻


      抽奖助⼿
 腾讯视频VIP⽉卡5份






































     ⼩程序

## PDF物理页 44

       腾讯技术⼯程
       腾讯技术官⽅号。 腾讯技术创新、 前沿领域发 布解读平台。
       690篇原创内 容


  公众号




















阅读 1.1万





留⾔


写留⾔





                         还没有 留⾔，来 写⾸评

## PDF物理页 45


