# 原文逐页转写

文本来自本次 PDF 文本层；不补写图片、截断内容或代码。图片和布局请打开每页 PDF 链接核对。AI 解释另见学习笔记。

## PDF 第 1 页

[原页](RAW.pdf#page=1)

````text
详尽地带你从零开始设计实现⼀个 AI  Agent 框架
腾讯程序员 2026 年 4 ⽉ 13 ⽇ 02 : 36⼴东腾讯技术⼯程 153 ⼈
作者： yabohe
年初⽕爆现在热度依旧的OpenClaw为 AI Agent 带来了新的想象。如果说 2025 是 AI Agent 智能
体元年，想必 2026 将会是 AI Agent 真正商⽤化的开端，⽽ AI Agent 商⽤化的前提是各⾏各业开
始落地实际商业领域的 AI Agent 。
作为⼀名程序员 / ⼯程师，思考的更多的可能是如何将 AI Agent 落地实现的层⾯。⼯程框架往
往是⼯程应⽤实现的基⽯，框架选型也是架构师们设计与实现⼀个 AI Agent 智能体的⾸要⼯
作。
⼀、 AI Agent 框架理论篇
Agent = Reasoning + Acting
1.1 AI Agent 框架基础理论
AI 智能体是使⽤  AI 来实现⽬标并代表⽤户完成任务的软件系统。其表现出了推理、规划和记
忆能⼒，并且具有⼀定的⾃主性，能够⾃主学习、适应和做出决定。
Google Cloud
关于 AI Agent 这⾥引⽤了Google Cloud 的定义，⾔简意赅。
1 ） ReAct 模式
````

## PDF 第 2 页

[原页](RAW.pdf#page=2)

````text
在当前 AI Agent 理论中，最具有基础性与代表性的要数 ReAct 模式，它是Yao 等⼈于 2022 年在
《 ReAct: Synergizing Reasoning and Acting in Language Models 》论⽂中提出，核⼼思想将推
理（ Reasoning ）和⾏动（ Acting ）相结合。 CoT 提升的是 LLM 的推理能⼒，但它的缺点在于
缺少与外部世界的交互从⽽缺少外部反馈来拓展⾃⾝的知识空间，ReAct弥补了这⼀缺陷。
ReAct 智能体的运作基于⼀个循环过程（不断迭代更新），包括以下三个步骤：
推理（ Reasoning ）：依赖 LLM ，分析当前任务状态，⽣产内部推理，决定下⼀步⾏动，核
⼼思想是 CoT （ Chain of Thought ）
执⾏（ Acting ）：根据上⼀步的推理结果，执⾏具体的操作，例如查询信息或调⽤外部⼯具
（ Function Tool ， MCP ，  Shell 命令，代码执⾏等），具体依赖宿主机的执⾏环境与应⽤场
景
观察（ Observation ）：观察⾏动的结果，将反馈⽤于下⼀轮的思考；或者观察到已经判断
是最终的答案，则整理输出结果
2 ） Plan-and-Execute 模式
2023 年 5 ⽉， Langchain 团队基于Lei Wang 等发表的《 Plan-and-Solve Prompting 》论⽂和开源
的 BabyAGI Agent 项⽬的⼯作，提出了Plan-and-Execute 模式。
《 Plan-and-Solve Prompting 》核⼼思想：让 LLM 先制定完整的分步计划，再按步骤执
⾏，⽽⾮边做边想（ ReAct ）
BabyAGI 项⽬：⾸个流⾏的任务驱动型⾃主 Agent ，实现了 " ⽣成任务列表→执⾏→再规
划 " 的 Agent Loop
Plan-and_Execute 模式强调先制定多步计划，再逐步执⾏，属于结构化⼯作流程（ Planing ->
Task1 -> Task2 -> Task3 -> Summary ），⽐较适合复杂且任务关系以来明确的长期任务。缺
点则是倾向于 workﬂow ，缺乏动态调整能⼒。
3 ） Reﬂection 模式
最早系统性的提出在 Agent 中引⼊反思概念的是Noah Shinn 、 Shunyu Yao （对，还是 ReAct 作
者）等的《 Reflexion: Language Agents with Verbal Reinforcement Learning 》论⽂，论⽂⾥提
出了 Reﬂexion 框架，通过语⾔反馈⽽⾮权重更新来强化语⾔ Agent 。 Agent 通过对任务反馈信
号进⾏  ⼝头反思，然后在情节记忆缓冲区中维护⾃⼰的反思⽂本，以在后续试验中做出更好
的决策。
````

## PDF 第 3 页

[原页](RAW.pdf#page=3)

````text
另外， Aman Madaan 等受⼈类改进⽂本⽅式的启发，在《 Self-Refine: Iterative Refinement
with Self-Feedback 》论⽂提出了⼀种名 Self-Reﬁne 的⽅法，通过迭代反馈和改进来提升  LLM
的初始输出：先让 LLM 输出，然后再根据输出提供反馈，不断迭代。在所有评估的任务中
Self-Reﬁne ⽅法可以使得任务性能平均提升约  20% 。
清华⼤学与微软联合发布的《 CRITIC: Large Language Models Can Self-Correct with Tool-
Interactive Critiquing 》论⽂则结合外部⼯具（如搜索引擎、代码执⾏器）验证输出，再基于
验证结果⾃我修。
这些⾥程碑论⽂都是 Reﬂection 模式的理论基础，当前主流的 Agent 框架虽然有各种演绎与变
形，也都是在 ReAct 提出之后发展出来的扩展和补充， Agent 核⼼实践依旧离不开 ReAct ：将
推理与执⾏结合起来。
1.2 主流  AI Agent 框架对⽐
当前主流 Agent 框架主要包含以下⼏种：
LangChain - 最成熟和流⾏的框架之⼀，提供丰富的⼯具链和集成，适合快速构建复杂的
AI 应⽤。⽀持多种 LLM 、向量数据库和⼯具调⽤，有完善的⽂档和社区⽀持。
LlamaIndex - 专注于数据索引和检索，特别擅长 RAG （检索增强⽣成）场景。提供⾼效的
⽂档处理和查询能⼒，适合知识密集型应⽤。
AutoGPT/AutoGen - 微软推出的多 Agent 协作框架，⽀持多个 Agent 之间的对话和协作，
可以处理更复杂的任务分解和执⾏。
CrewAI - 专注于⾓⾊扮演型 Agent 的协作框架，每个 Agent 有明确的⾓⾊和⽬标，适合模拟
团队协作场景。
LangGraph - LangChain 团队开发的状态图框架，提供更精细的流程控制，适合构建复杂
的、需要明确状态管理的 Agent 应⽤。
Semantic Kernel - 微软的轻量级框架，与 Azure 服务集成良好，⽀持多种编程语⾔，强调
插件化设计。
选择建议
如果是想快速出 Agent 原型，可以试试 LangChain ；
如果是构建 RAG 应⽤，则强烈建议 LlamaIndex ；
如果业务场景为多 Agent 协作，推荐 AutoGen 或 CrewAI ，它们是专为多智能体协作⽽⽣
的；
如果业务中涉及复杂的流程控制，建议使⽤ LangGraph ，通⽤性好，基于状态管理的
workﬂow 灵活性⾼；
如果⼯作环境围绕 .NET ⽣态展开的，那搭配 Semantic Kernel 是最佳选项。
另外，随着 Anthropic 公司的 Claude Cowork AI 通⽤ Agent 兴起，⼀些基于通⽤ Code Agent
SDK 的套壳 Agent 也开始流⾏（如公司 CodeBuddy 团队基于CodeBuddy Agent SDK等⽣成的
````

## PDF 第 4 页

[原页](RAW.pdf#page=4)

````text
WorkBuddy 应⽤），这些 Agent 的创新之处在于可以针对各类⽤户场景提供更好的交互设计与
⼯作流场景解决⽅案。
1.3 AI Agent 框架核⼼
在 Agent 应⽤发展与实践过程中，有⼀家公司的⼀款 Agent 应⽤不得不提，那就是 AI 初创公司
Monica 发布的 Agent C 端产品： Manus ，它的爆⽕让让 Agent 产品进⼊⼤众视野。
在 Agent 产品⼈机交互⽅⾯：它模糊地勾勒出了 Agent 应⽤的⼈机交互的雏型。想象⼀下，
键盘和⿏标的出现，第⼀代 iPhone 的出现，回过头来看都是变⾰性的历史事件。
在 Agent ⼯程实践⽅⾯：当 MCP 风靡⼀时时， Manus ⾸席科学家 Peak 在社交媒体直接回
复 "Actually, Manus doesn't use MCP" ； 4 个⽉后（ 2025 年 7 ⽉）， Manus ⼯程博客发表
《 AI Agent 的上下⽂⼯程：构建 Manus 的经验教训》，分享 Manus 为何放弃微调（ Fine-
tuning ）路线，转⽽选择基于已有通⽤⼤模型深耕上下⽂⼯程（ Context Engineering ），其
中的⼀条经验教训为：使⽤⽂件系统作为上下⽂。 3 个⽉后， Anthropic 在 2025 年 10 ⽉推出
Claude Skills ，从此 " 使⽤⽂件系统作为上下⽂ " 的理念开始深⼊⼈⼼。
"Actually, Manus doesn't use MCP" 还有后半句： "inspired by CodeAct" 。 CodeAct 是⼀个
Agent 设计架构，来⾃于 UIUC 的王星尧博⼠在 2024 年初发表的⼀篇论⽂《 Executable Code
Actions Elicit Better LLM Agents 》，它提出通过⽣成可执⾏的 Python 代码来统⼀ LLM Agent
的⾏动空间，也就是 Acting 不仅可以有 Fucntion Call 和 MCP ，还可以执⾏代码完成任务，⽽且
效果更好。 2025 年 11 ⽉， Anthropic 官⽅博客更新技术⽂章《 Code execution with MCP:
Building more efficient agents 》，提出将  MCP 服务器作为代码  API （⽽⾮直接的⼯具调⽤）
来提供，然后， Agent 就可以编写代码来与  MCP 服务器交互，这样 Agent 可以按需加载，更⾼
效地利⽤上下⽂。 CodeAct 这个观点与本⽂开头的 Shunyu Yao 的 " ⼈类最重要的  aﬀordance 是
⼿，⽽  AI 最重要的  aﬀordance 可能是代码 " 也不谋⽽合。
从 Manus 的故事，我们可以得出当前关于 Agent ⼯程的两⼤业内共识：
使⽤⽂件系统作为上下⽂（如使⽤⽂件保存 Agent 长期记忆，如OpenClaw 的
SOUL.md/TOOLS.md/MEMORY.md等）
编程是解决通⽤问题的⼀种普适⽅法（ AI 更擅长使⽤代码解决问题：问题 -> ⽣成代码 -> 执
⾏代码 ->Again-> 直到问题解决）
虽然当前 Agent 框架发展从 ReAct 模式逐渐融合 CodeAct 模式，但是 Agent 框架本质的推理与执
⾏功能并没有变化。
````

## PDF 第 5 页

[原页](RAW.pdf#page=5)

````text
在⼯程层⾯来说，推理本质就是 LLM Call ，执⾏本质则是 Tools Call （代码可认为是 Tools 的⼀
种），⽽连接这⼆者的上下⽂⼯程（ Context Engineering ）则是 Agent 框架的核⼼。
1.3.1 Agent 框架三⼤部分
下⾯我们来拆解⼀下 Agent 框架在⼯程上的解法，主要包括三⼤部分
LLM Call ：这部分为 API 管理的范畴，通常情况下，主要⼯作是兼容各⼤ LLM ⼚商的 API 实
现细节以及流式输出等基础能⼒，为 Agent 框架提供⼀个标准化的 API 调⽤。
Tools Call ：这部分主要是 LLM 如何使⽤外部⼯具，从最早的 Function Call 到后来的 MCP 以
及当前的 Skill 部分内容（涉及⼯具调⽤的那部分）都属于这⼀范畴。当前 Tools 的主流形式
包括⽂件操作、⽹络搜索、 Shell 命令 / 代码执⾏以及 API/MCP 调⽤等，根据 Agent 具体使⽤
场景⽽定，也可以后续增删改。
Context Engineering ：狭义的上下⽂⼯程特指提⽰词 Prompt 的⼯程实现（如 Rules 、
Claude.md 以及 AGENTS.md 等），⽽⼴义上的上下⽂⼯程其实也包含 LLM 使⽤外部⼯具这
部分（⽐如 Skills ，它是⼯具与提⽰词结合的典范）。
以上 Agent 三⼤部分中，第 1 部分的 LLM Call 基本上没有啥⼯程变量，这块的⼯程实践中
LiteLLM 库（它是⼀个 Python 库，旨在简化多种⼤型语⾔模型（ LLM ） API 的集成）已经是佼
佼者了；第 2 部分的 Tools 使⽤，包含的⼯具列表范围也有业内最佳实践，具体取决于 Agent 使
⽤的业务场景。
剩下的最⼤的⼀个变量是第 3 部分的上下⽂⼯程，这也是 Agent 框架智能的核⼼所在。
OpenClaw 的爆⽕出圈除了将⼿机即时应⽤与 Agent 结合这点之外，它的上下⽂⼯程的管理也
⾮常有创新。
近⽇， Shunyu Yao 团队在腾讯混元官⽹发表了⼀篇名为 《从  Context 学习，远⽐我们想象
的要难》的⽂章，提出 “ 模型想要迈向⾼价值应⽤，核⼼瓶颈就在于能否⽤好  Context 。 ” 的观
点。正如⽂中所⾔ " 在不提供任何  Context 的情况下，最先进的模型  GPT-5.1 (High) 仅能解决
不到  1% 的任务 " 。如果说 Agent 应⽤中，现在哪⾥还是低垂的果实可以摘取，那可能是上下
⽂⼯程（ Context Engineering ）。
简单总结为⼀句话：Agent 应⽤中上下⽂⼯程⼤有可为（仍有很⼤优化空间）。
1.3.2 Agent Loop
在 1.3.1 ⼩节中我们讨论了 Agent 框架的核⼼是上下⽂⼯程，⽽上下⽂⼯程的核⼼引擎或者称之
为运⾏框架则是 Agent Loop 。
Agent Loop 也不神秘，本质是⼀个 While 循环，每⼀次迭代是⼀次 LLM 推理外加⼯具调⽤和上
下⽂处理，也就是说所有 Agent ⾏为的发⽣都是在这个 While 循环⾥⾯，直到任务完成退出。
典型的⼯作流程如下：
初始上下⽂（系统提示词 + ⽤户请求）
    ↓
````

## PDF 第 6 页

[原页](RAW.pdf#page=6)

````text
[agent loop 开始 ]
    ↓
agent 读取上下⽂  → 思考  → 决定⾏动
    ↓
执⾏⼯具 / ⾏动  → 获得结果
    ↓
结果追加到上下⽂
    ↓
[ 循环继续或结束 ]
细分到 While 循环到每⼀次迭代（ Turn ）可简单表⽰为：
初始化上下⽂（⽤户请求）
  ↓
┌─────────────────────────────────┐
│  Agent Loop                     │
│                                 │
│  ┌─────────────────────┐        │
│  │ Turn 1              │        │
│  │  LLM Call 推理  #1            │
│  │  → 解析 LLM 响应         │        │
│  │  → 执⾏⼯具 1          │        │
│  │  → 返回结果，更新上下⽂  │        │
│  └─────────────────────┘        │
│           ↓                     │
│  ┌─────────────────────┐        │
│  │ Turn 2              │        │
│  │  LLM Call 推理  #2    │        │
│  │  → 执⾏⼯具 2          │        │
│  │  → 返回结果，更新上下⽂  │        │
│  └─────────────────────┘        │
│           ....                  │
└─────────────────────────────────┘
  ↓
完成 ( 当某⼀次 Turn 不再执⾏⼯具即表示完成，返回所有结果信息）
Agent Loop 通过在每次迭代中读取、利⽤和更新上下⽂来完成任务；上下⽂⼯程则是设计如
何组织、管理和优化这些上下⽂信息以提升 Agent 的决策质量和效率。
回到本节的主题，可总结为⼀句话：Agent 框架设计的核⼼就是在 Agent Loop 这个 While 循环
中设计如何管理上下⽂。
⼆、 AI Agent 框架实践篇
承接上篇： Agent 框架设计的核⼼是在 Agent Loop 这个 While 循环中设计如何管理上下⽂，本
篇即围绕这个核⼼论点展开。
````

## PDF 第 7 页

[原页](RAW.pdf#page=7)

````text
2.1 Agent 框架架构图⼀览
┌─────────────────────────────────────────────────────────────────────┐
│                User Interface （ CLI REPL Layer ）                      │
│  ┌──────────────┐   ┌──────────────┐   ┌──────────────────────────┐ │
│  │  User Input  │   │    Exit/     │   │   Message History        │ │
│  │   Handler    │   │   Clear Cmd  │   │   Management             │ │
│  └──────┬───────┘   └──────────────┘   └──────────────────────────┘ │
│         │                                                           │
│         ▼                                                            │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │                      Agent Loop Core                         │   │
│  │  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐   │   │
│  │  │   LLM Call   │─── ▶ │ Tool Call    │─── ▶ │   Tool Exec  │   │   │
│  │  │   (DeepSeek) │    │   Parser     │    │   Engine     │   │   │
│  │  └──────────────┘    └──────────────┘    └──────────────┘   │   │
│  │         │                                              │     │   │
│  │         │ ◀ ─────────────────────────────────────────────┘     │   │
│  │         │ (Tool Results Feedback)                            │   │
│  │         ▼                                                     │   │
│  │  ┌──────────────┐    ┌──────────────┐                       │   │
│  │  │   Response   │─── ▶ │   Context    │                       │   │
│  │  │   Formatter  │    │   Manager    │                       │   │
│  │  └──────────────┘    └──────────────┘                       │   │
│  └──────────────────────────────────────────────────────────────┘   │
│                              │                                      │
│                               ▼                                       │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │                    Tools Registry (TOOLS)                    │   │
│  │  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐            │   │
│  │  │ shell_  │ │ file_   │ │ file_   │ │ python_ │            │   │
│  │  │ exec    │ │ read    │ │ write   │ │ exec    │            │   │
│  │  └─────────┘ └─────────┘ └─────────┘ └─────────┘            │   │
│  │      │            │            │            │                │   │
│  │       ▼              ▼              ▼              ▼                 │   │
│  │  [Function]   [Function]   [Function]   [Function]          │   │
│  │  [Schema]     [Schema]     [Schema]     [Schema]            │   │
│  └──────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
再 review ⼀下⼯作流：
初始上下⽂（系统提示词 + ⽤户请求）
    ↓
[agent loop 开始 ]
    ↓
agent 读取上下⽂  → 思考  → 决定⾏动
    ↓
执⾏⼯具 / ⾏动  → 获得结果
````

## PDF 第 8 页

[原页](RAW.pdf#page=8)

````text
    ↓
结果追加到上下⽂
    ↓
[ 循环继续或结束 ]
2.2 Agent 框架三⼤要素设计
2.2.1 LLM Call
采⽤极简设计，以 DeepSeek 模型⽰例说明
LLM Provider ：使⽤ DeepSeek deepseek-chat 模型
LLM Call API ：使⽤标准化 OpenAI SDK
为保证代码的最⼤可读性，这⾥使⽤同步⾮流式调⽤。
2.2.2 Tools Call
采⽤极简的⼯具集，操作对象包含⽂件、 Shell 和 Python 代码执⾏
1） Tools 实现：总共⽀持 4 个⼯具函数
shell_exec ：执⾏ shell 命令并返回输出
ﬁle_read ：读取⽂件内容
ﬁle_write ：写⼊⽂件内容（⾃动创建⽬录）
python_exec ：在⼦进程中执⾏ Python 代码并返回输出
2） Tools 注册：这⾥选择的是⼿动维护字典映射的⽅式  name →  (function, OpenAI function
schema) ，这⼀步是为了解析 llm call 的 response 时可以根据 name 匹配需要具体执⾏哪个 tool
Tools 的定义遵循的是  OpenAI Function Calling 的标准格式（也称  OpenAI Tools API
schema ）
2.2.3 Context Engineering
System Prompt ：极简系统提⽰词，告知 LLM 可⽤⼯具和 ReAct 思考⽅式
⽤户 Session 管理：使⽤ messages 列表⽅式（ OpenAI chat 格式），它是核⼼状态，累积
系统提⽰词、⽤户消息、助⼿响应和⼯具结果
2.3 Agent 框架代码实现
2.3.1 第⼀部分： Agent Loop 与  上下⽂
基础流程：  LLM call →  parse tool_calls →  execute →  append results to messages →
loop or exit
安全设置：为 while 循环设置了⼀个迭代的安全上限： 20 轮（ MAX_TURNS=200 ）
使⽤全局变量 message 作为上下⽂的载体，累积系统提⽰词、⽤户消息、助⼿响应和⼯具
结果
其中，变量 message 按如下规则更新
````

## PDF 第 9 页

[原页](RAW.pdf#page=9)

````text
使⽤ System Prompt 初始化： {"role": "system", "content": system_prompt}
追增 User Message ： {"role": "user", "content": user_message}
追加 Tool Results ： {"role": "tool", "content": result}
# ============================================================
# Agent Loop — 核⼼
# ============================================================
MAX_TURNS = 20
def agent_loop(user_message: str, messages: list, client: OpenAI) -> str:
    """
    Agent Loop ： while 循环驱动  LLM 推理与⼯具调⽤。
    流程：
      1. 将⽤户消息追加到  messages
      2. 调⽤  LLM
      3. 若  LLM 返回  tool_calls → 逐个执⾏  → 结果追加到  messages → 继续循环
      4. 若  LLM 直接返回⽂本（⽆  tool_calls ） → 退出循环，返回⽂本
      5. 安全上限  MAX_TURNS 轮
    """
    messages.append({"role": "user", "content": user_message})
    tool_schemas = [t["schema"] for t in TOOLS.values()]
    for turn in range(1, MAX_TURNS + 1):
        # --- LLM Call ---
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=messages,
            tools=tool_schemas,
        )
        choice = response.choices[0]
        assistant_msg = choice.message
        # 将  assistant 消息追加到上下⽂
        messages.append(assistant_msg.model_dump())
        # --- 终⽌条件：⽆  tool_calls ---
        ifnot assistant_msg.tool_calls:
            return assistant_msg.content or""
        # --- 执⾏每个  tool_call ---
        for tool_call in assistant_msg.tool_calls:
            name = tool_call.function.name
            raw_args = tool_call.function.arguments
            print(f"  [tool] {name}({raw_args})")
            # 解析参数并调⽤⼯具
            try:
                args = json.loads(raw_args)
            except json.JSONDecodeError:
                args = {}
            tool_entry = TOOLS.get(name)
            if tool_entry isNone:
````

## PDF 第 10 页

[原页](RAW.pdf#page=10)

````text
                result = f"[error] unknown tool: {name}"
            else:
                result = tool_entry["function"](**args)
            # 将⼯具结果追加到上下⽂
            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": result,
                }
            )
    return"[agent] reached maximum turns, stopping."
注：这⾥使⽤的模型为 deepseek-chat ，主要考量因素是模型⽀持 Tool Calls ，并且完全兼容
OpenAI 的 SDK 。
2.3.2 第⼆部分： Tools 实现与注册
这⾥主要实现四个⼯具函数 : shell_exec, ﬁle_read, ﬁle_write, python_exec
# ============================================================
# Tools 实现  — 4 个⼯具函数
# ============================================================
def shell_exec(command: str) -> str:
    """ 执⾏  shell 命令并返回  stdout + stderr 。 """
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=30,
        )
        output = result.stdout
        if result.stderr:
            output += "\n[stderr]\n" + result.stderr
        if result.returncode != 0:
            output += f"\n[exit code: {result.returncode}]"
        return output.strip() or"(no output)"
    except subprocess.TimeoutExpired:
        return"[error] command timed out after 30s"
    except Exception as e:
        returnf"[error] {e}"
def file_read(path: str) -> str:
    """ 读取⽂件内容。 """
    try:
        with open(path, "r", encoding="utf-8") as f:
````

## PDF 第 11 页

[原页](RAW.pdf#page=11)

````text
            return f.read()
    except Exception as e:
        returnf"[error] {e}"
def file_write(path: str, content: str) -> str:
    """ 将内容写⼊⽂件（⾃动创建⽗⽬录）。 """
    try:
        os.makedirs(os.path.dirname(path) or".", exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        returnf"OK — wrote {len(content)} chars to {path}"
    except Exception as e:
        returnf"[error] {e}"
def python_exec(code: str) -> str:
    """ 在⼦进程中执⾏  Python 代码并返回输出。 """
    try:
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".py", delete=False, encoding="utf-8"
        ) as tmp:
            tmp.write(code)
            tmp_path = tmp.name
        result = subprocess.run(
            [sys.executable, tmp_path],
            capture_output=True,
            text=True,
            timeout=30,
        )
        output = result.stdout
        if result.stderr:
            output += "\n[stderr]\n" + result.stderr
        return output.strip() or"(no output)"
    except subprocess.TimeoutExpired:
        return"[error] execution timed out after 30s"
    except Exception as e:
        returnf"[error] {e}"
    finally:
        try:
            os.unlink(tmp_path)
        except OSError:
            pass
⼯具实现好了下⼀步就是注册，⽅便 Agent Loop 可以根据 LLM 的返回结果执⾏具体的⼯具⽅
法（实际上就是⼀个字典映射 name →  {function, OpenAI schema} ）
# ============================================================
# Tools 注册  — name → (function, OpenAI function schema)
# ============================================================
````

## PDF 第 12 页

[原页](RAW.pdf#page=12)

````text
TOOLS = {
    "shell_exec": {
        "function": shell_exec,
        "schema": {
            "type": "function",
            "function": {
                "name": "shell_exec",
                "description": "Execute a shell command and return its output.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "command": {
                            "type": "string",
                            "description": "The shell command to execute.",
                        }
                    },
                    "required": ["command"],
                },
            },
        },
    },
    "file_read": {
        "function": file_read,
        "schema": {
            "type": "function",
            "function": {
                "name": "file_read",
                "description": "Read the contents of a file at the given path.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "path": {
                            "type": "string",
                            "description": "Absolute or relative file path.",
                        }
                    },
                    "required": ["path"],
                },
            },
        },
    },
    "file_write": {
        "function": file_write,
        "schema": {
            "type": "function",
            "function": {
                "name": "file_write",
````

## PDF 第 13 页

[原页](RAW.pdf#page=13)

````text
                "description": "Write content to a file (creates parent directories if ne
                "parameters": {
                    "type": "object",
                    "properties": {
                        "path": {
                            "type": "string",
                            "description": "Absolute or relative file path.",
                        },
                        "content": {
                            "type": "string",
                            "description": "Content to write.",
                        },
                    },
                    "required": ["path", "content"],
                },
            },
        },
    },
    "python_exec": {
        "function": python_exec,
        "schema": {
            "type": "function",
            "function": {
                "name": "python_exec",
                "description": "Execute Python code in a subprocess and return its output
                "parameters": {
                    "type": "object",
                    "properties": {
                        "code": {
                            "type": "string",
                            "description": "Python source code to execute.",
                        }
                    },
                    "required": ["code"],
                },
            },
        },
    },
}
Tools 的定义遵循的是  OpenAI Function Calling 的标准格式（也称  OpenAI Tools API
schema ）。
具体来说， Agent 中每个⼯具的  schema 字段的结构如下：
{
      "type": "function",
````

## PDF 第 14 页

[原页](RAW.pdf#page=14)

````text
      "function": {
          "name": "...",
          "description": "...",
          "parameters": {
              "type": "object",
              "properties": { ... },
              "required": [ ... ],
          },
      },
  }
2.3.3 第三部分： System Prompt
这⾥定义 System Prompt ，每⼀次与 LLM 交互都需要带上它。
# ============================================================
# System Prompt
# ============================================================
SYSTEM_PROMPT = """You are a helpful AI assistant with access to the following tools:
1. shell_exec — run shell commands
2. file_read — read file contents
3. file_write — write content to a file
4. python_exec — execute Python code
Think step by step. Use tools when you need to interact with the file system, \
run commands, or execute code. When the task is complete, respond directly \
without calling any tool."""
明确告知：你是⼀个 AI 助⼿，当需要的时候可以使⽤哪些⼯具。
⾄此⼀个极简的 Agent 框架就此实现完成，单⽂件搞定，全部代码 279 ⾏。
2.4 基于极简  Agent 框架的极简  Agent 应⽤
2.4.1 ⽤户交互界⾯设计  - Python CLI REPL
框架实现完成之后，距离 Agent 应⽤就剩下最后⼀个⽤户交互界⾯了。
避免增加读者认知负担，从极简思想出发，这⾥使⽤ Python CLI REPL 即 Python 的交互式命
令⾏作为 Agent 的⼊⼝：
def main():
    api_key = os.environ.get("DEEPSEEK_API_KEY")
    ifnot api_key:
        print("Error: please set DEEPSEEK_API_KEY environment variable.")
        sys.exit(1)
    client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
    messages: list = [{"role": "system", "content": SYSTEM_PROMPT}]
````

## PDF 第 15 页

[原页](RAW.pdf#page=15)

````text
    print("Agent ready. Type your message (or 'exit' to quit, 'clear' to reset).\n")
    whileTrue:
        try:
            user_input = input("You> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nBye.")
            break
        ifnot user_input:
            continue
        if user_input.lower() == "exit":
            print("Bye.")
            break
        if user_input.lower() == "clear":
            messages.clear()
            messages.append({"role": "system", "content": SYSTEM_PROMPT})
            print("(context cleared)\n")
            continue
        reply = agent_loop(user_input, messages, client)
        print(f"\nAgent> {reply}\n")
2.4.2 DeepSeek 注册，获取  API Key
由于本⽂ Agent 框架的 LLM Provider 是基于 DeepSeek 实现的，所以需要获取 DeepSeek 模型
（ deepseek-chat 模型）的 API key 才能使⽤。
注册： https://platform.deepseek.com
获取 API Keys ： https://platform.deepseek.com/api_keys
2.4.3 极简  Agent 应⽤体验
使⽤之前设置 API key
export DEEPSEEK_API_KEY="sk-xxxxx"
先来问候⼀下：
````

## PDF 第 16 页

[原页](RAW.pdf#page=16)

````text
输出的基本上是 System Prompt 中的内容，符合预期。
1）第 1 个问题
帮我查⼀下当前⽬录都有哪些⽂件
2）第 2 个问题
让它执⾏⼀个统计任务：帮我统计下当前⽬录下的代码⾏数以及 token 数
````

## PDF 第 17 页

[原页](RAW.pdf#page=17)

````text
可以看到 Agent Loop ⾥在持续地调⽤ Tools 、写代码以及执⾏代码
最终的统计结果：
做完任务，使⽤ exit 命令退出当前 session
````

## PDF 第 18 页

[原页](RAW.pdf#page=18)

````text
可以看到实现的 Agent 应⽤，虽然实现极简，但是功能可以⼀点不简单（当 Agent 拥有⽂件读
写权限，外加 Shell ⼯具以及代码⽣成与执⾏权限，它在本机上真的可以 " 为所欲为 ") 。
要知道 OpenClaw 的底层 Agent Core （ Pi Agent ）的 Tools 层也是有且仅包含四个⼯具⽅法：读
⽂件（ Read ）、写⽂件（ Write ）、编辑⽂件（ Edit ）、命令⾏（ Shell ），其他的丰富且强⼤能⼒
均靠事件机制及 Skills 扩展⽽来。
三、写在后⾯的话
毫⽆疑问，当前极简版的 AI Agent 框架在程序健壮性、安全性、功能性（如流式输出）以
及优雅性（如 Tools 注册）都有很⼤改进空间，但是不容否认的是它五脏俱全，简单清晰，
可以帮助我们摒除那些复杂冗长的组件库，看清 Agent 的本质。
为什么需要极简？⼀⽅⾯是为了⽅便论述清楚 Agent 的关键点；另⼀⽅⾯是现实考量，代
码库（本质也是⽂件）也将逐渐成为上下⽂⼯程的⼀部分，代码库越简单上下⽂越清晰
（信息噪声越少）， Agent 则越智能。
Agent 框架之外， Agent 应⽤之内，上下⽂⼯程是智能的核⼼（短期 / 长期记忆、主动 / 被动
记忆、⽤户 Session 管理、动态 RAG 等等），也是 Agent 商业上应⽤的关键。框架提供基础
⼯具，上下⽂⼯程提供环境，搭配商业领域的 Skills ， Agent 就能发挥出巨⼤的潜⼒。
腾讯技术官⽅号。腾讯技术创新、前沿领域发布解读平台。
688 篇原创内容
腾讯技术⼯程
公众号
````

## PDF 第 19 页

[原页](RAW.pdf#page=19)

````text
阅读 1 . 9 万
留⾔
还没有留⾔，来写⾸评
写留⾔
````

## 采集与转写核验记录（非原文）

以下说明由本次核验添加；上方逐页文本保持文本层原样，图片与布局以PDF为准。

- PDF物理页 13,14：工具 schema 长字符串右侧实际裁切，完整项目与 import 未完整呈现；代码没有被运行
