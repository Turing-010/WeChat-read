# 卡片式对话的协议方案探索和思考：PDF文本转写

> 这是原始PDF文本层转写，不是学习摘要。页码为PDF物理页序；图表、代码版面和图片文字不能完整表达在此文本层。已查看图像的内容和质量问题见AI学习笔记及META.json。

[原文PDF](RAW.pdf) · [AI学习笔记](AI_卡片式对话协议方案探索.md) · [处理与质量记录](META.json)

## PDF 第1页

[查看原页](RAW.pdf#page=1)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
卡片式对话的协议
方
案探索和思考
原创
跨端技术团队 2026年4月17日 01:01 浙江
大淘宝技术 3人
本文探讨了在智能助手对话流中
实现卡片式交互的
系
统性工程方
案。文章围绕卡片如何
入Markdown流、数据来源以及多团队协作规范三个核心问题，详细分析了代码块扩
展
、占位符替换及自定义标签等嵌
入方
案，并对比了模型直出、增量Patch及Tool驱动
等数据获取模式。最终，文章提出了一套包含Markdown标记、消息传输、UI渲
及事
件通信的四层统一协议体系，旨在解决Agent时代下多端一致性、数据实时性及跨团队
协作混乱的问题，为构建高效、标准化的卡片式对话系
统提供了落地的架构参考。
嵌
染
引言
当我们第一次在智能助手中
看到一张可交互的商品卡片时，觉得这不过是"在聊天框里塞
了个组
件"。但真正实
践下来才发现，这件事远比想象中复杂——它不是一个前端渲
染问题，而是一个
贯穿 Agent 设计、 模型输出、数据流转、协议设计、跨端一致性的
系
统工程。
这篇文章不讲概念，讲我们探索过程中踩过的坑和沉淀的方
案。
文章将围绕三个问题展
开：
1. 卡片如何嵌
入对话流？ ——模型输出的是 Markdown 文本流，卡片怎
么"混"进去？
2. 卡片数据从何而来？ ——模型不
3. 多团队协作怎
知道实时价格，数据该由谁提供
怎
么填充？
么不乱？ ——当 N 个业务方都要接卡片时，如何用协议约束混乱？
、
卡片如何嵌
入对话流
▐ 问题的本质
大模型的
输出本质上是一个 token 流，经过拼接后形成 Markdown 文本。Markdown 本身
是一种排版标记语言，它能表
达标题、列表
、代码块、图片，但无法表
达"这里应该渲
染一个商
```

## PDF 第2页

[查看原页](RAW.pdf#page=2)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
品卡片组
件"这件事。
所以核心问题是：如何在不破坏 Markdown 流式解析的前提下，嵌
入自定义 UI 组
件的语义
信息？
我们调研和实
践了三种方
案，各有适用场景。
▐ 方
案一：代码块扩展
这是我们最终在生产环境中采用的方
案，原理非常直觉——Markdown 的代码块本身就有一
个 language 字段（用于语法高亮），我们把这个字段"借用"为组
件类型标识。
模型输出的 Markdown 长这样：
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
为你推荐以下商品：
```ProductCard
{
"title": "iPhone 15 Pro Max"
,
"description": "全
新钛金属设计，A17 Pro 芯片"
,
"itemPrice": 9999,
"imageUrl": "https://example.com/iphone.jpg"
"discount": "限时优惠 -10%"
,
}
```
以上商品支持分期免息，点击卡片可查看
详情。
前 端 Markdown 渲
染器 拿 到 这 段文 本 后 ， 在 解 析 代 码 块 时 检 查 是 javascript、python
这种已知语言就做语法高亮；如果是 Produ
就把代码体当作 JSON 解析，传给对应的 React 组
件渲
染。
以 react-markdown 为例，扩展逻辑如下：
language ctCard
字段： 如果
这种自定义标识，
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
import Markdown from 'react-markdown';
import { ProductCard } from '
./components/ProductCard';
// 组
件注册表：language 名 → React 组
const CARD
COMPONENTS = {
_
件的映射
ProductCard: ProductCard,
UserProfile: UserProfile,
FlightCard: FlightCard,
};
function ChatMessage({ markdown }) {
return (
<Markdown
children={markdown}
```

## PDF 第3页

[查看原页](RAW.pdf#page=3)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
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
components={{
code(props) {
const { children, className, ...rest } = props;
// className 格式为 "language-xxx"，提取 xxx 部分
const match = /language-(\w+)/.exec(className || '');
const langName = match ? match[1] : null;
// 命中
组
件注册表 → 渲
染业务卡片
if (langName && CARD
_
COMPONENTS[langName]) {
const CardComponent = CARD
_
COMPONENTS[langName];
const cardProps = JSON.parse(String(children));
return <CardComponent {...cardProps} />;
}
// 未命中
→ 走默认的代码高亮渲
return (
<code {...rest} className={className}>
{children}
</code>
染
);
},
}}
/>
);
}
有
这里
几个实
践细节值得展
开：
1. 为什么选代码块而不是其他 Markdown 元素？
代码块有两个天然优势：一是所有 Markdown 解析器
都支持 language 字段的提取，不需要
写自定义
parser；二是代码块内部的内容不会被 Markdown 解析器二次处理（不会把 {
当成
列表
、把 "
当成引号），JSON 数据可以安全传递。
2. 流式渲
染
的兼容性
代 码 块有 明 确 的 开 始 标 记 （ ``` ） 和 结 束 标 记 （ ``` ） ， 流 式解 析器 在 遇 到 开 始 标 记 时 就 能知
道"接下来是一个代码块"，在结束标记到来前持续缓冲内容。这意味着前端可以在代码块完整
输出后再做 JSON 解析和组
件渲
染，不会出现半截 JSON 导致的 parse error。
3. 模型输出约束
大模型不会天然知道要输出 Produ
ctCard
格式的代码块。我们通过 System Prompt 给模型
一份"卡片生成规范"：
1
2
3
4
# 卡片生成规范
## 语法
- 语言标识使用组
当需要展示结构化信息（商品、航班、用户资料等）时，使用 Markdown 代码块格式：
件名（PascalCase），如 `ProductCard`
、
`FlightCard`
```

## PDF 第4页

[查看原页](RAW.pdf#page=4)

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
- 代码体使用标准 JSON，属性名 camelCase
- 确保 JSON 格式合法，属性名使用双引号
## 示例
```ProductCard
{
"title": "商品名称"
,
"itemPrice": 99,
"imageUrl": "https://example.com/img.jpg"
}
实际调试中
发现，给模型 2-3 个 Few-Shot 示例就能稳定输出正确格式。如果对格式一致性
要求极高，还可以在服务端加一层正则校验——代码块输出完毕后检查 JSON 是否合法，不合
法就降
级为纯文本展示。
▐ 方
案二：占位符替换
占 位 符 替 换是一 个 更 轻 量的 思路 —— 模 型 在 Markdown 中
如 __placeholder__Produ
ctCard），前端识别到后替换为对应组
件。
输 出一 个 特殊 标 记 （比
1 推荐上午 10 点从杭州出发前往上海的高铁
__placeholder
__
ProductCard,早班直达
。
这个方
案
看起来简单，但在流式场景下有一个棘手的体验问题：模型是逐 token 输出的，当只
输出到 __place
的时候，前端无法判断
这是一个占位符还是普通文本。用户会先看到一串乱码
般的占位符文字，然后突然跳
变为卡片。
我 们 尝 试 过一 种 优 化方 式： 把 占 位 符 设 计 成 类 似 超链 接 的 语 法 [(Produ
ctCard)] 。 利用
Markdown 解析器
的已有机制——遇到 [ 时暂存等待后续字符，如果后续不符合链接语法就回
退为普通文本。在此基础上扩展：
1
2
3
遇到 [( → 暂存，推测可能是卡片
等待 )] 出现 → 匹配成功，渲
染组
件
超过 buffer 上限仍未匹配 → 回退为普通文本
在 markdown-it
中
实现为一个 inline rule 插件：
1
2
3
4
function componentPlugin(md) {
md.inline.ruler.before('link'
const start = state.pos;
const max = state.posMax;
,
'component'
, (state, silent) => {
```

## PDF 第5页

[查看原页](RAW.pdf#page=5)

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
28
29
30
31
32
// 检查起始标记 [(
if (state.src.charCodeAt(start) !== 0x5B /* [ */ ||
state.src.charCodeAt(start + 1) !== 0x28 /* ( */) {
return false;
}
// 向前扫描，寻找结束标记 )]
let pos = start + 2;
while (pos < max - 1) {
if (state.src.charCodeAt(pos) === 0x29 /* ) */ &&
state.src.charCodeAt(pos + 1) === 0x5D /* ] */) {
break;
}
pos++;
}
if (pos >= max - 1) return false;
const componentName = state.src.slice(start + 2, pos);
if (!silent) {
const token = state.push('component'
''
,
, 0);
token.content = componentName;
}
state.pos = pos + 2;
return true;
});
md.renderer.rules.component = (tokens, idx) => {
const name = tokens[idx].content;
return `
<div class="custom-component" data-component="${name}"></d
};
}
占位符方
案的优势是改造成本低（不需要模型生成完整 JSON），适合卡片数据完全由服务端
异步填充的场景。但劣势也很明显：占位符本身不携带数据，卡片要么需要事后补数据（增加
一次请求），要么需要约定好全局的
组
件-数据映射关系
。
实
践建议：如果选
择占位符方
廓"，而不是一闪而过的占位符文本。
案，务必配合前端骨架屏。用户看到的应该是"加载中的卡片轮
▐ 方
案三：自定义标签（XML-like）
这个方
案的灵感来自
Action：
bolt.new。bolt.new 在模型输出中引入了类 HTM
L 的自定义标签来描述
1
2
<boltArtifact title="Some title" id="artifact
1">
_
<boltAction type="shell">npm install</boltAction>
```

## PDF 第6页

[查看原页](RAW.pdf#page=6)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
3 </boltArtifact>
这 种方 式需 要 在 Markdown 解 析 之 外单独 写一 个 XM
L parser ， 从文 本 流中 提取
<boltArtifact> 标 签 及 其 属 性 和子 元 素 （ 解 析 参 考 ：
https://github.com/stackblitz/bolt.new/blob/main/app/lib/runtime/message-
parser.ts）。
自 定义 标 签 的 核心优 势在 于 表
达力最 强——XM
L 天 然支 持嵌 套 结 构、 属 性、 事 件 绑 定
（如 on-click="run"），可以描述比 JSON 更复杂的 UI 语义
。而且它与模型无关，任何能
生成合法 XM
L 的模型都可以接入，这对于需要同时对接多家模型（Qwen、Claude、GPT）
的场景尤其有价值。
但它的代价也很明显：需要维护一个独立的流式 XM
解析器
的协作关系（哪些部分走 Markdown 渲
染，哪些部分走 XM
L parser，且必须处理好与 Markdown
L 解析）。这个方
案的诞生
背景是部分模型厂商未提供 Tool Call API，需要通过 Prompt 工程来模拟工具调用。如果你
的模型已经支持 Function Calling，这个方
案的必要性就降
低了。
▐ 三种方
案的选
建议
择
总结一下：代码块扩展最稳健，复用现有解析链路、零额外依
赖
换最轻量，适合卡片数据完全由服务端提供的场景；自定义标签表
统一管控、或已有 XM
L 基础设施的团队。
，适合大
多数场景；占位符替
达力最强，适合需要多模型
我们在生产中选
择
了代码块扩展，原因很朴素：改造成本最低
、模型约束最简单、出问题时最
容易排查。
但到这里只解决了"卡片怎
么写进 Markdown"的问题。紧接着的问题是——卡片里的 JSON
数据从哪来？模型自己编的商品价格能用吗？库存状态、用户偏好这些实时信息怎
么办？
卡片数据从何而来
▐ 数据与 UI 必须解耦
这是一个关键的架构决策。卡片的视觉结构（"这是一个商品卡，有标题、价格
片的业务数据（"iPhone 15 Pro Max, ¥9999, 库存 32"）必须分开处理。
、图片"）和卡
```

## PDF 第7页

[查看原页](RAW.pdf#page=7)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
原因很现实：大模型的预训练数据不可能涵盖所有商品，即使涵盖了，价格库存也在实时变
化，更不用说千人千面的个性化推荐了。如果让模型直接生成完整的商品数据，你会得到一
个"看起来像回事但完全
这里我们归纳为三个阶段的方
不能用"的 JSON。
案演进。
▐ 方
案一：模型直出——能用，但不可靠
最简单
的方式：在 System Prompt 中告诉模型"需要展示商品时，生成一个包含完整数据的
代码块"，模型直接把标题、价格
、图片 U
R
L
都填进 JSON 里。
这在 Demo 阶段确实能跑通。但一上线
就暴露了问题：
模型编造了
不存在的商品链接（胡编乱造）
价格和实际售价不一致（训练数据过时）
同一个商品对
不同用户展示相同价格（无法做个性化）
结论：模型直出只适合静态内容（如百科摘要、功能说明），不适合
任何涉及实时业务数据的
场景。
▐ 方
案二：增量 Patch 更新——先占位，后补数据
既然模型不能直接生成可靠数据，那换一个思路：让模型只生成卡片的"骨架"（一个带 ID 的
占位 JSON），服务端异步获取真实数据后通过 Patch 机制更新到前端。
模型输出的内容是这样的——注意代码块里只有一个 id，没有真实数据：
1
2
3
4
5
6
7
为你推荐以下商品：
```ProductCard
{
"id": "xxx"
}
```
这些商品不仅实用，而且价格便宜。
然后前端和服务端各干各的事：
前端：解析到 Produ
ctCard 代码块后，发现数据不
完整，渲
染一个骨架屏占位。
```

## PDF 第8页

[查看原页](RAW.pdf#page=8)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
服务端：在识别到模型输出中包含 Produ
品 数 据 。 数 据 回 来 后 ， 通 过 我 们 在 标 准 符，将占位 JSON 替换为完整数据。
ctCard 代码块时，立即异步发起 RPC 请求获取商
JSON Patch 之 上 扩展 的
replace-substring 操 作
传输消息格式如下：
1
[
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
{
},
{
},
{
}
29
]
}
]
]
}
}
"type": "full"
"data": {
,
"markdown": "为你推荐以下商品：\n```ProductCard\n{\n id:xxx\n}\n``
"type": "patch"
"patch": [
{
,
"op": "replace-substring"
,
"path": "/markdown"
,
"substring": "```ProductCard\n{\n id:xxx\n}\n```"
,
"replacement": "```ProductCard\n{\n \"id\": \"12345\"
,\n \"t
"type": "patch"
"patch": [
{
,
"op": "add"
,
"path": "/markdown"
,
"value": "仅实用，而且价格便宜。"
整个时序是这样的：
```

## PDF 第9页

[查看原页](RAW.pdf#page=9)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
这个方
案解决了数据准确性问题，但体验上有一个明显缺陷：用户会先看到骨架屏，等数据回
来后才看到真实卡片，有一个可感知
的"跳
变"。如果 RPC 请求慢（比
如跨地域调用），这个
延迟会更明显。
另外还
有一个工程复杂度问题：replace-substring 需要在服务端精确匹配
中的占位片段再做替换，如果模型输出的格式有
微小偏差（多了个空格
、换
就会失败。这在生产中需要做鲁棒性处理。
Markdown 文本
不一致），替换
行
▐ 方
案三：Tool 驱动——让工具同时生产数据和 UI
方
案二的核心矛盾在于"模型先返回，数据后补"，数据和 UI 在时序上是割裂的。
有没有可能
让它们一步到位？
答案是：把数据获取和 UI 描述都交给 Tool 来做。 Agent 识别到用户意图后调用一个工具
（比
如 search_produ
cts），工具直接返回结构化数据
+ UI 描述，前端按约定渲
染。模型不
再需要"编"数据，它只负责意图理解和对话编排。
社区中有两个代表性协议在探索这条路：MCP Apps 和 A2UI。它们解决的是同一个问题——
Agent 如何驱动前端渲
染 UI？但设计哲学截然不同。
MCP Apps：工具驱动 UI
```

## PDF 第10页

[查看原页](RAW.pdf#page=10)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
MCP Apps 是 Anthropic 在 MCP（Model Context Protocol）基础上的扩展。它的核心理
念是：Tool 返回的不只是纯数据，还附带一份 UI 描述。
具体来说：
每个 MCP Tool 在注册时就声明"我的返回结果应该用什么 UI 来展示"
Agent 调用 Tool 后，前端根据 tool_id 匹配预注册的渲
染器，自动渲
染卡片
卡片内的交互事件可以回调到 Agent，形成闭环
MCP Apps 的设计隐喻是：UI 是 Tool 执
行结果的附属产物。工具先把活干了（查商品、查航
班），然后顺便告诉前端"结果长这样"，用什么 UI 地址渲
染。这意味着 UI 和 Tool 是强绑定的
——一个 search_produ
cts 工具对应一种 Produ
ctList 卡片。
A2UI：Agent 驱动 UI
A2UI（Agent to UI） 是 Google 提出的通用声明式
完全
不同：不绑定任何工具链，纯粹定义"界面应该长什么样"。
UI 协议。它的设计哲学和 MCP Apps
A2UI 定义了一套 JSON Schema，涵盖布局、
表
单、列表
、图表等常见 UI 组
件。Agent 只
需输出符合 Schema 的 JSON，各端（Web / iOS / Android）各自实现渲
染器。Action 事
件通过标准事件总线回传给 Agent。
与 MCP Apps 相比，A2UI 更关注渲
染层本身的标准化。它不
型直接生成的——它只管"拿到一份 JSON，画出对应的 UI"。
关
心数据是从 Tool来的
还是模
两者的本质区别
理解这两个协议
的关键在于看它们的驱动方式：
MCP Apps：工 具驱 动 。 UI 是 Tool 的 附 属 ， 粒 度 是 Tool 级
别（一 个工 具 对 应一 种 卡
片）。适合卡片类型确定、
交互模式固定的场景。
A2UI：Agent 驱动。UI 由 Agent 自主组合，粒度是组
件级
别（可以任
意拼装布局、
表
单、列表）。适合需要动态生成 UI、或者从预设卡片向 Agent 自主生成过渡的场景。
两者在实
践中并非互斥。一种可
的
行
组合方式是：在 MCP Tool 层使用 MCP Apps 的绑定机
制来管理 Tool 与 UI 的映射关系，同时用 A2UI 的 JSON Schema 作为 UI 描述的标准格式
——这样既有 Tool 层的确定性，又有
UI 层的通用性。
Tool 驱动的整体流程
无论选
择
哪种协议，Tool 驱动 UI 的核心时序是一致的，我们在实
的数据
+ UI 的方式：
践的过程中采用 Tool 返回
```

## PDF 第11页

[查看原页](RAW.pdf#page=11)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
Tool 驱动方
案的优势非常明显：
数据与 UI 在 Tool 层一步到位，没有"先占位后补数据"的体验断裂
业务方自主维护 Tool 和对应的卡片，Agent 只做编排，职责清晰
天然支持复杂交互——卡片内分页、筛选、
表
单提交都可以通过 Tool 回调实现
▐ 三种方
案的演进逻辑
回顾这三种方
案，它们不是简单
的"好坏之分"，而是一条渐进式的架构演进路径：
模型直出 → 最快出活，适合 Demo 和验证阶段
增量 Patch → 数据可靠了，但时序和工程复杂度上升
Tool 驱动 → 架构最干净，但需要 MCP 工具链和协议基础设施
核心方向是：把数据生产的责任从模型转移到工具链，让模型专注于意图理解和对话编排。
到这里，我们讨论了两个问题：卡片怎
么嵌
入
Markdown 流（第一部分的三种扩展方
案），
以及卡片数据从哪来（模型直出 → 增量 Patch → Tool 驱动）。
但当我们要把这套方
案推广到实际业务的时候，还需要考虑新的问题：A 团队用代码块扩展，
B 团队用占位符；C 团队的消息格式和 D 团队
不兼容；Web 端和 iOS 端对同一种卡片的事件
约定完全
不同。每接入一个新业务方，前端就要写一套新的解析和渲
逻辑。
这其实会让我们去思考一个更根本的问题：如何用协议来收敛混乱？
染
多团队协作怎
么不乱——四层统一协议
▐ 为什么需要协议
```

## PDF 第12页

[查看原页](RAW.pdf#page=12)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
"协议"这个词听起来很重，但它要解决的问题非常朴素：让不同团队
一套规范工作，减少重复建设和沟通成本。
、不同端的开
发
者面向同
没有
协议
的时候，每个 Agent 团队都在各自定义 Markdown 扩展
格式
、消息传输结构、卡片
事件约定。前端为每种 Agent 写一套解析器，iOS 和 Android 各自实现一遍，改一个字段要
同步通知 N 个团队。这种"自由"的代价是
系
统迅速碎片化。
我们把协议分成四层，每一层解决一个明确的问题：
协议层 解决什么问题一句话描述
1. Markdown 标 记
协议
卡片在文本流中怎
么
写
约定使用哪种 Markdown 扩展方式
的
组
件类型
、支持
前后端之间传什么格
2. 消息传输协议
式
定义流式响应的数据包结构（全量 / 增量
/ 推荐）
3. UI 渲
染协议 卡片长什么样
标准 JSON Schema，Web/iOS/Android
共用一份描述
4. 事件通信协议
用户点了卡片之后怎
么办
定义
卡片可触发
的 Action 及其响应方式
四层协议
的运作关系
如下图所示：
```

## PDF 第13页

[查看原页](RAW.pdf#page=13)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
下面逐层展
开。
▐ 第一层：Markdown 标记协议
回到第一部分的问题：我们列举了代码块扩展
、占位符替换、自定义标签三种方
约束，不同 Agent 团队各选各的，前端就要为每种格式维护一套解析器。
Markdown 标记协议就是做这个约束：统一选定一种扩展方式，定义
支持的
组
范 JSON 属性的命名和格式。
有了这层协议
后：
案。如果不做
件类型列表，规
所有 Agent 共用一份 System Prompt 中的"卡片生成规范"，只需调试一种输出格式
前端只维护一套 Markdown 解析器，新增卡片类型只需注册组
件，不需要改解析逻辑
设计师可以提前预知每种标记渲
染出来的样子，统一调整视觉规范
▐ 第二层：消息传输协议
模型输出经过 Agent 编排后，需要通过一个统一的消息格式传输给前端。我们约定每次传输
的是一个"动作
组"：
1
2
3
4
data: [
{"type": "text"
,
"content": "第一条消息"},
{"type": "recommend/prompt"
,
"content": ["你可能喜欢1"
,
"你可能喜欢2"]}
]
type 标识动作类型：text 是模型返回的 Markdown 消息，recommend/prompt 是追问推荐。第
二部分讲到的增量 Patch 更新，其中的
type=full 和 type=patch 也属于消息传输协议
的一部分
——正是
有了统一的数据包结构，前端才能用同一套逻辑处理全量消息和增量更新。
统一消息格式之后，最大的收益是前端组
件的可复用性。无论接入哪个 Agent，消息解析逻辑
都是同一套代码。新业务方接入时，不需要前端配合"定制消息格式"，只要按
协议传输就行
。
▐ 第三层：UI 渲
染协议
这一层定义
的是：一张卡片的结构化描述应该长什么样？
核心理念来自第二部分介绍的 A2UI 协议——Agent 输出一份标准 JSON，各端（Web / iOS
/ Android）各自实现渲
染器。这种"描述与渲
染分离"的设计，使得同一份 JSON 可以在三端
呈现一致的 UI，而不需要 Agent 关
心前端的技术实现。
```

## PDF 第14页

[查看原页](RAW.pdf#page=14)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
结合现状和对模型能力发
阶段：
展的期望， LUI（Language User Interface）的演进可以分为两个
第一阶段：预设卡片。 模型能力尚不
稳定，通过预定义
的卡片模板
+
对生成内容的把控力。每种卡片有固定的 Schema，Agent 只需要填数据。
JSON 数据来保证产品
第二阶段：Agent 生成。
随着模型能力提升，由 Agent 自主组合 UI 组
动态卡片。Agent 不再受限于预设模板，而是根据上下文自由拼装布局、
件，实现千人千面的
表
单、列表。
这两个阶段的关键在于平滑过渡。A2UI 协议
片和 Agent 动态生成可以共享同一套渲
染协议
虽然先阶段艰难，但是长
因为采用了框架无关
的 JSON Schema，预设卡
染器——切换时前端零改动。所以将 A2UI 作为 UI 渲
期看会是一个不错的选
。
择
▐ 第四层：事件通信协议
前三层解决了"卡片怎
么写、
怎
么传、
怎
么画"，但还
我们的设计原则是：卡片 JSON 只描述"是什么"和"能做什么"，不包含"怎
缺一环：用户和卡片交互之后，发生什么？
么做"。执
逻辑由
行
端侧事件处理器统一承担。
这样做有两个好处：一是 Agent 生成的 JSON 不包含可执
行
代码，降
低安全风险（想想如果
Agent 可以往卡片里注入任
意
JS 代码会怎样）；二是事件派发
逻辑端侧统一实现，各业务方
无需重复建设。
举个具体的例子走一遍完整流程：
1. 渲
阶段：Agent 返回一个商品卡片的 JSON，其中按
染
钮声明了一个 Action：
1
2
{
"type": "button"
,
```

## PDF 第15页

[查看原页](RAW.pdf#page=15)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
3
4
5
6
7
8
9
"text": "加入购物车"
,
"action": {
"type": "api"
,
"action": "addToCart"
,
"params": { "itemId": "12345" }
}
}
2. 交互阶段：用户点击按
钮，事件处理器
接收到 Action，识别 type=api，发起网关请求
调用
加购接口。
3. 反馈阶段：请求返回后，事件处理器根据结果更新卡片状态——成功则按
购"，失败则弹出 Toast 提示错误原因。
钮
变
灰显示"已加
整 个 过 程中 ， 卡片 addToCart"，但具体怎
JSON 么调、调
是 " 纯 声 明 " 的 —— 它说 " 我有一 个按
完怎
么更新 UI，全
部由端侧事件处理器负责。
钮 ， 点 了 之 后 应 该调
A2UI 本身已经定义了 Action 规范，在此基础上需要做的工作是：梳理业务中
实际需要的事件
类型（UI 事件：Toast、Dialog、页面跳转；API 事件：数据请求
、收藏
、加购），定义
统一
的事件格式和消费方式，让各业务方
不需要自己
发明事件协议，如果是 H5 那就是 uniapi。
总结
卡片式交互不是"在聊天框里塞组
件"这么简单。它重新定义了 Agent 时代的前后端协作
模型从"文本生成器"变成"界面规划师"——它需要理解什么时候该展示卡片、
型的卡片；
方式：
展示什么类
后端从"数据提供者"变成"协议协调
者"——它需要在 Tool 层打通数据获取与 UI 描述；
```

## PDF 第16页

[查看原页](RAW.pdf#page=16)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
前端从"页面渲
染器"变成"协议执
行
引擎"——它面向标准 JSON Schema 渲
染，而非为每
个业务方定制
。
四层协议体系（Markdown 标记 → 消息传输 → UI 渲
有多先进，而在于为复杂系
统建立了确定性——当每一层的
染 → 事件通信）的价值，不在于技术
入
输出都
有明确约定，问题排
输
查、能力复用、新业务接入的效率就会指数级提升。
最后，值得关注的是社区中正在涌现的 Agentic 协议生态：
AG-UI（Agent-用户交互协议）：基于事件的标准，连接 Agent 与面向用户的应用
MCP（Anthropic）：Agent 安全连接外部工具、工作流和数据源的开放标准
A2A（Google）：分布式 Agent 系
统中 Agent 之间的协调协议
A2UI（ Google） /
MCP Apps（ Anthropic） / Open-JSON-UI（ OpenAI） ： 声 明 式
UI 规范，定义 Agent 响应的视觉组织方式
Web MCP：让网页本身作为 MCP Server，为 Agent 提供工具访问
卡片式对话只是 Agentic 交互的起点。当协议
足够成熟、模型能力持续提升，对话界面将真正
成为用户与数字世界交互的统一入口。希望在真实的业务落地之后，能够有更多的分享。
如果你也在探索类似方向，欢迎在评论区交流——协议设计、
MCP 工具封装，任何话题都
。
行
渲
染器实现、Prompt 工程、
参考资料
https://github.com/stackblitz/bolt.new
https://modelcontextprotocol.io/extensions/apps/overview
https://a2ui.org/
https://docs.copilotkit.ai/built-in-agent/generative-ui/a2ui
https://remarkjs.github.io/react-markdown/
团队介绍
本文作者无二，来自淘天集团-跨端技术团队。本团队服务于淘宝基础用户产品，是淘宝重要
的 业 务 线 之一 。 团 队 以 前 端、 Weex
、 Native端 的 技术 解决
方
案框 架 和 研 发 模 式
不
断完善自
己，持续探索端智能等创
新，打造极致的体验和工程技术，保障多端设备的适配和稳定运
，
行
致力于让亿级规模的交付能够更丝滑、更稳定。
```

## PDF 第17页

[查看原页](RAW.pdf#page=17)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
¤ 拓展阅读 ¤
3DXR技术 | 终端技术 | 音视频技术
服务端技术 | 技术质量 | 数据算法
大淘宝技术
大淘宝技术官方账号
967篇原创内容
公众号
阅读 7830
留言
写留言
还没有
留言，来写首评
```
