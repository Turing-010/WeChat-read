# 万级实时推理的商品领域Agent实践思考和总结：PDF文本转写

> 这是原始PDF文本层转写，不是学习摘要。页码为PDF物理页序；图表、代码版面和图片文字不能完整表达在此文本层。已查看图像的内容和质量问题见AI学习笔记及META.json。

[原文PDF](RAW.pdf) · [AI学习笔记](AI_商品领域万级实时推理Agent.md) · [处理与质量记录](META.json)

## PDF 第1页

[查看原页](RAW.pdf#page=1)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
万级
原创
实时推理的商品领域Agent实
践思考和总结
商品中心技术团队 2026年5月25日 01:16 浙江
大淘宝技术 55人
过去几年商品域为应对AI化挑战，构建了"事件驱动的Functi
on-Centric Agent架构"。
该架构采用两层设计：上层为业务场景workflow编排层，下层为统一能力供给层，通过
AIFuncti
on标准化封装
工具和领域知
系
识。
统整合了显性事实、
关联情景和隐性经验三类
商品知
识库，实现了在离线业务流程统一，并基于商品事务事件
已在商品属性、卖点等核心场景落地，覆盖亿级商品，显著提升信息完整性和搜
率，新需求开
发
周期缩短至1周/人，为商品智能化从"单点提效"迈向"系
实现高效实时推理。目前
索转化
统自治"奠定基
础。
引言
随着大语言模型的兴起，商品域在商品理解业务中引入大模型能力，对商品卖点、规格等核心
链路进
行
升级改造。早期沿用T
+
1离线批处理的生产思路，已在多个场景取得了较好的前台效
果。
在这个过程中我们在不
断思考几个问题：
（1）AI化是未来很长一段时间的主线，商品域拥有最全
的品类和商品供给，工程侧应该储备什
么样的技术基建能力，能够立足
当下解决业务实际问题，并面向未来持续演进？仅在离线链路
跑通几个案例是远远不够的，数据资
产和能力的复用必须作为长
期目标来对待。
（2）AI化这一抽象命题在商品域如何拆解为可落地、可演进的技术路线？
（3）当前工程使用AI更多的是离线链路，且商品模型各异，是否从离线推理走向实时推理？
若到SKU粒度是否能够支撑？当前商品的数万级
的写入
变更， DB上数据
的
变更峰值至少为
数十万，是否有有
效的方
案能解决推理成本问题？大模型生产的数据怎
行
么评价？
（4）在业务上，SKU化的背景和趋势，已经提了这么多年（据材料记载SKU化从2015年左右
就有
陆续提出），能不能通过agent的思路在商品领域有更完整的解决
方
案？
```

## PDF 第2页

[查看原页](RAW.pdf#page=2)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
为什么是商品Agent？
在 2025 年初的大模型工程实
践中，业界已探索出多种将大模型能力落地的路径，包括：
Prompt Engineering（提示工程）：适用于简单、静态任务，但难以应对复杂逻辑、
多
步骤决策或与外部系
统交互；
RAG（检索增强生成）：有
互，缺乏主动规划与执
效解决知
识时效性与幻觉问题，但本质仍是“问答式”单
轮交
能力；
行
Fine-tuning（微调）：适合特定领域高精度任务，但成本高
且无法动态调用工具；
、迭代慢、泛化能力受限，
MaaS（Model-as-a-Service）：提供标准化 API，但将业务逻辑与模型强耦合，难以
支撑端到端闭环；
Functi
on Calling / Tool Use：允许模型调用预定义函数，是 Agent 的关键组
本身不包含状态管理、
目标分解或长
期记忆机制
。
件，但
这些范式在各自场景中仍有价值，但面对商品域这类高复杂度、强标准化、需持续演进的业务
系
统，它们均存在“能力碎片化”与“工程不可持续”的瓶颈。例如，仅靠 RAG 无法自动完成
“采集小红书站外知
识 → 调用统计算法策略 → 分析属性在当前类目下消费者的提及率 → 生成
决策属性建议和理由 → 提交审核”这一多跳流程；仅靠微调无法适应每日新增的品类规则或平
台政策
变化。
而 Agent 正是在这些基础能力之上构建的更高阶抽象：
它内嵌
了 Functi
on Calling，实现与现有系
统（如商品中心IC、类目中心本地数据包、
订单离线数据资
产ODPS）的安全集成；
它天然融
合 RAG 机制，通过向量记忆或知
识库检索获取上下文相关
事实（如类目属性的
定义）；
它可结合微调模型作为子能力，但整体架构保持松耦合（如算法的专用商品图片主体识别
模型、
算法专用商品图片提取属性模型）；
它超越 Prompt Engineering 的静态交互，具备目标驱动的动态推理与回溯能力。
更重要的是，2024–2025 年大模型原生支持 Agent 能力的技术拐点已经到来：
主 流大模 型 已原生支 持
ReAct、Plan-and-Execute、Self-Reflecti
on 等 推 理 框
架；
开源生态（如 LangChain、LlamaIndex
、AutoGen、CrewAI、OpenDevin）提供了成
熟的 Agent 编排
、记忆管理、工具注册与多智能体协作基础设施；
工程可观测性工具开始支持 Agent
行
为追踪与评估，使调试与治理成为可能。
因此，选
择 Agent 并非否定其他范式，而是以 Agent 为“操作系
级
统
”容器，将 Prompt、
RAG、Functi
on Calling、Fine-tuned 模型等能力有机整合为可工程化交付的智能单元。
```

## PDF 第3页

[查看原页](RAW.pdf#page=3)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
它既继承了已有技术的成果，又解决了其在复杂业务场景中的
组合性、
状态性和可持续性短
板。
商品域结合Agent这一新的技术趋势，我们认为搭建商品领域Agent是实现商品智能化从“单点
提效”迈向“系
统自治”的关键跃迁，不仅是技术架构的升级，更是对商品数据生产与消费范式
的重构，也正是工程侧在 2025 年坚定选
择 Agent 作为 AI 化主路径的根本原因。因此，过
去一个季度，商品中心围绕“商品Agent”开
展初步建设，探索将大模型能力以可控、可集成的
方式
入商品生命周期链路。重点围绕搜
索/详情参数&摘要的智能化建设，支持更清晰、一
致、可比
的商品信息呈现，从而辅助消费者更高效地获取
关键决策信息。
嵌
商品Agent架构建设
落地商品 Agent 这类面向具体业务领域的 AI Agent时，远不止“接入大模型 + 写 Prompt”
那么简单——真正实现其可用、可靠、可提效、可运维，需要系
统性地完成一系列工程化工作
▐ 框架选型
2025年被称为Agent元年，集团内外“涌现”了非常多的智能体框架，涵盖大模型Agent的方方
面面，包含workflow编排
、工具集成（MCP）、memory管理等，更有
CrewAI、MetaGPT
这样的多Agent解决
方
案。通过广泛评估和调研，我们最终决定选
择轻度“耦合”spring-ai-
alibaba来构建商品域Agent应用。毕竟在集团成熟的Java生态下，新的技术栈势必带来更多
的额外复杂度，可维护性差并且与现有系
统的集成难度显著升高。但未来也会向多应用类似微
服务的架构演进，引入开源社区丰
富的Agent组
性验证等。附上在调研阶段，对一些相关框架病结合商品特性做一个的简单
件如deepeval做评测、deepresearch做事实
对比小结：
```

## PDF 第4页

[查看原页](RAW.pdf#page=4)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
▐ 架构设计
架构设计主要围绕以下几个命题来进
：
行
（1）面对具象的各异的前台业务场景，需要重点建设哪些组
件来降
低新场景的开
发成本。
（2）商品领域知
识如何融
入大模型调用流程？
（3）要实现成本的最优，我们认为需实时和离线
结合使用，那如何设计workflow及其调度 实
现在离线
处理逻辑一致？
（4）是否能走向实时推理？
结 合大模 型 agent的几 个核心（ 抽 象 ） 要 素 ， 我 们 认 为Agent的应用 架 构应 该足 够 简单和灵
活，应采用类似大数据处理引擎的视角来看待Agent架构。因此我们将商品 Agent 抽象为两
层结构：上层是面向业务场景的 workflow 编排层，下层是统一的能力供给层，两层之间通过
抽象的AIFuncti
on接口来交互。
```

## PDF 第5页

[查看原页](RAW.pdf#page=5)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
我们希望底层通过 AIFuncti
on
对各类工具和领域知
识进
行
标准化封装，向上提供结构清晰、
语义明确、调用稳定的函数接口，从而支撑上层灵活、
高效地构建智能流程。为此也开
发
了轻
量的 aiagentsdk ， 提供一 组 简 洁 易用 的 注 解 ， 如：@AIWorkflow 、
@AIActi
on 、
@AIFuncti
on、
@AIParameter、
下，所有functi
on可轻易转换成一组
@AIResult、
@AIResultField等 。在注 解 和切面 的增强
高质量的mcp工具，供问答型agent自由调用。
AiParameter
AIActionDefine
Bind
+code(): String
+desc(): String
+value(): String
«annotates»
«annotates params»
AIAction
1
AIReduceAction
Annotations (注解层)
AIWorkFlowDefine
AiFunction
+name(): String
+description(): String
+tags(): String[]
+expose(): boolean
+author(): String
+code(): String
+desc(): String
+expose(): boolean
+enableSession(): boolean
+aiReq(): Class<?>
+aiResp(): Class<?>
+defaultSceneId(): long
Action Hierarchy (Action层级)
+name(): String
+description(): String
+type(): String
+required(): boolean
+defaultValue(): String
+enumValues(): String[]
AiResult
+description(): String
+fields(): AiResultField[]
wraps
AI Agent SDK 核⼼类图
Runtime Engine (运
⾏
时引擎层)
«static»
AIProcessEngine
+start(code: String, req: R, resp: S): void
+start(code: String, req: R, resp: S, contextParams: Map): void
+getBpm(code: String): AIWorkflow
-runActions(req, allActions, contextParams): ActionResult
-runAction(req, contextParams, actionDescriptor): ActionResult
-runLoopAction(...): List<ActionResult>
-runMapAction(...): Map<String, ActionResult>
-convertToMap(req): Map<String, Object>
-resolve(actionParams, classParams, param, req): Object
«Singleton»
AIWorkFlowLoader
-workFlowCache: Map<String, AIWorkflow>
uses
+init(applicationContext: ApplicationContext): void
+load(code: String): AIWorkflow
+get(): AIWorkFlowLoader
-buildCode(workflow, annotation): String
loads & caches
produces
executes
ActionResult
ActionDescriptor
-actionParams: Map<String, Object>
-terminated: boolean
-action: AIAction
+getActionName(): String
+getRunMethod(): Method
+getIterMethod(): Method
+getMapMethod(): Method
0..
*
+bind(): ActionResult
+bind(k1: String, v1: Object, ...): ActionResult
+bind(bindParams: Map): ActionResult
+terminate(): ActionResult
+get<T>(key: String): T
+isTerminated(): boolean
«scanned to»
Scanner & Executor (扫描器与执
⾏器层)
«@Component»
AIWorkflowScanner
«InitializingBean»
AiFunctionScanner
-aiFunctionScanner: AiFunctionScanner
-workflowInfoMap: Map<String, AIWorkflowInfo>
-workflowInfos: List<AIWorkflowInfo>
-functionInfos: List<AiFunctionInfo>
-packageNames: List<String>
+scanWorkflows(applicationContext: ApplicationContext): void
+scanFunctions(): void
registers exposed
+getWorkflowInfo(code: String): AIWorkflowInfo
+scanFunctions(packageName: String): List<AiFunctionInfo>
+getInstance(): AIWorkflowScanner
+scanFunctions(clazz: Class<?>): List<AiFunctionInfo>
-registerExposedWorkflowsAsFunctions(): void
+getFunctionInfos(): List<AiFunctionInfo>
-convertWorkflowToFunction(workflowInfo): AiFunctionInfo
+getExposedFunctionInfos(): List<AiFunctionInfo>
-extractWorkflowInfo(workflow, code): AIWorkflowInfo
+getFunctionInfoByName(name: String): AiFunctionInfo
-extractActionInfo(actionDescriptor): AIActionInfo
«annotates»
produces
produces
Model (模型层)
contains
AiFunctionInfo
AIWorkflowInfo
-code: String
-description: String
-className: String
-expose: boolean
-enableSession: boolean
-defaultSceneId: long
-actions: List<AIActionInfo>
-reqInfo: AIWorkflowParameterInfo
-respInfo: AIWorkflowParameterInfo
-actionDescriptors: List<ActionDescriptor>
-name: String
-description: String
-className: String
-methodName: String
-expose: boolean
<<converts when
-functionType: String
expose=true>>
-tags: String[]
-author: String
-parameters: List<AiParameterInfo>
-resultInfo: AiResultInfo
-method: Method
contains
contains
0..
*
0..
*
AiParameterInfo
AIActionInfo
-code: String
-description: String
-className: String
-parameters: List<AIActionParameterInfo>
«@Component»
AiFunctionExecutor
-objectMapper: ObjectMapper
Core Interfaces (核⼼接⼝层)
R extends AIReq, S extends AIResp
AIWorkflow
+executeFunction(functionInfo: AiFunctionInfo, arguments: Map): Object
-convertValue(value: Object, targetType: Class<?>): Object
-isPrimitiveOrWrapper(clazz: Class<?>): boolean
executes
+initAllActions(): void
+getAllActions(): List<ActionDescriptor>
«type param S»
R, S
AbstractWorkFlowAdapter
«type param R»
-applicationContext: ApplicationContext
-activities: List<ActionDescriptor>
+initAllActions(): void
+getAllActions(): List<ActionDescriptor>
#buildAllNodesClass(): List<Class>
AIResp
+isSuccess(): boolean
AIReq
+supportCache(): boolean
+getCacheKey(): String
+getUniqueKey(): String
-name: String
-description: String
-type: String
-required: boolean
-defaultValue: String
-enumValues: List<String>
AILoopAction
AIMapAction
+reduce(allResult: List<ActionResult>): ActionResult
+getExecutionActions(): List<ActionDescriptor>
+buildAllNodesClass(): List<Class>
+parallel(): boolean
+iterator(): Iterator
+reduce(allResult: Map<String, ActionResult>): ActionResult
+getMapExecutionActions(): List<Pair>
+buildAllNodesClass(): Map<String, List>
+map(): Map
AIFuncti
on：灵活高效可复用
AIFuncti
on定义规范
使用agent-sdk中定义
AiFuncti
on中包含如下字段：
的注解@AiFuncti
on进
行
声明，其中参数使用@AiParam进
行
标注。
基础必备字段（最小集合）：这部分字段须统一
的字段名和用途，具备健壮性。
行
业规范，如OpenAI Functi
on Spec中规定
name ：（可选，默认类/方法名）functi
on唯一标识或显示名
description ：（必需）一句话能力描述，主要给AI/开
发/文档看
parameters ：不需要必填，可通过反射自动通过@AiParam进
行
推导
returns ：（可选）返回值类型/含义说明
```

## PDF 第6页

[查看原页](RAW.pdf#page=6)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
expose ：（可选）默认false，标明当前functi
on是否对外暴露
扩展字段：
tags ： 能力 标 签 ， 便 于 多 维 分 组 检 索 ，比
"llm"、"rag"、"tool"、"java2python"、"电商数据"、"memory"
如
author ：维护人，便于治理
sideEffect ：布尔型，是否有副作用（如写库、发消息、变更状态等）
timeoutMs ：推荐执
行
超时时间（AI/流程调度友好）
deprecated ：是否废弃
AIFuncti
on访问规范
functi
on作为整体架构约束，提供workflow、AI自规划两
种模式下统一的访问方式会使得架
构更统一和完整；但workflow是提前编排好的一组节点，节点内functi
on也是固定的，基于
统一入口的调用方式会使得常量或者枚举类泛滥，不好管理。比
如下面这样的代码片段：
1
2
functionRegistry.invoke("ITEM
_QUERY");
functionRegistry.invoke(FuncEnum.ITEM
_QUERY);
因 此 必 须 在架 构SDK层面 对此 进
行
约 束 和改良。我 们 要求
调用 functi
on时， 必 须按 照
{Registry}.{D
omainRegistry}.{Functi
onClass}.{Functi
onName}的方式进
行
调用（仿照老
IC客户端的模式）。这种方式若人工实现，势必带来很重的负担，每次新增Functi
on都必须去
对应的分组
中进
行手动声明。
因此希望通过lombok的模式，对注解进
行
编译期扫描，自动生成引用，来完成以下这样的链
式
调用：
1 registry.item().query().invoke(params)
这样在代码层面、
编译
器、运
行
AIFuncti
on具体实例
一个典型的functi
on声明如下：
期架构拥有一个统一、
完整的视图。
1
2
3
4
5
6
7
8
publicinterfaceItemQuery {
String QUERY
AI
ITEM
BY
_
_
_
_
ID = "queryAiItemById";
@AiFunction(name = QUERY
AI
ITEM
BY
_
_
_
_
ID,
description = "查询商品信息"
,
expose = true)
@AiResult(description = "商品数据")
AiItemDO queryAiItemById(@AiParameter(name = "itemId"
, description =
}
```

## PDF 第7页

[查看原页](RAW.pdf#page=7)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
其中返回值AiItemDO对HSF接口返回的ItemDO做了
文档知
识库的辅助，帮助大模型在ReAct的loop中准确选
大量精简和字段含义
的标注，再通过商品
工具并得到恰当的解释。
择
回到前面提到的开
发成本的命题，在这样的设计下，新的场景可以快速复用已有
力。如“workflow产 出 的结 果 也 可 以 使用 通用 的Repo工 具 进
行
的functi
on能
context和推 理 结 果 的存储
（OdpsWriter和在线StorageWriter）。
商品领域知
识库：从定义
、生产到服务
知
识库架构图
知
识定义
1. 显性事实知
识
a. 在商品领域是对“显卡的GPU品牌是XXXX”、“显卡类目同一SPU下不同SKU差异较
大”的客观描述。
b. 关键使用场景：运营决策（试跑阶段的数据有
效的沉淀一些
行
以用于做类目灰度的优先决策）、prompt增强、数据清洗和标准化
业或者品类知
识，后续可
2. 关联情景知
识：
a. 这层知
识将商品与商品、需求场景连接起来，未来可以考虑与人的关联。如：商品-商
品关系
、商品-场景。
b. 关键使用场景：主配件
3. 隐性经验知
识
a. 知
识的顶层，难以被量化，但也最能建立信任和情感连接。通常来源于大量用户的使用
经验、专家的评测和品牌的文化沉淀。
b. 关键使用场景：商品卖点、参数说明
```

## PDF 第8页

[查看原页](RAW.pdf#page=8)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
知
识生产&应用
显性知
识生产
显性知
识生产链路围绕“类目-属性元信息”构建，整合五类数据源：商品SKU主数据、商品图
片（如主图）、外部素材（如小红书笔记和用户评价）、原始商品属性以及人工评测与运营配
置 ， 分 别输
入统 计 分 析 模 块 和LLM理 解 模 块 ： 前 者 计 算 填 写 率、SKU数量、PV对等 统 计 指
标，后者从图像和文本中提取属性、
识别用户关注点并生成同义词与解释说明；二者
输出与人
工校验结果共同汇聚为结构化的类目-属性元知
识库，包含决策属性重要性、必填性、枚举/输
入类型、填写率、TOP值、商品/SKU标识
、同义词、客观解释、SKU图上传率、属性覆盖
数、
平
均SKU数、优级SKU占比
、属性PV对及
单图平
均提取属性数等元信息；最终，知
识库
中的文本字段（如同义词、解释）被向量化存入向量数据库，支持高效语义
检索。
c/cp/cpv知
识样例：
商品属性名rerank的结果
{
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
"data": [
{
"cateName": "显卡"
,
"propertyName": "GPU品牌"
"topItemCntValues": [
"NVIDIA/英伟达"
"AMD"
,
"intel/英特尔"
"凌久"
,
,
,
"丽台"
,
],
```

## PDF 第9页

[查看原页](RAW.pdf#page=9)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
13
14
15
16
17
18
"definition": "GPU品牌 是指显卡中使用的图形处理单元（GPU）的
制造商或品牌，
},
...
],
"success": true
}
情景知
识提取
主配件场景在bad case结果集总结出的知
识库中当前在10个类目的近10000条案例中总结出
53条规则：
主配件场景badcase结果总结数据
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
[
{
},
...
]
},
"uuid": "7c2fb326-5226-4185-b7e0-c32219f65936"
"contentRaw": "{\"cate\":\"笔记本电脑\"
,
,\"examples\":[\"硬盘容量、
"customConfig": {
"cate": "笔记本电脑"
隐性经验知
识
V值场景化主观描述，知
SKU智能筛选场景
{
识样例
1
2
3
4
5
"core
_
scenario": "为现代家庭客厅提供兼具美观、实用与空间适配性的茶几选
择
，满足
"structured
filters": [
_
{
"attribute
name": "
_
长度"
,
```

## PDF 第10页

[查看原页](RAW.pdf#page=10)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33
34
35
36
37
38
39
40
41
42
43
44
45
46
47
48
"knowledge
_
needed": true,
"values": [
{
},
{
},
{
},
{
},
{
},
{
},
{
},
{
},
{
}
"value
name": "1.2米
"
_
,
"scenario
_
translation": "小户型优选，节省空间不拥挤。"
"value
name": "1.4米
"
_
,
"scenario
_
translation": "适合两人沙发，比例协调显精致。"
"value
name": "1.6米
"
_
,
"scenario
_
translation": "适配三人沙发，日常使用刚刚好。"
"value
name": "1.8米
"
_
,
"scenario
translation": "
_
大客厅标配，摆茶具零食更从容。"
"value
name": "2.0米
"
_
,
"scenario
_
translation": "宽敞客厅之选，聚会待客有面子。"
"value
name": "2.2米
"
_
,
"scenario
translation": "
_
大
平层理想尺寸，气场十足显档次。
"value
name": "2.4米
"
_
,
"scenario
_
translation": "别墅客厅优选，搭配L型沙发更和谐
"value
name": "2.6米
"
_
,
"scenario
_
translation": "超大空间专属，彰显大气家居格
调。
"value
name": "2.8米
"
_
,
"scenario
translation": "
_
豪
宅级
配置，打造客厅视觉焦点。"
]
...
}
]
}
知
识服务
```

## PDF 第11页

[查看原页](RAW.pdf#page=11)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
在知
识服务体系建设过程中，我们投入了
大量精力深
入探讨如何高效、灵活地存储和管理多类
知
型
识。面对多样化的知
识形态（如结构化元数据、半结构化规则、
非结构化文本等），系
统
不仅需要支持高可靠的知
识写入，还需满足多维度动态检索与基于语义
的精准召回需求。为
此，我们设计并实现了一套统一而可扩展的知
识存储模型与服务体系
。
该体系对外 提供 标 准化 的知
识 服务接口， 包 括写入（ save） 和 读取 （ query / count /
page
Query） 核心能力，便于上层业务流程通过函数调用（functi
on）无缝集成。在底层存
储架构上，采用两层异构存储
策略，兼顾实时性、持久性与语义
检索能力：
MySQL：作为主持久化存储，保障知
息的长
期保存；
识数据的强一致性与事务完整性，适用于结构化元信
TisPlus：提供批量向量化处理与大规模KV存储能力，适用于离线构建高维索引、深度语
义挖掘及历史知
识回溯。
通过协同工作，系
统既能支撑高频、
低延迟的在线知
识调用，又能满足复杂语义理解与大规模
知
识分析的需求，为上层智能应用（AI决策属性排序、筛选&SKU参数提取场景运营决策等场
景）提供坚实、灵活且可演进的知
识底座。
提示词工程：经验沉淀为模版
在提示词技术方面，一开始就提供了通过（workflowname，templatekey，versi
on）三元
组持久化和读取prompt的functi
on, 开
发可以通过不
断
调休提示词版本，来提升数据产出的质
量，同时开
发在可以开
发工作台低成本的维护提示词。
```

## PDF 第12页

[查看原页](RAW.pdf#page=12)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
Prompt管理模块类图
Router
ruleEngine: RuleEngine
templateManager: TemplateManager
Template selectTemplate(String taskType, String input)
String generatePrompt(Template template, String input)
1
1
uses
uses
1
TemplateManager
1
RuleEngine
templateStore: TemplateStore
rules: List<Rule>
Template createTemplate(Template template)
Template updateTemplate(Template template)
Template getTemplateById(String id)
List<Template> searchTemplates(String taskType, String language)
1
manages
1
TemplateStore
Template applyRules(Context context)
void addRule(Rule rule)
1
contains
0..
*
Rule
void saveTemplate(Template template)
Template getTemplate(String id)
List<Template> searchByTaskType(String taskType)
List<Template> searchByVersion(String version)
1
stores
0..
*
Template
boolean matches(Context context)
Template selectTemplate(Context context)
extends
id: Long
taskType: String
dimType: String
dimValue: String
language: String
version: String
content: String
paramaters: List<String>
StaticRule
taskType: String
language: String
version: String
boolean matches(Context context)
Template selectTemplate(Context context)
后面在对
不同workflow的长
期
调优过程中，我们总结出了几种最常用且有
术，即架构图中体现的几种：长prompt拆分后的分步推理、单prompt循环执
效的提示词使用技
行、并
推理&
行
统计
+
总结等。这几种不同的推理流程在sdk中使用不同类型的Acti
on节点来支持，如Map节
点、
Reduce节点、Loop节点等。这些宝贵
的实
践，主要由我们年轻的实习小师弟们在实习阶
段的实验场景：
```

## PDF 第13页

[查看原页](RAW.pdf#page=13)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
AIWorkflow：在离线业务流程统一
旧架构实现
```

## PDF 第14页

[查看原页](RAW.pdf#page=14)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
为什么旧架构采用上述模式？这主要受限于当时的技术条件与工程能力。具体原因
有三：首
先，彼时缺乏成熟的在离线一体化数据处理框架，难以统一支撑实时与批量场景；其次，大模
型的实时推理成本高
、响应延迟（RT）较长，且在线服务通常设有严格的
QPS 限流，难以满
足高并发实时需求，因此业界普遍采取“先离线
后实时”的演进路径；最后，业务尚处于探索
阶段，亟需快速验证大模型能否带来实际价值。基于上述背景，我们优先构建了基于 ODPS
离线
节点与批量推理平台（Omega）的离线推理链路
旧架构存在的问题
随着业务发
展，我们在 2024 年探索大模型与业务融
合的过程中，逐步暴露出原有链路的若干
关键问题：
1. 数据处理复杂且维护成本高：批量推理的核心工作量集中在输
入/输出数据的加工、解析
（如复杂 SQL、UDF）以及离散离线
节点的编排与调度。复杂的 SQL 可读性差，离散节
点难以统一管理；同时，受上游数据延迟、大促期间资源紧
张等因素影响，任务调度稳定
性难以保障。
2. 流程扩展性与灵活性不
足：面对复杂推理场景（如多轮迭代推理、
多模型对比
、推理后追
加评测子流程等），现有“离线
节点
+
Omega”模式难以灵活支持，即使勉强实现，也因
逻辑耦合、
缺乏抽象而难以长
期维护。
3. 推理调度存在不确定性：批量任务依
赖
共享资源池，易受资源争抢影响，导致任务延迟或
产出不
稳定。虽可申请独占 GPU 资源，但按
卡粒度分配易造成资源浪费（申请过多）或
处理效率低下（申请不
足），最终仍被迫回归共享模式，陷入
两难。
4. 在线与离线体系割裂：当前在线与离线
辑各自维护。不仅带来高昂的重复开
一致性，严重影响迭代效率与结果可靠性。
采用完全独立的两
套技术栈，代码、调度、推理逻
发与维护成本，更难以保证两者在数据处理逻辑上的
针对上述问题，我们在 2025 年通过构建一套更工程化、统一化的智能体（Agent）驱动架
构，系
统性地实现了在线与离线推理的
深度融
合与高效协同。
、
```

## PDF 第15页

[查看原页](RAW.pdf#page=15)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
新架构的实现
业务实现在离线
统一的方式有多种，例如可借助支持在离线一体的流程编排平台。但综
合考虑
业务逻辑的复杂性、未来对 Agent 扩展能力的需求，以及对全流程更高透明度和可控性的要
求，我们最终选
择
通过更工程化的方式来实现在线与离线
统一的处理。具体而言，我们基于
Spring AI Agent 将业务流程的复杂步骤封装为一个 Workflow，向上屏蔽触发源的差异（如
定时调度 vs 实时事件），向下屏蔽计算资源的差异（如单机执
行 vs 分布式集群），从而在
代码、部署、推理资源和存储层面实现真正的统一。
在核心逻辑层面，我们实现了
组
件化与标准化：将业务处理过程抽象为三个标准化组
件——
Functi
on（原子能力）、Acti
on（业务动作）和 Workflow（流程编排）。所有业务逻辑，
无论在线
还是离线，均封装在同一个“统一工作流”中，由统一的编排服务驱动。这不仅实现了
业务逻辑的集中管理，还彻底解耦
了原本散落在不同代码库或平台中的实现。同一套代码既能
支撑批量跑批，也能处理实时请求，显著提升了复用性与一致性。
在触发机制上，架构设计支持两
体 ID 列表，适用于大规模、
非
品信息变更）驱动，适用于低延迟、
种入口模式：一是离线批量推理，由调度任务触发，输
入为实
实时的存量数据处理；二是在线增量推理，由实时事件（如商
高时效的增量更新场景。两
种模式共享同一套工作流逻
辑，仅入口不同，真正实现“一套逻辑，多端适配”。
为应对离线场景下的高吞吐需求，Agent 应用内部实现了通用的分布式数据处理能力。基础
Functi
on 支持并
行
化与分片处理，Workflow 可根据负载动态调整批量处理的并发度与吞吐
量，确保离线任务高效稳定执
。
行
在结果存储方面，我们实现了统一的写入机制：无论是离线
还是在线
入 Functi
on 负责。该机制
支持将结果写入 MySQL/，供在线业务系
调用，均由统一的存储写
低延迟查询；同时
统进
行
可支持同步落盘至 ODPS，支撑离线数仓分析。双写操作由统一工作流协调，确保数据语义一
致、链路可追溯。
```

## PDF 第16页

[查看原页](RAW.pdf#page=16)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
通过上述设计，我们不仅实现了在线与离线 AI 推理的
、动态决策等高级能力沉淀
了丰
富的可复用原子业务组
深度融
合，也为未来引入多 Agent 协
件，为系
统长
期演进奠定了坚实基
作
础。
AI生产数据质量评测体系
基于商品侧知
识，利用AI实现商品与导购供给的智能化理解（特征识别、属性理解、场景导购
等），目标是高质量、规模化、实时化地产出数据。面临挑战包括数据质量、规模化成本、实
时性、
资源瓶颈、置信度、离线与实时不一致及合规问题。为此，工程和测试同学一起，基于
agent应用，构建一套可量化、可归因
、可复现的属性摘要大模型自动化评测
系
统，科学评估
新版数据的效果，评测
系
统流程如下：
实现新桶 vs 老桶召回属性商品的数量、
利用大模型进
行
性、一致性等；
可以根据不同的评测场景，配置打分规则集；
建设可持续的数据搜
的可追溯性。
排名等信息的AB对比评测；
语义理解与打分，构建多维度规则体系，覆盖V 值准确性、
完整性、可读
索与评测链路，评测归因等数据可视化，支撑决策优化，并确保结果
```

## PDF 第17页

[查看原页](RAW.pdf#page=17)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
评测归因后的可视化图
运营也可以针对
定向实时评测，帮助判断
单品或者线上badcase进
行
数据投放链路：低成本接入消费
基于商品领域agent生产的数据，通过saro+
RDS的存储方
案，可以通过调用ic现有
的商品查
询接口，但需要指定的特殊参数；在搜推广场景，我们也提供相应的tpp和saro能力，可以支
持不同的场域或者应用链路接入；当然也接受业务侧自
行
生产的数据通过ic链路进
行
投放，下
游进
消费。目前投放侧，也有一些投放策略进
选
行
行
择
，如query联动、字段优先级等。
事务型商品领域事件：实时推理的关键
在主搜SKU化的背景下，商品的存储模型复杂和迭代给ETL链路增加了理解成本和实施成本，
与此同时从商品
行
到SKU
的
行
变更（从万/s上升到数十万/s）处理给ETL链路带来了巨大的性
能 和成 本 的挑 战 。为了 解决前 者 问题， FY25通 过 saro
平 台 构建 了 SKU引擎 1.0版本 ， 主搜
```

## PDF 第18页

[查看原页](RAW.pdf#page=18)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
dump不再直接拉商品数据库GALIC
DB，而是通过saromirror的形式进
存储模型到导购商品或者sku引擎数据字段的加工和处理。
行
交互，IC内部完成
但不管是saro还是精卫这样的数据通道，为上层提供的都是数据表
+行变更的视角。而在商品
域商家或者平台一次操作往往涉及多个数据表间的事务操作，会造成量级
本身的放大；此外多
表间特定字段的
变更往往在应用层存在一定的链路或模型约束，如A表A1字段变更一定伴随B表
B1字段变更，在数据表视角下这类变更需要频繁使用多表JOIN来计算最终结果，进一步加大
了
计算量（在saro链路上多表jo
in由于A表B表
两个字段会单独变更，因此会触发2次JOIN，造成
进一步放大）。
为此，今年6月份我们升级了SKU引擎架构，通过将SKU变更降维到商品事务维度，作为ETL
链路的数据底座，同时作为商品Agent推理的驱动源。我们在精卫链路设计并实现了基于商品
ID
事务ID进
+
行数据
行变更聚合并转发
的事务消息链路。精卫任务中只处理并发送下游关注字
段（或模型）的事务消息，将秒级
别最终要处理的事务量级
低了一个数量级；下游使用Java
应用消费消息并补全数据，最终落到一张以经过增强的全局唯一skuId为主键的异构sku数据
表，这张数据表直接
DUMP到saro链路无须额外处理即可作为完整的sku数据供搜
索消费。以
上两
步分别消除了一次操作到多
行变更的放大和多
行变更间的JOIN计算，因此具备极好的性能
和低成本；
同时，我们获得了
实时的sku素材（包括属性文本、图片等）、商品基础信息等变更驱动源，
为接下来的商品实时Agent打下了良好的基础。当前，商品agent通过事务型商品领域事件搭
建了多个业务场景的实时推理能力。
降
▐ 应用分层
商品Agent
系
统采用高度模块化、分层解耦
的架构设计，以支撑复杂AI能力在商品领域的规模
化落地与持续演进。整体架构自上而下形成一条清晰的主干依
赖
链：
客户端层（item-agent-client）： 以 JDK 8 兼容的轻量级 SDK 形式，定义对外的
标准化能力。
服务层，包含3个模块：
```

## PDF 第19页

[查看原页](RAW.pdf#page=19)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
agent-server ： 该层 封装 商 品、属 性、素 材 等 核心领 域 的业 务 逻 辑 ， 通 过
repository/dao/model 分层实现数据访问与领域建模的分离，并提供统一的应用服
务接口；
Agent 实例层（item-agent-instances） 具体agent实例的实现，按业务场景拆
分为商品数据加工、商品数据问答、SKU引擎等多个可独立部署的子模块，每个模块内
含工作流编排与领域模型；
评估客户端层（item-agent-evaluation-client） 专注于agent实例的效果度
量与 A/B 测试，形成“执
行
-评估-优化”的闭环
功能层（item-agent-functions）： 提供 Agent 可调用的原子能力和业务能力，如
、文本解析、属性提取等，所有函数均注册至元数据中心，支持运
行
时动态发现
向量写入
与编排；
SDK 层（item-agent-sdk），抽象出面向 AI 与非 AI Agent 的统一调用契约；
两个公共模块：
事件引擎层（item-agent-event-engine） 负责异步消息与事件驱动，保障最终
一致性；
管理后台层（item-agent-admin） 提供运维管控、定时调度与人工干预能力；
▐ 部署架构
1. SKU引擎分组：通过商品领域事件，把从商家管理侧以商品粒度的商品信息，转换并映射
成前台导购链路需要的SKU粒度，在agent中完成有无SKU、
item和SKU状态以及属性文
本等商品领域内的逻辑处理；目前针对前台导购场景有主站SKU和门店SKU库。该集群随
着主搜切到SKU引擎，需重保。
2. LLM分组：承担基于不同业务场景的大模型实时推理核心职能，动态调度多类型Agent数
据生产链路；除实时推理任务外，离线推理任务也同样支持；在此分组上支持大模型评测
```

## PDF 第20页

[查看原页](RAW.pdf#page=20)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
体系
的任务，辅助提升业务推理数据的质量。
3. 服务分组：采用读写分离
+单元化架构实现Agent数据的高效写入和投放：
写服务：以张
北
中心为唯一写入节点，通过dh
_
L1服务层与双机房失效缓存机制，确保数
据写入的集中管控与容灾能力，所有写操作最终持久化至
中心数据库（DB）；
读服务 ：按 照
（NA610/NA620）及
详 情 等单元化 流 量进
行 部 署 ， 通 过 dh
_
L0d 服务 层、Tair分 布式缓 存
单元化读缓存链路，实现低延迟数据访问。跨中心数据通过"单元同
步"机制保障最终一致性，满足海量读请求的就近访问需求。
▐ 小结
相较于引入功能完备但复杂Agent框架或者试图在Java领域复刻一个完整的平台级框架，我们
只希望拥有一个“恰好够用”但又不会带来太多负担的SDK。这样的SDK仅需要cursor两个小
时的对话以及2天的测试打磨即可，事实上目前的aiagentsdk几乎100%都是AI生成的代码。
至此，我们初步搭建完成了以“事件驱动的Functi
on-Centric Agent架构”。
商品Agent应用进展
商品Agent已在商品属性、卖点等多个核心业务场景完成落地，覆盖亿级在线商品，显著提升
了商品信息的完整性、
准确率与丰
富性，并在搜
索、详情等核心导购场景中
实现了成交转化率
的正向提升。
在研发效能层面，面向数据流处理的商品Agent基础框架已全面搭建完成，具备较强的能力复
用性与快速扩展能力。新业务需求到来时，开
发团队仅需一周/人的时间即可完成能力开
发、数
据试跑及评测结果优化等全流程工作，大幅压缩了从需求到前台实验的交付周期，助力业务以
更快的节奏在前台场景完成验证与迭代。
总结
通过25年一个季度对商品域Agent的探索与建设，我们初步验证了将大模型能力以结构化、工
程化方式
入商品数据生产链路的可
行
性与价值。从底层事务驱动的数据引擎升级，到轻量
Agent架构设计，再到多个核心业务场景的成功落地，商品Agent已展现出从“单点提效”向“系
统自治”演进的巨大潜力。
展望未来，Agent技术正以前所未有
与范式的持续涌现，为商品域的智能化建设打开了全
的速度迭代演进，Harness、Skill等新一代Agent框架
新的想象空间。我们正积极拥抱这些前沿
嵌
```

## PDF 第21页

[查看原页](RAW.pdf#page=21)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
技术，将其与商品域的实际业务场景深度融
合：以更强的语义理解能力让Agent真正"读懂"商
品的
深层含义，以Skill模块化的方式沉淀和复用商品域的专业领域知
识，以商品理解"大
脑"为
核心构建自适应决策机制，实现对商品信息的主动感知与动态更新。我们相信，持续夯实"数据
工具
知
识
决策"四
+
+
+
位一体的Agent基础设施，在拥抱技术浪潮中驱动能力持续跃迁，让系
统
真正读懂每一件商品、理解每一位消费者，驱动电商导购体验进入“主动理解、精准表
达
高
效决策”的新阶段。
、
团队介绍
本文作者
勇清，来自淘天集团-商品中心技术团队。在海量商品构成的复杂生态下，我们系
统
性地构建了贯穿商品定义
、发布、存储
、治理、理解与消费分发
的全生命周期管理能力，帮助
商家与平台实现商品信息的标准化表
达
、智能化理解与规模化流通。我们的愿景，是让商品数
据如同血液一般在集团内健康循环、畅通流转、智慧运
行
——以集团统一的商品数据底座与商
品理解 Agent 为核心驱动力，全力支撑淘宝、天猫等核心电商业务线
的持续发
展与创
新。
¤ 拓展阅读 ¤
3DXR技术 | 终端技术 | 音视频技术
服务端技术 | 技术质量 | 数据算法
大淘宝技术
大淘宝技术官方账号
967篇原创内容
公众号
阅读 7641
留言
写留言
```

## PDF 第22页

[查看原页](RAW.pdf#page=22)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
还没有
留言，来写首评
```
