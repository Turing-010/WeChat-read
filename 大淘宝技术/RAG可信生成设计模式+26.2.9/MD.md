# 设计模式Trustworthy Generation：提升RAG信赖度：PDF文本转写

> 这是原始PDF文本层转写，不是学习摘要。页码为PDF物理页序；图表、代码版面和图片文字不能完整表达在此文本层。已查看图像的内容和质量问题见AI学习笔记及META.json。

[原文PDF](RAW.pdf) · [AI学习笔记](AI_RAG可信生成设计模式.md) · [处理与质量记录](META.json)

## PDF 第1页

[查看原页](RAW.pdf#page=1)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
设计模式Trustworthy Generation：提升RAG信赖
原创
直播技术团队 2026年2月9日 01:17 浙江
大淘宝技术 5人
度
本文介绍了名为 Trustworthy Generati
on
的设计模式，旨在提升 RAG 系
统生成内容
的信赖
度，即真实性（是否准确、无幻觉、无偏见）与完整度（是否全面、不遗漏关键信
息）。文章系
统分析了 RAG 信赖
度不
足
的四
大根源：检索错误、内容可靠性问题、前置
推理错误、模型幻觉。针对这些问题，文章提出围绕“可解释、可追溯、可反思、可监管”
四个层次的解决
方
案。作者指出该模式的权衡点：会增加系
统复杂度与计算开销，并存在
误过滤风险；并提供了三种替代路径——双知
识库交
叉验证、增强过程透明性、带置信分
的引用标注。
前言
Trustworthy Generati
on设计模式的目的是提升RAG生成内容的信赖
两个方面：真实性和完整度，该设计模式是一系列技术和功能模块的
面向的问题域、解决
方
案以及一些优劣权衡点来展
开介绍下。
度，这里的信赖
度包含
组合，下面从该设计模式
Problem
RAG在此就不过多赘述，目前实
践中RAG技术应用非常广泛，RAG是由两个主要动作
组成，
Retrieve和Generate，本质是在做Context Engineering中的内容补充，虽然我们在知
识库
中补 充、梳 理、构建 的都是我 们 认 为高 质量和真 实 的信 息 ， 但是RAG最 后 返 回 的是LLM
Generate的内容，该内容的生产会因为以下几种情况（不仅限于）出现信赖
度不
足
的问题：
1. 检索错误，包含a.准确率问题，即检索召回的部分信息相关性很弱（检索是按照语义向量
的 相似 性召 回 ，高 向量相似 度不 等 同 于高 内 容 相关 性， high similarity≠high
relevant），b.召回率问题，即知
识库中有些非常相关
的内容没有被检索召回；
2. 内容可靠性问题，比
内容有矛盾冲突的情况；
如召回的信息虽然都是相关
的，但是
有些内容存在偏见、过期或本身
```

## PDF 第2页

[查看原页](RAW.pdf#page=2)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
3. 前置推理错误，这个问题一般是由于在检索前做的query扩写，或者是step back问题抽象
出现一些偏差，导致最终检索的方向是错的，从而导致检索出来的内容也是偏差的；
4. 模型幻觉，在面向一个复杂问题做RAG时，由于问题的复杂和召回内容的繁杂，模型在最
后Generate的时候，就容易出现自导自演加戏
的情况；
以上所列举的情况，基本上涵盖了RAG使用过程中的大部分问题，但是针对这些问题，无法根
解，本文所说的设计模式也只是在一定程度上通过一些技术和人机交互的结合，来降
低问题出
现的概率，提升对于问题出现的感知，从而提高RAG的信赖
度。
Soluti
on
解决
方
案围绕着提升信赖
度的四个层次来展
开：
1. “解决
不
了事情要明确说出来”，不要自己
发挥，这是信赖
建立的第一步；
2. “说话要有依据”，生成的内容，关键的信息要附带内容出处；
3. “深思熟虑，为自己的言论负责”，检索过程中可以有反思和递进，同时对于返回的结果做
好质量卡口；
4. “建防护、受监管”，构建面向信赖
度提升的工程技术链路，同时增加人机交互的监督。
▐ 信息关联度识别
本质上我们在工程链路中使用RAG，是为了给当前query补充关联的信息，因此，如果RAG模
块 a.返回有关联的信息 且 b.在没有
检索到足够有关联信息的时候，明确不返回，能够做到这
两点，可以比
较大的提升人们对其的信赖
度。
当前比
较多的问题在于RAG经常返回一些相似但是不相关
的信息，提升对于相关信息的“识别”
是问题的关键，这里
有三种做法：
1. 相似度threshold设置：RAG的检索是计算query和知
识embedding index的相似度，然
后按照相似度降序返回k个，但是对于这个相似度本身没有做底线
threshold的要求，这里
可以设定一个threshold值，小于该值的相似度检索信息就不做召回（该threshold需要针
对各自的场景去摸索和调优）；同时有研究表明，当
两个信息没有关联性的时候，向量相
的趋势，截止到这个相似度分值之后的信息都是
似度会陡然下降，这里可以判断一个陡
关联性不大的；
2. 问题类型分类：就是在RAG之前做问题分类，如果不属于当前RAG知
识库可覆盖的信息类
型范围，就不做RAG的调用；
3. 领 域关 键 词 识 别 ： 只有在检 测 到 query中有包 含 特 定 的关 键 词 或者 领 域 术 语 时， 才 触 发
RAG调用，这是一种非常严格的限制
。
降
```

## PDF 第3页

[查看原页](RAW.pdf#page=3)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
▐ 引用出处说明
第二种提升RAG信赖
度的方式是，针对RAG生成的内容，明确标识出这部分结果信息来自于哪
段知
识的引用，和写论文引用他人观点或者文章内容类似。
这里引用说明的实现有三种方式，分别是：
1. 信息直接来源引用说明，即只要指出这段内容来源于哪个知
识文档（如果有chunking的
话，就是某个chunk，后面统一称doc），相关
的prompt和结果如下所示：
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
template = """Answer the question based on the following sources, using
SOURCES:
{sources}
QUESTION: {question}
INSTRUCTIONS:
1. Use information only from the provided sources
2. Provide an answer with in-line citations using brackets, e.g.,
"Eins
3. Use the source ID in brackets [1], [2], etc., corresponding to the s
4. Cite ALL facts with their source IDs
5. If multiple sources support a fact, you can include multiple citatio
6. If the information isn't in the sources, say "I don't have enough in
7. Include a "References" section at the end listing all the sources yo
Your answer should be comprehensive, accurate, and include citations fo
"""
附带引用来源的结果示例
2. 有判断
的引用来源说明，先判断
这段内容是否需要引用说明来增加信赖
度，这个判断可能和
当 前 应用 的领 域 ， 以 及 该事 实 内容 对于整 体 内容 的影响 来评 估 ，比
如这段文 字： ”王二生 于
1990年3月3日，出生在一农民家庭，于2015年被评为全
国劳模“，那么对于王二的出生日期和
出生情况，不需要引用做说明，对于后面获得荣誉，要指明出处，不然如果胡诌的话影响比
较
大；这里
对于返回内容哪些需要进一步说明引用出处，需要面向特定领域做小模型微调，会有
额外的成本。
3. 基 于token级
别 的关 联 说 明 ， 在面 向一些 复杂 问题的回 答 时， 可 能 会检 索 召 回比
较 多 的
doc，同时最终结论生成的内容中每个段落，都是结合了多个doc的内容来关联生成的，因此
还是会存在模型会生成逻辑错误（不同的内容编排形式可能就会引入重大事实差异）或事实错
```

## PDF 第4页

[查看原页](RAW.pdf#page=4)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
误（参考的doc太多，上下文一长，容易自我发挥）；基于token级
实际实现的类库，整体示意如下图所示：
别的关联说明，当前没有
Token级
别关联引用说明
▐ 自我批判和自我反思
在我们设计和应用RAG时候的初衷是，为当前用户的query补充相关联的高质量信息，但是
有
时候随着事情的
发
展，会有一些事与愿违的情况
发生，没有帮助降
低模型幻觉，反而助长了模
型幻觉产生的可能；这里
有个认知前提，我们认为知
识库里面的内容是精心梳理、
准备和录入
的，因此在使用中对这部分内容是缺乏批判和反思的，但是事实证明，知
识库中的内容是否足
够正确 以及 知
识库中的内容是否比模型本身能力可返回能力更高质量，这不是一个固定的结
论或判断，因时因事而异。
批判性的看待和在此过程中增加反思，对于提升RAG信赖
度，亦显得非常重要。
```

## PDF 第5页

[查看原页](RAW.pdf#page=5)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
CRAG
首先先来介绍下带自我批判的RAG，也称Corrective retrieval-augmented generati
on
(CRAG)，主要解决两个问题：
a. 评估检索出来的doc的质量（信息正确性），对于低质量doc做过滤，或者关联其他知
或者外部搜
索来补充正确的数据；
b. 评估检索出来的doc的质量（关联性），对于doc中和query不相关
的内容做裁剪；
识库
整体流程示意如下：
CRAG流程示意图
下面是来自于langchain中LLM-based的doc打分实现：
1
2
3
4
def grade
documents(state):
_
"""
Determines whether the retrieved documents are relevant to the que
Args:
```

## PDF 第6页

[查看原页](RAW.pdf#page=6)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
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
state (dict): The current graph state
Returns:
state (dict): Updates documents key with only filtered relevan
"""
print("
---CHECK DOCUMENT RELEVANCE TO QUESTION---
")
question = state["question"]
documents = state["documents"]
# Score each doc
filtered
docs = []
_
web
search = "No"
_
for d in documents:
score = retrieval
_grader.invoke(
{"question": question,
"document": d.page
_
content}
)
grade = score.binary_
score
if grade == "yes":
print("
---GRADE: DOCUMENT RELEVANT---
")
filtered
_
docs.append(d)
else:
print("
---GRADE: DOCUMENT NOT RELEVANT---
")
web
search = "Yes"
_
continue
return {"documents": filtered
_
docs,
"question": question,
"web
sea
_
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
# Data model
class GradeDocuments(BaseModel):
"""Binary score for relevance check on retrieved documents.
binary_
score: str = Field(
"""
description="Documents are relevant to the question,
'yes' or
)
# LLM with function call
llm = ChatOpenAI(model="gpt-4o-mini"
, temperature=0)
structured
llm
_
_grader = llm.with
structured
_
_
output(GradeDocuments)
# Prompt
system = """You are a grader assessing relevance of a retrieved docume
If the document contains keyword(s) or semantic meaning related to
Give a binary score 'yes' or 'no' score to indicate whether the do
grade
_prompt = ChatPromptTemplate.from
_
messages(
[
("system"
("human"
,
, system),
"Retrieved document: \n\n {document} \n\n User quest
]
)
retrieval
_grader = grade
_prompt | structured
llm
_
_grader
```

## PDF 第7页

[查看原页](RAW.pdf#page=7)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
Self-RAG
Sefl-RAG，带自我反思的RAG，主要有以下三个职能：
a. 评估检索到的doc的相关性和质量，过滤掉相关性不大或低质量的doc；
b. 针对当前检索到的doc，判断
是否需要进一步做信息检索召回（这部分设计有点Agentic
RAG的意思，不过Agentic RAG面向的是一个全面和泛化的“知
识库”，包含文档知
识
接
口、search等）；
c. 评估doc的内容，判断
以比
较好利用和结合基模的快速发
是否直接基于底层LLM做问答召回，来替换该部分doc内容（这里可
展红利）；
、
Self-RAG流程示意图如下：
Self-RAG流程示意图
▐ 防护&人机监管
Guardrails
整体防护是围绕RAG核心两个动作（Retrieve和Generate）划分了4个阶段，配合相关
进
设计的，具体如下：
行
Pre-retrieval阶段：过滤掉不在能力范围的内的query调用，对于doc进
行
过滤掉错误或者过期的doc；
的手段
正确性评估，
```

## PDF 第8页

[查看原页](RAW.pdf#page=8)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
Post-retrieval阶段：过滤掉低于相似度阈值的doc，针对检索返回的doc进
行
正确性验
证和隐私合规性验证；
Pre-generate阶段：过期信息过滤，比
如过滤掉1年前的doc，关键信息设置多个引用来
源交
叉验证；
Post-generate阶段：针对生成的结果做评判和反思，检查结果内容相较于引用内容是否
存在幻觉等；
Human Feedback
Human-in-the-Loop，可以发生在RAG流程中的每个核心步骤中，如下示意：
Hu
man feedback关联设计示意
基 于人的交互 监 督 设 计 ，背 后都会涉 及 到比
较 多 的专家人员 的人力投入，因 此 围 绕 human
feedback设计的初衷，都是要回收关键的再训练样本数据，去做针对性的工程以及模型的调
优工作。
Considerati
on
在上述说的提升RAG信赖
度的方式中，基本上都会一定程度上增加整体架构的复杂度以及增加
对于模型的调用，从而会影响整体的性能和开销，因此是否使用，使用哪些方式和手段，都需
要结合实际去做权衡
。
▐ 局限性
RAG在检索的时候非常依
赖
向量的相似度计算的值，上面有提到一个相似度分值threshold的
问题，但是这个threshold在实际过程中，不一定能够非常直观的被发现或者被决定，需要结
```

## PDF 第9页

[查看原页](RAW.pdf#page=9)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
合一些评测进
行
化，需要定期检测和判断
调整，同时该值还会随着知
调整。
识库内容的
变化以及知
识领域的扩充，也会发生变
同时本模式在实现设计中，有针对检索内容的打分、质量判断
、正确性判断，然后基于这样的
判断做一些过滤；这些动作本身都
有一定的成功率，如果过滤策略严格，那么同时也会带来另
外一个负面影响，就是会误杀掉一些有用的信息，从而最终影响返回的结果。
▐ 可选的其他方式
如果针对该设计模式基于权衡下不考虑采用，可以有
另外三种方式推荐：
识库（知
1. 给RAG增加另外一个知
识库做信息检索召回，然后针对双方结果做交
识的维护和组织方式都是独立的），每次query面向两个
知
叉验证，提升整体信息的可靠性；
2. 让过程更透明，给出检索出来的信息概述，以及最终得出结论的思考，变相增加整体过程
的解释性，从而提升信赖
度；
3. 针对返回的结果，附上引用来源，同时在引用来源上增加“置信分”，给到用户自己判断某
些段落的信息表
达
的正确性和后置
为的依
程度。
行
赖
参考资料
https://learning.oreilly.com/library/view/generative-ai-design/9798341622654/
https://langchain-ai.github.i
o/langgraph/tutorials/rag/langgraph_crag/#create-index
团队介绍
本文作者 Mari
o，来自淘天集团-直播技术团队。淘宝直播作为全
球领先的直播电商平台，正
在重新定义人与商品、人与内容的连接方式。我们致力于打造沉浸式
、互动式的购物体验，让
数亿用户在这里发现好货、感受乐趣。无论是时尚穿搭、美食评测，还是科技新品发布，淘宝
直播都在引领电商
业的创
行
新潮流。同时淘宝直播也在推进打造行
业领先的AI数字人技术，实
现虚拟主播、智能互动、个性化推荐等创
新功能。
¤ 拓展阅读 ¤
```

## PDF 第10页

[查看原页](RAW.pdf#page=10)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
3DXR技术 | 终端技术 | 音视频技术
服务端技术 | 技术质量 | 数据算法
大淘宝技术
大淘宝技术官方账号
967篇原创内容
公众号
阅读 2112
留言
写留言
还没有
留言，来写首评
```
