# 从代码生成到自主决策：打造一个Coding驱动的“自我编程”Agent：PDF文本转写

> 这是原始PDF文本层转写，不是学习摘要。页码为PDF物理页序；图表、代码版面和图片文字不能完整表达在此文本层。已查看图像的内容和质量问题见AI学习笔记及META.json。

[原文PDF](RAW.pdf) · [AI学习笔记](AI_Coding驱动自我编程Agent.md) · [处理与质量记录](META.json)

## PDF 第1页

[查看原页](RAW.pdf#page=1)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
从代码生成到自主决策：打造一个Coding驱动的“自我编程”Agent
残风 2025年12月22日 01:48 浙江
大淘宝技术 16人
本文介绍了如何构建一个“自我编程”的Coding驱动型Agent，通过让大模型生成并执
行
Python代码来实现自主决策与复杂任务处理。该Agent基于ReAct架构优化，采用FIM
（Fill-in-the-Middle）代码生成格式，结合Py4j实现Java与Python双向调用，并设
计了分层记忆系
统（感知
、短期
长
期）和模块化Prompt工程。其核心
创
新在于用“代
码即指令”替代传统JSON工具调用，显著提升灵活性与执
行
能力，目标是打造能胜任
DevOps场景的“1.5线
”AI助手，具备自我评估
多Agent协作和持续学习能力。
、
、
前言
在探索 LL
M 应用的过程中，LL
M作为 Agent 的"大
脑"有着无限可能。其中，"代码编写"已经
成为了少数几个成功大规模落地的场景之一，这让我们不禁想到：既然 LL
M 可以写出高质量
的代码，为什么不能让它更进一步，编写并运
行
代码来控制 Agent 自身的
行
为呢？这样运
行
逻辑，就不简简单单
的是“下一个”这么简单，而是让Agent拥有分支、循环等各种复杂逻辑。
这个想法虽然听起来有点魔幻，但仔细想想确实是可
行
们是如何一步步构建这样一个能够"自我编程"的 Agent 的历程。
的。在这篇文章中，我想和大家分享我
我们的目标是将Agent模式，打造成一个“师弟”，一个真正能在内部的DevOps系
得上忙的AI助手。
统中，能帮
Agent
系
统设计
▐ Agent简介
```

## PDF 第2页

[查看原页](RAW.pdf#page=2)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
技术架构方面，我们在 ReAct Agent 模式基础上进
了
行
深度优化：
改造传统 JSON + 组
装
调用方式，基于Py4j，实现" Code+
泛化调用 "机制，显著提升
工具调用的灵活性和执
效率；
行
采用 Spring Boot 技术栈构建后端架构，整合 Spring AI 生态及 Spring AI Alibaba 能
力完成模型接入；
通过 内部评测
平台 和 内部观测
平台 实现全链路评测与观测；
底层工具采用 Mcp 协议实现业务能力补充；
基于 A2A 协议实现 Multi Agent 架构，高效对接各子 Agent；
模型策略采用混合部署方
案，根据不同场景使用最优模型：
翻译/数据提取
任务：Qwen3-Turbo（低延迟优先）；
思考/动态代码生成：Qwen3-Coder（强化代码能力）；
通用 场 景：按 需调用 各 个平 台 提供 的Qwen、Deepseek 等 模 型 布）；
（ Agent 内部 模 块 分
（Agent内部模块分布）
Memory 记忆
Short Term Memory 短期记忆: Session维度的记忆，仅在当前Session内生效；
Sansory Memory 感知记忆: 通过悬浮球，捕捉的页面、
url等环境感知记忆；
Experience 经验: 来自配置、总结的经验，主要用于指导Agent各个环节的内容生成；
Context 上下文
System Prompt: 配置化、动态化的
系
统提示词；
可配置的：平台介绍
用工具
+ 重要原则
来自记忆的文本；
+
+ 角色定义
使用经验；
工作机制
+
+ 输
Inference Segment 推理段落(User Prompt)；
入格式说明
+ 输出格式要求
可
+
```

## PDF 第3页

[查看原页](RAW.pdf#page=3)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
Round “轮”: 在复杂任务执
行
时，每轮会作为一个单独的Segment用作当前轮次的执
行
总结和后续轮次的目标定义；
Express 表
达: Agent返回给用户的内容；
Thought 思考: Agent在每一步执
时的思考内容；
行
Code 代码: 代码也会作为一个段落，出现在Prompt中；
其他: 如果后续有其他的环节，将作为新的Segment加入到User Prompt中；
Code 代码
Python Executor: Java中通过调用本地的Python进程；
Py4j: Python回调
Java代码的时候，使用此工具实现回调的泛化调用；
Toolkit 工具包
Python语义
化模板设计: 提供将Toolkit转化为Python代码的模板设计模式，在Prompt
中使用模板方法，生成Python代码参与Prompt中；
泛化调用。
▐ 核心Coding驱动逻辑
```

## PDF 第4页

[查看原页](RAW.pdf#page=4)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
在我 们 的Agent中， Segment 采用 " [Segment]: [Content] " 的结 构， 通 过 组 合不 同 的
Segment来形成Prompt，从而实现CoT（Chain of Thought）推理。
除了"外界"工具，我们还为Agent提供了"系
统"工具，使其能够获取和控制自身能力。这些能
力包括：检查已
发起的任务、查询掌握的技能、主动休眠、主动与用户对话、
通过大模型进
行
深 度 思考 ， 以 及 利用大模 型 解 析 数据 等 。在实 现 上 ， 每个工 具 箱都被 设 计 为Python的一个
Class，其中的各项工具则作为函数实现。我们将不同的描述和属性都相应地映射为Python中
的各种定义
。
由此，我们打造出了一个"自我编程"驱动的Agent。在运
行
可以充分利用Python的原生功能保障数据的确定性，如字符串运算
更重要的是，它能够实现自我控制，可以发起复杂任务，并对自身能力进
行
时，它不仅能够调用外部能力，还
、数字运算
、时间运算等。
检查评估。
（PS：除了我们的“人类程序员”外，AI在这次迭代功不可没，凭感觉大概有50-60%的无修
改代码，来自AI编写，尤其是《代码驱动》环节，几乎有80%的代码来自AI编写）
▐ Agent工程结构
```

## PDF 第5页

[查看原页](RAW.pdf#page=5)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
Agent
在我们的
系
统中，一个Agent是一个线程。在Agent运
行
各个Area和Act。其生命周期如下图所示：
过程中，将会在线程池中，同时运
行
```

## PDF 第6页

[查看原页](RAW.pdf#page=6)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
Area —— 功能区介绍
Area的最初设计，是来自1.0向2.0演进时，创造出来的概念。其设计理念来源于人类的大
脑分
区，我们将Agent的逻辑区域分成了：感知区、认知区、
表
达区、自我评估区、运动区，将不
同种类的Act收纳到Area中，让整个架构体系
看着更加的清晰，也让相同能力的动作，可以具
备相互沟通的可能。
各功能区关系和详细介绍
（1）感知区
主要负责接收外部信息，包括但不限于：用户发送的消息、用户点击的卡片事件
异 步 返 回 结 果 等 。在接 收到 消 息 后 ， 感 知 区还 会调用 内部 的Act， 对数据 进
行
估：
、子Agent的
系列处 理、评
用户主语言解析
模糊化解析
场景分析
用户问题的增强
解析环境感知
的数据
解析附件的数据
针对
不同搜
索场景的
```

## PDF 第7页

[查看原页](RAW.pdf#page=7)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
（2）认知区
当感知区完成系列解析后，会将解析数据，传递到认知区，由认知区的IntentPlanner来使用
Segment机制，处理用户需求并生成对应代码。生成代码后，提交给Python执
引擎，进
行
行
执
。
行
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
IntentPlanner
├── SegmentBuilder (成员
变量)
│ ├── List<InferencePromptNewBuilder> promptBuilders
│ ├── InferencePromptConfigManager (prompt配置管理)
│ ├── build(type, segments, context, config) -> InferenceSegment
│ └── 路由到具体的PromptBuilder
│
└── PromptBuilder实现类
├── BaseInferencePromptBuilder (抽象父类)
│ └── 使用InferencePromptConfigManager获取配置化prompt
├── ThoughtPromptBuilder
├── CmdPromptBuilder
└── 其他自定义PromptBuilder
[Act] IntentPlanner 核心思想
用户输
入后，仅执
一轮逻辑；
行
若存在复杂任务，则将任务移交给运动区处理；
```

## PDF 第8页

[查看原页](RAW.pdf#page=8)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
（3）运动区(高级认知区)
```

## PDF 第9页

[查看原页](RAW.pdf#page=9)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
在当前Agent系
统中，运动区作为一种高级认知区，将会承担复杂任务。当认知区的无法处理
的任务被提交过来后。运动区将会发起一个内部循环，来使用Segment的机制，逐步完成任
务。
[Act] TaskExecutor 核心思想
根据传入的目标，逐轮执
计划；
行
每轮重新制定子目标，本轮完成后，都会评估任务进度，任务完成后汇报给感知区，若未
完成，重新评估目标达成情况；若无法完成，可以选
放弃；
择
若目标判断可以达成，继续制定下轮目标；
1
2
3
Round 1 Segments: [User, Context, Thought1, Plan1, Cmd1, Evaluation1, NextGo
Round 2 Segments: [User, Context, Thought1, Plan1, Cmd1, Evaluation1, NextGo
Round 3 Segments: [所有历史Segments + Thought3, Plan3, Cmd3, Evaluation3, Nex
```

## PDF 第10页

[查看原页](RAW.pdf#page=10)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text

```

## PDF 第11页

[查看原页](RAW.pdf#page=11)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
（4）表
达区
表
达区负责将内部信息传递给外部，包括但不限于：发送给用户的话、发送给用户的卡片、发
送给用户的
系列事件。
在传递文本时，表
达区一般不做过多总结；
在传递数据时，表
达区会根据历史Segment机制，依据数据，回答当前表
在传递表
单、复杂数据时，表
达区将会直接向用户传递数据。
达诉求；
（5）自我评估区
当IntentPlanner、TaskExecutor，执
行
完初始目标后。将触发自我评估区的SelfTaskCheck
评估任务完成情况。如果发现任务失败，或是能执
行
的，那么将重新触发回来源。
Context Engineering 上下文工程
```

## PDF 第12页

[查看原页](RAW.pdf#page=12)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
▐ 上下文 与 Prompt
在Agent中，上下文和Prompt体系
是整个Agent决策的核心组
件。该体系
一管 理 不 同 类 型 的Prompt构建 过 程， 实 现 了 配 置 化、模 块 化 的上 下文 组
通过Segment机制
统
装 和Prompt生 成 机
制
。
在Prompt和上下文拼装
的过程，主要代码结构和逻辑如下图所示：
```

## PDF 第13页

[查看原页](RAW.pdf#page=13)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
Context上下文组成
1. Segments
当前Segments
Segments : 当前轮次已生成的Segment集合；
作用 : 提供当前轮次的执
行
状态和中间结果；
动态更新 : 随着当前轮次的进
不
行
断增加新的Segment；
历史Segments
Segments : 来自历史轮次的所有Segment集合；
作用 : 为Agent提供
长
期记忆和上下文连续性；
内容 : 包含用户输
入
、思考过程、执
行
代码、结果反馈等完整历史；
调用经验
成功案例 : 基于历史成功案例的工具使用经验；
失败总结 : 从历史失败中提取的经验教训；
践 : 经过验证的代码模式和调用方式；
知
最佳实
识增强
动态知
识检索 : 基于用户查询的实时知
识获取；
领域知
识注入 : 特定场景下的专业知
识补充；
上下文关联 : 与当前任务相关
的背景知
识；
2. 环境上下文
ToolkitContext : 包含会话ID、追踪ID、
租户信息、执
SegmentBuildConfig : 包含模型配置、功能开关
知
Agent状态 : 当前Agent的内部状态和能力配置；
、
过程的
行
变量存储等执
识增强设置等；
环境；
行
3. 工具上下文
可用工具清单 : 动态获取当前可用的工具包和API；
工具描述 : 自动生成的Python风格的工具使用说明；
Prompt组成架构
Prompt示例
为了更好地理解我们的Prompt设计，这里展示一个基于Prompt拼接思路编写的案例：
（1）System Prompt示例
1
## 平台介绍
2
你是一个Agent，专注于阿里巴巴DevOps平台的智能助手，能够操作DevOps的相关平台。
3
```

## PDF 第14页

[查看原页](RAW.pdf#page=14)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
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
49
## 角色定义
你是一个专业的DevOps智能助手，具备代码生成、工具调用、
任务执
行
等核心能力。
## 工作机制
基于用户输
入和上下文信息，通过思考-执
-评估的循环模式完成任务。
行
## 输
入格式说明
用户输
入可能包含自然语言描述、页面截图、URL信息等多模态内容。
## 输出格式要求
代码将以Fill-in-Middle(FIM)格式提供
,包含三个部分:
- <|fim_prefix|> 前缀代码 <|fim_suffix|> 后缀代码 <|fim_middle|>
你需要在 <|fim_middle|> 处续写代码,使前缀代码和后缀代码能够正确连接并执
注意:
- 仅在 <|fim_middle|> 处续写代码
- 确保续写的代码与前后文逻辑连贯
- 不要修改或重复前缀和后缀中的代码
## 可用工具
classexample_toolkit:
def get_project_info(project_id):
"""获取项目基本信息"""
pass
def search_requirements(project_id, query):
"""搜
索需求信息"""
pass
def create_requirement(project_id, title, description):
"""创建新需求"""
pass
class normandy_toolkit:
def get_app_list(project_id):
"""获取应用列表"""
pass
def deploy_app(app_id, version):
"""部署应用"""
pass
def get_deploy_status(deploy_id):
"""获取部署状态"""
pass
## 重要原则
。
行
```

## PDF 第15页

[查看原页](RAW.pdf#page=15)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
50
51
52
53
54
55
56
57
58
59
1. 严格按照FIM格式
输出代码
2. 确保代码的安全性和正确性
3. 优先使用提供的工具包完成任务
4. 对于不确定的操作要进
二次确认
行
## 补充的增强知
识（在后台配置的一些知
%s
%s
识点，比
如DevOps各个子系
统间的关系
、变更和分支的关
## 历史经验（自动学习+后台配置的一些代码示例，基于知
识库团队提供的检索能力进
行
相关性召回
（2）User Prompt示例
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
期望返回结果：
User: 帮我查询项目123的需求信息，关键词是"登录功能"
Context: 当前页面URL为https://example.com/project/123，用户正在查看项目概览页面
Thought: 用户想要查询项目123中关
于"登录功能"的需求信息。我需要使用example_toolkit的s
Python:
<|fim_prefix|># 查询项目需求信息
project_id = "123"
query = "登录功能"
try:
<|fim_suffix|>
except Exception as e:
print(f"查询过程中
发生错误: {str(e)}")<|fim_middle|>
1
# 调用工具查询需求
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
result = example_toolkit.search_requirements(id = 123, keyword = "登录功
# 处理查询结果
if result and result.get('success'):
requirements = result.get('data', [])
if requirements:
print(f"找到 {len(requirements)} 个相关需求:")
for req in requirements:
print(f"- {req.get('title')}: {req.get('description')}")
else:
print("未找到相关需求信息")
else:
print("查询失败，请检查项目ID或网络连接
")
System Prompt 结构
```

## PDF 第16页

[查看原页](RAW.pdf#page=16)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
我们采用
配置化
动态化
系
的
+
统提示词设计，主要包含以下模块：
1. 基础配置
1
2
3
4
5
6
7
8
## 平台介绍
基于OpsInferencePrompt配置的平台能力介绍
## 角色定义
Agent的角色定位和核心职责描述
## 工作机制
Agent的工作流程和决策机制说明
2. 规范相关
1
2
3
4
5
6
7
## 输
入格式说明
用户输
入的解析规则和格式要求
## 输出格式要求
不同PromptBuilder的专属输出格式定义
- ThoughtPromptBuilder: 思考过程的结构化输出
- CmdPromptBuilder: FIM格式的代码续写规范
3. 能力增强
1
2
3
4
5
6
7
8
4. 经验
1
2
3
4
5
6
7
8
## 系
统基础
Agent的基础能力和限制说明
## 可用工具
动态生成的工具包描述和使用方法
- Python语义
- 泛化调用接口说明
化模板设计
- 工具调用示例
## 使用经验
基于历史成功案例的少样本示例
## 重要原则
核心的执
行
原则和安全约束
## 常见错误
常见问题的预防和处理方
案
```

## PDF 第17页

[查看原页](RAW.pdf#page=17)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
User Prompt 结构
1. Segment List
用户提示词主要由Segment序列组成，按时间顺序排列：
1
2
3
4
5
6
7
User Segment: 用户的原始输
入
Context Segment: 环境感知数据（页面信息、URL等）
Thought Segment: Agent的思考过程
Command Segment: 生成的执
行
代码
Evaluation Segment: 执
行结果评估
NextGoal Segment: 下一步目标规划
...
2. FIM格式 (Fill-In-Middle)
我们使用FIM格式进
行
代码续写。FIM技术基于论文"Efficient Training of Language Models to
Fill in the Middle"[ https://arxiv.org/abs/2207.14255 ]，是一种专门针对代码生成优化的技
术：
1
2
3
代码将以Fill-in-Middle(FIM)格式提供
,包含三个部分:
- <|fim_prefix|> 前缀代码 <|fim_suffix|> 后缀代码 <|fim_middle|>
你需要在 <|fim_middle|> 处续写代码,使前缀代码和后缀代码能够正确连接并执
行
。
4
5
6
7
注意:
- 仅在 <|fim_middle|> 处续写代码
- 确保续写的代码与前后文逻辑连贯
- 不要修改或重复前缀和后缀中的代码
FIM技术的核心优势 ：
上下文感知 : 模型能够同时理解前缀和后缀代码的语义；
精准填充 : 专门训练用于中间代码片段的生成，而非从头编写；
逻辑连贯 : 确保生成的代码能够与前后文完美衔接；
FIM格式的实际结构：
1
2
3
4
5
6
7
8
9
<|fim_prefix|>
# 已有上下文和代码
# 包含函数定义
、变量声明等前置逻辑
<|fim_suffix|>
# 后续期望的代码结构
# 包含返回值处理、异常处理等后置逻辑
<|fim_middle|>
# LLM需要在此处填充代码
# 生成连接前后文的核心业务逻辑
在Agent中的应用场景 ：
逻辑补全 : 在明确输
入
输出的前提下，补全中间的处理逻辑。
```

## PDF 第18页

[查看原页](RAW.pdf#page=18)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
记忆
记忆系
统是构建真正智能Agent的关键组
件。正如人类认知系
习、推理和决策，AI Agent也需要类似的记忆架构来：
维持长
期对话状态 ：在多轮交互中保持上下文连贯性；
积累经验知
识 ：从历史交互中
学习和改进；
支持复杂推理 ：基于历史信息进
行
更深
入的分析；
个性化服务 ：根据用户历史偏好提供定制
化体验；
统依
于复杂的记忆机制来学
赖
Agent在处理复杂任务时，主要依
赖
于上下文窗口来维持对话状态和任务记忆，这种方式存在
明显的局限性：
1. 上下文长度限制 ：上下文窗口有固定的token限制，无法处理超长的历史信息；
2. 记忆组织缺失 ：简单
的上下文拼接无法有
效组织和检索历史信息；
3. 知
识更新困难 ：静态的上下文无法动态更新和优化已有知
识；
4. 计算成本高昂 ：长上下文处理需要大量的计算资源；
为了解决这些问题，需要在Agent工程侧开
发各种Agent记忆系
统，旨在为AI Agent提供持久
化、结构化、可检索的记忆能力，它记录了Agent过往的所见所闻和互动历程。
▐ 记忆分层
按照存储时间的记忆分类法最早是在 1968 年发布的 Atkinson-Shiffrin Memory Model 中
提出，将记忆分为感知记忆（Sensory Memory）、短期记忆（Short-term Memory）和长
期记忆（Long-term Memory）。
感知记忆存储了人脑从环境中捕获的信息，例如声音、视觉等信息，在感知记忆区这类信
息只能保留很短的时间；
短 期 记 忆 存储人脑 在思考 过 程中所 需 要 处 理 的信 息 ， 也 被 称 为工 作 记 忆 （ 在 1974 年
Baddeley & Hitch 模型中提出），通常也只能保留很短的时间；
长
期记忆是指Agent中存储时间较长的信息，它类似于人类大
脑中的记忆，能够保留大量的
数据和经验，并且可以存储很长时间，甚
至是永久性的。
长
期记忆和短期记忆在Agent中是相互补充的。短期记忆可以快速访问和处理当前需要的信
息，而长
期记忆则提供了丰
富的背景知
识和历史数据。Agent需要将短期记忆中的信息与长
期
记忆中的知
识结合起来，以实现更智能的
为和决策。行
```

## PDF 第19页

[查看原页](RAW.pdf#page=19)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
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
15
16
17
┌─────────────────────────────────────────────────────────────┐
│ 记忆分层
├─────────────────────────────────────────────────────────────┤
│ 感知记忆 - 标签页维度
├─────────────────────────────────────────────────────────────┤
│ 短期记忆 - 会话纬度
│ ├─ 会话记忆
| ├─ 实体记忆
│ └─ 工作记忆
├─────────────────────────────────────────────────────────────┤
│ 长
期记忆
│ ├─ 用户偏好 (业务实体记忆,...) - 用户纬度
│ ├─ 历史会话 (历史会话记忆总结)
│ ├─ 用户画像 (角色定位、技能标签、工作习惯)
| ├─ 平台知
识
│ └─ 经验
└─────────────────────────────────────────────────────────────┘
▐ 环境感知记忆
鱼的记忆只有 7 秒，实际上人也有
非常多的记忆过目就忘，但不管怎样，这个记忆始终存在
过。
环境感知记忆是最短期的记忆，只在当下这一瞬间有
在网页上的任
意动作
效的数据，不具有
长
期价值。
都会让前一瞬间的数据失效：例如打开抽屉/弹窗时，之前感知到的数
据可能就没有
意义了；
如果要记得之前看过哪些东西，则需要转成工作记忆或者沉淀到长
期记忆中。
```

## PDF 第20页

[查看原页](RAW.pdf#page=20)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
使用场景
在答疑场景中，用户打开对话时，大概率是遇到了问题，需要寻找对应的解决
方
案。这个时候
需 要用 户 编 写一些文 字向 Agent 说 明 在哪 个页面 进
行
什 么操 作 时， 遇 到 了 什 么问题。如果
Agent 能有一双眼睛，跟用户一样看着当前的页面，那么或许就能够提前帮用户预输
入当前的
上下文，减少用户的使用成本。
▐ 短期记忆
在Agent中，我们设计了基于Session级
别的短期记忆存储，基于ES实现。在短期记忆中，会
话、实体、工作记忆均被设计统一的Segment格式存储，为Agent提供上下文连续性。
1用户对话 → 内部产生Segment → 短期记忆存储 → 下轮对话时检索 → 提供上下文
记忆消息类型
1. 段落记忆消息
存储推理段落信息，是Agent执
数据结构 :
行
过程的核心记忆载体。
1
2
classSegmentMemoryMessageextendsShortTerm3MemoryMessage {
InferenceSegment segment; // 推理段落内容 (Thought/Command/Evaluation等
```

## PDF 第21页

[查看原页](RAW.pdf#page=21)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
3
String execId; // 所属执
行
ID，标识当前轮次
4
List<String> parentExecId; // 父节点执
ID列表，支持执
行
行
链追溯
5
}
2. 实体记忆消息
存储结构化实体信息，用于记录关键对象和状态。
数据结构 :
1
classEntity3MemoryMessageextendsShortTerm3MemoryMessage {
2
String title; // 实体标题/名称
3
Object data; // 实体数据内容(可为任
意
对象)
4
}
使用场景 :
工具调用结果存储
用户关键信息提取
环境状态快照
3. 基础消息类型
所有短期记忆消息的基类，提供通用属性。
数据结构 :
1
2
3
4
5
6
7
▐ 长
abstract classShortTerm3MemoryMessage {
String uuid; // 唯一标识符，用于更新和删除操作
String sessionId; // 会话ID，Session级
别隔离
List<String> tags; // 标签列表，支持多维度分类
Long timestamp; // 创建时间戳，用于时序管理
Long sortValue; // 排序值，控制记忆优先级
}
期记忆
知
识点
知
识点目标是将内部积累的研发经验和专业知
识系
模拟开
发人员的问题解决思路，提供更加专业和精准的支持。
统化。特别是在与MCP系
统集成后，将能够
知
识点的内容，需要主要覆盖几个关键领域：
DevOps相关平台研发团队的工具/api/平台使用调用实战经验；
团队私有
域知
识；
除了正面的知
识注入，系
统还包含了约束性知
佳实
践以及常见问题的标准处理流程。这些知
识，例如平台使用的注意事项、特定场景下的最
识将直接影响Agent的响应策略和问题处理方
```

## PDF 第22页

[查看原页](RAW.pdf#page=22)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
式。
值得注意的是，这些新增的知
识点与知
识库的区别 ：
新的知
识点，会作为Agent思考的Prompt的指引。往往包含“概念性”的内容。当一个知
沉淀成一个“文档”比
较重，又希望告知Agent的时候，就可以使用短知
识来进
维护；
行
短知
识往往是一句话，比
如：重新部署是流水线
的概念，重启
是诺曼底的运维概念。
识
代码执
行经验
这里描述的是接下来将推出的形态，在目前版本中，大模型投票机制
识图谱方
还没有，记忆的存储与检
索目前只是在向量数据库中，知
案还在对接
中。在Agent每轮逻辑执
完成后，本轮
行
执
行
的细节将会被记录到经验记录表中。经过人工审核+大模型投票机制，会将记忆录入到知
识库团队提供的经验图谱进
行
存储。在Agent每次使用大模型生成代码时，将会从知
识图谱中
检索到对应的经验，随后拼接到Prompt中的固定位置。
用户偏好记忆
通过环境感知，根据用户页面访问情况，实时动态上报业务实体操作，作为业务实体记忆上下
文。
Memory 部 分 ，接 收环 境 感 知 上 报 的 数 据 ， 进而 转 换成 业 务 实 体 记 忆 存储
(BizEntityMemroy),BizEntityMemroy主要组成部分:
schema: 定义业务实体的结构schema，json schema格式
data: 定义业务实体的具体数据
operation: 平台操作
```

## PDF 第23页

[查看原页](RAW.pdf#page=23)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
tags: 实体标签
历史会话记忆
用户通过助手进
成时，对会话记忆进
行
行会话时，由Agent规划模块进
行意图识别，并规划Task。在规划Task执
完
行
总结。
HistoryChatMemory(历史会话总结记忆)存储结构：
1
2
3
4
{
"time": "2025-09-18 17:14:00"
"question_type": "操作
实施"
"keys": "应用名: example",
,
```

## PDF 第24页

[查看原页](RAW.pdf#page=24)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
5
6
7
"summary": "用户在明天(2025-09-18 14:00:00)有一个example的
"userId":""
发布计划"
,
}
历史会话记忆检索，通过全文向量融
向量化字段：keys
filter：userId
记忆淘汰策略：
合查询，召回会话记忆：
代码驱动
在 Agent 开
发
的早期，我们用业界必选的Agent实现方式，走了
LL
M返回"JSON "
+
"固定文
本前缀"的路。这看起来是最直观的选
择
，我们的Agent 1.0 和 2.0 版本都是这么实现的。
但随着项目
深
入，作为一个重工具调用的Agent，频繁调用Mcp、Agent的问题接踵而至：
数据格式虽然可以保证，但是内容质量并不能保证；
Token 超长导致的性能下降；
JSON 格式
不够稳定；
多轮对话既要保证灵活性又要保证速度；
无论是对接
Mcp 还是 A2A，想要又快又准确地调用各种能力，都面临着重重困难。我们也在
断
不
借鉴业界各领域的优秀实
践，从 mem0 到 JManus，但始终觉得差点意思。为了提高任
务成功率，我们牺牲了响应速度；为了提升速度，我们又不得不降
低灵活性；而灵活性的
低，恰恰又导致了任务成功率的下降。这似乎成了一个难解的死循环。
降
2.0 版本虽然是对 1.0 的全面重构，但经过一段时间的实
践，我们发现它在执
逻辑时总是一
行
条路走到黑，一旦
开始节点错了，就很难再纠正回来。正当我们为此困扰时，一次偶然的
发现
给了我们启
发：在研究 Github Copilot Agent 时，我们注意到它使用 JavaScript 来定义
工
```

## PDF 第25页

[查看原页](RAW.pdf#page=25)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
具。虽然它最终还是用 JSON 来调用，但这个设计却让我们灵光一现 —— 为什么不让 Agent
直接通过编写代码来实现自己的逻辑呢？
▐ 代码执
行
在Agent中，代码与执
行部分是整个系
统的核心执
行
果反馈的完整闭环，让Agent真正具备了"自我编程"的能力。
引擎。它实现了从代码生成到执
行
再到结
Python Execution Engine [Java]
PythonExecutionEngine作为整个代码执
行
架构模式。本质上就是用Java发起Python，让Python执
行
的引擎，设计上采用了"线程池
+异步执
代码，调用工具时回调
监控"的
行+
Java，同时
Java负责调度和监控。
```

## PDF 第26页

[查看原页](RAW.pdf#page=26)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
核心设计思想：
异步执
行
: 每个Python脚
生命周期管理 : 从执
本都在独立线程中运
行
行
ID生成到结果回收，全程可追踪；
超时控制 : 防止Python脚
本死循环，默认3600秒超时；
资源隔离 : 每个执
都
行
有独立的上下文环境；
，避免阻塞主流程；
脚
执
本执
流程
行
流程：
行
1. 准备阶段 : Agent把生成的Python代码传递给PythonExecutionEngine；
2. 初始化 : 分配执
行
ID，设置上下文，注册工具包；
3. 执
行
: 启动Python进程，加载toolkit_bridge.py；
4. 监控 : ExecutionMonitor实时跟踪执
状态；
行
5. 收尾 : 收集结果，清理资源，反馈给Agent；
代码执
行
的核心逻辑在PythonScriptExecutor中，它负责：
动态生成Python运
环境；
行
注入toolkit_bridge.py作为桥接层；
管理Python进程的生命周期；
处理标准
输出和错误输出；
安全与监控
执
行
日志 : 记录每次代码执
性能监控 : 统计执
的
行
详细信息；
时间、成功率、错误分布；
行
安全
检查 : 虽然还没完全
实现，但预留了代码安全扫描的接口。此处应该严格禁止，某些
系
统函数的调用，比
资源监控 : 监控Python进程的CPU和内存使用。
如随便引用import、使用os操作系
统文件等；
Toolkit Bridge [Python]
Toolkit Bridge是整个Python和Java沟通的桥梁，可以说是这套架构中最关键的一环。它解决
了"Python怎
么调用Java工具包"这个核心问题。
Py4j桥接机制
我 们用 Py4j 来实 现 Python 和Java 的双 向通 信 。简单来说 ， Java 实 现一个Py4j 的Gateway
Server，Python对接到这个Server中，就能互相调用了。
关键设计点：
```

## PDF 第27页

[查看原页](RAW.pdf#page=27)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
单例Gateway : 全局只维护一个Gateway连接，避免重复连接
连接池化 : Gateway连接失败时自动重试，保证连接的稳定性；
端口固定 : 默认使用15333端口，避免端口冲突；
开销；
会话上下文管理
SessionContext解决了"Python代码怎
么知道当前是哪个用户、哪个会话"的问题：
1
2
3
4
5
6
7
8
classSessionContext:
def __init__(self):
self._data = {}
self._toolkit_context = None
def set_data(self, key, value):
"""设置会话数据，如session_id、trace_id等"""
self._data[key] = value
每次Python脚
本 执
行
前 ， Java 会 把 session_id、 trace_id、用 户 信 息 等 存储 到
SessionContext里，这样Python代码调用工具包时就知道自己代表哪个用户在执
了。
行
异步调用支持
PythonToolkitProxy这个类是我们的核心调用逻辑，他提供一个动态代理入口，它让Python代
码可以像
调用本地函数一样调用Java工具包：
1
2
3
4
5
6
7
8
classPythonToolkitProxy:
def __init__(self, toolkit_name):
self.toolkit_name = toolkit_name
def __getattr__(self, operation_name):
async def async_operation_method(*args, **kwargs):
return await call_toolkit_async(self.toolkit_name, operation_nam
return async_operation_method
这样，Python代码就能这么写：
1
2
# 这样调用就行
了，简单直观
result = await example_toolkit.get_project_info(project_id="123")
就可以调用到在Java中的代码了：
1
2
3
4
publicclassExampleToolkit{
public Object get_project_info(String projectId){
return null;
}
```

## PDF 第28页

[查看原页](RAW.pdf#page=28)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
5 }
运
行
参数捕捉机制
参数处理这块我们踩了
不少坑。最开始位置参数和命名参数混用会出问题，后来做了参数规范
化：
1. 捕 获运
行
参 数 ： 使用装
饰器 ， 标 记 在对应 的函 数上 ， 那么就 能 获取 到 函 数中的临 时变 量
了；
2. 参数统一 : 优先使用命名参数，位置参数自动转换；
3. 类型转换 : DynamicEntity等Java对象自动转换为Python字典；
4. 序列化 : 所有
参数最终都序列化为JSON传递给Java端；
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
def capture_execution_variables_async():
"""装
饰器：捕获异步Python函数执
行
def decorator(func):
时的局部变量"""
@functools.wraps(func)
async def wrapper(*args, **kwargs):
captured = {}
def tracer(frame, event, arg):
if event == 'return'and frame.f_code == func.__code__:
try:
# 复制局部变量，过滤掉内部变量
for key, value in frame.f_locals.items():
ifnot key.startswith('_') and key not in ['args
# 检查值是否可序列化
try:
json.dumps(value, default=str, ensure_a
captured[key] = value
except (TypeError, ValueError):
# 对于不可序列化的对象，转换为字符串
captured[key] = str(value)
except Exception as e:
print(f"ExecutionVariableMonitor capture error: {e}
return tracer
sys.settrace(tracer)
try:
result = await func(*args, **kwargs)
finally:
sys.settrace(None)
# 保存变量到全局context中供Java侧获取
if hasattr(sys.modules[__name__], 'captured_variables'):
sys.modules[__name__].captured_variables.update(captured)
else:
```

## PDF 第29页

[查看原页](RAW.pdf#page=29)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
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
sys.modules[__name__].captured_variables = captured.copy()
# 输出捕获的
变量，使用特殊
格式供Java端解析
for key, value in captured.items():
print(f"VARIABLE_CAPTURED:{key}={json.dumps(value, default=
return result
return wrapper
return decorator
通过注解捕捉到运
行
参数后，会在完成运
行
后，由java解析，并存储到redis里面。当下次执
行
的时候，会从redis取出会话中的参数。以实现在下轮对话中，可以感知到上轮对话的
变量及内
容。
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
# 第一轮对话
def main():
a = 1
# 第二轮对话
a = 1 # 通过redis回放回来的参数
def main():
print(a+1)
Toolkit Mapper [Java]
ToolkitMapper是整个工具包体系
工具包实现。
的调度中心，它负责把Python的调用请求路由到具体的Java
工具包映射与路由
核心路 由 逻 辑 很直 接 ： 根据 toolkit_name找 到 对应 的实 现 类 ， 然 后 调用 对应 的operation方
法。但实际实现中有
几个关键点：
```

## PDF 第30页

[查看原页](RAW.pdf#page=30)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
动 态 路 由 AgentToolkitManager来执
行
类型适配 : 不同类型的工具包有
: 通 过 sessionId 找 到 对 应 的 Agent3 实 例 ， 再 通 过 Agent 的
具体操作；
结果包装 : 所有返回结果都通过ResultWrapper进
不同的接口，ToolkitMapper负责做适配；
统一包装；
行
数据传递机制
为了
实现让历史Python运
行
的临时参数，可以被传递到下次运
行
Python的过程中，我们在数
据传递过程中，在Java内部通过Base64将原始数据反编译，然后使用参数，传递到python脚
本中。Python脚
本拿到Base64之后，自
行
解码，将数据在内存恢复到目标参数中。
方法调用机制
我 们 在Agent、
Class。每个Agent、
Mcp 的Toolkit中， 将 技能 /工 具 映 射 成方 法 ， Agent/McpServer 映 射 成
McpServer都对应一个独立的Toolkit。
因此当某个Toolkit被调用时，将会拿到自身的class、
泛化调用。
方法名，从而找到对应的技能/工具，进
行
▐ Toolkit工具包
```

## PDF 第31页

[查看原页](RAW.pdf#page=31)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
Toolkit体系
们设计了四
是整个Agent能力的具体体现，它把抽象的"智能助手"落地为可执
行
大类工具包，每类都
有自己的特色和应用场景。
的工具包。我
Custom Card Toolkit
自定义
卡片工具包是我们为了解决"Agent怎
话太单调，我们需要更丰
富的交互形式。
么和用户交互"这个问题而设计的。传统的文本对
卡片组
卡片系
件系
统
统采用了
组
件化的设计思路，每个卡片都是一个独立的UI组
件：
支持的卡片类型：
转人工卡片 : 支持用户有转人工意图时，发送卡片进
行
运维卡片 : 用户想要进
行
运维操作时，将会发送运维卡片；
转人工处理；
Mcp Toolkit
Mcp（Model Context Protocol） Toolkit是我 们 对接 外 部 服务 的标 准化接口。通 过Mcp协
议，我们可以快速集成各种外部能力，而不需要为每个服务单独开
发适配
器。
```

## PDF 第32页

[查看原页](RAW.pdf#page=32)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
Agent Toolkit
Agent Toolkit实现了Agent之间的协作机制
成所有
工作，需要和其他专业Agent协作。
。在复杂任务场景下，单个Agent可能无法独立完
A2A协议支持
A2A（Agent to Agent）协议定义了Agent间交互的标准格式：
任务分发 : 主Agent将复杂任务分解后分发给子Agent；
进度汇报 : 子Agent定期汇报任务执
进度；
行
异常处理 : 子Agent执
行
失败时的异常上报机制；
资源协调 : 多个Agent竞争同一资源时的协调机制；
工具包注册与管理
工具包的注册与管理是整个Toolkit体系
计了两
套并
行
场景，互不耦合。
的基础设施，它支持多种注册方式和管理机制
。我们设
的注册体系：基于接口的动态工具包和基于注解的声明式工具包，它们各有适用
动态工具包注册
动态工具包是我们的核心注册机制，通过实现DynamicToolkit接口来定义
工具包：
1
2
3
4
5
6
7
8
public interface DynamicToolkit {
String name(); // 工具包名称
String getClassComment(); // 工具包描述
Map<String, String> getMethodPython(); // Python方法定义
Map<String, Type[]> getMethods(); // 方法参数类型
Map<String, String[]> getParameterNames(); // 参数名称
Object execute(String methodName, String execId, Map<String, Object> par
}
接口驱动 : 所有动态工具包都
实现DynamicToolkit接口，保证接口的一致性；
运
行
时注册 : 工具包可以在运
行
时动态注册和卸载，支持热插拔；
元数据自描述 : 工具包自己描述自己的能力和接口，无需外部配置；
典型的动态工具包实现：
1
2
3
@Component
publicclassExampleDynamicToolkitimplementsDynamicToolkit {
```

## PDF 第33页

[查看原页](RAW.pdf#page=33)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
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
15
16
17
18
@Override
public String name(){
return"example_toolkit";
}
@Override
public Object execute(String methodName, String execId, Map<String, Obj
// 动态分发到具体方法
switch (methodName) {
case"get_project_info":
return getProjectInfo(params);
// 其他方法...
}
}
}
注解式工具包注册
注解式注册是一种声明式的工具包定义
方式，适合结构相对固定的工具包：
1
@ToolkitComponent(
2
python = "system_toolkit",
3
description = "系
统
级
工具包，提供基础的
系
统操作能力"
4
)
5
publicclassSystemToolkit {
6
7
@ToolkitOperation(python = "send_message")
8
public ToolkitResult sendMessage(Map<String, Object> params){
9
// 发送消息的具体实现
10
}
11
12
@ToolkitOperation(python = "get_current_time", enabled = true)
13
14
public ToolkitResult getCurrentTime(Map<String, Object> params){
// 获取当前时间的具体实现
15
}
16
}
声明式配置 : 通过注解声明工具包的元数据，简化配置；
编译时检查 : 注解在编译时就能发现配置错误；
Spring集成 : 与Spring的Bean管理机制无缝集成；
注册机制分离设计
两
种注册机制在实现上完全分离，各自有独立的处理流程：
```

## PDF 第34页

[查看原页](RAW.pdf#page=34)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
独立 注 册表 包；
: DynamicToolkitRegistry和AnnotationToolkitRegistry分 别管 理 两 类工 具
统一访问 : ToolkitMapper提供统一的访问接口，屏蔽底层注册机制
互不干扰 : 两
种机制可以独立开启或关
闭，不会相互影响；
的差异；
反思
▐ 开
发一个Agent，需要做的几件事情
经过三轮Agent的升级与优化，关
核心要素：
于如何打造优质AI Agent，我结合Agent实
践经验总结几点
1. Prompt组
装与上下文工程的合理设计
上下文管理影响多轮对话的稳定性。
在搭建Agent时，需要对Prompt进
Agent运
行
过程的不同形态下，上下文的
推荐的Prompt/上下文开
发过程：
行单独的设计，明确Prompt的
装
方式等。
组成部分、上下文的选
择、
组
```

## PDF 第35页

[查看原页](RAW.pdf#page=35)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
可以先准备一段完整的比
较粗糙的prompt，其中记忆、经验相关
的内容都先使用mock的
方式拼接在其中，然后使用LL
M的api对prompt的效果进
行
初步验证；
验证没问题后，可以进入代码实现，将prompt按逻辑和结构拆分成多个部分，例如自我介
绍、工作机制
入格式
、输出格式
、示例等，然后分别实现每个部分；
、输
后 续 需 要 在运
过 程中
断
不
行
调整 prompt， 可 以 在每次发现bad prompt、出现的问题和自己的思路发给LL
M，让LL
M帮助优化；
case的时候 ， 将目前 的
我们在前两个版本的时候，Prompt组
装，是没有系
统性、结构性设计的，这也就导致了过程中
出现了一个900多
的超级
行
大的Prompt，它里面各个位置的内容都是比
较乱的。Prompt和上
下文的
装
组
、拼接经过了
单独的设计，实现的代码中，对其组
装也模板设计模式
、Builder设计
模式的
组合，来完成Prompt的拼接。
2. Agent的工程架构设计也很重要
工程架构直接影响交互体验的流畅度。
工程层面，Agent需要考虑：Agent运
行
何定义和管理、日志/监控/可观测/评测
过程如何持久化、优雅上下线
制度的建立、记忆如何管理。
、
任务的完成与失败如
"模型决定上限，工程决定下限"这种说法就像曾经的"PHP是世界上最好的语言"一样片面。实
际上二者是相辅相成的关系
。
有些产品即便采用了Claude这样的强大模型，整体效果反而不如
使用Deepseek但工程实现更优秀
的同类产品。
关键在于模型能力与工程细节的契合度。在工程层面比
如工具调用编排
、用户交互设计、内部
流程优化等，都需要在工程层面深度打磨，才能充分发挥模型潜力。过分迷信模型能力而"死等
模型升级"是不可取的。
3. Agent提高运
行
质量和稳定性，可以通过让他自我积累、自我学习
经验积累则确保跨会话的一致性。
不论是JSON、文本前缀还是Coding驱动，经验都是一个好东西。它可以大大地提高返回数据
的稳定性。这里分享几篇论文：
《ExpeL: LL
M Agents Are Experiential Learners》
《How Memory Management Impacts LL
M Agents: An Empirical Study of Experience-
Following Behavior》
```

## PDF 第36页

[查看原页](RAW.pdf#page=36)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
《Get Experience from Practice: LL
M Agents with Record & Replay》
简单来说，经验的
组
装，就是：
1 收集 -> 加工 -> 存储 -> 检索
在Agent运
行
过程中， 收集一切有用的信息，随后在完成运
后，通过 LL
M 或者各种解析逻
行
辑加工成一段文本、一个json，代表本次执
的起因
行
、经过、结果、思考等信息。随后存储到
数据库中（不仅局限于向量数据库）。在Agent运
行
阶段，将用户文本做简单加工，随后进
行
检索。 只不过在工程层面，检索过后的结果，可以用作“回放”，可以用作“Prompt”拼接。单
纯的向量数据库检索，不一定能让经验检索变得准确，我们目前正在向图索引的方向探索，让
图谱的能力辅助经验的检索与加工。
▐ 展望
目标定位
我们的最终目标是致力于让它成为可靠的"1.5线"答疑助手，具备初级程序员（1-3年）的知
储备和问题解决能力，同时拥有自我进化和持续学习能力。
识
优化路径
1. 除 了
调用 过 程是代 码 ， 拼接 Prompt能 否 变 得 更 加 动态 ？甚
至 在Cmd、Thought阶 段的
Prompt，都是由Agent自我选
择
Toolkit拼装
的；
2. 在IntentPlanner阶段，并非是不可循环的，我们后续会把IntentPlanner、TaskExecutor
的底 层 能力合 并 ， 提供一个通用 的Coding驱 动Agent 模 型 ， 基 于此 模 型 ， 实 现 各 层 的
ReAct操作；
3. 任务间的上下文隔离还需要做的更加精细；
4. 知
识点和经验的数据，需要持续保鲜；
5. Mcp和Agent的
深度和广度，都需要持续提升；
6. 开
发一个桌面应用程序，随时随地可以唤起；
7. 日志、观测、报表
、监控、评测机制
的的完善。
¤ 拓展阅读 ¤
```

## PDF 第37页

[查看原页](RAW.pdf#page=37)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
3DXR技术 | 终端技术 | 音视频技术
服务端技术 | 技术质量 | 数据算法
大淘宝技术
大淘宝技术官方账号
967篇原创内容
公众号
阅读 5096
```
