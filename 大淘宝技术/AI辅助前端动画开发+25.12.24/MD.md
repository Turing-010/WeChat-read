# AI 辅助前端动画开发：PDF文本转写

> 这是原始PDF文本层转写，不是学习摘要。页码为PDF物理页序；图表、代码版面和图片文字不能完整表达在此文本层。已查看图像的内容和质量问题见AI学习笔记及META.json。

[原文PDF](RAW.pdf) · [AI学习笔记](AI_AI辅助前端动画开发.md) · [处理与质量记录](META.json)

## PDF 第1页

[查看原页](RAW.pdf#page=1)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
AI 辅助前端动画开
发
原创
用户&内容技术 2025年12月24日 01:49 浙江
大淘宝技术 8人
本文介绍了AI辅助前端动画开
践
发
的实
数难获取
、沟通成本高
方
案与技术思路，核心围绕解决传统动画开
中“参
发
开。作者以 After Effects（AE）为动效源头，
构建了一套基于
反复返工”等痛点展
MCP（Model Context Protocol）工具链
+
Cursor AI IDE
的协作工作
流，强调“L3级自动驾驶”——即AI生成关键步骤，但保留开
发
者随时介入
、校验与调整的灵
活性。
、
前言
AI 辅助代码生成在前端领域有两个难点，第一个是 Design To Code（下文检查称 D2C），
D2C的出发点虽然也是需求文档，但前端拿到的是设计师交付的设计稿，如何将设计软件中的
结构化数据映射为准确的前端UI，是目前阶段的一个难点，Pixelator 和 Figma 等团队都在
探索。另一个难点是生成动画代码，动画开
发依
赖
静态样式
还原，还依
赖
美术交付的动效资
产
（视频、Lottie、Spien、各类动效图片）等（见下图）。
传统动画开
的问题
发
1. 美术导出文件后，需要手动发到群里，前端工程师手动下载；
2. 前端工程师，反复看视频猜
测动画参数，导致研发效率低下；
```

## PDF 第2页

[查看原页](RAW.pdf#page=2)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
3. 不确定的的参数需要反复找美术沟通，沟通成本高；
4. 因为猜
测的参数比
较多，设计&美术走查时容易发现问题，造成重复反
工。
▐ 我的思路
前置条件
1. After Effect（下文简称AE） 作为业界最广泛被使用的视效软件，使用AE的游戏、视效
公司及从业者较为广泛，因此以 AE 为源头
的动画研发流程将会存在很长时间。
2. 无论手写动画代码、还是AI生成动画代码，准确的动画参数都是不可或缺
的，这直接影响
着动画交付的质量，和美术走查的效率。
什么不做
交付动效文件的场景： lottie、svg、spine、pag、webp、apng、gif、sprite
动效标注系
统
互动前端团队跟跨端技术团队合作，通过 AE 扩展一键将 AE 制作的动画生成动画标注数据保
存到互动资
产平台上，资
产平台提供交互界面让开
发
者查看动画参数，也提供 MCP Tool 让
Agent 获取到动画标注数据。
```

## PDF 第3页

[查看原页](RAW.pdf#page=3)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
00:25
00:25
失败的一次尝试
最开始我尝试构建工作流，通过将不同的工具节点组合为一条工作流，最终生成带有动画的
React 组
件。但很快就遇到了瓶颈：
1. 一旦
中间某个节点出错，需要重新调整从头开始运
，调试成本高。
行
2. 当某个节点的LLM输出结果比
较差，因为无法干预，导致输出结果质量劣化严重。
3. 只能使用一套固定的技术栈，不同项目之间可复用性较差。
4. 输出的结果需要手动搬运到项目中做调整。
转变思路，尝试 Cursor + Animati
on MCP
```

## PDF 第4页

[查看原页](RAW.pdf#page=4)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
工作流的方
案是企图将动画从0到1实现（L5级
别的自动驾驶），但现实情况是开
发
者
不得不做
好随时介入的准备（L3级
别自动驾驶），以及针对
不同项目，动画复杂度优化流程。因此我将
思路转为“在AI辅助下前端快速交付动画”，通过提供一套动画开
发
的 MCP Tool，结合可以灵
活调整的 SOP（通过 MCP Prompt 实现），将动画开
发拆分为7到16个左右的代办项。下面
是 AI 辅助动画开
发
的流程图，可以视为完整 SOP 的骨架。
▐ 提示词设计（动画开
发SOP）
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
## 角色
你是专业的 React 动画组
件开
发 Agent，借助 pixelator、animation-mcp、context7
## 核心规则
务必严格遵守核心规则，如果违反
核心规则会导致非常严重的问题！
- 确保百分之百按照用户需求执
标准工作流程
行
- 在完成每一个 Todo 后，都需要让我确认是否继续，这对我非常重要！！！
## 可使用工具列表
-
-
-
-
-
-
-
-
-
`
`
`
`
`
`
`
`
`
mcp__
context7` Context7 MCP Server，用于查阅技术文档
mcp__pixelator
__get
ast
from
url`：从 URL 获取 Pixelator AST
_
_
_
mcp__
animation-mcp__
animation
_
mcp_
version
`：获取 MCP 版本
mcp__
animation-mcp__
scan
_
workspace
`：扫描工作区
mcp__
animation-mcp__
list
_
workspaces
`：列出工作区
mcp__
animation-mcp__
animation
_guideline
`：获取 MCP 动画开
发指导规范
mcp__
animation-mcp__
init
animation
_
_
workspace
`：初始化动画工作区
mcp__
animation-mcp__
analyze
motion
_
_
video
`：分析动效视频，生成动效技术方
案
mcp__
animation-mcp__generate
motion
measurement`：从 Lottie 获取动效标
_
_
## 标准工作流程
```

## PDF 第5页

[查看原页](RAW.pdf#page=5)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
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
### 初始化动画工作区
1. 使用 `
2. 使用 `
mcp__
animation-mcp__
scan
_
workspace
`
mcp__
animation-mcp__
init
animation
工具扫描工作区，强制执
不可跳过
行
_
_
workspace
`
工具初始化动画工作区
### 分析项目架构和技术栈
你需要分析项目架构和技术栈信息，然后写入 manifest.json 的 constraints 字段，需要
1. 项目的目录结构
2. 项目使用的 UI 框架及版本，React、Vue、Angular、Svelte、Solid 等
3. 项目使用的 CSS 方
案，Tailwind CSS、CSS Modules、Scoped CSS、Pure CSS
4. 项目是否可以播放 Lottie 动画，使用的 Lottie 库及版本
5. 项目使用的 JavaScript 动画库及版本，Anime.js 4、GSAP 等
6. 项目使用的图片库及版本，@ali/picture、@ali/hudong-picture 等
// .....
▐ 关键物料
pixelator 设计稿链接
pixelator mcp 是雪萤团队 MGD
one 设计稿生码 MCP，首先通过 MGD
one pixelator 插
件获取视觉稿的端链接，将端链接提供给 pixelator mcp，可以获取设计稿的 AST，或者走
OneDay 生码流程。
```

## PDF 第6页

[查看原页](RAW.pdf#page=6)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
动效标注文件链接
动效标注文件链接可以从互动资
产平台或者 Ani
平台获取，Animati
on MCP 中提供工具从中
提取出关键动画参数。后续AI会严格按照动画参数去生成动画代码，最大程度上确保动画准
确。
动画视频
多模态模型将会分析动画视频，生成动画开
关键动画代码，性能优化建议等。
发技术方
案，包含动画阶段拆分，前端布局建议，
```

## PDF 第7页

[查看原页](RAW.pdf#page=7)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
▐ MCP Tool 列表
Pixelator MCP，MGD
one 设计稿转代码 MCP 服务
○get_ast_from_url，以 MGD
one 的设计稿链接为参数，获取视觉稿 AST
Animati
on MCP，基于上面的工作流，我做的 MCP 服务
Prompt * 2
animati
on_develop_guideline 互动动画开
发标准工作流
mini_animati
on_develop_guideline 互动微动画开
发工作流
动画工作区管理 Tool * 4
scan_workspace，扫描项目架构、技术栈
list_workspace
init_animati
on_workspace
set_active_workspace
辅助动效还原 Tool * 3
analyze_moti
on_video，分析动画视频，产出分析报告
generate_moti
on_measurement， 基 于动效 标 注 能力，生 成 动效 标 注 JSON
数据
enchance_moti
on_layers，使用 Pixelator MCP 获得视觉稿，对动效标注数
据语义
化增强
```

## PDF 第8页

[查看原页](RAW.pdf#page=8)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
一些尝试
▐ 动画研发标准流程
标准工作流提供最完成的动画开
发流程，要求开
发
的 Todo List，本文先不详细介绍，有太多东西要讲估计要单
者提供上文提供的所有物料，生成10步以上
开一篇。
```

## PDF 第9页

[查看原页](RAW.pdf#page=9)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
▐ 互动微动画研发流程
有时候 动画不 复杂， 或者 物 料不
全 时， 可 以 使用 微 动画 提示 词 。下 图展 示 了一个不 提供
pixelator 短链（不提供设计稿）情况下动画开
发流程，Agent 自动省掉了获取设计稿结构化
数据 的步 骤 ， 仍 然 保 留 了 动画 视 频分 析 和获取 动效 标 注 数据 的步 骤 ， 最 终生 成 了 只有
7步 的
Todo List。
```

## PDF 第10页

[查看原页](RAW.pdf#page=10)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
中间过程我发现 AI 生成了svg 图片代码有点丑，还是得提供一张图片，于是我点了暂停，找
了一张肥料图片给它。
```

## PDF 第11页

[查看原页](RAW.pdf#page=11)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
最后有一个小错误，因为我提示词里没有关
要求它修改后，动画就正确了。
于移动端适配的要求，AI没有
处理好单位，我主动
最终动画
00:0300:03
```

## PDF 第12页

[查看原页](RAW.pdf#page=12)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
▐ 如果只给一个动画视频呢？
我在 Ani
平台上看到一个简单
的进度条 Lottie 动画，背景色渐变
的动画还
录屏交给微动画研发流程，其他物料都没给，AI 生成了 5 步的 Todo List，并封装
件。
挺好看的，我直接
好了动画
组
AI 生成的动画技术方
案
1
2
3
4
5
6
7
# 技术方
案文档 - progressLine 动画
## 动画概述
这是一个进度条动画，展示一条线
的颜色随着进度发生变化的效果。该动画是一个无交互的加载
## 交互与动画流程
```

## PDF 第13页

[查看原页](RAW.pdf#page=13)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

````text
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
50
51
52
53
动画流程分为两个主要阶段：线条的绘
制伸展
阶段和渐变色的循环流动阶段。
```
mermaid
graph TD
A[开始] --> B{动画自动开始};
B --> C[阶段一: 绘
制阶段];
C --> D{线条从左侧由0开始向右伸展};
D --> E{在伸展的同时，渐变色跟随头
部移动};
E --> F{线条伸展至最大宽度};
F --> G[阶段二: 循环阶段];
G --> H{线条宽度保持不变};
H --> I{渐变色在完整线条上从左至右循环流动};
I --> G;
```
## 动画整体分析与分段
这是一个典型的加载或进度条动画，其核心是**宽度/缩放动画**与**背景渐变位移动画**的结
### 阶段一：绘
制阶段 (00:00 - 00:04)
**核心表现：** 一条水平线从无到有，从左到右逐渐伸展
开来，直至
达到预设的最终宽度。
**细节：** 在伸展的过程中，线条内部的彩色渐变似乎也随着线条的"笔尖"一起移动。
### 阶段二：循环阶段 (00:04 - 结束)
**核心表现：** 线条的长度不再变化，保持在最大宽度。
**细节：** 线条内部的彩色渐变
开始在一个固定的区域内，从左到右无限循环滚动，创造出一
## 动画各阶段技术方
案分析与建议
### 技术选型：Anime.js + CSS
综
合考虑实现效果、可控性和性能，**推荐使用 Anime.js 结合 CSS 实现**。CSS 负责定
**技术选型理由：**
- **Anime.js:** 非常适合编排这种多阶段、
- **Pure CSS:** 也可以通过 `@keyframes
`
- **Lottie/APNG:** 对于这种纯几何图形和渐变
多属性的动画。其 Timeline 功能可以完美地
实现，但将两个阶段无缝衔接并控制
的动画，使用 Lottie 或 APNG 属于"杀
循环需
### 阶段一：绘
制阶段实现方
案
````

## PDF 第14页

[查看原页](RAW.pdf#page=14)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

````text
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
94
95
96
97
98
99
**目标：** 实现线条从左到右的伸展效果。
**技术方
案：**
1. **元素：** 使用一个 `
<div>
` 元素作为线条。
2. **样式 (CSS):**
- 设置 `div
`
的高度（例如 `height: 2px;
- **关键点：** 使用 `transform-origin: left;
- 初始状态下，设置 `transform: scaleX(0);
- 为了
实现流光效果，设置一个比元素自身宽的线性渐变
`），初始宽度为 `
width: 100%;
`（最
` 将变换的基点设置在元素的左侧
` 将其在水平
方向上缩放为0，视觉上不
背景。例如，`background-siz
3. **动画 (Anime.js):**
- 使用 Anime.js 创建一个动画，目标为该 `div
`
。
- 动画属性为 `transform
`
的
`
scaleX` 从 `0`
变化到 `1`
。
- 同时，为了让渐变
看起来是跟随头
部移动的，可以动画化 `background-position
`
。
- 设置合适的
`duration
` (约4000ms) 和 `
easing
` (例如 'easeInOutQuad')。
### 阶段二：循环阶段实现方
案
**目标：** 在满宽度的线条上实现渐变循环流动的效果。
**技术方
案：**
1. **元素：** 沿用阶段一的
`
<div>
` 元素。此时它的
`
scaleX` 已经是 `1`
。
2. **动画 (Anime.js):**
- 紧接在阶段一动画之后，添加一个新的动画片段。
- 动画属性为 `background-position
`
。
- 让 `background-position
` 从 `50% 0`
- 设置 `loop: true
` 使其无限循环。
- 设置 `
easing: 'linear'` 保证匀速流动。
变化到 `
-50% 0`（或一个完整的循环周
### 组合实现代码示例
```javascript
// 获取
线条元素
const lineEl = document.querySelector('
.gradient-line');
// 使用 Anime.js 的 timeline 功能编排动画
const timeline = anime.timeline({
easing: 'linear'
, // 默认缓动函数
});
// 阶段一：绘
制
timeline.add({
````

## PDF 第15页

[查看原页](RAW.pdf#page=15)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

````text
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
140
141
142
143
144
145
targets: lineEl,
scaleX: [0, 1],
duration: 4000,
easing: 'easeInOutQuad'
, // 绘
制阶段使用缓入缓出，效果更自然
});
// 阶段二：循环
// 注意：这个动画会紧接着上一个动画结束时开始
timeline.add({
targets: lineEl,
backgroundPosition: ['100% 0'
,
duration: 2000, // 循环一次的速度
loop: true,
'
-100% 0'], // 移动一个完整的背景宽度
});
```
## DOM 布局建议
该动画结构非常简单，可以作为一个独立的
组
件。考虑到它可能作为页面加载指示器
覆盖在其他
```txt
Root
└── AnimationContainer (div, position: relative)
└── GradientLine (div, position: absolute; top: 50%; left: 0;)
```
**元素说明：**
- **AnimationContainer:** 一个容器
`div
- **GradientLine:** 真正的线条元素。使用 `
`，用于定位和约束内部的动画元素。如果这
position: absolute
` 可以方便地在
## React 组
件布局建议
对于 React 项目，建议
按照以下结构组织组
件：
```tsx
function ProgressLine() {
return (
<div className="progress-line-container">
<div className="gradient-line"></div>
</div>
);
}
```
## 性能优化建议
````

## PDF 第16页

[查看原页](RAW.pdf#page=16)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
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
1. **使用 `transform
` 代替 `
width`：** 方
案
中已经采用了 `transform: scaleX
2. **硬件加速:** 对 `GradientLine
` 元素应用 CSS 属性 `
will-change: transf
3. **背景动画：** `background-position
`
的动画性能在现代浏览器
中已经相当不错。
## 技术栈信息
- **UI Framework:** React 19.1.0
- **CSS Solution:** TailwindCSS 4.1.4 (utility-first)
- **Animation Library:** Anime.js 4.0.2
- **Build Tool:** Vite 7.1.5
- **Design Width:** 750px
- **Target FPS:** 60fps
- **Target Devices:** Mobile
AI 生成的动画组
件代码
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
import { useEffect, useRef } from 'react';
import { createScope, Timeline, eases, type Scope } from 'animejs';
/**
* ProgressLine 组
* 一个进度条动画组
件
件，展示线条颜色随进度变化的效果
*
* 动画分为两个阶段：
* 1. 绘
制阶段：线条从左到右伸展
* 2. 循环阶段：渐变色在线条上循环流动
*/
export function ProgressLine() {
const containerRef = useRef<HTMLDivElement>(null);
const scopeRef = useRef<Scope | null>(null);
useEffect(() => {
if (!containerRef.current) return;
// 创建 anime.js scope
scopeRef.current = createScope({ root: containerRef.current }).add
// 创建时间线
const timeline = new Timeline({
frameRate: 60,
playbackRate: 1,
```

## PDF 第17页

[查看原页](RAW.pdf#page=17)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
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
67
68
69
70
delay: 0,
});
// 阶段一：绘
制阶段 (0-4秒)
// 线条从左到右伸展，同时渐变跟随移动
timeline.add(
'[data-semantic-name="gradient-line"]'
,
{
scaleX: {
from: 0,
to: 1,
ease: eases.cubicBezier(0.42, 0, 0.58, 1), // easeInOutQua
},
backgroundPosition: {
from: '100% 0'
,
to: '50% 0'
,
ease: eases.cubicBezier(0.42, 0, 0.58, 1),
},
duration: 4000,
},
0,
);
// 阶段二：循环阶段
// 渐变色在满宽度线条上循环流动
timeline.add(
'[data-semantic-name="gradient-line"]'
{
,
backgroundPosition: {
from: '100% 0'
to: '
-100% 0'
,
ease: 'linear'
,
,
},
duration: 2000,
loop: true,
},
4000,
);
});
// 清理函数
return () => {
scopeRef.current?.revert();
};
}, []);
```

## PDF 第18页

[查看原页](RAW.pdf#page=18)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
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
return (
<div
ref={containerRef}
className="progress-line-container relative flex h-[100px] w-ful
data-semantic-name="progress-line-container"
>
<div
className="gradient-line absolute left-0 h-[2px] w-full"
data-semantic-name="gradient-line"
style={{
transformOrigin: 'left'
,
transform: 'scaleX(0)'
,
background: 'linear-gradient(90deg, #4F46E5 0%, #06B6D4 50%,
backgroundSize: '200% 100%'
,
backgroundPosition: '100% 0'
,
willChange: 'transform, background-position'
,
}}
/>
</div>
);
}
AI 生成的预览页面
00:0700:07
```

## PDF 第19页

[查看原页](RAW.pdf#page=19)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
写在最后
1. 受限于当前 D2C 尚不
题，导致同一个动画视频给出不同的技术方
完善，很难一步到位。以及多模态模型理解视频有时会因为抽帧问
案，因此 AI 辅助前端动开
发
的定位，比
较符合
目前 AI 发
展的特点。
2. 基于 Cursor（AI IDE）
代 码 ， 通 过调整 提示 词 适配
+ Animati
on MCP 的方式，生成符合项目结构和技术栈的动画
不 同 复杂度 的动画 研 发流 程和技术方
案， 灵活 性还 是比
较 好
的。
团队介绍
本文作者齐纪，来自淘天集团-用户&内容技术团队，本团队服务于淘宝基础用户产品，是淘宝
最重要的业务线之一。首页、信息流推荐、消息、
搜
索、我淘、用增、互动、内容等亿级用户
规模产品，为我们带来大量业务/技术挑战及机会。团队在保证业务的同时，以先进的跨端框架
和研发模式
不
断完善自己，打造最极致的体验和工程技术，保障多端设备的适配和稳定运
，
行
并探索端智能等创
求到上线
新机会，通过技术高效驱动业务的良性发
的端到端自动化与产品化能力，使亿级规模的交付更快、更稳
展。持续探索以AI为底座构建从需
、更可控。
¤ 拓展阅读 ¤
3DXR技术 | 终端技术 | 音视频技术
服务端技术 | 技术质量 | 数据算法
大淘宝技术
大淘宝技术官方账号
967篇原创内容
公众号
```

## PDF 第20页

[查看原页](RAW.pdf#page=20)

> 仅转写文本层。表格、图像与代码长行请对照PDF；提取为空不等于原页为空白。

```text
阅读 4424
留言
写留言
还没有
留言，来写首评
```
