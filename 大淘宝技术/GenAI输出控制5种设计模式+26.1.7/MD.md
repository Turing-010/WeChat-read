# GenAI输出内容控制的5种设计模式：PDF文本转写

> 这是原始PDF文本层转写，不是学习摘要。页码为PDF物理页序；图表、代码版面和图片文字不能完整表达在此文本层。已查看图像的内容和质量问题见AI学习笔记及META.json。

[原文PDF](RAW.pdf) · [AI学习笔记](AI_GenAI输出控制5种设计模式.md) · [处理与质量记录](META.json)

## PDF 第1页

[查看原页](RAW.pdf#page=1)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
GenAI输出内容控制
的5种设计模式
原创
直播技术团队 2026年1月7日 02:17 浙江
大淘宝技术 7人
本文系
统介绍了在生成式人工智能（GenAI）应用中控制模型输出内容的五种设计模式，
并对比了各模式的适用场景、优缺点及典型反模式，为开
发
者提供了一套结构化的
输出控
制
方法论。
写在前面
我们在结合LLM做应用的时候，如何去约束模型的生成样式
格式
、
、风格，这个是一些比
较常
见的问题，对于通用问题沉淀下来的通用解决
方
案，有一个大家熟悉的名词，设计模式，笔者
下面 基 于如何 在大家 的应用中去 更方 便 的控制
输 出 内容 style， 介 绍 五 种 设 计 模 式， 分 别是
Logits掩 码 模 式（ Logits Masking）、语 法 模 式（ Grammar）、样式转 换 模 式（ Style
Transfer）、逆 向中和模 式（Reverse Neutralizati
on） 以 及 内容 优 化 模 式（Content
Optimizati
on）。
模式一：Logits Masking
Logits Masking，Logits掩码模式，介绍该模式之前，简单
什么，另外一个涉及到Logits Masking后续实现的束搜
说下两个概念，一个是Logits是
索（Beam Search）的概念。
LLM在生成结果的时候，是token by token生成的，LLM在每个token生成时，给的不是一
个token，是给了一系列的tokens，同时附带了模型对这些tokens作为下一个token输出的推
荐 分 值 ， 之 后 再 做 激 活 （比
如softmax） 得 到一个整 体 加 和等 于1的概 率 值 ， 后面 会结 合
Sampling算法和Temperature，来决定哪个token作为要输出的那个结果。
然后再来介绍下束搜
索，束搜
索解决的是如何在确定性优先（每次输出都是最高概率的那个
token）和随机创
新（引入Temperature，在比
较高概率的tokens小集合中做一定的随机选
```

## PDF 第2页

[查看原页](RAW.pdf#page=2)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
取）之间的权衡，在束搜
索的机制下，LLM会在生成token的过程中维护多个队列（通过束宽
beam_width来控制），意味着每次在生成下一个token的时候，中间会保留beam_width个
可能的候选结果分支（比
如概率最高的beam_width个tokens），然后每个分支各自继续生成
下一个结 果 的token概 率 列表 ， 每 个分支 选
择
beam_width * beam_width个分支做修剪，按照
beam_width个可 能 候 选 结 果 ，接 着对这
新增tokens的logits加和的
降序排列，只保
留加和最高的beam_width个，整体持续迭代，直到句子完结（<EOS>出现或者达到长度限
制）。
Logits掩码，是在模型内部进
每一步的token选
择
束搜
行
索的时候，增加用户给于的其他一些约束和限制，去干预
，最后达到控制LLM输出内容符合自身期望的结果。
▐ Cases
这里列举一些可能可以使用该设计模式的场景：
品牌一致性，在述说A商品相关
的信息时，需要使用该商品对应的品牌主打的特性词汇，比
如运动、舒适，而不要使用B商品品牌主打的品牌特性，比
如优雅、大方等；
准确性，比
如在输出一份账单
的时候，账单
的编码以及账单金额只输出在特定位置，不在
正文中重复出现，避免多次输出可能带来的不一致性；
合规性，在引用A公司的案例进
行
陈述的时候，不要同时引用其竞争对手B公司的案例，以
免造成商业敏感和合规等问题；
风格指南，可能对于
输出文档的语法、标点、
格式或术语有特定的要求。
▐ Antipattern
该模式的反例，估计大家都
比
较熟悉，就是对模型生成的结果，使用rule set进
行
校验，如果
不仅会新增很多
不符合，打回让模型重新生成，一直到生成的结果满足
输出规则为止；该方式
不必要的模型调用（成本），同时也会增加本次服务的RT（体验）。
Logits Masking模式的反例描述
```

## PDF 第3页

[查看原页](RAW.pdf#page=3)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
▐ Solution
Logits掩码（Logits Masking） 的工作原理如下：
1. 用户可以针对
输出内容的约束，生成一些Rules，这些Rule是可以通过程序来自己实现的
（比
如对于一些关键字、词的屏蔽）；
2. 在生成过程的每一个中间步骤，获取当前可能的后续词元（continuati
ons）集合，对于不
符合预设规则的候选续写项，将其对应的logits（模型输出的原始分数）置零，从而在概率
分布中彻底排除这些非法选项；
3. 只要还存在至少一个符合规则的合法续写路径，生成过程就可以继续向前推进；
4. 如果 当 前 状 态 没有符 合 条 件 的续 写 选 项 ， 或该状 态 此 前 已被 标 记 为“死 胡同 ”（ dead
end），则需要回退一步（backtrack），尝试其他可能的前序选
；
择
5. 当
达到预设的最大重试次数后，若仍无法生成满足所有规则的内容，则向用户返回拒绝响
应，说明“无法生成符合要求的内容”。
相关
的流程图如下所示：
Logits Masking流程图
```

## PDF 第4页

[查看原页](RAW.pdf#page=4)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
具 体 实 现 上 写一 个单 独 的 继 承 了 transformers.generati
on.logits_process 中
LogitsProcessor的处理类，复写__call__方法，在该方法中
实现自己定义
的rule的程序化逻
辑。
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
from transformers import pipeline
MODEL
_
ID = "/Users/mario/.cache/modelscope/hub/models/LLM-Research/Phi-
pipe = pipeline(
task="text-generation"
,
model=MODEL
_
ID,
kwargs={
"return
full
_
_
text": False,
},
model
_
kwargs={}
)
results = pipe(input
_
message,
max
new
_
_
tokens=512,
do
_
sample=True,
temperature=0.8,
num
_
beams=10, # 束宽为10
use
_
cache=True,
logits
_processor=[<Your
Customized
_
_
Processor extends Log
模式二：Grammar
语 法 模 式， Grammar， 基 于语 法 的字符输 出 限制， 可 以 理 解 为一种 内置 的特殊 的Logits
Masking， 可 以 类比内置 了一套 正则表
达 式（ 实 际 使用 的是GBNF， Grammar-Based
Normal Form，基于语法的范式），用于Logits的权重调整，从而控制最终输出的内容和样
式。
比
如一段控制时间格式
输出的Grammar如下所示：
1
2
3
4
5
6
7
8
grammar
str = """
_
timestamp_
literal ::=
{ t 'yyyy-mm-dd hh:mi:ss' } |'date
literal time
_
_
literal'
date
literal ::=
_
{ d'yyyy-mm-dd'}
|mm-dd-yyyy| mm/dd/yyyy| mm-dd-yy| mm/dd/yy| yyyy-mm-dd
| yyyy/mm/dd| dd-mon-yyyy| dd/mon/yyyy| dd-mon-yy| dd/mon/yy
time
literal ::=
_
```

## PDF 第5页

[查看原页](RAW.pdf#page=5)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
9
10
{ t 'hh:mi:ss'}|hh:mi:ss[:mls]
"""
由于该模式的实现需要模型在推理引擎中集成GBNF解析器，因此不是所有
的LLM都支持，目
前从大面来看，闭源的模型基本都
不支持，开源的模型在这块的支持会好一些，如果是私有
部
署的模型，也可以自己在推理框架中集成这个能力。
▐ Antipattern
当前的做法是在prompt中写清楚需要返回的信息的格式，比
如是JSON，或者是一些特殊的
sql，虽然Anthropic也推荐了这样的做法，但是这个方式
不一定能保证结果格式的
输出一定能
如你 所 愿 ，头
部 的大模 型 在模 型 能力上有比
较 好 的调优 ， 可 以 在更大概 率 上 遵 循用 户 在
prompt中约束的指令，但是小一些的模型，在这方面的表现就会比
较差，同时不管是头
源 模 型还 是一些自己 部 署 的小 模 型 ， 在输 出 格式遵 循 的确 定 性上 ，都是
部闭
有一定 的概 率 ；
LangGraph（25年6月）的实现是通过在一个额外的模型调用，去重新调整返回格式到目标格
式上，这样的做法也不是特别推荐，因为会有额外的调用的损耗。
▐ Solution
该模式整体的处理流程如下，步骤上和Logits Masking类似，原理上稍有区别：
Grammar执
流程
行
```

## PDF 第6页

[查看原页](RAW.pdf#page=6)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
下面是一个简单
的针对数据问题解答结果的
输出约束的例子，该例子中的Grammar限制了
输出
结果中可以出现任
意数量的空格和制
表符（ws ::= [ \t\n]*），数字0-9且后面可以跟任
意空
格和制
表 符 （ num ::= [0-9]
+
ws） ， 变 量必 须小 写 字母 开头（ident ::= [a-z] [a-z0-
9_]* ws），项term可以是标识符或者
单个数字或者是括号包裹的表
达式（term ::= ident |
num | "(" ws expr ")" ws，即不太能出现z = 1 +
2这样的结果），等等。
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
34
35
36
37
38
from transformers import pipeline
from transformers
_
cfg.grammar
_
utils import IncrementalGrammarConstrain
from transformers
_
cfg.generation.logits
_process import GrammarConstrai
MODEL
_
ID = "/Users/mario/.cache/modelscope/hub/models/LLM-Research/Phi
pipe = pipeline(
task="text-generation"
,
model=MODEL
_
ID,
kwargs={
"return
full
_
_
text": False,
},
model
_
kwargs={}
)
def get
_
expression
that
solves(math
_
_
_problem: str) -> str:
system
_prompt = """
You are a math instructor. I will ask you a math question.
Respond with the mathematical expression that can be used to solve
"""
# load the grammar
grammar
str = """
_
root ::= (expr "=" ws term "\n")+
expr ::= term ([-+*/] term)*
term ::= ident | num | "(" ws expr ")" ws
ident ::= [a-z] [a-z0-9
]* ws
_
num ::= [0-9]+ ws
ws ::= [ \t\n]*
"""
grammar = IncrementalGrammarConstraint(grammar
_
str,
"root"
, pipe.t
grammar
_processor = GrammarConstrainedLogitsProcessor(grammar)
input
_
message = [
{"role": "system"
{"role": "user"
,
,
"content": system
_prompt},
"content": math
_problem}
]
results = pipe(input
_
message,
max
new
_
_
tokens=256,
do
_
sample=False,
logits
_processor=[grammar
_processor]
)
return results[0]['generated
_
text'][-1]['content'].strip()
```

## PDF 第7页

[查看原页](RAW.pdf#page=7)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
上面说到该模式可以支持约束最终的
输出结果的格式，比
用的针对返回类型的控制，现在很多模型API中可以去做指定，如下例子：
如按照JSON输出，但是这类比
较通
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
import os
from openai import OpenAI
client = OpenAI(
# 若没有
配置环境变量，请用ideaLAB的API Key将下
行
替换为：api
_
key=
"xxx"
api
_
key=os.getenv("OPENAI
API
_
_
KEY"),
base
_
url="https://idealab.alibaba-inc.com/api/openai/v1"
,
,
)
system
_prompt = """
You will be given a short paragraph about a book.
Extract the author, title, and publication year of the book.
Return the result as JSON with the keys author, title, and year.
If any piece of information is not found, fill the spot with NULL
"""
completion = client.chat.completions.create(
, # 此处以DeepSeek-R1-671B为例，可按需更换模型名
model="DeepSeek-R1-671B"
messages=[
{'role': 'system'
{'role': 'user'
response
,
'content': system
_prompt},
,
'content': 'Love in the Time of Cholera'}],
_
format={"type": "json
_
object"}, # 指定返回的结果类型
)
print(completion.choices[0].message.content)
当然也可以支持自定义
方式上做了公共API的参数封装
的python数据类，这里的实现逻辑还是Grammar这一套，只是在使用
支持，内部还是会根据这样的类型约束转换成具体的Grammar
语法。
▐ 和Logits Masking的比
较
Grammar机制相比Logits Masking，在下面这些维度的权衡上，可能会更推荐后者：1.如果
只是一些逻辑上的规则，不是一些特定的格式或者结构的约束；2.BNF的grammar不太好调
试，也不太容易发现错误，人不友好；3.规则可以覆盖更多的场景，同时处理起来更加动态；
4.规则可以通过一层规则引擎来针对
不同的场景做选取；5.规则可以进
行
外部api的调用，更加
灵活，功能更强大。
同时Grammar和Logits都是针对模型输出的中间结果做了干预，主要是去除了一些不
满足
要
求的token的
输出，这个
行
为对于模型生成结果的整体准确性以及生成结果的成功率（因为会
出现排除完之后没有往下生成的token序列的情况，会默认输出一堆空格）都会有影响。
```

## PDF 第8页

[查看原页](RAW.pdf#page=8)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
模式三：Style Transfer
介绍完Logits掩码和Grammar之后，我们发现这两
种模式都
有一个共同的前提，那就是我可
以明确的定义出来规则，才能以程序化的方式去做输出的干预，那接下来介绍的样式转换模式
比
较适用于在没有
这样的共同前提下，该如何处理。
▐ Cases
如果你的场景和下面三种描述比
较符合，那么Style Transfer可能是一个不错的选
：
择
1. 内容已经ready，但是最终的
输出我们有额外的偏好、
格式等要求；
2. 这些要求，有些比
较具体，这部分可能可以通过上述的基于动态规则以及一些数据格式来
约束，但是
有些要求比
较细节，不太容易沉淀出rule，也不太容易去做格式化的约束；
3. 虽然给不出具体的判定规则，但是可以给出一些范本的例子。
▐ Solution
样式转换模式涉及的解决
方
有两
案
种，分别是few-shot和Fine-Tuning；
Few-shot：通过Few-shot的方式，让模型按照
示例所给出的
（输出的格式
、语调、风格等），来约束回答的样式，这是一种比
入和输出案例的一些特征
较常用的方式；
Fine-Tuning：收集示例数据，使用这部分数据对模型进
重新部署微调后的模型；
行
微调，改变相关
的权重参数，
输
相较于第一种通过few-shot来约束输出style的方式，第二种fine-tuning的方式，具有
如下
一些优点：
1. 微调可以让模型更充分地学习到输出样式的细节，比
如需要按照标准术语及口语类型进
行
较庞
大的术语映射表和映射关系，这个通过few-shot的方式
不太能很好的
输出，会涉及比
达到最终效果；
2. 可以提升整体推理速度，因为相较于前者，在整体context的token数上有比
较明显的优
势；
当然Fine-Tuning方式也需要增加额外的成本，包括去对模型做训练，同时对微调后的模型做
部署，这里
有一些知
识门槛，数据准备和模型微调、部署的成本。
▐ Considerations
```

## PDF 第9页

[查看原页](RAW.pdf#page=9)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
不管是few-shot方式，还是微调模型的方式，都是在一定程度上增加了模型对于结果输出样
式的约束力，相比
于Logits Masking和Grammar这两
种方式，在输出的确定性上都是
有
足
不
的；但是Style Transfer中通过few-shot方式来实现，在成本上是最低的。
因此，面对你要处理的场景，如果能够比
较好的做结构化的约束输出（比
据格式），那优先选用Logits Masking和Grammar，但是如果约束条件
能是一种人为的隐性判断，那么few-shot和Fine-Tuning的方式会是不错的选
择
如规则或者具体的数
不太能全面表
达，可
。
在使用few-shot方式的时候，有以下几点可能和效果有关联：
1. Bigger models lead to better results：模型参数越
更优，不过效果不好时，可以先看下纰漏点在哪里，可以适当进
一步的调优；
大，在同等example下，表现会
例子的补充，来进
行
行第
2. Limits of the Context：例子的数量多，会让模型可以有更好的转换效果，但是同时，
这些例子会增加推理上下文的长度，长度过大，模型整体的处理效果，极端的话会超出模
型可处理的context长度的上限，这里可以对用户的问题进
行
分类，同时去额外召回和该
query相关
的例子来补充context，可以达到一定程度的平衡；
3. 推 理 速 度 ： few-shot会增 加 模 型 处 理 的context大小 ， 这部 分 会直 接 影响 推 理 响 应 的速
度，优化这部分损失可以是换比
较小的模型，亦或者是对few-shot的例子进
行
一些缩减或
者按需添加，如果对rt非常敏感，可能建议做fine-tuning。
模式四：Reverse Neutralizati
on
Reverse Neutralizati
on（逆向中和），和Style Transfer类似，都是将原始回答转换成一种
特定类型、风格的最终输出；实现上一般是先使用一个通用的GenAI生成中性的中间态的结
果，然后再使用一个经过微调过的特定模型，将中间态结果转换成所需要的特定类型和风格的
输出。
不同于Style Transfer的点在于，Style Transfer是通过提供给模型Input-Output这样的案
例对，通过few-shot或者是Fine-Tuning的方式让模型在两
种类型之间做转换，而Reverse
Neutralizati
on模式下，只需要给出目标Output的样例，让模型基于这样的数据样本进
微
行
调，能够比
较好的生成这种类型的
输出。
▐ Cases
```

## PDF 第10页

[查看原页](RAW.pdf#page=10)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
比
如你想让模型按照你的人设和风格，去写一篇文章或者电子邮件，在这样的场景下，按照
Style Transfer的方式，需要给出不同场景下或者面向不同主题下的普通风格内容和你个人风
格下的内容的样本pair，这里会存在两个问题：
1. 历史内容中没有沉淀所谓你个人风格下的内容产物对应的普通风格内容；
2. 这类内容所能覆盖的内容主题会比
较有限；
▐ Solution
逆向中和（Reverse Neutralizati
on）模式的关键是需要微调训练出一个能够产生目标风格的
模型，该训练过程如下图（以个人邮件场景为例）所示：
逆向中和模式的流程图
核心有以下三步：
```

## PDF 第11页

[查看原页](RAW.pdf#page=11)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
1. 收集你的历史的邮件，让一个通用LLM以你的历史邮件为输
一个商务邮件对话风格）；
2. 将上一步产生的结果和你的历史邮件一一对应，但是输
入
版本为输
入，你个人的邮件作为输出，构建一个训练样本集；
入，生成中性的版本（可以是
输出做调换，即产生的中性邮件
1 Neutralize the tone and style from the following email to make it pro
3. 使用该训练数据，选
择
一个开源模型，进
微调；
行
在实际推理使用中，和上述描述的一样，会分拆
两
步，首先使用普通GenAI模型进
行
中性结果
生成，然后再把该结果输
入到微调后的模型，进
行定制风格内容形式的
输出，如下图所示：
逆向中和模式推理流程
▐ Consideration
Reverse Neutralizati
on非常依
赖
不同，核心内容上要保持完整并且准确的。
中性结果的生成质量，需要保证这个结果只是在风格上有
因此在使用的过程中，需要额外关注中性结果和目标风格结果之间的信息关联度，尽量保证不
要因为风格的转换丢失关键的内容，或者让原本清晰的表
达
变得模糊、词不
达
意；这里可以通
过下面两个方面进
行
一些尝试和调整：
```

## PDF 第12页

[查看原页](RAW.pdf#page=12)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
1. 中性风格的选
择
上，可以做一些调试，还是以邮件为例，比
如按照
初中一年级水平
输出，
亦或是按照英国商务标准
输出，都可以是一种中性内容输出的提示，但是这里可以针对两
种风格定义
看下输出的内容和原始个人邮件内容的差异性，选一种差异性小、在表
达
的内
容完整程度上更接近的一种风格；
2. 微调数据的选
择
上，在主题方面也需要尽量涵盖丰
的场景，同时针对模型生成的训练数据，进
行
富一些，至少能覆盖到后续可能使用到
人为的判断和筛选，可以提升整体的效果。
模式五：Content Optimizati
on
Content Optimizati
on（内容优化），是一种利用偏好调优来生成表现最优内容的模式；即
通过持续在多个输出中，标识哪个输出更优，从而强化模型在更优输出上的产出比例。
▐ Cases
传统的内容优化的方式，使用比
较多的是A/B实验，但是A/B实验有一个前提，就是需要明确
定义出来产生A、B内容样本的规则或者差异的因子，如果这个不能很好的被定义，那么A、B
的实验比
较，以及后续如何决策和使用，都是问题。
▐ Solution
Content Optimizati
on模式的特点是，不要明确定义A、B产生的差异因子，同时在评判的时
候，只需要说明更喜欢A还是更喜欢B，而不用进一步说明为什么更喜欢的理由，然后把更喜欢
的内容和不太喜欢的内容生成为一个pair数据集，通过该数据集对模型进
微调，使该微调后
行
的模型可以更大概率的生成用户更喜欢的内容。简单
说：用户只决定更喜欢哪个，至于更喜欢
的理由交给模型中数据中去学习获取。
整体解决
方
案的流程如下：
```

## PDF 第13页

[查看原页](RAW.pdf#page=13)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
图中几点做下额外说明：
1. 在Step1中，有
涉及到对于原始Prompt的改写，这里的改写主要做的是在保持prompt原
意的前提下，进
行
同等的替换、或者是进一步的解释说明，或者是提供一些例子，使得让
两次生成的结果有一些差异性；
2. Step2中使用的是LLM来评估两个结果的好坏，标注为LLM-as-judge，一般是参数量更
大的模型，当然也可以是人为标注，这里可以结合场景来看，各有利弊；
较常见的是做DPO强化，增对一个prompt，有倾向的
3. Step4中的Preference tuning，比
选
择
“chosen”，和不太倾向的结果选
择
“rejected”。
▐ Considerations
Content Optimizati
on模式比
较关键的点在于如何评估两个结果的好坏，或者说决定哪个结
果更优，比
较主流的做法有以下三个：
1. 使用更权威的模型做判定，模型参数越
大，一般来说效果越好，整体在处理大量数据的标
注上，有比
较大的优势，但是对于什么是更好的评定标准是个黑盒，不一定能够非常好的
match使用场景；
2. 专家标注，该方式成本偏高，在处理少数据量的时候，有可
行
性，同时在一些客观和高难
度问题上，标注准确性有比
较大的保障，但是，对于一些主观类的问题，在标注的时候会
潜在带入个人的价值观、喜好等因素；
```

## PDF 第14页

[查看原页](RAW.pdf#page=14)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
3. 基于反馈的判定，比
的一些判定（比
景。
如在产品链路上做的反馈设计（好or不好），亦或者是基于结果指标
如基于某个回答下，用户后续的互动率更高等等），该方式需要结合后置
的体 验 交互 链 路 设 计 以 及 相关 指 标 的定义 和数据 的回 收 来达 成 ， 优 点 是会更 契 合 使用 场
结语
这里简单把上述几个模式的问题、解决
方
案和使用场景做了个表格化展示：
模式（Patter
n） 问题（Problems） 解决
Logits掩码模式
（ Logits Maski
ng）
需要针对
输出的内容做
一些准确性、合规、风
格等的规则约束
语法模式
（Grammar）
需要对
输出有一定的
出格式和数据结构的要
求
输
样式转换模式
（ Style Transf
er）
想要输出去follow一定
的风格或者人设，但是
又没法去针对这样的
出定义明确的规则
输
逆向中和模式
（Reverse Neutr
alizati
on）
和 Style Transfer 类
似，也不太能抽象一些
明确的规则，同时也不
太能 提供
input-outpu
t例子 ， 只 能 提供 想 要
的样式的
输出的例子
方
案（Soluti
on
s）
在模 型 Sampling阶
段 ， 针 对
不 符 合 规则
的Token生 成 分支 ，
进
行提前干预
使用 类 似 BNF的语 法
明 确输 出 的格式规
则， 约 束 token的生
成
使用input-output对
的例子 ， 使用 few-s
hot或者 微 调的方 式
让 模 型 去 follow这样
的样式
使用 模 型 针 对目标风
格生 成中性风格内
容 ， 然 后 使用 该内容
对模 型 进
微 调， 使
行
模 型 可 以驾 驭 这样的
风格；
使用场景（Usage
Scenari
os）
明确的一些屏蔽词规
则， 相关
的风格要
求，避免重复的陈述
内容等
比
如生 成 SQL 语
句，生成一些标准的
JSON格式或者是
有
明确数据结构的返回
值
特 定 领 域文 本 的编
写，特定受众的内容
生成（比
如科普文章
或者专业技术文章）
个人人设 的邮 件
文档编写；
or
```

## PDF 第15页

[查看原页](RAW.pdf#page=15)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
内容优化模式
（Content Opti
mizati
on）
需要对
输出进
行
一版优
化，但是无法定义出可
用 于传 统 AB实 验比对
的不同元素；
生 成 多 个结 果 ， 并 且
对于多 个结 果 进
评
行
估（好or不好），然
后 基 于某 个prompt
下 的好 和不 好 的结 果
样本 对模 型 进
强化
行
训练；
在一些影响因素不太
的场
能 显 性化 定义
景，比
如如何编写一
份更好的营销文案，
教材等；
GenAI相关
的设计模式属于一个新的话题，不
共识，这里罗列的几种设计模式，从针对模型输出内容控制
分实
践中的场景都在案例范围内，大家可以看下自身的场景、
供的思路做一个实现的参考，同时在使用某
像Java的设计模式，非常成熟以及具有比
较多的
这个方面来说，笔者认为应该大部
当前的做法，结合上面模式中提
种方式的时候，结合自己的上下文，权衡
好利弊
~~~
参考资料
https://learning.oreilly.com/library/view/generative-ai-design/9798341622654/
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
3DXR技术 | 终端技术 | 音视频技术
服务端技术 | 技术质量 | 数据算法
```

## PDF 第16页

[查看原页](RAW.pdf#page=16)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
大淘宝技术
大淘宝技术官方账号
967篇原创内容
公众号
阅读 2527
留言
写留言
还没有
留言，来写首评
```
