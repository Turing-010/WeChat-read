# 软件为何越做越乱？万字长文讲透软件的“复杂性”：PDF文本转写

> 这是原始PDF文本层转写，不是学习摘要。页码为PDF物理页序；图表、代码版面和图片文字不能完整表达在此文本层。已查看图像的内容和质量问题见AI学习笔记及META.json。

[原文PDF](RAW.pdf) · [AI学习笔记](AI_软件复杂性演进与治理.md) · [处理与质量记录](META.json)

## PDF 第1页

[查看原页](RAW.pdf#page=1)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
软件为何越做越乱？万字长文讲透软件的“复杂性”
原创
营销&交易技术 2026年3月16日 02:58 浙江
大淘宝技术 1489人
本文通过一个电商系
统“限时折扣
”功能从快速上线到逐渐演变为复杂黑箱的典型案例，
深
入剖析了软件系
统为何越做越乱的根本原因——复杂性的累积。文章指出，复杂性并
非源于重大错误，而是由无数看似合理的小妥协（如随意添加开关
、复制逻辑、
临时补
丁 ） 层 层 叠 加 所 致 ， 最 终 导 致 变 更 放大、认知
负荷 加 重、未 知
的未 知 增多 。在此 基 础
上，文章对比了“战术性编程”（追求短期交付速度，忽视设计）与“战略性编程”（以长
期可维护性为目标，持续投入10%–20%时间优化架构）的本质差异，并系
统阐述了管
理复杂性的核心方法。作者强调：真正的开
发速度来自良好设计，而非侥幸“跑起来”；
每一次对设计的轻视，都在为未来的瘫痪埋下伏笔。
前言小故事
文章的开始，首先来看一个AI帮忙写的小故事《限时折扣到“补丁风暴”的一年》。
第一周：破局的英雄
电商团队要在两周内上线“限时折扣
”。产品经理说，这波活动成败在此。阿杰是团队
里的“战
术快枪手”，当晚就把需求“跑起来”了：他在订单服务里加了一个大
开关，判断
当前时间是否
命中折扣时段，如果是，就在结算价上直接打一个比例折扣
。没有
新服务、没有抽象、测试也
只有两条冒烟用例。第二天演示一切顺利，大家鼓掌，产品表扬“效率太高”。
第三周：再来一个
“团购”和“会员价”紧接着到来。阿杰把限时折扣
的那段逻辑复制了一份，叠加两个if分支，再
加上两个Feature Flag。因为赶时间，他把用户等级
的查询直接打到了用户服务的同步接口
里，并在超时的时候默认用户是普通会员，避免影响下单成功率。上线
顺利，数字也漂亮，项
目周会上，大家一致认为这套“战术打法”可复制
。
第二个月：小问题，但能修
```

## PDF 第2页

[查看原页](RAW.pdf#page=2)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
第一个诡异Bug出现：会员价和满减券叠加时，有时多打了一次折。回溯发现是一个分支顺序
问题。阿杰十分钟
修好了：他在优惠计算前面加了一个短路条件，遇到某些券就跳过后面的逻
辑。为稳妥，他又加了一个保护开关，默认开启
。产品问是否要重构？阿杰看了看排期表说：
“等这波活动过了先，不然这个月目标完
不成。”
第四个月：复杂悄悄长
大
需 求 继 续 滚 动： “新人礼金 ”“跨 品 类 满 减 ”“店 铺 券 优 先级
”。每次都很紧 ， 每次都能 “跑 起
来 ” 。 订单服务里 的 折扣模 块 从 两 个文 件长 成 了十几 个文 件 ，方 法 名里 充 满 了
and/or/byGroup/byMember的后缀。构建时间变
长了，代码审查也越来越
像形式走过场：
大家都
知道，真正的问题在于设计，但没人有时间停下来改。
第六个月：补丁叠补丁
有一天凌晨，线上报警：东八区和UTC时间换算错了，午夜跨天时部分订单重复计算折扣
。阿
杰拉起小团队开了个Zoom，二十分钟上线了一个临时补丁：在午夜前后5分钟内，把两个时间
都计算一遍，取最小值。问题止住了，技术群里一片赞扬。第二天复盘，大家写下了“待重构”
的卡片，又被新一轮活动排期盖过去。
第九个月：谁来重构？
一个关键需求来了：“跨店合并优惠”，而且要支持活动实时生效、规则热更新。阿杰说，这事
儿用现在的代码堆不起来了，需要一个规则引擎，把“优惠规则”“应用顺序”“冲突解决”抽成模
型，至少两个月。产品摇头：大促在即，必须四周上线
。会议室陷入沉默。最终的决定是：先
在旧逻辑上面再搭一层“适配
器”，把新规则翻译成旧分支能理解的形式。上线
勉强过了，但从
那之后，任何一个小小的改动都会牵动三处地方，回归测试用例从20条涨到200条。
第十一个月：速度的假象
新来的同学
了一周才敢改第一
行
逻辑——因为一处看似无害的改动，可能触发
四个开关下的
三种叠加路径，线上又会冒出某个边角Bug。阿杰依旧很“快”，他熟悉每个旮旯，知道该在哪
一层加一个临时判断，问题能被“快刀”切开。团队
里的其他人看起来变“慢”了：他们需要读懂
上下游的
耦合、确认二十个开关
的默认状态、跑几百条回归。这种对比让管理层误以为“还是
战术有
效”。
花
一年后：代价账单
系
统的复杂性不是某个大错误造成的，而是无数小捷径的总和。每一个“合理的妥协”——多一
个开关
、复制一段逻辑、加一个短路条件——当时都像
救命稻草，叠起来就是沼泽。现在，任
何一次真正的重构都需要数月时间、跨四个服务、影响五条业务线，排期
里根本挤不进去。团
队开始习惯了补丁式思维：先把新功能“跑起来”，出了问题再补。补丁带来更多复杂性，更多
复杂性产生更多补丁，系
统变成了一个谁也不想碰的黑箱。
```

## PDF 第3页

[查看原页](RAW.pdf#page=3)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
尾声：如果可以重来
回望最初的“限时折扣
”，当时若花
两三天把“优惠规则—应用顺序—冲突解决—时间模型”抽出
个雏形，设立基本的用例与回归框架，后面每个需求的边际成本都会更低。战术并非
不重要，
但如果没有战略性设计作为地基，战术的每一次成功，都在为下一次失败埋雷。真正的速度来
自良好的设计，而不是一次次“跑起来”的侥幸。
看完上述的小故事，不
知道大家是否曾经亲身经历或者遇到过类似的场景。在开
发生涯的早期
阶段，很多开
发
者包括我都会犯“战术快枪手”的毛病。战术快枪手总是喜欢“战术编程”，即不
为未来做考虑，只想快速地完成眼前的需求，哪怕引入一些复杂性或者bug。而多次的战术编
程的代价就是
系
统变得格外复杂。
复杂性的本质
复杂性存在多种形式。例如，可能很难理解一段代码是如何工作的。可能需要花费很多精力才
能实现较小的改进，或者可能不清楚必须修改系
统的哪些部分才能完成新特性。如果一个软件
系
统难以理解和修改，那就很复杂。如果很容易理解和修改，那就很简单。
阅读代码的人比写代码的人更容易理解复杂性。如果你编写了一段代码，可能对你来说很简
单，但是其他人则认为它很复杂，那么它就是复杂的。
▐ 复杂性的表现
复杂性一般有以下三种表现：
1. 变更放大：看似简单
的
变更需要在许多
不同地方进
行
代码修改。
2. 认知
负荷：指开
发
者需要多少知
识才能完成一项任务。较高的认知
负担意味着开
发
者必须
花更多的时间来学习所需的信息，并且可能错过重要的东西而导致引发bug的可能性也更
大。
3. 未知
执
行
的未知：必须修改哪些代码才能完成任务，或者开
发
者必须获得哪些信息才能成功地
任务，这些信息不明显。
▐ 复杂性的原因
良好设计的最重要目标之一就是使系
了解现有代码的工作
方式以及
统显而易见。在一个显而易见的
系
变更所需的内容。一个显而易见的
系
统是，开
统中，开
发
发
者可以快速
者可以在不费力
```

## PDF 第4页

[查看原页](RAW.pdf#page=4)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
地思考的情况下快速猜
测要做什么，同时又可以确信该猜
测是正确的。
依
赖
复杂性的第一个原因是依
，依
赖
在软件设计过程中有
意引入了依
赖
赖
是，软件设计的目标之一是减少依
关系
是软件的基本组成部分，无法完全消除。实际上，我们
。每次编写新类时，都会围绕该类的API创建依
关系
。但
赖
关系
赖
的数量，并使依
赖
关系保持尽可能简单和明显。
晦涩
复杂性的第二个原因是晦涩。当重要的信息不明显时，就会发生模糊。一个简单
名称如果过于笼统就没有携带太多有用的信息。或者，某个变量的文档没有说明它的
的例子是变量
单位（秒
还是毫秒？），所以找到它的唯一方法是扫描代码中使用该变量的位置。晦涩常常与依
项相
赖
关联。
知
依
赖
就可以降
和晦涩共同导致了上述描述的三种表现。依
的未知数，还会增加认知
负担。如果能找到最小化依
低软件的复杂性。
赖导致变化放大和高认知
负荷。晦涩会产生未
赖
关系和模糊性的设计技巧，那么我们
复杂性不是由单个致命性错误引起的；而是由很多小的错误堆积而成。之所以会出现复杂性，
是因为随着时间的流逝，成千上万的小的依
赖
和晦涩问题层层堆叠。最终，这些小问题太多
了，以至于对系
统的每次可能更改都会受到其中几个问题的影响。
战术性编程 VS 战略性编程
前面提到了战术编程，即开
发思路是“越快完成任务越好，之后的问题之后再说”。其代码特点
是“不会花费太多时间来寻找最佳设计，每次增加一些复杂性或引入一两个小错误”。
几乎每个软件开
发团队都
有
至少一个将战术编程发挥到极致的开
发
者：战术快枪手。战术快枪
手是一位多产的开
发
者，他编写代码的速度比其他人快得多。实施新功能时，没有人能比战术
快枪手更快地完成任务。在某些组织中，管理层将战术快枪手视为英雄。但是，战术快枪手留
下了风卷残云般的痕迹。他们很少被将接手代码的开
者视为英雄。通常，其他开
发
发
者必须清
理战术快枪手留下的混乱局面，这使得那些接手的开
者的开
发
发速度好像
比战术快枪手慢。
成为一名优秀
的开
发
者的第一步是要意识到仅工作代码是不够的。引入不必要的复杂性以更快
地完成当前任务不是长宜之计。最重要的是
过扩展现有代码库编写的。因此，作为开
发
系
统的长
期架构。任何系
统中的大
多数代码都是通
者，最重要的工作就是使得未来的架构易于扩展。
```

## PDF 第5页

[查看原页](RAW.pdf#page=5)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
因此，尽管眼前的需求很紧
急
必须是设计出卓越的架构，并且这种架构也能满足
、很重要，但不应将“完成需求”视为主要目标。我们的主要目标
当前的需求。这是战略。
战略性编程需要一种投资
心态。我们必须花费时间来改进系
来完成当前的项目。这些投资会在短期内让我们放慢脚
统的设计，而不是采取最快的方式
步，但从长远来看会加快我们的速度。
那么，正确的投资比例是多少？随着我们对系
统和业务的不
断了解，理想的设计会逐渐出现。
因此，最好的方法是连续进
行大量小额投资
。建议我们将总开
发时间的10
％到20
％用于投资
。
该比例足够小，不会对我们的日常安排产生重大影响，但又足够大，可以随着时间的推移产生
重大收益。因此，虽然项目在开始时比纯战术方
多
案
花费10-20
％的时间。但是额外的时间将
带来更好的软件设计，并且我们将在几个月内开始逐渐体现。不久之后，我们的开
发速度将比
战术编程快至少10–20
％。最终，我们过去投资
节省
的时间足以抵消一开始做投入的时间。马
上就可以收回初始投资
的成本。
一种好的思维方式是将今天的事情今天解决。当遇到难题时，大家总是会想下次再去优化。但
是，这是一个隐形的坑。一旦
这次选
择
推迟优化，之后也基本会继续推迟优化，并且不
知
不觉
中就变成了战术快枪手。总之，等待解决问题的时间越
长，问题就会变得越
大；解决
方
案变得
更加令人生畏，这使得轻松推迟解决
方
案变得更加容易。
如何管理复杂性
管理软件复杂性最重要的技术之一就是对系
对整体复杂性的一小部分。
统好好设计，以便开
发
者在任何规定时间只需要面
```

## PDF 第6页

[查看原页](RAW.pdf#page=6)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
▐ 抽象和细节
为了管理依
赖
关系，我们将每个模块分为两个部分：接口和实现。接口包含使用其他模块的开
发
者必须知道的所有内容，才能使用给定的模块。通常，接口描述模块做什么，而不描述模块
如何做。该实现由执
行
接口所承诺的代码组成。在特定模块中工作的开
发
者必须了解该模块的
接口和实现，以及由给定模块调用的任何其他模块的接口。除了正在使用的模块以外，开
者
发
无需了解其他模块的实现。
单
最好的模块是那些其接口比其实现简单得多的模块。这样的模块具有两个优点。首先，一个简
的接口可以将模块强加于
系
统其余部分的复杂性降
至最低。其次，如果以不更改其接口的方
式修改了一个模块，则该修改不会影响其他模块。如果模块的接口比其实现简单得多，则可以
在不影响其他模块的情况下更改模块的许多方面。
模块的接口包含两
种信息：正式信息和非正式信息。接口的形式部分在代码中明确指定，并且
其中一些可以通过编程语言检查其正确性。例如，方法的形式接口是其签名，其中包括其参数
的名称和类型，其返回值的类型以及有关该方法引发
的异常的信息。
每个接口还包括非正式元素。这些没有以编程语言可以理解或执
行
的方式指定。接口的非正式
部分包括其高级
行
为，例如，函数删除由其参数之一命名的文件的事实。如果对类的使用在限
制（比
如必须先调用另一个方法），则这些约束也是类接口的一部分。通常，如果开
发
者需要
了解特定信息才能使用模块，则该信息是模块接口的一部分。接口的非正式方面只能使用注释
来描述，而编程语言不能确保描述是完整或准确的。对于大
多数接口，非正式方面比正式方面
更大，更复杂。
术语抽象与模块化设计的思想紧密相关
。抽象是实体的简化视图，其中
抽象是
有用的，因为它们使我们更容易思考和操纵复杂的事物。
省略了
不重要的细节。
在抽象的定义中，“无关
紧要”一词至
关
重要。从抽象中忽略的不重要的细节越多越好。但是，
如果细节不重要，则只能将其从抽象中
省略。抽象可以通过两
种方式出错。首先，它可以包含
并非真正重要的细节。当这种情况
发生时，它会使抽象变得不必要的复杂，从而增加了使用抽
象的开
者的认知
发
负担。第二个错误是抽象忽略了真正重要的细节。这导致模糊不清：仅查看
抽象的开
发
者将不会获得正确使用抽象所需的全
部信息。忽略重要细节的抽象是错误的抽象：
它可能看起来很简单，但实际上并非如此。
我们不仅依靠抽象来管理复杂性，而且不仅在编程中，而且在日常生活中无处不在。举个例
子，汽车提供了一种简单
的抽象概念，使我们可以在不
了解电动机，电池电源管理，防抱死制
动，巡航控制等机制
的情况下驾驶它们。
```

## PDF 第7页

[查看原页](RAW.pdf#page=7)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
▐ 深模块和浅模块
最好的模块是那些提供强大功能但具有简单
接口的模块。本文用“深
入”一词来描述这样的模
块。为了形象化深度的概念，假设每个模块都由一个矩形表示。每个矩形的面积与模块实现的
功能成比例。矩形的顶部边缘代表模块的接口；边缘的长度表示接口的复杂性。最好的模块很
深：它们在简单
的接口后隐藏了许多功能。深模块是一个很好的抽象，因为其内部复杂性的一
小部分对其用户可见。
模块深度是考虑成本与收益的一种方式。模块提供的好处是其功能。模块的成本是其接口。模
块的接口代表了模块强加给系
统其余部分的复杂性：接口越小越简单，引入的复杂性就越小。
最好的模块是那些收益最大，成本最低的模块。接口不错，但更多或更大的接口不一定更好。
深模块的另一个示例是诸如Go或Java之类的语言中的垃圾收集器。这个模块根本没有
接口。
它在后台进
行
隐形操作以回收未使用的内存。由于将垃圾收集消除了用于释放对象的接口，因
此向系
语言的开
统中添加垃圾回收实际上会缩小其总体接口。垃圾收集器
的实现非常复杂，但是使用该
发
者却无需关注这种复杂性。
▐ 信息隐藏和信息泄露
实现深层模块最重要的技术是信息隐藏
。基本思想是每个模块应封装一些知
识，这些知
识代表
设计决策。
比
如如何实现TCP网络协议。如何在多核处理器上调度线程。如何解析JSON文档。这些知
识
都
入在模块的实现中，但不会出现在其接口中，因此其他模块不可见。
嵌
信息隐藏
```

## PDF 第8页

[查看原页](RAW.pdf#page=8)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
信息隐藏在两个方面降
低了复杂性。首先，它将接口简化为模块。接口反映了模块功能的更简
单、更抽象的视图，并隐藏了细节;这减少了使用该模块的开
者的认知
发
负担。其次，信息隐藏
使系
统更容易迭代。如果隐藏了一段信息，那么在包含该信息的模块之外就不再对该信息的依
赖
，因此与该信息相关
的设计更改将只影响一个模块。设计新模块时，应仔细考虑可以在该模
块中隐藏哪些信息。如果我们可以隐藏更多信息，则还应该能够简化模块的接口，这会使模块
更深。
信息隐藏
的最佳形式是将信息完全隐藏在模块中，从而使该信息对模块的用户无关且不可见。
但是，部分信息隐藏也具有价值。例如，如果某个类的某些用户仅需要特定的功能或信息，并
且可以通过单独的方法对其进
访问，以使其在最常见的用例中
行
不可见，则该信息通常会被隐
藏
。与类的每个用户可见的信息相比，此类信息将创建更少的依
项。
赖
除此之外，信息隐藏也可以应用于
系
统中的其他
级
别，例如类级
别。尝试在一个类中设计私有
方法，以便每个方法都封装一些信息或功能，并将其隐藏在类的其余部分中。此外，请尽量减
少使用每个实例变量的位置数量。
有些变量可能需要在整个类中广泛使用，但是其他
变量可能
只需要在少数地方使用；如果可以减少使用变量的位置的数量，则将消除类内的依
关系并降
赖
低其复杂性。
信息泄漏
信息隐藏
模块之间创建了依
的反面是信息泄漏。当一个设计决策反映在多个模块中时，就会发生信息泄漏。这在
赖
关系：对该设计决策的任何更改都将要求对所有
涉及的模块进
更改。如
行
果格式更改，则两个类都将需要修改。
```

## PDF 第9页

[查看原页](RAW.pdf#page=9)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
信息泄漏是软件设计中最重要的危险信号之一。作为一个开
者，我们能学到的最好的技能之
发
一就是对信息泄露的高度敏感性。如果我们在类之间发现信息泄漏，请自问“我如何才能重新
组织这些类，使这些特定的知
识只影响一个类?”如果受影响的类相对较小，并且与泄漏的信息
紧密相关，那么将它们合并到一个类中是
有
意义
的。另一种可能的方法是从所有受影响的类中
提取信息，并创建一个只封装
节中抽象出来的简单
太多的价值。
这些信息的新类。但是，这种方法只有在我们能够找到一个从细
接口时才有
效;如果新类通过其接口公开了
大部分知
识，那么它就不会提供
信息泄漏的一个常见原因称为时间分解的设计风格。在时间分解中，系
统的结构对应于操作将
发生的时间顺序。考虑一个应用程序，该应用程序以特定格式读取文件，修改文件内容，然后
再次将文件写出。通过时间分解，该应用程序可以分为三类：一类用于读取文件，另一类用于
执
行
修改，第三类用于写出新版本。文件读取和文件写入步骤都具有有关文件格式的知
识，这
会导致信息泄漏。解决
方
案是将用于读写文件的核心机制结合到一个类中。该类将在应用程序
的读取和写入阶段使用。在日常开
发过程中，我们很容易陷入时间分解的陷阱，因为在编写代
码时通常会想到必须执
行
操作的顺序。但是，大
多数设计决策会在应用程序的整个生命周期中
的多个不同时刻表现出来。结果就是时间分解常常导致信息泄漏。
在时间分解中，执
果在执
行
行
顺序反映在代码结构中：在不同时间发生的操作在不同的方法或类中。如
的不同点使用相同的知
识，则会在多个位置对其进
行
编码，从而导致信息泄漏。
最后需要提醒的是，仅当在其模块外部不需要隐藏信息时，隐藏信息才有
意义
。如果模块外部
需要该信息，则不得隐藏
它。假设模块的性能受某些配置参数的影响，并且模块的不同用途将
需要对参数进
其进
行
不同的设置。在这种情况下，将参数暴露在模块的接口中很重要，以便可以对
行
适当的旋转。作为开
发
者，我们的目标应该是最大限度地减少模块外部所需的信息量。
例如，如果模块可以自动调整其配置，那将比公开
配置参数更好。但是，最重要的是要识别模
块外部需要哪些信息，并确保将其公开。
专用好还是通用好
设计新模块时，我们面临
的最普通的决策之一就是是以通用还是专用方式
实现它。
有人可能会
说，不管什么情况下，我们都应该采用通用方法，我们应该追求一种可用于解决广泛问题的机
制，而不仅是眼前重要的问题。在这种情况下，新机制可能会在将来发现意外用途，从而节省
时间。
另一方面，我们知道很难预测软件系
统的演变
方向，因此通用解决
方
案可能包含从未真正需要
的功能。此外，如果我们实现的东西过于通用，那么可能无法很好地解决我们今天遇到的特定
```

## PDF 第10页

[查看原页](RAW.pdf#page=10)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
问题。结果，另外一些人可能会说，最好只关注眼前的需求，完成我们所知道的需求，并针对
我们今天打算使用的方式进
行特殊处理。如果我们采用特殊处理并在以后
发现更多用途，则始
终可以对其进
行重构以使其通用。专用方法似乎与软件开
发
的增量方法一致。
▐ “有点”通用比
较好
以笔者个人的经验，最有
效的方法是
有点通用的方式
实现新模块。“有点通用”表示该模块的功
能应反映我们当前的需求，但其接口则不应该这样。相反，该接口应该足够通用以支持多种用
途。该接口应易于使用，以满足眼前的需求，而不必专门与它们联系在一起。“有点”这个词很
重要：不要被带偏追求过于通用的东西，以至于反而很难满足
当前的需求。
通用方法最重要的好处是，与专用方法相比，它产生了更简单，更深
入的接口。如果我们将该
类用于其他目的，则通用方法还可以节省将来的时间。但是，即使该模块仅用于其原始用途，
由于其简单性，通用方法仍然更好。
满足我当前所有需求的最简单
的接口是什么？
如果在不减少 API 整体功能的情况下减少其方法数量，那么很可能是创建了更加通用的方法。
只有在每个方法的 API 保持简单
的情况下，减少方法的数量才有
意义
。如果为了减少方法的数
量而不得不引入大量额外的参数，那可能这不是真正的简化。
这个接口会在多少情况下使用？
如果一个方法是为专用而设计的，则意味着它可能过于专用。看看能否用一个通用方法取代几
个专用方法。
这个接口是否已经满足我当前的需求？
这个问题可以帮助我们确定何时使接口变得简单而通用。如果我们必须编写许多其他代码才能
将类用于当前用途，那么这是一个危险信号，即该接口未提供正确的功能。
通用接口比专用接口具有许多优点。它们往往更简单，使用的方法更少。它们还提供了类之间
的更清晰的分隔，而专用接口则倾向于在类之间泄漏信息。使模块具有某
种通用性是降
低整体
系
统复杂性的最佳方法之一。
▐ 专用代码无法完全避免
但是大
多数软件系
统都
不可避免地有一些专用代码。例如应用程序为其用户提供专用特性，这
些特性通常是高度专用的。因此通常不可能完全消除专用性。不过专用代码应该与通用代码清
晰的分离，这可以通过将专用代码在软件栈中向上推或者向向下推来实现。
```

## PDF 第11页

[查看原页](RAW.pdf#page=11)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
分离专用代码的一种方法是向上推。应用程序的顶层类提供专用特性，必然会针对这些专用特
性做一些优化。但这种专用并不会渗透到用于实现这些特性的底层类中。
有时最好的方法是向下推专用代码。设备驱动程序就是一个例子。操作系
统通常必须支持成百
上千
种不同的设备类型。设备驱动程序模块使得使用该设备的专用特性来实现通用接口。这种
方法将专用代码推向了设备驱动程序。因此在编写操作系
统核心时，无需了解特定设备的特
性。这种方法也让添加新设备变得更加容易。如果一个设备有足够的特性来实现设备驱动程序
接口，就可以将其添加到系
统中，而无需对主操作系
统进
任何修改。
行
分层抽象
软件系
统由层组成，其中较高的层使用较低层提供的功能。在设计良好的
系
统中，每一层都提
供与其上、下两层不同的抽象。如果我们通过调用方法遵循单个操作在层中上下移动，则每个
方法调用的抽象都会改变。如果系
统包含具有相似抽象的相邻层，则这是一个危险信号，表明
类分解存在问题。
下面讲述一些在分层抽象中我们当遇到的一些设计问题。
▐ 直通方法
当相邻的层具有相似的抽象时，问题通常以直通方法的形式表现出来。直通方法是一种很少执
行
的方法，除了
调用另一个方法（其签名与调用方法的签名相似或相同）之外。
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
@Repository
@Transactional(readOnly = true)
public class SimpleJpaRepository<T, ID> implements JpaRepositoryImplem
// 直通方法：几乎直接
委托给EntityManager
@Override
public List<T> findAll() {
return getQuery(null, Sort.unsorted()).getResultList();
}
@Override
public List<T> findAll(Sort sort) {
return getQuery(null, sort).getResultList();
}
@Override
```

## PDF 第12页

[查看原页](RAW.pdf#page=12)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
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
60
61
62
public Page<T> findAll(Pageable pageable) {
// 直通方法：只是添加分页逻辑后委托
if (isUnpaged(pageable)) {
return new PageImpl<>(findAll());
}
return findAll(pageable, null);
}
@Override
public Optional<T> findById(ID id) {
Assert.notNull(id, ID
MUST
NOT
BE
_
_
_
_
NULL);
Class<T> domainType = getDomainClass();
if (metadata == null) {
// 直通方法：直接
委托给EntityManager.find()
return Optional.ofNullable(em.find(domainType, id));
}
// 稍微复杂一点但本质还是直通
LockModeType type = metadata.getLockModeType();
Map<String, Object> hints = getQueryHints().withFetchGraphs(em
return Optional.ofNullable(type == null ? em.find(domainType,
em.find(domainType, id, type, hints))
}
@Transactional
@Override
public void deleteById(ID id) {
Assert.notNull(id, ID
MUST
NOT
BE
_
_
_
_
NULL);
// 直通方法：查找后删除
delete(findById(id).orElseThrow(() -> new EmptyResultDataAcces
String.format("No %s entity with id %s exists!"
, entit
}
@Transactional
@Override
public void delete(T entity) {
Assert.notNull(entity,
"Entity must not be null!");
// 直通方法：直接
委托给EntityManager
if (entityInformation.isNew(entity)) {
return;
}
Class<?> type = ProxyUtils.getUserClass(entity);
T existing = (T) em.find(type, entityInformation.getId(entity)
if (existing == null) {
return;
}
```

## PDF 第13页

[查看原页](RAW.pdf#page=13)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
63
64
65
66
em.remove(em.contains(entity) ? entity : em.merge(entity));
}
}
直通方法使类变
整体功能。在上述CRUD相关
创建依
关系
。
赖
浅：它们增加了类的接口复杂性，从而增加了复杂性，但是并没有增加系
统的
的方法中，前面三个基本没有什么功能。直通方法还会在类之间
但是也不能一棒子打死直通方法，我们需要警惕的是尽量不要在一个类内，大部分都是直通方
法。可以因为代码分层小部分是直通方法。如果真的遇到了一个类里大部分都是直通方法。那
解决
方
案可以是重构这个类，以使每个类都
有各自不同且连贯的职责。比
如能不能把直通对应
的关联类合并为一个类，或者索性可以让更上层直接依
赖直通关联的两个类。
另外还需要警惕的就是滥用装
饰器设计模式，装
饰器
的动机是将类的专用扩展与更通用的核心
分开。但是，装
饰器类往往很浅：它们引入了
大量的样板，以实现少量的新功能。装
饰器类通
常包含许多直通方法。过度使用装
饰器模式很容易，为每个小的新功能创建一个新类，但是会
导致浅层类激增。
以org.springframework.data.repository.support.RepositoryCompositi
on类举个例子：
1
public class RepositoryComposition {
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
// 装
饰器组合类，主要是样板代码
private final Fragments fragments;
private RepositoryComposition(Fragments fragments) {
this.fragments = fragments;
}
public static RepositoryComposition empty() {
return new RepositoryComposition(Fragments.empty());
}
public static RepositoryComposition just(RepositoryFragment fragme
return new RepositoryComposition(Fragments.just(fragment));
}
// 直通方法
public RepositoryComposition append(RepositoryFragment fragment) {
return new RepositoryComposition(this.fragments.append(fragmen
```

## PDF 第14页

[查看原页](RAW.pdf#page=14)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
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
60
61
62
63
64
65
66
public RepositoryComposition prepend(RepositoryFragment fragment)
return new RepositoryComposition(this.fragments.prepend(fragme
}
}
// 更多直通方法
public Streamable<RepositoryFragment> getFragments() {
return this.fragments;
}
public RepositoryFragment getFragment(Class<?> interfaceClass) {
return this.fragments.getFragment(interfaceClass);
}
// 浅层装
饰器
的典型特征
static class Fragments implements Streamable<RepositoryFragment> {
private final List<RepositoryFragment> fragments;
private Fragments(List<RepositoryFragment> fragments) {
this.fragments = fragments;
}
static Fragments empty() {
return new Fragments(Collections.emptyList());
}
static Fragments just(RepositoryFragment fragment) {
return new Fragments(Collections.singletonList(fragment));
}
// 大量样板装
饰方法
Fragments append(RepositoryFragment fragment) {
List<RepositoryFragment> newFragments = new ArrayList<>(th
newFragments.addAll(this.fragments);
newFragments.add(fragment);
return new Fragments(newFragments);
}
Fragments prepend(RepositoryFragment fragment) {
List<RepositoryFragment> newFragments = new ArrayList<>(th
newFragments.add(fragment);
newFragments.addAll(this.fragments);
return new Fragments(newFragments);
}
```

## PDF 第15页

[查看原页](RAW.pdf#page=15)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
67
68
69
}
}
▐ 传递变量
传递变量是通过一长串方法向下传递的
变量。传递变量增加了复杂性，因为它强制所有中间方
法知道它们的存在，即使这些方法对
变量没有用处。此外，如果存在一个新变量，则可能必须
修改大量的接口和方 法 才 能 将 变 量传 递 给 所有相关 路 径 。以 Apache Struts 1.x 的
Acti
onContext为例，可以看到从起始execute方法到最终的checkUserInput，一路上所有
方法都必须包含mapping, form, request, response四个变量。
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
public class UserAction extends Action {
public ActionForward execute(ActionMapping mapping, ActionForm for
HttpServletRequest request, HttpServlet
return processUserAction(mapping, form, request, response);
}
private ActionForward processUserAction(ActionMapping mapping, Act
HttpServletRequest request,
validateInput(mapping, form, request, response);
return performBusinessLogic(mapping, form, request, response);
}
private void validateInput(ActionMapping mapping, ActionForm form,
HttpServletRequest request, HttpServletRe
// 可能只需要form和request，但必须传递所有
参数
checkUserInput(mapping, form, request, response);
}
private void checkUserInput(ActionMapping mapping, ActionForm form
HttpServletRequest request, HttpServletR
// mapping和response在这里可能不需要，但必须传递
String username = ((LoginForm) form).getUsername();
// 验证逻辑...
}
}
```

## PDF 第16页

[查看原页](RAW.pdf#page=16)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
但实际情况中，由于代码分层或业务逻辑的问题，又不可避免会存在从顶端到底层的
变量，完
全消除传递变量是不可能的，只能相对性地做一些优化。以下是几种解决
方
案：
查看最顶层和最底层方法之间是否已共享对象。
将 信 息 存储 在全 局 变 量中， 如果 是串
行
处 理 的话也 可 以 考 虑用 threadlocal（ 但
threadlocal具有隐蔽性）。
引入一个上下文对象（context）。上下文对象专门从来存储所有全局状态。大
多数应用程
序在处理时都需要共享全局状态下具有多个变量，比
如配置项，计数器之类的内容。
笔者现在最常用的解决
方
案是上下文对象方
案，上下文对象的优点是统一了所有系
统全局信息
的处理，并且不需要传递变量。如果需要添加新变量，则可以将其添加到上下文对象；除了上
下文的构造函数和析构函数外，现有代码均不受影响。由于上下文全
部存储在一个位置，因此
上下文可以轻松识别和管理系
统的全局状态。上下文也便于测试：测试代码可以通过修改上下
文中的字段来更改应用程序的全局配置。如果系
统使用传递变量，则实施此类更改将更加困
难。
上下文远非理想的解决
方
案。存储在上下文中的
变量具有全局变量的大
多数缺点。例如，哪些
特定变量用在哪里的很不明显。与此同时，上下文容易逐步变成巨大的「大
个系
统中创建不明显的依
关系
。上下文也可能产生线程安全问题（解决
赖
泥
球」，从而在整
方法是让上下文中的
一些变量不可变）。但是在较为复杂的业务场景下，上下文方
案
已经算是较好的解决
方
案
了。
简单留给别人，复杂交给自己
假设我们正在开
发一个新模块，并且发现存在不可避免的复杂性。那这个复杂性到底由谁承担
更好：应该让模块使用者处理复杂性，还是应该在模块开
者处理复杂性？如果复杂度与模块
发
提供的功能有关，那
于开
大
多数情况下应该由模块开
发
者处理。因为大
者麻烦些总是比使用者麻烦些好。作为模块开
多数情况下，模块使用者多
者，应该努力使模块使用
发
者的开
者，因此开
发
发
发尽可能轻松，即使这意味着开
发
者需要额外的工作。换句话说，模块具有简单
的接口
比简单
的实现更为重要。
中，作为开
但是实际开
发
发
者却很容易做相反
的事：把简单留给自己，把复杂交给别人。比
如
如果出现不确定如何处理的边界条件，最简单
的方法是引发异常并让调用方处理它；再如果不
确定要实施什么策略，就定义一些配置参数来控制该策略，然后由调用方自
行
确定最佳策略。
这样的方法虽然短期内让模块的开
发
者轻松，但它们会增加复杂性，因为调用方必须处理这个
被「抛」出来的问题（而且往往不止一个调用方）。例如，如果一个类抛出异常，则该类的每
个调用者
都必须处理该异常。如果一个类导出配置参数，则每个使用这个类的调用方都必须学
习如何正确使用它们。
```

## PDF 第17页

[查看原页](RAW.pdf#page=17)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
▐ 配置参数
配置参数是提高复杂度而不是降
低复杂度的一个示例。类可以在内部输出一些控制其
为的参
行
数，而不是在内部确定特定的
行
为，例如失败重试次数。然后，该类的用户必须为参数指定适
当的值。在现在的
系
统中，配置参数非常流
行
，到处可见。但是，配置参数并不是一种很好的
处理方式，它虽然提供了一定的灵活性。但是在许多情况下，调用方很难或无法确定参数的正
确值。
如果可能的话，应该尽可能在系
统内部通过一些额外的工作来自动确定正确的值。以网络丢包
问题举例。如果发送了请求但在一定时间内未收到响应，则需要重新发送该请求。确定重试间
隔的一种方法是引入配置参数。但是，传输协议可以通过测量成功请求的响应时间，自己计算
出一个合理的值。这种方法降
低了复杂性，使用户不必自己找出正确的重试间隔。相反，如果
让调用方配置参数，由于不
知道网络协议细节，容易无法计算出合适的值。
因此，应尽可能避免使用配置参数。在使用配置参数之前，可以先问自己一个问题：“用户是
否能够确定比我们在此确定的更好的值？”当我们创建配置参数时，请查看是否可以自动计算
合理的默认值，因此用户仅需在特殊情况下提供值即可。理想情况下，每个模块都应完全自主
解决问题。配置参数导致解决
方
案不
完整，从而增加了系
统复杂性。
在一起更好还是分开更好
软件设计中最基本的问题之一是：给定两个功能，它们应该在同一位置一起实现，还是应该分
开
实现？这个问题基本适用于
系
统中的所有级
别，例如功能，方法，类和服务。
在决定是合并还是分开时，目标是降
低整个系
统的复杂性并改善其模块化。过往的经验总是推
荐将系
统划分为大量的小组
件：组
件越小，每个单独的
组
件可能越简单。但是，细分的
为也
行
会带来额外的复杂性，而这在细分之前是不在的。
组
件越多，就越难以追踪所有
组
件：也就越难在大型代码接口中找到所需的
组
件。细分通
常会导致更多接口，并且每个新接口都会增加复杂性。
细分可能会导致附加代码来管理组
件：例如，在细分之前使用单个对象的一段代码现在可
能必须管理多个对象。
细分产生分离：细分后的
件将比细分前的
件距离更远。例如，在细分之前位于
单个类
组
组
中的方法可能在细分之后位于不同的类中。分离使开
发
者更难同时查看这些组
件，甚
知道它们的存在。如果组
件真正独立，那么分离是好的：它使开
者可以一次专注于
发
至
不
单个
```

## PDF 第18页

[查看原页](RAW.pdf#page=18)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
组
发
件，而不会被其他
者 最 终 将 在组
组
件分散注意力。但是如果组
件之间存在依
件 之 间 来回 跳 转 。更 糟 糕 的是， 他 们 可 能不
赖
了 解 依
误。
细分导致重复：细分之前的
单个实例中存在的代码可能需要存在于每个细分的
组
，则分离是不好的：开
赖
关 系， 导 致 理 解 错
件中。
那么我们该如何判断应该独立还是分离呢？以下是判断标准：
是否 共 享 信 息 ； 例如， 这两 段代 码都可 能取
决于
的）。
输
入的文 件 格式（ Excel还 是PDF之 类
是否一起使用：任何使用A代码的人都可能同时使用B代码。作为反例，磁盘块高速缓存几
乎总是包含哈希表，但是哈希表可以在许多
不涉及块高速缓存的情况下使用，因此模块应
该分开。
是否概念上重叠：是否存在一个更高级
符串和大小写转换都属于字符串操作类。
是否不
看A的代码就很难理解B的代码。
别的类，会同时包括这两段代码。例如，搜
索子字
▐ 通用还是专用
通常来说，在设计理念上，系
统的下层倾向于更通用，而上层则更专用。例如，应用程序的最
顶层包含完全特定于该应用程序的功能。将专用代码与通用代码分开的方法是将专用代码向上
拉到较高的层，而将较低的层保留为通用。当我们遇到同时包含通用功能和专用功能的类时，
请查看该类是否可以分为两个类，一个包含通用功能，另一个在其上层提供特殊功能。
▐ 拆分还是合并
何时细分的问题不仅适用于类，而且还适用于方法：是否有时最好将现有
方法分为多个较小的
方法？还是应该将两
种较小的方法合并为一种较大的方法？长方法比短方法更难于理解，因此
许多人认为仅长度是分解方法的一个很好的理由。课堂上的学生通常会获得严格的标准，例
如"拆分超过20
行
的任何方法！"
但是，长度本身并不是拆分方法判断条件的一个很好的理由。通常，开
发人员倾向于过多地分
解方法。拆分方法会引入其他接口，从而增加了复杂性。它
还将原始方法的各个部分分开，如
果 这 些 部 分 实 际 上 是 相关
的 ， 则使 代 码 更 难阅 读。长方 法 并 不 总 是 坏 的 。 以
org.springframework.beans.factory.support.AbstractBeanFactory 中
的
doGetBean() 举例，这是Spring框架中的长方法之一，大约160
行
代码。
1 protected <T> T doGetBean(
```

## PDF 第19页

[查看原页](RAW.pdf#page=19)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
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
39
40
41
42
43
44
45
46
47
String name, @Nullable Class<T> requiredType,
throws BeansException {
String beanName = transformedBeanName(name);
Object bean;
// Eagerly check singleton cache for manually registered singletons.
Object sharedInstance = getSingleton(beanName);
if (sharedInstance != null && args == null) {
if (logger.isTraceEnabled()) {
if (isSingletonCurrentlyInCreation(beanName)) {
logger.trace("Returning eagerl
"' that is not fully initialized yet - a consequence of a circular ref
}
else {
logger.trace("Returning cached
}
}
bean = getObjectForBeanInstance(sharedInstance
}
else {
// Fail if we're already creating this bean instance:
// We're assumably within a circular reference.
if (isPrototypeCurrentlyInCreation(beanName)) {
throw new BeanCurrentlyInCreationException(beanName);
}
// Check if bean definition exists in this factory.
BeanFactory parentBeanFactory = getParentBeanFactory();
if (parentBeanFactory != null && !containsBeanDefinition(beanName)) {
// Not found -> check parent.
String nameToLookup = originalBeanName(name);
if (parentBeanFactory instanceof AbstractBeanFactory) {
return ((AbstractBeanFactory) parentBeanFactory).doGetBean(
nameToLookup,
}
else if (args != null) {
// Delegation to parent with explicit args.
return (T) parentBeanFactory.getBean(nameToLookup, args);
}
else if (requiredType != null) {
// No args -> delegate to standard getBean method.
return parentBeanFactory.getBean(nameToLookup, requiredType);
}
else {
```

## PDF 第20页

[查看原页](RAW.pdf#page=20)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
48
49
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
60
61
62
63
64
65
66
67
68
69
70
71
72
73
74
75
76
77
78
79
80
81
82
83
84
85
86
87
88
89
90
91
92
93
return (T) parentBeanFactory.getBean(nameToLookup);
}
}
if (!typeCheckOnly) {
markBeanAsCreated(beanName);
}
try {
RootBeanDefinition mbd = getMergedLocalBeanDefinition(beanName);
checkMergedBeanDefinition(mbd, beanNam
// Guarantee initialization of beans that the current bean depends on
String[] dependsOn = mbd.getDependsOn
if (dependsOn != null) {
for (String dep : dependsOn) {
if (isDependent(beanName, dep)) {
throw new BeanCreationException(mbd.getResourceDescription(), beanName
"Circular depends-on relationship between '" + beanName + "' and '" +
}
registerDependentBean
try {
getBean(dep);
}
catch (NoSuchBeanDefinitionException ex) {
throw new BeanCreationException(mbd.getResourceDescription(), beanName
"'" + beanName + "' depends on missing bean '" + dep + "'"
, ex);
}
}
}
// Create bean instance.
if (mbd.isSingleton()) {
sharedInstance = getSingleton
try {
return createBean(beanName, mbd, args);
}
catch (BeansException ex) {
// Explicitly remove instance from singleton cache: It might have been
// eagerly by the creation process, to allow for circular reference re
// Also remove any beans that received a temporary reference to the be
destroySinglet
throw ex;
}
});
bean = getObjectForBeanInstanc
```

## PDF 第21页

[查看原页](RAW.pdf#page=21)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
94
95
96
97
98
99
100
101
102
103
104
105
106
107
108
109
110
111
112
113
114
115
116
117
118
119
120
121
122
123
124
125
126
127
128
129
130
131
132
133
134
135
136
137
138
139
}
else if (mbd.isPrototype()) {
// It's a prototype -> create a new instance.
Object prototypeInstance = null;
try {
beforePrototypeCreatio
prototypeInstance = c
finally {
}
}
afterPrototypeCreation
bean = getObjectForBeanInstanc
}
else {
String scopeName = mbd.getScope();
if (!StringUtils.hasLength(scopeName)) {
throw new IllegalStateException("No scope name defined for bean
´" + b
}
Scope scope = this.scopes.get(scopeName);
if (scope == null) {
throw new IllegalStateException("No Scope registered for scope name '"
}
try {
Object scopedInstance = scope.get(beanName, () -> {
try {
return createBean(beanName, mbd, args);
beforePrototyp
finally {
});
}
}
afterP
bean = getObjectForBea
}
catch (IllegalStateException ex) {
throw new BeanCreationException(beanName,
"Scope '" + scopeName + "' is not active for the current thread; consi
"defining a scoped proxy for this bean if you intend to refer to it f
ex);
}
}
}
catch (BeansException ex) {
cleanupAfterBeanCreationFailure(beanNa
```

## PDF 第22页

[查看原页](RAW.pdf#page=22)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
140
141
142
143
144
145
146
147
148
149
150
151
152
153
154
155
156
157
158
159
160
161
162
throw ex;
}
}
// Check if required type matches the type of the actual bean instance
if (requiredType != null && !requiredType.isInstance(bean)) {
try {
T convertedBean = getTypeConverter().convertIfNecessary(bean, required
if (convertedBean == null) {
throw new BeanNotOfRequiredTypeException(name, requiredType, bean.getC
}
return convertedBean;
}
catch (TypeMismatchException ex) {
if (logger.isTraceEnabled()) {
logger.trace("Failed to conve
ClassUtils.get
}
throw new BeanNotOfRequiredTypeException(name, requiredType, bean.getC
}
}
return (T) bean;
}
以上代码块相对独立，所以可以一次阅读所有逻辑。如何将其中的代码块抽到单独的方法中并
没有太大的好处。如果这些代码块具有复杂的交互作用，则将它们保持在一起就显得尤为重
要，这样阅读代码的人就可以一次看到所有代码。如果每个块使用单独的方法，则阅读代码的
人将不得不在这些扩展方法之间来回切换，以了解它们如何协同工作。如果方法具有简单
的签
名并且易于阅读，则包含数百
行
代码的方法就可以了。这些方法很深就没关系
。
总之，设计方法时，最重要的目标是提供简洁的抽象。每种方法都应该做一件事并且完全做到
这一点。该方法应该具有简洁的接口，以便用户无需费神就可以正确使用它。该方法应该很
深：其接口应该比其实现简单得多。如果一个方法具有所有
这些属性，那么它的长短与否可能
无关
紧要。
简化异常处理逻辑
异常处理是软件系
况的代码更难编写，并且开
发
统中最糟糕的复杂性来源之一。处理特殊情况的代码在本质上比
者经常在定义
异常时不考虑异常的处理方式。
处理正常情
```

## PDF 第23页

[查看原页](RAW.pdf#page=23)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
许多编程语言都包含一种正式的异常机制（Java的try-catch，Python的try-excep等），该
机制允许底层代码抛出异常，由外层代码捕获处理。但是，即使不使用正式的异常机制，也可
能发生异常，比
如某个方法返回一个特殊值指示其未完成其正常
为时（比
行
如redis的set带条
件参数时返回nil表示失败）。所有
这些形式的异常都会增加复杂性。以下几种情况
都可能造成
异常：
参数错误：调用方可能会提供错误的参数或配置信息。
资源异常：调用的方法可能无法完成请求的操作。例如，I/O 操作可能失败，或者所需的
资源可能不可用。
分布式系
统网络异常：在分布式系
统中，网络数据包可能会丢失或延迟，服务器可能无法
及时响应。
系
统内部异常：该代码可能会检测到错误，内部不一致或未准备处理的情况。
异常处理代码天生就比正常情况下的代码更难写。异常中断了正常的代码流；它通常意味着某
事没有
像预期的那样工作。当异常发生时，开
者可以用两
发
种方法处理它，每种方法都很复
杂。第一种方法是向前推进并完成正在进
行
的工作。例如，如果一个网络数据包丢失，它可以
被重发；如果数据损坏了，也许可以从冗余副本中
恢复数据。第二种方法是中
止正在进
的操
作，向上报告异常。但是，中
止可能很复杂，因为异常可能发生在系
行
统状态不一致的地方；异
常处理代码必须处理一致性问题，例如
撤
销发生异常之前所做的任何更改。
此外，异常处理代码还可能造成更多异常。考虑重新发送丢失的网络数据包的情况。也许该数
据包实际上并没有丢失，但是只是被延迟了。在这种情况下，重新发送数据包将导致重复的数
据包到达
接收方；这引入了接收方必须处理的新异常情况。或者，考虑从冗余副本恢复丢失的
数据的情况：如果冗余副本也丢失了怎
么办？在恢复期间发生的次要异常通常比主要异常更加
微妙和复杂。如果通过中
止正在进
行
的操作来处理异常，则必须将此异常作为另一个异常报告
给调用方。为了防止无休止
的异常级联，开
发
者最终必须找到一种在不引入更多异常的情况下
处理异常的方法。
确保异常处理代码真正起作用是困难的。某些异常（例如I/O错误）在测试环境中
不易生成，
因此很难测试处理它们的代码。异常在运
系
的
行
统中很少发生，因此异常处理代码很少执
行
错误可能会长时间未被发现，并且当最终需要异常处理代码时，它很有可能无法正常工作。
。
▐ 异常是不是越多越好
开
发
者通过定义
不必要的异常加剧了与异常处理有关
的问题。绝大
多数开
者
发
理很重要。他们通常将其解释为“检测到的错误越多越好”。这导致了一种过分防御
都被教导异常处
的风格，其
```

## PDF 第24页

[查看原页](RAW.pdf#page=24)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
中任何看起来甚
至
有点可疑的东西都被拒绝，并带有
异常，这导致了
不必要的异常的泛滥，从
而增加了系
统的复杂性。
直接抛出异常的解决
方
案听起来很诱人：与其想出一种干净
的方法来处理它，不如抛出一个异
常并将问题转交给调用者。
有人可能会争辩说，这种方法可以赋予调用者权力，因为它允许每
个调用者以不同的方式处理异常。但是，如果开
发
者在确定情况下都
不
知道该怎
么做，那么怎
么能期待调用方能知道怎
么做呢。这种情况下生成的异常只会将问题传递给其他人，并增加系
统的复杂性。
抛出异常很容易；处理它们很困难。因此，异常的复杂性来自异常处理代码。减少由异常处理
引起的复杂性破坏的最佳方法是减少必须处理异常的数量。
▐ 尽可能少定义
异常
消 除 异 常处 理 复杂性的最 好方 法 是定义 我 们 的API， 提供 更 多 默认
行
码。这看起来有点奇怪，但在实
践中
非常有
效。
为， 减 少 抛 出 异 常的代
以 Spring 中 的
AbstractApplicati
onContext 的 异 常处 理 策 略 举例， 由 于 实 现
AutoCloseable接口了close()方法，就算在refresh过程中出现了异常
行
理资源，而不是将异常抛给调用者，并且让调用者处理异常带来的烂摊子。
为，也可以正确的清
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
public abstract class AbstractApplicationContext extends DefaultResour
implements ConfigurableApplicationContext {
@Override
public void refresh() throws BeansException, IllegalStateException
synchronized (this.startupShutdownMonitor) {
prepareRefresh();
try {
// 核心刷新逻辑
ConfigurableListableBeanFactory beanFactory = obtainFr
prepareBeanFactory(beanFactory);
// ... 其他步骤
}
catch (BeansException ex) {
// Spring知道如何处理这种异常情况
if (logger.isWarnEnabled()) {
logger.warn("Exception encountered during context
}
// 清理已创建的资源
```

## PDF 第25页

[查看原页](RAW.pdf#page=25)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
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
destroyBeans();
cancelRefresh(ex);
throw ex; // 只有在清理后才抛出
}
finally {
// 清理缓存
resetCommonCaches();
}
}
}
// 提供优雅的关
闭机制，而不是简单抛异常
@Override
public void close() {
synchronized (this.startupShutdownMonitor) {
doClose();
if (this.shutdownHook != null) {
try {
Runtime.getRuntime().removeShutdownHook(this.shutd
}
catch (IllegalStateException ex) {
// 框架知道这种情况可能发生，不抛给调用者
// JVM关
闭时可能发生，忽略即可
}
}
}
}
}
▐ 异常屏蔽
减少必须处理异常的地方数量的第二种技术是异常屏蔽。使用这种方法，可以在系
统的较低
别上检测和处理异常情况，因此，更高级
别的软件无需知道该情况。异常屏蔽在分布式系
尤其常见。
级
统中
以Spring框架中
org.springframework.web.client.RestTemplate 类举例，doExecute方
法蔽了各种IO异常、网络异常，统一转换为RestClientExcepti
on，使得开
发
者无须关注法底
层的IO、网络相关
的异常，只需专注包装
后的RestClientExcepti
on即可。
1
2
public class RestTemplate extends InterceptingHttpAccessor implements
```

## PDF 第26页

[查看原页](RAW.pdf#page=26)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
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
39
40
41
42
43
44
45
@Override
public <T> ResponseEntity<T> exchange(String url, HttpMethod metho
@Nullable HttpEntity<?> requestEntity, Class<T> responseTy
Object... uriVariables) throws RestClientException {
RequestCallback requestCallback = httpEntityCallback(requestEn
ResponseExtractor<ResponseEntity<T>> responseExtractor = respo
// 底层屏蔽了各种IO异常、网络异常，统一转换为RestClientException
return nonNull(execute(url, method, requestCallback, responseE
}
// 异常屏蔽的核心实现
protected <T> T doExecute(URI url, @Nullable HttpMethod method,
@Nullable RequestCallback requestCallback,
@Nullable ResponseExtractor<T> responseExtractor) throws R
ClientHttpResponse response = null;
try {
ClientHttpRequest request = createRequest(url, method);
if (requestCallback != null) {
requestCallback.doWithRequest(request);
}
response = request.execute();
handleResponse(url, method, response);
return (responseExtractor != null ? responseExtractor.extr
}
catch (IOException ex) {
// 屏蔽底层IO异常，转换为业务异常
String resource = url.toString();
String query = url.getRawQuery();
resource = (query != null ? resource.substring(0, resource
throw new ResourceAccessException("I/O error on " + method
" request for \"" + resource + "\": " + ex.getMess
}
finally {
if (response != null) {
response.close();
}
}
}
}
```

## PDF 第27页

[查看原页](RAW.pdf#page=27)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
▐ 异常聚集
减少与异常相关
的复杂性的第三种技术是异常聚合。异常聚合的思想是用一个代码段处理许多
异常。与其为多个单独的异常编写不同的处理程序，不如用一个处理程序将它们全
部处理在一
个地方。
此示例说明了用于异常处理的通用设计模式。如果系
当前请求，清除系
统状态并继续下一个请求
单个位置。在处理中
统处理一系列请求，则定义一个异常以中
非常有用。异常被捕获在系
统请求处理循环顶部
附近的
止请求的任何时候都可以抛出该异常。可以为不同的条件定义
异常
的不同子类。应该将这种类型的异常与对整个系
统致命的异常区分开来。
止
如果异常在处理之前在堆栈中传播了多个级
别，则异常聚集最有
效。这样可以在同一位置处理
更多方法的更多异常。这与异常屏蔽相反：如果使用低
级
方法处理异常，则屏蔽通常效果最
好。对于屏蔽，低
级
方法通常是许多其他方法使用的库方法，因此，允许传播异常会增加处理
该异常的位置数。掩码和聚合的相似之处在于，这两
种方法都将异常处理程序置于可以捕获最
多异常的位置，从而消除了许多本来需要创建的处理程序。
以 Spring MVC
中的
DefaultHandlerExcepti
onResolver 可 以看 到 异 常聚 合 理 念 的具 体 实
现，doResolveExcepti
on方法在一个地方处理统一各种下层抛出的异常并针对性地处理。
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
public class HandlerExceptionResolverComposite implements HandlerExcep
private List<HandlerExceptionResolver> resolvers;
@Override
@Nullable
public ModelAndView resolveException(HttpServletRequest request,
HttpServletResponse response,
@Nullable Object handler, Exception ex) {
if (this.resolvers != null) {
// 异常聚合：遍历所有解析器来处理不同类型的异常
for (HandlerExceptionResolver handlerExceptionResolver : t
ModelAndView mav = handlerExceptionResolver.resolveExc
request, response, handler, ex);
if (mav != null) {
return mav;
}
}
}
```

## PDF 第28页

[查看原页](RAW.pdf#page=28)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
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
60
61
62
63
64
65
66
return null;
}
}
// 具体的异常解析器
- DefaultHandlerExceptionResolver
public class DefaultHandlerExceptionResolver extends AbstractHandlerEx
@Override
@Nullable
protected ModelAndView doResolveException(HttpServletRequest reque
HttpServletResponse response,
@Nullable Object handler, Exception ex) {
try {
// 异常聚合：一个方法处理多种不同的异常类型
if (ex instanceof HttpRequestMethodNotSupportedException)
return handleHttpRequestMethodNotSupported(
(HttpRequestMethodNotSupportedException) ex, reque
else if (ex instanceof HttpMediaTypeNotSupportedException
return handleHttpMediaTypeNotSupported(
(HttpMediaTypeNotSupportedException) ex, request,
else if (ex instanceof HttpMediaTypeNotAcceptableException
return handleHttpMediaTypeNotAcceptable(
(HttpMediaTypeNotAcceptableException) ex, request,
}
}
}
else if (ex instanceof MissingPathVariableException) {
return handleMissingPathVariable(
(MissingPathVariableException) ex, request, respon
else if (ex instanceof MissingServletRequestParameterExcep
return handleMissingServletRequestParameter(
(MissingServletRequestParameterException) ex, requ
else if (ex instanceof ServletRequestBindingException) {
return handleServletRequestBindingException(
(ServletRequestBindingException) ex, request, resp
else if (ex instanceof ConversionNotSupportedException) {
return handleConversionNotSupported(
(ConversionNotSupportedException) ex, request, res
}
}
}
}
else if (ex instanceof TypeMismatchException) {
return handleTypeMismatch(
(TypeMismatchException) ex, request, response, han
```

## PDF 第29页

[查看原页](RAW.pdf#page=29)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
67
68
69
70
71
72
73
74
75
76
77
78
79
80
81
82
83
84
85
86
87
88
89
90
91
92
93
94
95
96
97
98
99
100
101
102
103
104
}
else if (ex instanceof HttpMessageNotReadableException) {
return handleHttpMessageNotReadable(
(HttpMessageNotReadableException) ex, request, res
catch (Exception handlerEx) {
if (logger.isWarnEnabled()) {
logger.warn("Failure while trying to resolve exception
}
}
}
}
}
}
}
}
}
}
return null;
else if (ex instanceof HttpMessageNotWritableException) {
return handleHttpMessageNotWritable(
(HttpMessageNotWritableException) ex, request, res
else if (ex instanceof MethodArgumentNotValidException) {
return handleMethodArgumentNotValidException(
(MethodArgumentNotValidException) ex, request, res
else if (ex instanceof MissingServletRequestPartException
return handleMissingServletRequestPartException(
(MissingServletRequestPartException) ex, request,
else if (ex instanceof BindException) {
return handleBindException((BindException) ex, request
else if (ex instanceof NoHandlerFoundException) {
return handleNoHandlerFoundException(
(NoHandlerFoundException) ex, request, response, h
else if (ex instanceof AsyncRequestTimeoutException) {
return handleAsyncRequestTimeoutException(
(AsyncRequestTimeoutException) ex, request, respon
}
}
▐ 该崩溃就奔
溃
减少与异常处理相关
的复杂性的第四
种技术是使应用程序崩溃。在大
多数应用程序中，有些错
误是不值得尝试的。通常，这些错误很难或不可能处理，而且很少发生。针对这些错误的最简
```

## PDF 第30页

[查看原页](RAW.pdf#page=30)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
单
的操作是打印诊断信息，然后中
止应用程序。
以Spring中的最经典的入口 SpringApplicati
on 类举例， 看下它在启动失败时，是如何处理
的。核心代码在 run方法第一个try catch内的
handleRunFailure方法，在遇到致命错误
时，启动会导致应用崩溃。
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
39
public class SpringApplication {
public static ConfigurableApplicationContext run(Class<?> primaryS
return run(new Class<?>[] { primarySource }, args);
}
public static ConfigurableApplicationContext run(Class<?>[] primar
return new SpringApplication(primarySources).run(args);
}
public ConfigurableApplicationContext run(String... args) {
StopWatch stopWatch = new StopWatch();
stopWatch.start();
ConfigurableApplicationContext context = null;
Collection<SpringBootExceptionReporter> exceptionReporters = n
configureHeadlessProperty();
SpringApplicationRunListeners listeners = getRunListeners(args
listeners.starting();
try {
ApplicationArguments applicationArguments = new DefaultApp
ConfigurableEnvironment environment = prepareEnvironment(l
configureIgnoreBeanInfo(environment);
Banner printedBanner = printBanner(environment);
context = createApplicationContext();
exceptionReporters = getSpringFactoriesInstances(SpringBoo
new Class[] { ConfigurableApplicationContext.class
prepareContext(context, environment, listeners, applicatio
refreshContext(context);
afterRefresh(context, applicationArguments);
stopWatch.stop();
if (this.logStartupInfo) {
new StartupInfoLogger(this.mainApplicationClass).logSt
}
listeners.started(context);
callRunners(context, applicationArguments);
}
catch (Throwable ex) {
```

## PDF 第31页

[查看原页](RAW.pdf#page=31)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
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
60
61
62
63
64
65
66
67
68
69
70
71
72
73
74
75
76
77
78
79
80
81
82
83
84
85
// 关键：不可恢复的启动错误直接崩溃应用
handleRunFailure(context, ex, exceptionReporters, listener
throw new IllegalStateException(ex); // 直接抛出导致应用崩溃
}
try {
}
listeners.running(context);
catch (Throwable ex) {
// 运
行
时严重错误也直接崩溃
handleRunFailure(context, ex, exceptionReporters, null);
throw new IllegalStateException(ex);
}
return context;
}
private void handleRunFailure(ConfigurableApplicationContext conte
Collection<SpringBootExceptionReporter> exceptionReporters
SpringApplicationRunListeners listeners) {
try {
try {
handleExitCode(context, exception);
if (listeners != null) {
listeners.failed(context, exception);
}
}
finally {
// 打印诊断信息
reportFailure(exceptionReporters, exception);
if (context != null) {
context.close();
}
}
}
catch (Exception ex) {
logger.warn("Unable to close ApplicationContext"
, ex);
}
// 注意：这里不捕获异常，让应用自然崩溃
ReflectionUtils.rethrowRuntimeException(exception);
}
private void reportFailure(Collection<SpringBootExceptionReporter>
Throwable failure) {
try {
// 打印
详细的诊断信息
for (SpringBootExceptionReporter reporter : exceptionRepor
```

## PDF 第32页

[查看原页](RAW.pdf#page=32)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
86
87
88
89
90
91
92
93
94
95
96
97
98
99
100
101
102
103
if (reporter.reportException(failure)) {
registerLoggedException(failure);
return;
}
}
catch (Throwable ex) {
// 连诊断信息都无法打印时，记录基本错误
logger.warn("Error reporting exception"
// 确保错误被记录
if (logger.isErrorEnabled()) {
logger.error("Application run failed"
}
}
}
, ex);
, failure);
}
}
在特定错误上崩溃是否可以接受取
决于应用程序。对于复制
的存储
系
统，不适合因I/O错误而
中
止。相反，系
统必须使用复制
的复杂性，但是恢复丢失的数据是
的数据来恢复丢失的任何信息。恢复机制将给程序增加相当大
系
统为用户提供的价值的重要组成部分。
准备PlanB（做技术选型）
软件设计并不容易，尤其是在复杂的框架层代码。往往来说，对模块或系
统的第一版设计不太
可能是最佳的设计。如果为每个主要设计决策考虑多个选项，最终将获得更好的结果：设计两
次。
尝试选
择
根本不同的方法，或者说做技术选型；这样将学到更多知
识。极端一点说，即使当前
场景确定只有一种合理的方法，你
其他设计的特征进
对比将很有启
行
都应该尝试考虑第二种设计。考虑该设计的
弱点并将它们与
发性。在对备选方
案进
行
粗略设计之后，列出每个方
案的优
缺点。
比
较了备选设计之后，如果主设计方
案的确更佳，那可以佐
证主设计的确最佳。或者我们可能
在过程中
发现，将多个方
案的部分功能组合到一个比任一原始设计都要好。
有些人可能会顾虑额外设计带来的时间成本。但是进
行
对于较小的模块，可能一两个小时就能搞定，这和实现该方
两次设计不需要花费很多额外的时间。
案的时间（往往是几天或者一周以
```

## PDF 第33页

[查看原页](RAW.pdf#page=33)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
上）相比
实现不值一提。最初的设计方
案可能会导致明显更好的设计方
时间划算的多。对于较大的模块，我们将花费更多的时间进
行
将花费更长的时间，并且更好的设计带来的收益也会更高。
案，这比
早期多投入的
初始设计探索，但是实现起来也
迭代型重构（小步快跑）
大型软件系
统是无一例外都是通过一系列演化发
展而来的，每个阶段都添加了新功能并修改了
现有模块。这意味着系
统的设计在不
断
发
展。一开始就不可能为系
统设计正确的设计。一个成
熟的
系
统的设计更多地取
决于
系
统演化过程中所做的更改，而不是一开始所的初始设想。
在战术编程中，主要目标是使某些功能快速工作，即使这会导致额外的复杂性；在战略编程
中，最重要的目标是进
个易于维护和增强的
系
出色的
系
行
统设计。战术方法很快导致系
统设计混乱。如果我们想要一
统，那么“能工作”是远远不够的。我们必须优先考虑设计并进
行
战略思
考。
不幸的是，当开
发
者进入现有代码以进
行
更改时，他们通常不会从战略角度进
行
型的心态是“我能做出我需要做的最小的改变是什么？”
有时，开
思考。一个典
者证明这是合理的，因为他
发
们对修改的代码不
满
意。他们担心较大的更改会带来更大的引入新错误的风险。但是，这导致
了战术编程。这些最小的
变化中的每一个都会引入一些特殊情况
、依
赖
或其他形式的复杂性。
结果，系
统设计变得更糟，并且问题随着系
统发
展的每个步骤而累积。
如果要维护系
统的简洁设计，则在修改现有代码时必须采取战略性方法。理想情况下，当我们
完成每次更改时，如果我们从一开始就考虑到更改就设计了系
统，那么系
统将具有
它应该具有
的结构。为了
实现此目标，我们必须抵制诱惑以快速解决问题。相反，请根据所需的更改来考
虑当前的
系
统设计是否仍然是最佳的。如果不是，请重构系
统，以便最终获得最佳设计。通过
这种方法，每次修改都会改善系
统设计。
如果我们花费一些额外的时间来重构和改善系
统设计，我们将得到一个更干净
系
的
统。最终将
加快开
发速度，我们将回收在重构方面投入的时间和精力。即使我们的特定更改不需要重构，
我们仍然应该注意在代码中可以修复的设计缺陷。每当我们修改任何代码时，都尝试在该过程
中
至少找到一点方法来改进系
统设计。如果我们没有使设计更好，则可能会使它
变得更糟。
有些人可能会说，业务的需求很急，实在抽不出时间来重构。比
需要二个月，但是按照现在的逻辑修修补补只要两个小时，采取快速而肮
脏
如某个功能如果要重构后上线
的方法很值。又或
```

## PDF 第34页

[查看原页](RAW.pdf#page=34)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
者说，如果重构系
实际。
统会造成许多团队其他成员的模块也需要修改，上下游会不兼容，重构不切
的确在大
多数时候，业务需求总是很急，留给我们完善的设计和实现时间并不
多。但是即便如
此，我们还是应该尽可能抵制
这些妥协。可以问问自己：“考虑到目前的时间，这是不是我能
做到的最干净
系
的
统设计？也许有一种替代方法几乎可以像2个月的重构一样干净，但是可以
在几天内完成？或者，如果我们现在负担不起大型重构，请让我们的老板为我们分配时间，或
者找一个业务需求相对
紧
不
急的时候。
总体来说，每个开
发团队都应计划将其全
很值得。
部工作的一小部分用于清理和重构。从长远来看，这
系
统应该是风格一致的
一致性是降
系
低
统复杂性并使其
行
为更明显的强大工具。如果系
统是一致的，则意味着相似的
事情以相似的方式完成，而不同的事情则以不同的方式完成。一致性会产生认知影响力：一旦
我们了解某个地方的工作
方式，就可以使用该知
识立即了解其他使用相同方法的地方。如果系
统的实施方式
不一致，则开
发
者必须分别了解每种情况。这将花费更多时间。
一致性减少了错误。如果系
统不一致，则实际上两
种情况可能不同，但两
种情况可能看起来相
同。开
发
者可能会看到一个看起来很熟悉的模式，并根据以前对该模式的遭遇做出错误的假
设。另一方面，如果系
统是一致的，则基于熟悉情况的假设将是安全
的。一致性允许开
发
者以
更少的错误来更快地工作。
以下是
系
统一致性的几种体现：
编码样式。如今，开
强制执
发团队通常拥有样式指南，这些样式指南将程序结构限制在编译
器所
行
的规则之外。现代风格指南解决了一系列问题，例如缩进，大括号放置，声明顺
序，命名，注释以及对认为危险的语言功能的限制
。样式指南使代码更易于阅读，并且可
以减少某些类型的错误。
接口。具有多个实现的接口是一致性的另一个示例。一旦
实现都将变得更易于理解，因为我们已经知道它将必须提供的功能。
了解接口的一种实现，其他任何
设计模式。设计模式是某些常见问题的普遍接受的解决
方
案，例如用于用户接口设计的模
型 视 图 控制
方 法 。如果 我 们 可 以 使用 现有
的设 计 模 式来解决问题， 则实 现 会更 快 地 进
行
，更有可能起作用，并且我们的代码对阅读代码的人来说也会更明显。
器
```

## PDF 第35页

[查看原页](RAW.pdf#page=35)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
一致性很难维护，尤其是当许多人长时间从事一个项目时。一组人可能不
了解另一组
中建立的
约定。新来的同学
不
了解规则，因此他们无意间违反了约定并创建了与现有约定冲突的新约
定。以下是建立和保持一致性的一些技巧：
文档。创建一份文档，列出最主要的重要约定。比
如编码风格指南（阿里巴巴有Java编码
规范）。
执
。即使有
好的文档，开
行
发
者也很难记住所有约定。实施约定的最佳方法是编写一个检
查违规的自动化工具，并确保代码通过检查程序。
一致性是投资
心态的另一个例子。确保一致性的工作将需要一些额外的工作：确定约定，创建
自动检查程序，寻找类似情况以模仿新代码，以及进
行
代码审查以教育团队。这项投资
的回报
使我们的代码将更加明显。开
发
者将能够更快，更准确地了解代码的
为，这将使他们能够以
行
更少的错误来更快地工作。
代码应该是易于理解的
如果代码很明显，则意味着某人可以不
假思索地快速阅读该代码，并且他们对代码的
为或含
行
义
的最初猜
测将是正确的。如果代码很明显，那么阅读代码的人就不需要花费很多时间或精力
来收集他们使用代码所需的所有信息。如果代码不明显，那么阅读代码的人必须花费大量时间
和精力来理解它。这不仅降
低了它们的效率，而且还增加了误解和错误的可能性。明显的代码
比
不明显的代码需要更少的注释。
阅读代码的人的想法是“显而易见”：注意到别人的代码不明显比
发现自己的代码有问题要容易
得多。因此，确定代码是否显而易见的最佳方法是通过代码审查。如果有人在阅读我们的代码
时说它并不明显，那么无论我们看起来多么清晰，它也不是显而易见。通过尝试理解什么使代
码变得不明显，我们将学习如何在将来编写更好的代码。
软件应设计为易于阅读而不是易于编写。通用容器
对于编写代码的人来说是很方便的，但是它
们会使随后的所有
阅读代码的人感到困惑。对于编写代码的人来说，花一些额外的时间来定义
特定的容器结构是更好的选
择
，以便使生成的代码更加明显。
▐ 直观的技巧
选
好名字：精确而有
择
意义
的名称可以阐明代码的
行
为，并减少对文档的需求。如果名称
含糊不清或含糊不清，那么阅读代码的人将通读代码以推论命名实体的含义；这既费时又
容易出错。
```

## PDF 第36页

[查看原页](RAW.pdf#page=36)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
一致性：如果总是以相似的方式完成相似的事情，那么阅读代码的人可以识别出他们以前
所见过的模式，并立即得出结论，而无需详细分析代码
以下是使代码更明显的其他一些通用技术：
使用空白。代码格式化的方式会影响其理解的容易程度。（代码）
注释。
有时无法避免
非显而易见的代码。发生这种情况时，重要的是使用注释来提供缺少
的信息以进
行
补偿。（代码）
▐ 不直观的案例
事件驱动编程。在事件驱动编程中，应用程序对外部事件做出响应。应用程序的其他部分
通过在事件
发生时要求事件模块调用给定的函数或方法来注册对某些事件的兴趣。倒不是
说事件驱动编程这种思想不好，而是说这种思想写出的代码对阅读代码的人的确增加了模
糊性。为了弥补这种模糊性，可以为每个处理程序函数使用接口注释，以明确说服何时调
用该函数。
通用容器。许多语言提供了用于将两个或多个结构到一个对象中的通用类，例如Java中的
Pair。这些类很诱人，常见的用途是从一个方法返回多个值。不幸的是，通用容器导致代
码不清晰，因为分组
后的元素的通用名称模糊
了它们的含义
。JDK17中Java提供了新的
record类型，合理的使用record可以有
效提高代码的可读性。
反直觉。如果代码符合阅读代码的人期望的惯例，那么它是最明显的。如果没有，那么为
该
行
为增加注释很重要，以免使阅读代码的人感到困惑。比
如fastJson框架是通过执
类
中的getXXX方法实现对象构造的，如果在类中有
非字段相关
的getXXX也会被执
行
行
（曾经
触发过很多故障）。
警惕过早优化性能
到目前为止，关
于软件设计的讨论都集中在复杂性上。目标是使软件尽可能简单易懂。但是，
如果我们需要高性能的
系
统实现，该怎
么办？性能方面的考量会如何影响设计过程？
要解决的第一个问题是“在正常的开
发过程中应该为性能花
多少心思？”。因为优化性能需要不
少的时间成本，同时也增加了复杂性。假设如果每条语句都需要尝试优化以获得最高的性能，
那么它不仅会大幅度减慢开
发速度，同时许多
不必要的复杂性。此外，许多“优化”实际上对性
能并没有帮助。但是如果完全
不考虑性能问题，则可能导致整个代码的效率低下，最终系
统比
预想的速度慢5–10倍。（总不能ToB或者ToC的接口RT在秒级）
如果提高效率的唯一方法是增加复杂性，那么选
择
增加了少量复杂性，并且复杂性是隐藏
起来就会比
的，那么可以放心地选
较困难。如果更高性能的设计仅
性能更优的方
案。但是如果更
择
```

## PDF 第37页

[查看原页](RAW.pdf#page=37)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
高性能设计需要增加很多复杂性，那么最好是先从更简单
的实现开始，然后在性能出现瓶颈时
进
行
优化。但是，如果我们有明确的需求表明性能在特定情况下很重要（比
如我曾经做过一个
需求必须满足所有
投放逻辑包括外调在5ms内处理），那么最好一开始就选
性能更好的方
择
法。
如果真的决定了需要优化性能，那么先好好测量系
统的现有
首先，这些测量将确定对性能影响最大的地方。仅仅测量系
知道系
统速度太慢，但不
知道原因。我们还需要进
行
更深
表现。这
有两个目的。
统性能是不够的。虽然我们能
入的测量，详细确定影响整体性
能的核心因素。
其次是提供基线，以便在优化后重新测量性能，以确保性能得到实际改善。如果这些更改
没有显著提高性能，则保持优化带来的复杂性毫无意义
。
最后
全文只讲一件事：复杂性。控制复杂性是软件设计的核心挑战。它让系
护，也常常拖慢运
效率。
统难以构建、难以维
行
虽然本文中的建议在实操时会带来一定的代价：它们会在项目早期增加额外工作量；如果我们
不习惯从设计角度思考，学习这些技巧会让我们一时变慢。但是如果我们的唯一目标是尽快把
当前功能跑起来，设计思考看起来就像是在“挡路”，妨碍我们达成眼前目标。
但如果我们把良好设计当成重要目标，这些想法会让编程更有趣。设计是一道迷人的题：用最
简单
案本身就很有
的结构解决特定问题。探索不同方
解法时，会有一种难以替代的满足感。简单、清晰的
意思，而当我们找到一个既简单又有力的
系
统本身就是一种美。
更重要的是，这种投入很快回本。我们会不
省大量时间。
断复用在项目初期精心定义
的模块和边界，从而节
成为优秀
的设计者的回报在于：我们能把更多时间花在设计与抽象上；而糟糕的设计者则把大
部分时间耗在修复复杂、脆弱代码中的各种问题上。
参考书籍
《软件设计的哲学》
《架构整洁之道》
《Google软件工程》
```

## PDF 第38页

[查看原页](RAW.pdf#page=38)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
《OnJava中文版》
《凤凰架构》
《软件架构设计：大型网站技术架构与业务架构融
《系
统架构：复杂系
统的产品设计与开
》
发
《架构师修炼之道》
合之道》
团队介绍
本文作者思诚，来自淘天集团营销&交易技术团队。本团队承担淘天电商全链路交易技术攻
坚，致力于通过技术创
新推动业务增长与用户体验升级
。过去一年主导了多个高价值项目，包
括：支撑618、双11、春晚等亿级流量洪峰、构建业界领先的全网价格力体系
、承接淘宝全面
接入微 信支 付、搭 建 集 团 最大的AI创
新平 台 -ideaLAB，支 撑 淘宝秒 杀 等创
新 业 务 的高 速增
长。
¤ 拓展阅读 ¤
3DXR技术 | 终端技术 | 音视频技术
服务端技术 | 技术质量 | 数据算法
大淘宝技术
大淘宝技术官方账号
967篇原创内容
公众号
阅读 7436
留言
```

## PDF 第39页

[查看原页](RAW.pdf#page=39)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
写留言
还没有
留言，来写首评
```
