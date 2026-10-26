# 2025必看系列：AI如何重新定义研究？万字长文讲透Deep Research

来源：[RAW.pdf](RAW.pdf)，capture-001。

这是PDF文本层按物理页码转写，不是AI总结。图片未嵌入；图内文字、截图、公式、表格及代码排版可能未提取或不可靠；源PDF中存在的右侧裁切不补写。实际复核范围详见META.json。

## PDF物理页 1

2025必看系列：      AI如何重新定义研究？万字⻓⽂讲透                  Deep
Research


原创 腾讯程序员    腾讯技术⼯程    2025年11⽉28⽇   01:36⼴东  3486⼈
















作者：  anthonyguo (郭沛)、 karolinaliu（刘恩婕）
  导语

如果AI的终极使命是拓展⼈类认知的边界，那么“研究”——这项系统性探索未知的核⼼活动，
⽆疑是其最重要的试⾦⽯。         2024年，AI  Agent技术迎来突破性进展，⼀个名为          Deep
Research（深度研究）  的⽅向正以前所未有的速度站上风⼝，成为推动“AI应⽤元年”的真正
引擎。 但热潮之下，我们更需要深度的思考：Deep Research 究竟是什么？它从何⽽来，⼜
将去往何处？其背后的技术架构有何精妙之处？我们⼜如何客观评价⼀个系统的优劣？

本篇近万字的深度剖析，将为你彻底理清Deep Research的“前世今⽣”，拆解其核⼼架构与⽅
法论，建⽴⼀套清晰的评测视⾓，并直⾔不讳地指出当前顶尖系统的优势与缺陷。这是⼀份为
你准备的   AI研究进化论地图，请坐好，我们马上发车！



  前言

⾃ 2023 年 AutoGPT、GPT-Engineer 等原型⼯程引爆“Agent”概念以来，⼤模型的应⽤落地从
“问答和摘要”迅速升级为“⾃治任务执⾏”。所谓 AI Agent，是可以在最⼩⼈⼯⼲预下完成「感
知 → 规划 → ⾏动 → 反馈」闭环的智能体，既能解析⾃然语⾔⽬标，⼜能调⽤搜索引擎、数
据库等外部⼯具。随着互联⽹等领域陆续跑通第⼀批端到端 PoC，企业级需求出现了三条明
显的技术主诉：

● 实时性：  Agent 必须随时接⼊最新数                                           据⽽不依赖百亿参数中 “冻结” 的旧知识；

● 可追溯性：  Agent 的每⼀步决策都需                                     要有可 audit 的依据，⽅便合规审计                                                与灰度调参；

● 稳定性：多轮规划链     + Tool 调⽤若全部依赖⼤模型长上下⽂，会让推理                                                                                                 结果不可控；

上述三点恰好暴露了“仅靠参数记忆”范式的软肋，指引着 AI Agent 向“知识增强、检索驱动、
成本可控   ”的新⽅向演进。

## PDF物理页 2

                  Deep Research Agent 的演变历程

步⼊ 2025 这⼀被誉为 “AI 应⽤元年” 的关键节点，OpenAI ，Google 和 Perplexity 等头部⼚
商相继推出了各⾃的 Deep Research 系统，以满⾜上述需求。⾯向复杂且多步骤的研究任
务，⽤户只需输⼊待解的问题，原本需要数⼩时甚⾄数天才能完成的深度分析，如今往往在⼏
分钟内即可交付，极⼤节省了时间与⼈⼒成本，真正把 “AI Agent × Deep Research” 推向规
模化落地的新拐点。

那么它究竟是如何做到像专家⼀样，对⼀个领域的问题进⾏分析和研究的？本⽂将带你：

● 快速拆解 Deep Research 的由来、通⽤框架以及各模块的制胜技巧；

● 了解 Deep Research 的相关评测⽅法、现有系统及其局限性；

● 最后带⼤家认识下   Dola —— 具备整          合⾮结构化公域数据 ✚ 结构化私域数据的数据助⼿；



 一、从  RAG走向深度研究

1.1 RAG: 开启动态知识的新纪元

尽管⼤语⾔模型（LLMs）在处理复杂任务⽅⾯展现出卓越的能⼒，但其内部知识存在明显的
边界性限制。  这些限制主要体现在三个⽅⾯    ：

1.知识的时效性问题，模型训练数据存在截⽌时间，⽆法获取最新信息；

2.专业领域知识的深度不⾜，在特定垂直领域可能缺乏⾜够的专业性；

3.容易产⽣"幻觉"现象，即⽣成看似合理但实际错误的信息；

这些局限性严重制约了⼤模型在实时性要求⾼和专业性要求强的场景中的有效应⽤。为了克服
这⼀挑战， 检索增强⽣成（   Retrieval-Augmented Generation, RAG）技术应运⽽⽣。

## PDF物理页 3

                       RAG 流程

RAG 通过检索相关的外部⽂档，为⼤模型提供额外的信息源，从⽽显著提升⽣成⽂本的时效
性和专业性。

然⽽，传统RAG⽅法存在⼀个根本性问题：⼤模型只是被动地运⽤检索得到的结果，缺乏更
为深⼊的推理能⼒。例如，当搜索得到的结果与查询不相关时，系统⽆法⾃主调整搜索关键词
重新获取信息源，也⽆法进⾏多轮迭代优化检索策略。

1.2 Deep Search: 主动探索的开                           端














                     Deep Research 流程



随着 LLMs 技术的蓬勃发展，LLMs 开始具备反思推理等智能体（agentic）能⼒，这标志着
搜索范式从原来的“被动检索”转为“主动探索”。基于此，研究⼈员提出了 Deep Search，开启
了模型主动探索的道路。

整个 Deep Search 流程如上图所⽰：⽤户输⼊相关问题后，系统会初步检索，并阅读检索的
结果，然后推理判断⽬前的检索结果是否⾜以很好的回答当前的问题，如果分析发现依然存在
信息缺⼝后触发⼆次检索，直⾄满⾜预设终⽌条件，最后⽣成答案。从上述流程可以看到，
Deep Search 最⼤的特点就是能⾃适应的在 Web 上主动进⾏多轮检索，以不断获取与任务⽬
标匹配的⾼质量信息，充分体现了从    “被动检索 ”到“主动探索”的变化。

1.3 Deep Research: 引领复杂推                     理的新范式

然⽽，Deep Search主要专注于搜索结果的优化，对于需要多步骤执⾏深度分析、证据整合和
结构化输出的复杂研究任务仍显不⾜。为此，Deep Research 在 Deep Search 的基础上进⼀
步发展，结合了主动探索和结构化分析框架的优势。

## PDF物理页 4

                      Deep Research 流程

从上图可以发现，Deep Research 继承了 Deep Search 的主动探索能⼒，且增加了任务规
划和报告⽣成模块。

1.任务规划：负责将复杂的问题进⾏拆解，⽣成多个对应的⼦问题，以⽀持不同分⽀的探索；

2.报告⽣成：将多源证据整合为连贯、可信的结构化输出，真正满⾜复杂研究任务的需求。

讲到这⾥是不是已经对 RAG 到 Deep Research 的发展历程有了初步了解了？下⾯我们再通过
⼀个例⼦来直观展⽰下    DR 与传统信息                检索⽅法的区别：



















信息检索⽅法对⽐：(左上) Query：在 2024 巴黎奥运期间，看完 100 ⽶决赛后，当晚赶去伦敦看⾳乐
 剧，最晚能坐哪趟 Eurostar？(左中) 传统的搜索⽅法：直接通过浏览器或 API 进⾏检索；(左下⻆)
RAG：将检索结果与⽣成式模型结合，以⾃然语⾔输出答案；(右侧) Deep Research：通过检索和显式
                    推理⽣成复杂的决策或分析。

1、传统搜索⼯具调⽤：难以理解⽤户意图，进⾏搜索后只回答了 100 ⽶决赛时间。这体现了
传统搜索⼯具调⽤依赖预定义的⼯作流，灵活性差的缺陷；

2、RAG：相⽐传统搜索，RAG ⼀次性搜索了多个关键词，取回若⼲⽚段后给予 LLMs 回答，
但由于缺乏深⼊的推理能⼒，只回答了       Eurostar 的末班车时间，依旧不是⽤户想要的答案；

3、Deep Research：先 “think”：显式列出求解任务的⼦⽬标，再 “search”：针对每个⼦⽬标
逐步检索、验证、更新假设，最后 “answer”：整合所有已验证信息并给出⾏动可⾏性判断和
⽅案。


      腾讯技术⼯程
      腾讯技术官⽅号。 腾讯技术创新、 前沿领域发 布解读平台。
      690篇原创内 容


 公众号

## PDF物理页 5

 二、 Deep Research 通用架构


















                    Deep Research 通⽤架构

下⾯我们将对   Deep Research 的⼯作流程进⾏介绍，让⼤家可以清晰的了解其原理。Deep
Research 架构主要由四个模块组成，分别是   “规划”、“问题演化”、“⽹页探索” 和 “报告⽣
成”，下⾯将对四个模块进⾏功能介绍                                     ：

● 规划：此模块将⽤户问题转换为⼀系列可执⾏的⼦⽬标或⼦步骤，以指导后续的推理和检
索；

● 问题演化：基于规划部分给定的⼦⽬标，将其转换为⼀组符合⽬标需求的查询关键字；

● ⽹页探索：基于“问题转换”的关键字，此模块⾃驱动地进⾏迭代式的搜索以获取相关和可信
的信息；

● 报告⽣成：基于检索到的与研究问题相关的信息，本模块对其进⾏汇总并⽣成⼀篇连贯且可
靠的报告；

2.1 Planning：规划模块

2.1.1 模块定位

Planning 模块是 Deep Research 流程的第⼀阶段，其核⼼作⽤包括：

1.将⽤户意图转化为可执⾏计划  ：将⾼层次研究问题分解为结构化⼦⽬标序列；

2.提供结构化路线图 ：⽣成明确的、任务感知的执⾏路线图；

3.克服被动检索局限 ：实现主动规划和系统化推理；

## PDF物理页 6

                     Planning 框架

在上图的框架中，Planning 模块通常包含三个核⼼组件：任务规划器（task planner）、计划
执⾏器（plan executor）以及环境（environment）具体⽽⾔：

● 任务规划器：LLMs 负责⽣成解决⽬标任务的完整计划，该计划可以采⽤多种形式呈现，例
如⽤⾃然语⾔描述的⼀系列动作序列或⽤编程语⾔编写的可执⾏程序，为了应对长流程任务，
通常还会结合记忆机制来存储与检索计划；

● 计划执⾏器：负责按照计划执⾏各项动作：对于⽂本类任务，可由 LLMs 等模型实现，对于
编程类任务，则可利⽤代码解释器等⼯具来完成；

● 环境：指计划执⾏器执⾏动作的场所，例如基于⼤模型内部知识以及外部知识（知识图谱
等）来进⾏规划，环境会以⾃然语⾔或其他多模态信号的形式向任务规划器反馈执⾏结果；

总的来说，在解决复杂任务时，任务规划器⾸先需要充分理解任务⽬标，并基于 LLMs 的推理
能⼒⽣成合理的计划。随后，计划执⾏器按照计划在环境中执⾏相应动作，环境再将执⾏的反
馈返回给任务规划器。任务规划器可以结合这些反馈，对最初的计划进⾏调整与优化，并迭代
地重复上述流程，以获得更优的任务解决⽅案。

2.1.2 代表性⽅法

















更多关于 Planning 的⽅法还可以参考 Agent ：Understanding the planning of LLM agents: A
survey

2.1.3 应⽤⽅式

## PDF物理页 7

在现实应⽤中，可以将为了更好地响应⽤户需求，Planning 动态⼯作流通常采⽤以下三种⼯
程⼿段来进⼀步优化规划策略：

● 仅规划 (Planning-Only)：直接根据⽤户初始提⽰⽣成任务计划，不进⾏意图澄清，⼤多数
DR 智能体（如 Grok、Manus）采⽤     此策略；

● 意图到规划 (Intent-to-Planning)：在规划前通过提问主动澄清⽤户意图，再⽣成定制化计
划，OpenAI DR 是典型代表；

● 统⼀意图规划 (Uniﬁed Intent-Planning)：先⽣成初步计划，然后与⽤户交互以确认或修改该
计划，Gemini DR 采⽤此策略，有效结合了⾃主规划和⽤户引导；

2.1.4 总结

Planning 模块标志着 AI 从被动提⽰到主动规划的范式转变。通过两⼤⽅法论——结构化世界
知识和可学习过程，以及三种额外⼯程⼿段来优化该模块，为后续的 Question Developing、
Web Exploration 和 Report Generation 阶段奠定了坚实基础，是实现端到端⾃主研究的关键
环节。

2.2 Question Developing：问题     演化模块

2.2.1 模块定位

要完成多步推理、信息综合等深度研究任务，仅依赖⼀次性的静态查询往往不够，系统必须动
态地产⽣更加针对性、更具上下⽂、或经过拆分的查询，以便从检索模块或互联⽹中提取有价
值的证据，此过程便是    Question Developing。

Question Developing 模块是 Deep Research 流程的关键转换阶段，其核⼼作⽤包括：

1.将结构化计划转化为可执⾏查询   ：将规划阶段⽣成的⼦⽬标转换为具体的搜索查询序列；

2.实现上下⽂感知的查询⽣成  ：根据累积证据和任务演变动态调整查询策略；

3.平衡查询的特异性与覆盖范围   ：确保查询既精确⼜全⾯，避免信息遗漏；

4.指导后续检索过程 ：为⽹络探索阶段提供⾼质量的检索指令；

## PDF物理页 8

                      M  anuSearch 架构图

以 ManuSearch 为例来进⾏介绍，采⽤基于智能体、模块化的体系结构，通过三类协作
Agent 完成 Web 级复杂推理任务：

● 规划智能体（Solution Planning Agent）：依托 LLM，对⽤户查询进⾏解析，制定整体策略
（即⼀系列⼦问题或步骤）                         ，并在每⼀步决定需要检索的信息；

● 互联⽹搜索智能体（Internet Search Agent）：根据规划器的请求执⾏⽹络搜索，从开放互
联⽹收集相关证据；

● ⽹页阅读智能体（Webpage Reading Agent）：负责阅读检索到的⽹页，提取回答问题所需
的关键信息。

此处我们重点关注 Solution Planning Agent，从图中可以观察到，基于⽤户 Query 和中间执
⾏结果，该阶段分别⽣成了对应的待执⾏步骤，后续便进⼊了 Extract Problems 阶段，该阶
段便是基于执⾏步骤来对问题进⾏转换，转变为后续可执⾏搜索的问题，且该转换内容随着证
据的积累和任务演变动态调整。

2.2.2 代表性⽅法

## PDF物理页 9

2.2.3 总结

Question Developing 模块是 Deep Research Agent 的核⼼组件，负责将⼦⽬标转化为⼀系列
具体的检索查询。这些查询既要准确反映⼦⽬标的意图，⼜需具有⾜够的⼴度，以便从外部信
息源获取全⾯且相关的内容。它本质上是 Agent 探索信息空间的起点，直接影响后续检索与
答案⽣成的质量。 ⽬前主要通过基于奖励和监督驱动的⽅式来进⾏优化，旨在让 Agent 更“聪
明地提问 ”，以满⾜复杂的研究需求。

2.3 Web Exploration：⽹页探索                     模块

2.3.1 模块定位

从科学发现、⽂献综述到事实核查等各类专家级调研流程，都⾼度依赖于在浩瀚且异构的互联
⽹信息中检索精确、具备上下⽂且可信的证据。然⽽，由于相关资料零散地分布在⽆数⽹页之
中，如何让 Agent 准确定位并提取最有价值的内容，便是 Web Exploration 模块需要完成的
任务。

Web Exploration 模块作为 Deep Research 流程的第三阶段，其核⼼作⽤                                包括：

1.信息检索与获取  ：从在线资源中⾼效检索相关且可信的信息；

2.动态导航能⼒ ：在复杂⽹络环境中进⾏⾃主导航和交互；

3.多模态内容处理  ：处理⽂本、图像、结构化数据等多种内容形式；

4.质量过滤与验证  ：确保检索内容的相关性和可信度；

当前的  Web Exploration 模块分为两种                           形式：

● 基于 API 的搜索：基于 API 的搜索引擎通过与结构化数据源（如搜索引擎 API 或科学数据
库 API）交互，实现对结构化信息的⾼                                                                      效检索；

● 基于浏览器的搜索：通过模拟⼈类的⽹页交互⾏为，能够实时提取动态或⾮结构化内容，从
⽽提升外部知识的全⾯性；









                       基于 API 检索流程

基于 API 的搜索⽅式，因其速度快、效率⾼、结构化好且具备可扩展性，成为深度研究智能
体获取外部知识的常⽤⽅式，所需时间和计算成本相对较低；例如，Gemini DR 通过多源接
⼝——尤以 Google Search API 和 arXiv API 为代表——在数百到上千个⽹页中进⾏⼤规模检
索，⼤幅扩展了信息覆盖范围。尽管这些 API 驱动的⽅法在结构化、⾼吞吐的数据获取⽅⾯
表现优异，但⾯对深层次的客户端 JavaScript 渲染内容、交互组件或⾝份验证壁垒时往往捉
襟见肘，促使研究者开发能够全⾯抓取和分析动态及⾮结构化信息的浏览器级检索机制；

## PDF物理页 10

                     基于浏览器检索流程

浏览器级检索通过模拟⼈类的浏览操作，为深度研究智能体提供了动态、灵活且可交互的多模
态与⾮结构化⽹页访问能⼒。例如，Manus AI 的浏览智能体在每次研究会话中都会启⽤隔离
的 Chromium 实例，编程式地打开新标签、发起搜索、点击结果链接、滚动页⾯（直⾄达到
内容阈值）、必要时填写表单、执⾏页⾯内 JavaScript 以展开懒加载区块，并下载⽂件或 PDF
以供本地分析。虽然浏览器级检索能捕获 API ⽆法触及的实时和深层内容，但其延迟、资源
消耗更⾼，且需处理页⾯差异和错误。

2.3.2 代表性⽅法















2.3.3 总结

● Web Exploration 模块是深度研究系统的信息获取引擎，通过两⼤架构范式——Web Agent
系统和 API 检索系统——实现了从简          单检索到复杂交互的全⽅位⽹络探索能⼒；

● 未来的 Web 探索将依赖混合式架构，把上述两种⽅法的长处整合到同⼀系统中，以系统化
⽅式解决核⼼挑战。⾼级系统需内置专门模块，⽤于证据抽取、正确性验证和内容质量评估，
先实现快速的初步检索，再进⾏深层交互分析；

● 多模态处理技术与实时验证框架的突破也⾄关重要，可确保系统跟上 Web ⽣态的快速演
变。通过为不同模块建⽴完善的分类框架，并系统性地攻克这些技术难题，Web 探索将成长
为深度研究的坚实基础，提供更精准且更可靠的证据检索能⼒。

2.4 Report Generation：报告⽣成模块

2.4.1 模块定位

在深度研究场景中，⽂本⽣成的⽬标已超越传统的问答任务，⽽是要产出⼀份全⾯、具有分析
性的报告，此过程就是“报告⽣成（”   report generation），旨在将从⽹络检索到的零散信息整合
为结构连贯、逻辑清晰、且忠于底层证据的报告。

Report Generation 模块是 Deep Research 流程的最终阶段，其核⼼作⽤包                                                                括：

1.信息整合与综合 ：将零散的检索证据转化为结构化、连贯的分析报告；

## PDF物理页 11

2.知识合成与推理：从多源信息中提取洞察，⽣成新的知识和结论；

3.结构化输出：按照特定格式和逻辑组织内容，确保报告的可读性和专业性；

4.事实性保障：确保⽣成内容的准确性、可信度和可追溯性；

同样可以将该模块的⽅法进⾏分类：























                 LongWriter 章节式合成流程

1. 结构控制：

● 旨在⽣成在整体结构上连贯且⼀致的长篇⽂本，这类长篇输出往往包含多个章节，因⽽必须
兼顾有效的整体规划、主题对齐以及版式   /层级结构的遵循；

● 此块研究主要从三个维度来解决这⼀问题：基于规划的⽣成，约束引导的⽣成以及结构感知
的对齐；

● 以基于规划的⽣成为例，如上图所⽰，LongWriter 通过将超长的⽣成任务拆分为多个⼦任
务，并对每个⼦任务⽣成对应的长⽂本内容，将此思路应⽤于构建数据，经过此数据训练后的
LLMs 能够⽣成超过 20,000 词、且连        贯⼀致的长⽂本；


















                    BRIDGE 整体流程

2. 事实完整性：

● 旨在确保⽣成的报告忠实于检索到的证据，通常通过证据对齐机制或⽣成后的验证环节来实
现；

## PDF物理页 12

● 此块研究同样从三个维度来解决这⼀问题：忠实建模、冲突解析与事实评估；

● 以忠实建模为例，其侧重于确保⽣成⽂本与经过验证且具有上下⽂相关性的证据保持⼀致。
如上图所⽰，BRIDGE 在检索与⽣成之间插⼊了验证层，使 LLMs 能够动态决策并输出综合应
答策略。BRIDGE ⾸先利⽤⼀种⾃适应加权机制——soft bias——来指导知识收集；随后通过
“最⼤软偏置决策树”评估内外部知识的可靠性，并在“信任内部知识 / 信任外部知识 / 拒绝回
答”三种策略中选取最优⽅案；

2.4.2 代表性⽅法



















2.4.3 总结

Report Generation 模块是深度研究系统的知识合成引擎，任务是将各⼦问题所得的零散证据
转化为结构化且可信的完整报告。为了确保报告质量，现有⽅法主要通过结构控制和事实完整
性⽅法实现了从零散信息到结构化知识的转化。


      腾讯技术⼯程
      腾讯技术官⽅号。 腾讯技术创新、 前沿领域发 布解读平台。
      690篇原创内 容


 公众号


 三、如何评测     Deep Research

如何验证 Deep Research 系统的效果也是⼀个重要的研究课题，这驱动着 Deep Research 的
不断优化改进。当前不少⼯作设计了⼀些 benchmark 来评估上述四个核⼼技术模块的性能，
我们可以将这些   benchmark 根据其任务范围⼤致分为两类：

1. ⾯向搜索 (Search) 的 benchmark ：主     要关注涉及⽹络探索和问题开发的信息检索任务，
  通常在交互式或特定语⾔的浏览场景中进⾏（缺少最终结果的评估，有⼀定局限性）                                                                                             ；

2. ⾯向研究 (Research) 的 benchmark：涵盖四个模块的内容，充分评估 Agent 流程的整体
  性能；

下⾯我们将通过表格的形式来对上述两种类型进⾏总结。

## PDF物理页 13

3.1 ⾯向 Search 的评测




















3.2 ⾯向 Research 的评测









 四、主流   Deep Research 系统及缺陷分析

4.1 OpenAI

OpenAI 于 2025 年 2 ⽉发布了其深度研究能⼒，采⽤单智能体框架。当系统接收到研究查询
后，会先进⾏简短的交互式澄清步骤，以精准界定⽤户意图和研究⽬标。随后，智能体将⾃主
制定并执⾏⼀套复杂的多步研究策略，涵盖多模态信息检索、⽹页浏览，以及通过浏览器⼯具
进⾏数据分析与可视化等计算任务。在技术层⾯，该⽅案带来三项重要创新：

1.动态⾃适应的迭代研究⼯作流：在任务执⾏过程中可不断优化⾃⾝策略；

2.增强的上下⽂记忆与强⼤的多模态处理能⼒：能够⾼效整合多元信息来源；

3.完整的⼯具链整合：将⽹页浏览功能与内置编程⼯具相结合，输出结构化且附带精准引⽤的
权威报告；

案例展⽰（查看完整案例请点击：   链接）

## PDF物理页 14

4.2 Qwen

阿⾥巴巴推出的 Qwen Deep Research 系统，采⽤统⼀智能体框架，并通过强化学习优化的
任务调度机制，提升了⾃主规划与⾃适应执⾏能⼒，可⾼效完成复杂的研究⼯作流。其关键技
术亮点包括：

1.动态研究蓝图绘制：⽀持交互式计划迭代与细化，确保研究路径随需求实时调整； 2.并⾏化
任务编排：可同时进⾏信息检索、证据验证与综合⽣成，从⽽加速研究流程并增强结果⼀致性

## PDF物理页 15

与可靠性。

案例展⽰：



































除前⽂提到的先锋级深度研究服务外，微软、字节跳动、Jina AI、H2O、智谱 AI 等企业也相
继推出了⾃家的 DR 平台。这些解决⽅案的涌现迅速在全球范围内激起了⼴泛关注，既彰显了
DR 技术的吸引⼒，也折射出其巨⼤的                                                                      市场潜⼒。

4.3 现有系统缺陷分析

尽管 DR 领域已取得可观进展，但从上述的案例展⽰中其实我们可以发现，现有的 DR 系统存
在着以下缺陷：

数据源单⼀性问题

当前的 Deep Research 在很⼤程度上依赖于公开可⽤的互联⽹数据进⾏信息检索和知识获
取。尽管互联⽹提供了海量信息，但这种单⼀的数据来源存在显著局限性，尤其是在需要特定
领域知识或企业内部信息时。其中企业私有数据访问障碍是最为突出的问题；

数据质量问题

依赖互联⽹数据也带来了固有的数据质量挑战，这直接影响 Deep Research 输出报告的准确
性和可靠性。⼤模型幻觉问题是 Deep Research ⾯临的⼀⼤挑战。当 Deep Research 在互联
⽹上检索到不准确、⽭盾或误导性的信息时，LLMs 可能会基于这些信息产⽣幻觉，从⽽导致
研究报告中出现不实内容，严重损害研究结果的可靠性。

## PDF物理页 16

针对单⼀数据源问题，以   “分析  2025 年美联储降息对美股的影响  ”为例——前⽂提到的
OpenAI 与 Qwen Deep Research 均主要依赖互联⽹上的⾮结构化资讯来完成综合判断，却缺
乏对结构化数据的定量⽀撑（如 2025 年实时美股价格⾛势）。为了突破这⼀“单⼀数据源”局
限、获得更深⼊的洞察，Dola 团队提出并实践了“⾮结构化公域数据 ✚ 结构化私域数据”的融
合⽅案：通过将SQL ⼯具获取结构化资产与搜索获取的外部公开信息有机整合，为专业、可
靠的分析／研究报告提供坚实保障。接下来，让我们看看      Dola 是如何做到的吧！



 五、 Dola 介绍与方案设计

5.1Dola 是谁❓







Dola —— 是腾讯PCG⼤数据平台部的新⼀代数据分析AI助⼿，是⼀款基于Agentic AI能⼒开
发的数据分析助⼿：⽤户只需要引⼊个⼈的数据表，就能得到⼀枚专属的       AI分析师。






















它不仅能够完成⽇常的取数、跑数等基础任务，还能⾃主规划并执⾏复杂场景的数据分析，例
如异动归因、画像对⽐分析、股票基⾦回测、房价预测等。Dola可以⾃⾏编写SQL、纠正SQL
错误、执⾏查询、使⽤Python进⾏数据处理与可视化，并最终⽣成⼀份完整的分析报告。全
程⽆需编写⼀⾏代码，只需通过⾃然语⾔对话，你就能拥有⼀个全⾃动⼯作的“数据⼩⿊⼯”。
⽬前已经能⾃⼰⾃主完成数据   /产运同          学的部分⼯作。

这⾥以1个股票回测的例⼦看看  dola的效果：

## PDF物理页 17

接下来让我们看下   dola是如何解决deep Research缺陷的

5.2 Dola 如何解决 Deep Research 缺陷❓

解决⽬标

Dola 的产品定位是“⾯向数据分析场景的智能助⼿”。这⼀定位决定了它在信息获取与推理环
节上的两条核⼼策略：

1、有条件地调⽤   Web 探索模块

a)时效性与相关性优先：当⽤户提出的是“近 24 ⼩时股价异动原因”“本周新出的监管⽂件对某
⾏业的影响”这类依赖实时动态的查询时，Dola 会主动触发 Web 探索模块，抓取最新⽹页、
公告、新闻源等实时数据，为后续分析提供及时补充；

b)噪声控制：如果⽤户的问题⾼度依赖内部数据仓库或历史沉淀（例如“2023Q4 在XX业务上
的⾼价值⽤户画像”“过去三年各渠道的 GMV 增⻓率拆解”），Dola 会判定 Web 结果的增量价
值低且容易引⼊噪声，因⽽不会调⽤ Web 探索。这样既保证了答案的聚焦度，也避免了⽆关
信息稀释结论；

2、以知识库为主、  Web 为辅的多源融合

a) 层次化信息结构：Dola 把企业内部的数仓、报表、API    结果等“结构化知识”视为⼀级数据
源；Web 抓取的内容归为⼆级数据源。回答问题时先⾃上⽽下检索，保障内部权威信息优
先；

b) 可信度加权：当相同指标在知识库与⽹页中均有展⽰时，Dola 会⾃动为知识库赋予更⾼置
信权重， Web 结果则作为补充验证或细节说明；若⼆者冲突，则默认内部                                                                                                                                 数据为准；

c)结果融合策略：对于“宏观+微观”或“定量+定性”混合型分析，例如“近⼀年渠道 A 与渠道 B
的市场份额变化，并结合最新合规政策给出建议”，Dola 会先从数仓拿到⽉度或季度等份额做
数据分析，再调⽤ Web 模块抓取政策解读与专家观点，并利⽤⼤模型推理能⼒将两部分内容
进⾏串联，最终输出带有数据图表与要点摘要的综合报告。

通过以上两条策略，   Dola 能做到：

## PDF物理页 18

● 快速响应实时、突发性问题，⽽不会因     “⽆关联⽹”增加时延；

● 在深度业务分析场景中保持结论的专业度与⼀致性；

● 把外部公开信息转化为洞察补丁，⽽不是⼲扰源；

● 最终为⽤户提供 “既准⼜新、既深且                                     稳”的数据分析决策⽀持；

5.3 案例分析：美联储降息对美股趋势影响

针对第四节提到的案例，我们引⼊了美股市场的股票数据到数据库中，以此作为本次案例的知
识库内容。针对问题   “分析下2025年美联储降息，对美股的影响如何”      ，Dola 先规划后续步
骤：














由于美联储降息属于实时新闻，模型并⽆相关知识，为此调⽤了搜索获取最新降息⽇期，并进
⾏简单总结：






















基于获取的降息⽇期，通过执⾏⼀系列      SQL 获取部分代表性美股降息前后                             的指标情况：

## PDF物理页 19

之后同样顺畅衔接   Python 🔧进⾏数据加载，下钻分析和可视化：

数据加载与下钻分析：























分析结果可视化：

## PDF物理页 20

最终结合两种数据源内容，形成总结报告：

















...... (此处省略总结内容)

## PDF物理页 21

  六、文章总结

本篇主要介绍了 Deep Research 的相关概念（从 RAG 到 Deep Research 的技术演变）、通⽤
架构（四⼤核⼼ 模 块：planning                      、   Question   Developing    、   Web   Exploration    和   Report
Generation）、现有评测 Benchmark 以及主流系统，最后我们针对当前 Deep Research 系统
单⼀数据源的局限性，介绍了 Dola 团队的⽅案 —— 充分结合结构化私域和⾮结构化公域数
据，让分析报告更可靠。



  参考文献


[1] Deep Research: A Survey of Autonomous Research Agents


[2] A Comprehensive Survey of Deep Research: Systems, Methodologies, and Applications


[3] DEEP RESEARCH AGENTS: A SYSTEMATIC EXAMINATION AND ROADMAP


[4] Is Your LLM Secretly a World Model of the Internet? Model-Based Planning for Web Agents


[5] Agent Planning with World Knowledge Model


[6] Thought of Search: Planning with Language Models Through The Lens of Efficiency


[7] AGENTSQUARE: AUTOMATIC LLM AGENT SEARCH IN MODULAR DESIGN SPACE


[8] InSTA: Towards Internet-Scale Training For Agents


[9] WEPO: WEB ELEMENT PREFERENCE OPTIMIZATION FOR LLM-BASED WEB NAVIGATION


[10] DeepResearcher: Scaling Deep Research via Reinforcement Learning in Real-world Environments


[11] ZEROSEARCH: Incentivize the Search Capability of LLMs without Searching


[12] Scent of Knowledge: Optimizing Search-Enhanced Reasoning with Information Foraging

## PDF物理页 22

[13] Reinforced Internal-External Knowledge Synergistic Reasoning for Efficient Adaptive Search Agent


[14] ManuSearch: Democratizing Deep Search in Large Language Models with a Transparent and Open Multi-Agent

Framework


[15] Process vs. Outcome Reward: Which is Better for Agentic RAG Reinforcement Learning


[16] WebGPT: Browser-assisted question-answering with human feedback


[17] MM-REACT : Prompting ChatGPT for Multimodal Reasoning and Action


[18] Introducing deep research | OpenAI


[19] Perplexity DeepResearch


[20] Agent Laboratory: Using LLM Agents as Research Assistants


[21] LongEval: A Comprehensive Analysis of Long-Text Generation Through a Plan-based Paradigm


[22] LONGWRITER: UNLEASHING 10,000+ WORD GENERATION FROM LONG CONTEXT LLMS


[23] WebThinker: Empowering Large Reasoning Models with Deep Research Capability


[24] LONG2RAG: Evaluating Long-Context & Long-Form Retrieval-Augmented Generation with Key Point Recall


[25] After Retrieval, Before Generation: Enhancing the Trustworthiness of Large Language Models in RAG


[26] FaithfulRAG: Fact-Level Conflict Modeling for Context-Faithful Retrieval-Augmented Generation


[27] Mind2Web 2: Evaluating Agentic Search with Agent-as-a-Judge


[28] Browsecomp: A simple yet challenging benchmark for browsing agents


[29] Browsecomp-zh: Benchmarking web browsing ability of large language models in chinese


[30] Gaia: a benchmark for general ai assistants


[31] Humanity’s last exam


[32] Webarena: A realistic web environment for building autonomous agents


[33] MedBrowseComp: Benchmarking Medical Deep Research and Computer Use


[34] Gpqa: A graduate-level google-proof q&a benchmark


[35] InfoDeepSeek: Benchmarking Agentic Information Seeking for Retrieval-Augmented Generation


[36] DeepResearch Bench: A Comprehensive Benchmark for Deep Research Agents


[37] Deepresearchgym: A free, transparent, and reproducible evaluation sandbox for deep research


[38] Understanding the planning of LLM agents: A survey

## PDF物理页 23

       腾讯技术⼯程
       腾讯技术官⽅号。 腾讯技术创新、 前沿领域发 布解读平台。
       690篇原创内 容


  公众号


















       腾讯技术⼯程
       腾讯技术官⽅号。 腾讯技术创新、 前沿领域发 布解读平台。
       690篇原创内 容


  公众号








阅读 1.7万




留⾔

## PDF物理页 24

写留⾔





                         还没有 留⾔，来 写⾸评
